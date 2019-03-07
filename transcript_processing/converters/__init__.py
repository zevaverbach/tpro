from .amazon import AmazonConverter
from .speechmatics import SpeechmaticsConverter
from .gentle import GentleConverter
from .google import GoogleConverter

services = {
        'amazon': AmazonConverter,
        'gentle': GentleConverter,
        'speechmatics': SpeechmaticsConverter,
        'google': GoogleConverter,
        }
