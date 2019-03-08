import json
import os

import pytest

from transcript_processing.converters.amazon import AmazonConverter


@pytest.fixture
def transcript_data():
    with open(os.getenv('AMAZON_TRANSCRIPT_TEST_FILE'), 'r') as fin:
        return json.load(fin)


@pytest.fixture
def converter(transcript_data):
    return AmazonConverter(transcript_data)


def test_get_word_objects(converter):
    word_objects = converter.get_word_objects(converter.json_data)
    assert word_objects


def test_get_speaker_segments(converter):
    speaker_segments = converter.get_speaker_segments()
    assert speaker_segments


def test_get_speaker_id(converter):
    speaker_segments = converter.get_speaker_segments()
    assert speaker_segments[54.58] == 0
    assert speaker_segments[32.36] == 1


def test_convert(converter):
    converter.convert()
    print(converter.converted_words)
