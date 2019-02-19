from pathlib import Path

from nltk.tag.stanford import StanfordNERTagger

st = StanfordNERTagger('/usr/local/bin/english.all.3class.distsim.crf.ser.gz',
                       '/usr/local/bin/stanford-ner.jar')


PROPER_NOUN_TAGS = ['ORGANIZATION', 'PERSON', 'LOCATION']

PUNCTUATION = ['.', '?', ',', ':', '"', '!']


def tag_words(words):
    return st.tag(words)


def is_a_proper_noun(phrase):
    tagged_words = tag_words(phrase.split())
    return any(tagged_word[1] in PROPER_NOUN_TAGS
               for tagged_word in tagged_words)


def get_punc_before(word):
    punc = []
    for char in word:
        if char.isalpha():
            return punc
        if char in PUNCTUATION:
            punc.append(char)


def get_punc_after(word):
    punc = []
    for char in reversed(word):
        if char.isalpha():
            return punc
        if char in PUNCTUATION:
            punc.insert(0, char)


def is_path(string):
    return '/' in string and Path(string).exists()
