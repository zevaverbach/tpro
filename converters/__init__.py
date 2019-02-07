"""

fields for converted transcript:

    start
    end
    word
    confidence
    index
    always_capitalized
    punc_before
    punc_after

"""

from transcript_processing.converters.amazon import amazon_converter
from transcript_processing.converters.speechmatics import speechmatics_aligned_text_converter, speechmatics_converter


converters = {
    'speechmatics': speechmatics_converter,
    'speechmatics_align': speechmatics_aligned_text_converter,
    'amazon': amazon_converter,
}
