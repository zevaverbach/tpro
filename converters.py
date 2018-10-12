from decimal import Decimal
from typing import Dict, Union, List

from helpers import tag_words, PROPER_NOUN_TAGS


def speechmatics_converter(data: Dict[str, Union[Dict[str, str], List[Dict[str, str]]]]):
    converted_words = []
    words = data['words']
    tagged_words = tag_words([w['name'] for w in words])

    for index, w in enumerate(words):
        word_start = Decimal(w['time'])
        word_end = word_start + Decimal(w['duration'])
        confidence = Decimal(w['confidence'])
        word = w['name']
        space = '' if word == '.' else ' '
        is_proper_noun = tagged_words[index][1] in PROPER_NOUN_TAGS
        converted_words.append({
            'wordStart': word_start,
            'wordEnd': word_end,
            'confidence': confidence,
            'word': word,
            'space': space,
            'alwaysCapitalized': is_proper_noun or word == 'I',
            'index': index,
        })
    return converted_words


converters = {
    'speechmatics': speechmatics_converter,
}
