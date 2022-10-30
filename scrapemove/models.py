"""Data classes to enclose rightmove data"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from enum import Enum

from datetime import datetime

from inflection import camelize


class CamelCaseBaseModel(BaseModel):
    class Config:
        alias_generator = lambda s: camelize(s, False)


class Location(CamelCaseBaseModel):
    latitude: Optional[float]
    longitude: float


class ListingUpdate(CamelCaseBaseModel):
    reason: str = Field(alias="listingUpdateReason")
    date: datetime = Field(alias="listingUpdateDate")


class Price(CamelCaseBaseModel):
    amount: int
    currency_code: str
    frequency: Optional[str]
    qualifier: Optional[str]


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
    feesApply: bool
    displaySize: str
    propertyUrl: str
    contactUrl: str
    firstVisibleDate: datetime

    def __init__(self, **kwargs):
        """Remap some fields"""
        # Unnest product label
        kwargs["productLabel"] = kwargs["productLabel"]["productLabelText"]
        super().__init__(**kwargs)


class ResultsScreenData(CamelCaseBaseModel):
    properties: List[Property]
    pagination: Pagination
    resultCount: int