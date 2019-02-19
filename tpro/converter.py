import abc
from collections import namedtuple
import os

from . import helpers
from . import converters



Word = namedtuple('Word', 'start end confidence word always_capitalized next_word')


class TranscriptConverter:

    __metaclass__ = abc.ABCMeta

    def __init__(self, json_data):
        self.json_data = json_data

    def convert(self):
        tagged_words = None

        word_objects = self.get_word_objects(self.json_data)
        words = self.get_words(word_objects)

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
    def check_if_always_capitalized(word, index, tagged_words):
        if word.upper() == 'I':
            return True
        word_category = tagged_words[index][1] 
        return word_category in helpers.PROPER_NOUN_TAGS

    def get_word_object(self, word_object, index, tagged_words, word_objects):
        word = self.get_word_word(word_object)
        return Word(
            self.get_word_start(word_object),
            self.get_word_end(word_object),
            self.get_word_confidence(word_object),
            word,
            self.check_if_always_capitalized(word, index, tagged_words),
            self.get_next_word(word_objects, index)
                ) 

    def get_next_word(self, word_objects, index):
        if index < len(word_objects) - 1:
            return word_objects[index + 1]

    def save(self, path, output_target):
        with open(path, 'w') as fout:
            fout.write(getattr(self, output_target)())
        return path


from . import outputs
for name, val in outputs.__dict__.items():
    if callable(val):
        setattr(TranscriptConverter, name, val)
