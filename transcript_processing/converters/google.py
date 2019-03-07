import json
import re

from ..converter import TranscriptConverter
from .. import helpers



class GoogleConverter(TranscriptConverter):

    def __init__(self, transcript_data: str):
        super().__init__(transcript_data)
        self.json_data = self.pre_process(transcript_data)

    def pre_process(self, transcript_data):
        friendly = make_json_friendly(transcript_data)
        return json.loads(friendly)

    def get_word_objects(self, json_data):
        return json_data

    def convert_words(self, word_objects, words, tagged_words=None):
        converted_words = []

        punc_before = False
        punc_after = False

        for i, w in enumerate(word_objects):
            word_obj = self.get_word_object(w, i, tagged_words, word_objects)
            punc_before = helpers.get_punc_before(word_obj.word) or False
            punc_after = helpers.get_punc_after(word_obj.word) or False

            the_word = word_obj.word
            if punc_before:
                the_word = the_word[len(punc_before):]
            if punc_after:
                the_word = the_word[:-len(punc_after)]

            converted_words.append({
                'start': word_obj.start,
                'end': word_obj.end,
                'confidence': word_obj.confidence,
                'word': the_word,
                'always_capitalized': self.check_if_always_capitalized(
                    word_obj.word, 
                    i,
                    tagged_words),
                'punc_after': punc_after,
                'punc_before': punc_before,
            })

        return converted_words

    @classmethod
    def get_word_start(cls, word_object):
        return cls.get_seconds(word_object['start_time'])

    @classmethod
    def get_word_end(cls, word_object):
        return cls.get_seconds(word_object['end_time'])

    @staticmethod
    def get_seconds(time: dict) -> float:
        seconds = 0
        if 'seconds' in time:
            seconds = time['seconds']
        if 'nanos' in time:
            seconds += time['nanos'] / 1_000_000_000
        return seconds

    @staticmethod
    def get_word_confidence(word_object):
        return word_object['confidence']

    @staticmethod
    def get_word_word(word_object):
        print(word_object)
        return word_object['word']



def make_json_friendly(json_string):
    lines = [line.strip() for line in json_string.split('\\n')]

    fields = [
        'words {', 
        'start_time {', 
        '}',
        'end_time {', 
        '}',
        'word: ', 
        'confidence: '
        ]

    current_field_index = 0
    new_string = ''

    for line in lines:

        current_field = fields[current_field_index]

        if current_field in line:
            if current_field_index == len(fields) - 1:
               current_field_index = 0
            else:
                current_field_index += 1
                if current_field_index == 1:
                    new_string += '}, {'
                    # "words" was found, don't want to append that
                    continue

        else:
            if current_field_index == 0:
                # haven't found the beginning of the next word object
                continue

        # add quotes around keys
        line = re.sub('^(?!")([0-9a-zA-Z_]+)', 
                        '"\\1"', 
                        line)

        # add colons after keys
        if line.endswith('{'):
            line = line.replace('" ', '": ')

        # use first two decimals of confidence
        if 'confidence' in current_field:
            line = ', ' + line
            line = line[:20]

        if current_field == '}':
            line = line + ', '

        new_string += line

    # cleanup
    if new_string.startswith('}, '):
        new_string = new_string[3:]
    if not new_string.startswith('['):
        new_string = '[' + new_string
    if not new_string.endswith('}]'):
        new_string = new_string + '}]'
    new_string = new_string.replace(', }', '}').replace('\\', '')

    return new_string
