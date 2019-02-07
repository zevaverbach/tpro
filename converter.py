import abc
import json
from collections import namedtuple
import os

import helpers
from transcript_processing.converters import converters



Word = namedtuple('Word', 'start end confidence word is_proper_noun next_word')


class TranscriptConverter:

    __metaclass__ = abc.ABCMeta

    def __init__(self, path, output_target):
        self.path = path
        self.output_target = output_target

    def convert(self):
        tagged_words = None

        with open(self.path) as f:
            data = json.load(f)
            word_objects = self.get_word_objects(data)
            words = self.get_words(word_objects)

            if self.output_target == 'interactive_transcript':
                tagged_words = helpers.tag_words(words)

            self.converted_words = self.convert_words(
                    word_objects,
                    words,
                    tagged_words
                    )

    @staticmethod
    @abc.abstractmethod
    def get_word_objects(json_data):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_words(word_objects):
        pass

    @staticmethod
    @abc.abstractmethod
    def convert_words(word_objects, words, tagged_words=None):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_word_start(word_object):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_word_end(word_object):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_word_confidence(word_object):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_word_word(word_object):
        pass

    @staticmethod
    def check_if_proper_noun(index, tagged_words):
        return tagged_words[index][1] in helpers.PROPER_NOUN_TAGS

    def get_word_object(self, word_object, index, tagged_words, word_objects):
        return Word(
            self.get_word_start(word_object),
            self.get_word_end(word_object),
            self.get_word_confidence(word_object),
            self.get_word_word(word_object),
            self.check_if_proper_noun(index, tagged_words),
            self.get_next_word(word_objects, index)
                ) 

    def get_next_word(self, word_objects, index):
        if index < len(word_objects) - 1:
            return word_objects[index + 1]

    def to_json(self):
        return json.dumps(self.converted_words, indent=4)

    def save(self, path):
        with open(path, 'w') as fout:
            fout.write(self.to_json())
        return path
