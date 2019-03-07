import json
import os

import pytest

from transcript_processing.converters.google import (
    make_json_friendly,
    GoogleConverter,
        )
from transcript_processing.config import GOOGLE_TRANSCRIPT_TEST_FILE


@pytest.fixture
def transcript():
    with open(GOOGLE_TRANSCRIPT_TEST_FILE, 'r') as fin:
        return fin.read()


def test_make_json_friendly(transcript):
    friendly = make_json_friendly(transcript)
    assert json.loads(friendly)


def test_pre_process(transcript):
    with open(os.getenv('GOOGLE_TRANSCRIPT_TEST_FILE'), 'r') as fin:
        transcript_data = fin.read()

    g = GoogleConverter(transcript_data)
    assert g.json_data
            


