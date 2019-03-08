import json
import os

import pytest

from transcript_processing.converters.amazon import AmazonConverter
from transcript_processing.converters.speechmatics import SpeechmaticsConverter
from transcript_processing.converters.gentle import GentleConverter
from transcript_processing.converters.google import GoogleConverter


@pytest.fixture
def json_transcript():
    with open(os.getenv('AMAZON_TRANSCRIPT_TEST_FILE')) as fin:
        transcript = json.load(fin)
        yield transcript


def test_json_transcript(json_transcript):
    assert json_transcript["jobName"] == "Lelandmp3"


def test_amazon():
    with open(os.getenv('AMAZON_TRANSCRIPT_TEST_FILE'), 'r') as fin:
        json_data = json.load(fin)

    a = AmazonConverter(json_data)
    a.convert()
    assert a.converted_words[0] == {
            'start': 5.49, 
            'end': 5.97, 
            'confidence': 1.0,
            'word': 'So',
            'always_capitalized': False,
            'punc_after': False,
            'punc_before': False
            }


def test_speechmatics():
    with open(os.getenv('SPEECHMATICS_TRANSCRIPT_TEST_FILE'), 'r') as fin:
        json_data = json.load(fin)

    a = SpeechmaticsConverter(json_data)
            
    a.convert()
    assert a.converted_words[0] == {
            'start': 5.98,
            'end': 6.11,
            'confidence': 0.67,
            'word': 'For',
            'always_capitalized': False,
            'punc_after': False,
            'punc_before': False,
            }


def test_gentle():
    with open(os.getenv('GENTLE_TRANSCRIPT_TEST_FILE'), 'r') as fin:
        json_data = json.load(fin)

    a = GentleConverter(json_data)
    a.convert()
    assert a.converted_words[0] == {
            'start': 0.35,
            'end': 1.58, 
            'confidence': 1, 
            'word': '[noise]', 
            'always_capitalized': False, 
            'punc_after': False,
            'punc_before': False
            }


def test_google():
    with open(os.getenv('GOOGLE_TRANSCRIPT_TEST_FILE'), 'r') as fin:
        transcript_data = fin.read()

    g = GoogleConverter(transcript_data)
            
    g.convert()
    print(g.converted_words[0])
    assert g.converted_words[0] == {
        'start': 0.4, 
        'end': 2.1,
        'confidence': 0.9128385782241821,
        'word': 'Okay',
        'always_capitalized': False,
        'punc_after': [','],
        'punc_before': False,
        'speaker_id': None
        }
