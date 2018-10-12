from nltk.tag.stanford import StanfordNERTagger

st = StanfordNERTagger('/usr/local/bin/english.all.3class.distsim.crf.ser.gz',
                       '/usr/local/bin/stanford-ner.jar')


PROPER_NOUN_TAGS = ['ORGANIZATION', 'PERSON', 'LOCATION']


def tag_words(words):
    return st.tag(words)


def is_a_proper_noun(phrase):
    tagged_words = tag_words(phrase.split())
    return any(tagged_word[1] in PROPER_NOUN_TAGS
               for tagged_word in tagged_words)
