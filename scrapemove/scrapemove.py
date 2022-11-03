"""Main module."""
import json
import re
from multiprocessing import Pool
from typing import Dict, List
from urllib import parse

import requests
from bs4 import BeautifulSoup

from scrapemove.models import Property, ResultsScreenData
from scrapemove.property_details import PropertyDetailsScreenData

_DEFAULT_THREADPOOL = 1
_VALID_DOMAIN = "www.rightmove.co.uk"


def _validate_url(url: str):
    """Basic validation of the user-supplied URL"""
    parsed = parse.urlsplit(url)

    valid_protocols = ["http", "https"]
    if parsed.scheme not in valid_protocols:
        raise ValueError(f"Invalid scheme {parsed.scheme} (must be {valid_protocols})")

    if parsed.netloc != _VALID_DOMAIN:
        raise ValueError(f"Invalid domain: {parsed.netloc} (must be {_VALID_DOMAIN}")

    valid_paths = [
        f"/{p}/find.html"
        for p in ["property-to-rent", "property-for-sale", "new-homes-for-sale"]
    ]
    if parsed.path not in valid_paths:
        raise ValueError(f"Invalid path: {parsed.path} (must be {valid_paths}")


def _request_results_page(url: str) -> bytes:
    # Request
    r = requests.get(url)
    status_code, content = r.status_code, r.content
    if status_code != 200:
        raise RuntimeError(f"Request for {url} failed with: [{status_code}]: {content}")
    # Parse the data
    return content


def _load_results_page(url: str) -> ResultsScreenData:
    raw_content = _request_results_page(url)
    return ResultsScreenData.from_page_content(raw_content)


def _load_details_page(url: str) -> PropertyDetailsScreenData:
    raw_content = _request_results_page(url)
    return PropertyDetailsScreenData.from_page_content(raw_content)


def _build_url(url: str, params: Dict[str, str]) -> str:
    url_parts = list(parse.urlparse(url))
    query = dict(parse.parse_qs(url_parts[4]))
    query.update(params)
    url_parts[4] = parse.urlencode(query)
    return parse.urlunparse(url_parts)


def _flat_map(f, xs):
    ys = []
    for x in xs:
        ys.extend(f(x))
    return ys


def request(
    url: str, detailed=False, parallelism=_DEFAULT_THREADPOOL
) -> List[Property]:
    # Validate
    _validate_url(url)
    # Request the first page
    first_page = _load_results_page(url)
    # Extract the remaining pages
    next_page_urls = [
        f"{url}&index={option.value}" for option in first_page.pagination.options
    ]
    with Pool(parallelism) as p:
        subsequent_pages = p.map(_load_results_page, next_page_urls[1:])
    # Assemble together
    all_pages = [first_page] + subsequent_pages
    property_list = _flat_map(lambda r: r.properties, all_pages)
    # Request further details if necessary
    if detailed:
        with Pool(parallelism) as p:
            details_pages = p.map(
                _load_details_page,
                [f"https://{_VALID_DOMAIN}{p.propertyUrl}" for p in property_list],
            )
        return list(map(lambda d: d.property_data, details_pages))
    else:
        return property_list
