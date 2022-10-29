from pathlib import Path
import json

import pytest
from pydantic import ValidationError

from scrapemove.models import Property


_TEST_DIR = Path(__file__).parent
_TEST_DATA_DIR = _TEST_DIR / "test_data"
_RESULTS_SCREEN_DATA_FILE = _TEST_DATA_DIR / "results-screen-data.json"

with open(_RESULTS_SCREEN_DATA_FILE) as file:
	_RESULTS_SCREEN_DATA = json.load(file)



@pytest.mark.parametrize("data", _RESULTS_SCREEN_DATA["properties"])
def test_parse_properties(data):
	try:
		Property(**data)
	except ValidationError as exc:
		assert False, f"Validation failed: {exc}"