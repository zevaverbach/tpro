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

from collections import namedtuple
from decimal import Decimal
import json
from typing import Dict, Union, List

import helpers


def amazon_converter(data: dict):
    data = json.load(data)
    converted_words = []
    words = data['results']['items']
    tagged_words = helpers.tag_words(
        [w['alternatives'][0]['content'] for w in words])
    punc_before = False
    punc_after = False
    num_words = len(words)
    index = 0

    for i, w in enumerate(words):
        if w['type'] == 'punctuation':
            continue
        next_word_punc_after = None
        word_start = float(w['start_time'])
        word_end = float(w['end_time'])
        confidence = float(w['alternatives'][0]['confidence'])
        word = w['alternatives'][0]['content']
        is_proper_noun = tagged_words[i][1] in helpers.PROPER_NOUN_TAGS

        next_word = None
        if i < num_words - 1:
            next_word = words[i + 1]['alternatives'][0]['content']
            next_word_type = words[i + 1]['type']
        if next_word == '.':
            punc_after = '.'
        elif next_word == ',':
            punc_after = ','
        elif next_word_punc_after:
            punc_after = next_word_punc_after
            next_word_punc_after = None

        if word == 'i':
            # weird Amazon quirk
            word = 'I'

        if word.lower() == 'you' and next_word == 'know':
            prev_word = words[i - 1]
            if prev_word['type'] != 'punctuation':
                converted_words[-1]['punc_after'] = ','
            if next_word_type != 'punctuation':
                next_word_punc_after = ','

        converted_words.append({
            'start': word_start,
            'end': word_end,
            'confidence': confidence,
            'word': word,
            'always_capitalized': is_proper_noun or word == 'I',
            'index': index,
            'punc_after': punc_after,
            'punc_before': punc_before,
        })

        index += 1
        punc_after = False

    return converted_words


def speechmatics_converter(data: dict):
    data = json.load(data)
    converted_words = []
    words = data['words']
    tagged_words = helpers.tag_words([w['name'] for w in words])
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
        is_proper_noun = tagged_words[i][1] in helpers.PROPER_NOUN_TAGS

        next_word = None
        if i < num_words - 1:
            next_word = words[i + 1]['name']
        if next_word == '.':
            punc_after = '.'

        converted_words.append({
            'start': word_start,
            'end': word_end,
            'confidence': confidence,
            'word': word,
            'always_capitalized': is_proper_noun or word == 'I',
            'index': index,
            'punc_after': punc_after,
            'punc_before': punc_before,
        })

        index += 1
        punc_after = False

    return converted_words


def speechmatics_aligned_text_converter(data):
    data = data.readlines()[0]
    Word = namedtuple('Word', 'start end word')

    class Exhausted(Exception):
        pass

    def get_time(transcript, index):
        time_index = transcript.find('time=', index)
        if time_index == -1:
            raise Exhausted
        close_index = transcript.find('>', time_index)
        return float(transcript[time_index + 5: close_index]), close_index

    def find_next_word(transcript, start_index):
        start, end_of_start_index = get_time(transcript, start_index)

        word_start_index = end_of_start_index + 1
        word_end_index = transcript.find('<', word_start_index)
        word = transcript[word_start_index: word_end_index]

        end, close_index = get_time(transcript, word_end_index)

        return Word(start, end, word), close_index

    words = []
    next_index = 0
    word = None

    while True:
        try:
            word, next_index = find_next_word(data, next_index)
        except Exhausted:
            break
        else:
            words.append(word)

    tagged_words = helpers.tag_words([w.word for w in words])
    converted_words = []

    for i, word in enumerate(words):
        is_proper_noun = tagged_words[i][1] in helpers.PROPER_NOUN_TAGS
        punc_before = helpers.get_punc_before(word.word)
        punc_after = helpers.get_punc_after(word.word)
        the_word = word.word
        if punc_before or punc_after:
            for p in helpers.PUNCTUATION:
                the_word = the_word.replace(p, '')
        converted_words.append({
            'start': word.start,
            'end': word.end,
            'confidence': 1,
            'word': the_word,
            'always_capitalized': is_proper_noun or word == 'I',
            'index': i,
            'punc_before': punc_before,
            'punc_after': punc_after,
        })

    return converted_words


converters = {
    'speechmatics': speechmatics_converter,
    'speechmatics_align': speechmatics_aligned_text_converter,
    'amazon': amazon_converter,
}
