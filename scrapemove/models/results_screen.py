"""Data classes to enclose rightmove data"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl

from scrapemove.models.common import (
    CamelCaseBaseModel,
    Location,
    Price,
    _parse_from_page,
)


class ListingUpdate(CamelCaseBaseModel):
    reason: str = Field(alias="listingUpdateReason")
    date: datetime = Field(alias="listingUpdateDate")


class PaginationOption(CamelCaseBaseModel):
    value: int
    description: int


class Pagination(CamelCaseBaseModel):
    first: int
    last: int
    options: List[PaginationOption]


class Property(CamelCaseBaseModel):
    id: int
    bedrooms: int
    bathrooms: Optional[int]
    number_of_images: int
    number_of_floorplans: int
    summary: Optional[str]
    display_address: Optional[str]
    country_code: Optional[str]
    location: Location
    property_sub_type: Optional[str]
    listing_update: ListingUpdate
    price: Price
    transaction_type: str
    product_label: str
    commercial: bool
    development: bool
    residential: bool
    students: bool
    auction: bool
    fees_apply: bool
    display_size: str
    property_url: str
    contact_url: str
    first_visible_date: datetime

    def __init__(self, **kwargs):
        """Remap some fields"""
        # Unnest product label
        kwargs["productLabel"] = kwargs["productLabel"]["productLabelText"]
        super().__init__(**kwargs)


class ResultsScreenData(CamelCaseBaseModel):
    properties: List[Property]
    pagination: Pagination
    resultCount: int

    @staticmethod
    def from_page_content(content: str) -> "ResultsScreenData":
        return _parse_from_page(content, r"window\.jsonModel =", ResultsScreenData)
