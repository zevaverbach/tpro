import json
import os

import pytest

from transcript_processing.converters.amazon import AmazonConverter


@pytest.fixture
def transcript_data():
    with open(os.getenv('AMAZON_TRANSCRIPT_TEST_FILE'), 'r') as fin:
        return json.load(fin)


@pytest.fixture
def transcript_data_no_speaker_id():
    with open(
           os.getenv('AMAZON_TRANSCRIPT_TEST_FILE_NO_SPEAKER_ID'), 'r') as fin:
        return json.load(fin)


@pytest.fixture
def converter(transcript_data):
    return AmazonConverter(transcript_data)

@pytest.fixture
def converter_no_speaker_id(transcript_data_no_speaker_id):
    return AmazonConverter(transcript_data_no_speaker_id)


def test_get_word_objects(converter, converter_no_speaker_id):
    word_objects = converter.get_word_objects(converter.json_data)
    assert word_objects

    word_objects = converter_no_speaker_id.get_word_objects(
            converter_no_speaker_id.json_data)
    assert word_objects


def test_get_speaker_segments(converter, converter_no_speaker_id):
    speaker_segments = converter.get_speaker_segments()
    assert speaker_segments

    speaker_segments = converter_no_speaker_id.get_speaker_segments()
    assert speaker_segments is None

def test_get_speaker_id(converter):
    speaker_segments = converter.get_speaker_segments()
    assert speaker_segments[54.58] == 0
    assert speaker_segments[32.36] == 1

def test_convert(converter, converter_no_speaker_id):
    converter.convert()
    print(converter.converted_words)

    converter_no_speaker_id.convert()
    print(converter.converted_words)
