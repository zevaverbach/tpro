

import json
import os

import pytest

from converters.amazon import AmazonConverter
from converters.speechmatics import SpeechmaticsConverter
from converters.gentle import GentleConverter



def test_gentle():
    a = GentleConverter(
            os.getenv('GENTLE_TRANSCRIPT_TEST_FILE'),
            'viral_overlay')
    a.convert()
    assert json.loads(a.viral_overlay())[0] == {
            'start': 0.35,
            'stop': 1.58, 
            'word': '[noise]', 
            }
