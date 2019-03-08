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
def transcript_data_no_speaker_id():
    with open(
           os.getenv('GOOGLE_TRANSCRIPT_TEST_FILE_NO_SPEAKER_ID'), 'r') as fin:
        return fin.read()


@pytest.fixture
def converter(transcript_data):
    return GoogleConverter(transcript_data)


@pytest.fixture
def converter_no_speaker_id(transcript_data_no_speaker_id):
    return GoogleConverter(transcript_data_no_speaker_id)


def test_get_word_objects(converter, converter_no_speaker_id):
    word_objects = converter.get_word_objects(converter.json_data)
    assert word_objects

    word_objects = converter_no_speaker_id.get_word_objects(
            converter_no_speaker_id.json_data)
    assert word_objects


def test_convert(converter, converter_no_speaker_id):
    converter.convert()
    converter_no_speaker_id.convert()


def test_make_json_friendly(transcript_data):
    friendly = make_json_friendly(transcript_data)
    assert json.loads(friendly)


def test_pre_process(converter, converter_no_speaker_id):
    assert converter.json_data
    assert converter_no_speaker_id.json_data
