import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from scrapemove.models import PropertyDetailsScreenData

_TEST_DIR = Path(__file__).parent
_TEST_DATA_DIR = _TEST_DIR / "test_data"
_PROPERTY_DETAILS_SCREEN_DATA_FILE = (
    _TEST_DATA_DIR / "property-details-screen-data.json"
)

with open(_PROPERTY_DETAILS_SCREEN_DATA_FILE) as file:
    _PROPERTY_DETAILS_SCREEN_DATA = json.load(file)


@pytest.mark.parametrize("data", [_PROPERTY_DETAILS_SCREEN_DATA])
def test_parse_property_details(data):
    try:
        PropertyDetailsScreenData(**data)
    except ValidationError as exc:
        assert False, f"Validation failed: {exc}"
