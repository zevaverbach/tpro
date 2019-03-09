import json
from typing import Dict, Optional

from ..converter import TranscriptConverter
from .. import helpers



class AmazonConverter(TranscriptConverter):

    name = 'amazon'
    transcript_type = dict

    def __init__(self, json_data):
        super().__init__(json_data)

    def get_word_objects(self, json_data) -> list:
        return json_data['results']['items']

    def get_speaker_segments(self) -> Optional[Dict[float, str]]:
        try:
            segments = self.json_data['results']['speaker_labels']['segments']
        except KeyError:
            return None
        else:
            segment_dict = {}
            for segment in segments:
                word_level_segment = segment['items']
                for word in word_level_segment:
                    start_time = float(word['start_time'])
                    speaker_label = word['speaker_label']
                    speaker_id = ''
                    for char in speaker_label:
                        if char.isnumeric():
                            speaker_id += char
                    segment_dict[start_time] = int(speaker_id)
            return segment_dict

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
    def get_word_word(word_object) -> str:
        word_word = word_object['alternatives'][0]['content']
        if word_word == 'i':
            # weird Amazon quirk
            word_word = 'I'
        return word_word

    @classmethod
    def get_speaker_id(cls, word_object, speaker_segments=None):
        if speaker_segments is None:
            return None
        else:
            word_start = cls.get_word_start(word_object)
            return speaker_segments[word_start]

    def convert_words(self, word_objects, words, tagged_words=None):
        converted_words = []
        speaker_segments = self.get_speaker_segments()

        punc_before = False
        punc_after = False

        for i, w in enumerate(word_objects):
            if w['type'] == 'punctuation':
                continue
            next_word_punc_after = None
            word_obj = self.get_word_object(
                    w, 
                    i,
                    tagged_words,
                    word_objects,
                    speaker_segments,
                    )

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
                'speaker_id': word_obj.speaker_id,
            })

            punc_after = False

        return converted_words
