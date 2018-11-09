"""

fields for converted transcript:

    wordStart
    wordEnd
    word
    confidence
    index
    alwaysCapitalized
    puncBefore
    puncAfter

"""

from decimal import Decimal
from typing import Dict, Union, List

from helpers import tag_words, PROPER_NOUN_TAGS


def speechmatics_converter(data: Dict[str, Union[Dict[str, str], List[Dict[str, str]]]]):
    converted_words = []
    words = data['words']
    tagged_words = tag_words([w['name'] for w in words])
    punc_before = False
    punc_after = False
    num_words = len(words)
    index = 0

    for i, w in enumerate(words):
        word_start = float(w['time'])
        word_end = word_start + float(w['duration'])
        confidence = float(w['confidence'])
        word = w['name']
        if word == '.':
            continue
        is_proper_noun = tagged_words[i][1] in PROPER_NOUN_TAGS

        next_word = None
        if i < num_words - 1:
            next_word = words[i + 1]['name']
        if next_word == '.':
            punc_after = '.'

        converted_words.append({
            'wordStart': word_start,
            'wordEnd': word_end,
            'confidence': confidence,
            'word': word,
            'alwaysCapitalized': is_proper_noun or word == 'I',
            'index': index,
            'puncAfter': punc_after,
            'puncBefore': punc_before,
        })

        index += 1
        punc_after = False

    return converted_words


converters = {
    'speechmatics': speechmatics_converter,
}
