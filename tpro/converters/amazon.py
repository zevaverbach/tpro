import json

from ..converter import TranscriptConverter
from .. import helpers



class AmazonConverter(TranscriptConverter):

    name = 'amazon'

    def __init__(self, json_data):
        super().__init__(json_data)

    def get_word_objects(self, json_data):
        return json_data['results']['items']

    def get_words(self, word_objects):
        return [self.get_word_word(w)
                for w in word_objects]

    @staticmethod
    def get_word_start(word_object):
        return float(word_object['start_time'])

    @staticmethod
    def get_word_end(word_object):
        return float(word_object['end_time'])

    @staticmethod
    def get_word_confidence(word_object):
        return float(word_object['alternatives'][0]['confidence'])

    @staticmethod
    def get_word_word(word_object):
        word_word = word_object['alternatives'][0]['content']
        if word_word == 'i':
            # weird Amazon quirk
            word_word = 'I'
        return word_word

    def convert_words(self, word_objects, words, tagged_words=None):
        converted_words = []

        punc_before = False
        punc_after = False
        num_words = len(words)

        for i, w in enumerate(word_objects):
            if w['type'] == 'punctuation':
                continue
            next_word_punc_after = None
            word_obj = self.get_word_object(w, i, tagged_words, word_objects)

            if word_obj.next_word:
                next_word = self.get_word_word(word_obj.next_word)
                next_word_type = word_obj.next_word['type']
                if next_word in ['.', ',']:
                    punc_after = next_word
                elif next_word_punc_after:
                    punc_after = next_word_punc_after
                    next_word_punc_after = None

            if word_obj.word.lower() == 'you' and next_word == 'know':
                prev_word = word_objects[i - 1]
                if prev_word['type'] != 'punctuation':
                    converted_words[-1]['punc_after'] = ','
                if next_word_type != 'punctuation':
                    next_word_punc_after = ','

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
