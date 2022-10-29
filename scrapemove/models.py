"""Data classes to enclose rightmove data"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
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


class Property(CamelCaseBaseModel):
    id: int
    bedrooms: int
    bathrooms: int
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
    propertyUrl: str
    contactUrl: str
    firstVisibleDate: datetime

    def __init__(self, **kwargs):
        """Remap some fields"""
        kwargs["productLabel"] = kwargs["productLabel"]["productLabelText"]
        super().__init__(**kwargs)


"""
{
        "id": 0,
        "bedrooms": 0,
        "bathrooms": 0,
        "numberOfImages": 0,
        "numberOfFloorplans": 0,
        "numberOfVirtualTours": 0,
        "summary": null,
        "displayAddress": null,
        "countryCode": null,
        "location":
        {
            "latitude": null,
            "longitude": null
        },
        "propertyImages":
        {
            "images":
            [],
            "mainImageSrc": "",
            "mainMapImageSrc": ""
        },
        "propertySubType": null,
        "listingUpdate":
        {
            "listingUpdateReason": null,
            "listingUpdateDate": "2016-12-03T23:53:38Z"
        },
        "premiumListing": false,
        "featuredProperty": false,
        "price":
        {
            "amount": 0,
            "frequency": "",
            "currencyCode": "",
            "displayPrices":
            [
                {
                    "displayPrice": "",
                    "displayPriceQualifier": ""
                }
            ]
        },
        "customer":
        {
            "branchId": null,
            "brandPlusLogoURI": null,
            "contactTelephone": null,
            "branchDisplayName": null,
            "branchName": null,
            "brandTradingName": null,
            "branchLandingPageUrl": null,
            "development": false,
            "showReducedProperties": false,
            "commercial": false,
            "showOnMap": false,
            "enhancedListing": false,
            "developmentContent": null,
            "buildToRent": false,
            "buildToRentBenefits": null,
            "brandPlusLogoUrl": ""
        },
        "distance": null,
        "transactionType": null,
        "productLabel":
        {
            "productLabelText": null,
            "spotlightLabel": false
        },
        "commercial": false,
        "development": false,
        "residential": false,
        "students": false,
        "auction": false,
        "feesApply": false,
        "feesApplyText": "fees apply text",
        "displaySize": "size label",
        "showOnMap": false,
        "propertyUrl": "",
        "contactUrl": "",
        "staticMapUrl": "",
        "channel": "BUY",
        "firstVisibleDate": "2017-11-05T23:53:38Z",
        "keywords":
        [],
        "keywordMatchType": "no_keyword",
        "saved": false,
        "hidden": false,
        "onlineViewingsAvailable": false,
        "lozengeModel":
        {
            "matchingLozenges":
            []
        },
        "hasBrandPlus": false,
        "displayStatus": "",
        "enquiredTimestamp": null,
        "isRecent": false,
        "enhancedListing": false,
        "heading": "",
        "addedOrReduced": "",
        "formattedBranchName": "",
        "formattedDistance": "",
        "propertyTypeFullDescription": "Property"
    },
"""