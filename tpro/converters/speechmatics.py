from collections import namedtuple
import json

from ..converter import TranscriptConverter
from .. import helpers



class SpeechmaticsConverter(TranscriptConverter):

    name = 'speechmatics'

    def __init__(self, path):
        super().__init__(path)

    def get_word_objects(self, json_data):
        return json_data['words']

    def get_words(self, word_objects):
        return [self.get_word_word(w)
                for w in word_objects]

    @staticmethod
    def get_word_start(word_object):
        return float(word_object['time'])

    @staticmethod
    def get_word_end(word_object):
        return (SpeechmaticsConverter.get_word_start(word_object) 
                + float(word_object['duration']))

    @staticmethod
    def get_word_confidence(word_object):
        return float(word_object['confidence'])

    @staticmethod
    def get_word_word(word_object):
        return word_object['name']

    def convert_words(self, word_objects, words, tagged_words=None):
        converted_words = []
        punc_before = False
        punc_after = False
        num_words = len(words)

        for i, w in enumerate(word_objects):
            word_obj = self.get_word_object(w, i, tagged_words, word_objects)
            if word_obj.word == '.':
                continue

            if word_obj.next_word:
                next_word = self.get_word_word(word_obj.next_word)
                if next_word == '.':
                    punc_after = '.'

            converted_words.append({
                'start': word_obj.start,
                'end': word_obj.end,
                'confidence': word_obj.confidence,
                'word': word_obj.word,
                'always_capitalized': self.check_if_always_capitalized(
                    word_obj.word, 
                    i,
                    tagged_words),
                'punc_after': punc_after,
                'punc_before': punc_before,
            })

            punc_after = False

        return converted_words


def speechmatics_aligned_text_converter(data):
    data = data.readlines()[0]

    class Exhausted(Exception):
        pass

    Word = namedtuple('Word', 'start end word')

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
            'always_capitalized': self.check_if_always_capitalized(
                word.word, 
                i,
                tagged_words),
            'index': i,
            'punc_before': punc_before,
            'punc_after': punc_after,
        })

    return converted_words
