from .amazon import AmazonConverter
from .speechmatics import SpeechmaticsConverter
from .gentle import GentleConverter

services = {
        'amazon': AmazonConverter,
        'gentle': GentleConverter,
        'speechmatics': SpeechmaticsConverter,
        }
