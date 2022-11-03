from typing import List, Optional

from pydantic import HttpUrl

from scrapemove.models.common import CamelCaseBaseModel, Location, Price, _parse_from_page


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
    # Sizings
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

    @staticmethod
    def from_page_content(content: str) -> "PropertyDetailsScreenData":
        return _parse_from_page(
            content, r"window\.PAGE_MODEL =", PropertyDetailsScreenData
        )
