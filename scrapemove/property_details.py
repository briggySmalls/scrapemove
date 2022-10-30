from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from enum import Enum

from datetime import datetime

from inflection import camelize

from scrapemove.models import CamelCaseBaseModel, Price, Location


class Station(CamelCaseBaseModel):
    name: str
    types: List[str]
    distance: float
    unit: str


class PropertyDetails(CamelCaseBaseModel):
    id: int
    title: str
    description: str
    share_description: str
    property_phrase: str
    key_features: List[str]
    prices: Price
    images: List[HttpUrl]
    floorplans: List[HttpUrl]
    location: Location
    nearest_stations: List[Station]
    bedrooms: int
    bathrooms: Optional[int]
    brochures: List[str]

    def __init__(self, **kwargs):
        """Remap some fields"""
        # Unnest product label
        kwargs["images"] = [i["url"] for i in kwargs["images"]]
        kwargs["floorplans"] = [i["url"] for i in kwargs["floorplans"]]
        kwargs["brochures"] = [i["url"] for i in kwargs["brochures"]]
        text = kwargs["text"]
        kwargs["title"] = text["pageTitle"]
        kwargs["description"] = text["description"]
        kwargs["shareDescription"] = text["shareDescription"]
        kwargs["propertyPhrase"] = text["propertyPhrase"]
        super().__init__(**kwargs)

class PropertyDetailsScreenData(CamelCaseBaseModel):
    property_data: PropertyDetails