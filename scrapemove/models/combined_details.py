from pydantic import BaseModel, HttpUrl

from scrapemove.models.property_details_screen import PropertyDetails
from scrapemove.models.results_screen import Property


class CombinedDetails(BaseModel):
    property: Property
    additional_details: PropertyDetails

    def merged_dict(self):
        return {**self.property.dict(), **self.additional_details.dict()}
