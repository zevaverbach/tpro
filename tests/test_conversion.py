import json
import os

import pytest

from converters.amazon import AmazonConverter
from converters.speechmatics import SpeechmaticsConverter
from converters.gentle import GentleConverter


@pytest.fixture
def json_transcript():
    with open(os.getenv('AMAZON_TRANSCRIPT_TEST_FILE')) as fin:
        transcript = json.load(fin)
        yield transcript


def test_json_transcript(json_transcript):
    assert json_transcript["jobName"] == "Lelandmp3"


def test_amazon():
    a = AmazonConverter(
            os.getenv('AMAZON_TRANSCRIPT_TEST_FILE'),
            'interactive_transcript')
    a.convert()
    assert a.converted_words[0] == {
            'start': 5.49, 
            'end': 5.97, 
            'confidence': 1.0,
            'word': 'So',
            'always_capitalized': False,
            'index': 0,
            'punc_after': False,
            'punc_before': False
            }


def test_speechmatics():
    a = SpeechmaticsConverter(
            os.getenv('SPEECHMATICS_TRANSCRIPT_TEST_FILE'),
            'interactive_transcript')
    a.convert()
    assert a.converted_words[0] == {
            'start': 5.98,
            'end': 6.11,
            'confidence': 0.67,
            'word': 'For',
            'always_capitalized': False,
            'index': 0,
            'punc_after': False,
            'punc_before': False,
            }


def test_gentle():
    a = GentleConverter(
            os.getenv('GENTLE_TRANSCRIPT_TEST_FILE'),
            'interactive_transcript')
    a.convert()
    assert a.converted_words[0] == {
            'start': 0.35,
            'end': 1.58, 
            'confidence': 1, 
            'word': '[noise]', 
            'always_capitalized': False, 
            'index': 0, 
            'punc_after': False,
            'punc_before': False
            }
