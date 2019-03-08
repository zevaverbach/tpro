import json
import os

import pytest

from transcript_processing.converters.google import (
    make_json_friendly,
    GoogleConverter,
        )


@pytest.fixture
def transcript_data():
    with open(os.getenv('GOOGLE_TRANSCRIPT_TEST_FILE'), 'r') as fin:
        return fin.read()


@pytest.fixture
def converter(transcript_data):
    return GoogleConverter(transcript_data)


def test_get_word_objects(converter):
    word_objects = converter.get_word_objects(converter.json_data)
    assert word_objects


def test_make_json_friendly(transcript_data):
    friendly = make_json_friendly(transcript_data)
    assert json.loads(friendly)


def test_pre_process(converter):
    assert converter.json_data


def test_convert(converter):
    converter.convert()
    print(converter.converted_words)
