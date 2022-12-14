import json
import re
from typing import Optional

from bs4 import BeautifulSoup
from inflection import camelize
from pydantic import BaseModel


class CamelCaseBaseModel(BaseModel):
    class Config:
        alias_generator = lambda s: camelize(s, False)


class Location(CamelCaseBaseModel):
    latitude: Optional[float]
    longitude: float


class Price(CamelCaseBaseModel):
    amount: Optional[int]
    currency_code: Optional[str]
    frequency: Optional[str]
    qualifier: Optional[str]


def _parse_from_page(content: str, regex, cls):
    soup = BeautifulSoup(content, "html.parser")
    script = soup.find("script", string=re.compile(regex))
    data_str = re.sub(regex, "", script.string)
    data_py = json.loads(data_str)
    return cls(**data_py)
