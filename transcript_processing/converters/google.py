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
        json_data = json.loads(friendly)
        last_datum = json_data[-1]
        if last_datum.get('speaker_tag'):
            """Get rid of duplicate content that doesn't have speaker_tags"""
            json_data = [jd for jd in json_data if jd.get('speaker_tag')]
        return json_data

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
                'speaker_id': word_obj.speaker_id,
            })

        return converted_words

    @staticmethod
    def get_speaker_id(word_object, _):
        return word_object.get('speaker_tag')        

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
        return word_object['word']



def make_json_friendly(json_string):
    lines = [line.strip() for line in json_string.split('\n')]
    new_string = '['

    start_field = 'words {'

    open_braces = 0

    for index, line in enumerate(lines):
        if open_braces == 0:
            if start_field in line:
                open_braces = 1
                new_string += '{'
            continue

        if '{' in line:
            open_braces += 1
        if '}' in line:
            open_braces -= 1

        if open_braces == 0:
            new_string += '}, '
            continue

        elif '{' not in line and '}' not in lines[index + 1]:
            line = line + ', '

        line = re.sub('^(?!")([0-9a-zA-Z_]+)',
                '"\\1"',
                line)

        if 'start_time' in line:
            line = line.replace('"start_time"', '"start_time":')
        if 'end_time' in line:
            line = line.replace('"end_time"', '"end_time":')

        new_string += line

    new_string = new_string.replace('\\', '')

    return new_string[:-2] + ']'
