import json

from transcript_processing import helpers



class AmazonConverter(TranscriptConverter):

    def __init__(self, path, output_target):
        super().__init__(path, output_target)

    def get_word_objects(self, json_data):
        return data['results']['items']

    def get_words(self, word_objects):
        return [self.get_word_word(w)
                for w in word_objects])

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
        word_word = w['alternatives'][0]['content']
        if word_word == 'i':
            # weird Amazon quirk
            word_word = 'I'
        return word_word

    def convert_words(self, word_objects, words, tagged_words=None):
        converted_words = []

        punc_before = False
        punc_after = False
        num_words = len(words)
        index = 0

        for i, w in enumerate(words):
            if w['type'] == 'punctuation':
                continue
            next_word_punc_after = None
            word_obj = self.get_word_object(w, i, tagged_words, words)

            if word_obj.next_word:
                next_word = self.get_word_word(word_obj.next_word)
                next_word_type = word_obj.next_word['type']
                if next_word in ['.', ',']:
                    punc_after = next_word
                elif next_word_punc_after:
                    punc_after = next_word_punc_after
                    next_word_punc_after = None

            if word_obj.word.lower() == 'you' and next_word == 'know':
                prev_word = words[i - 1]
                if prev_word['type'] != 'punctuation':
                    converted_words[-1]['punc_after'] = ','
                if next_word_type != 'punctuation':
                    next_word_punc_after = ','

            converted_words.append({
                'start': word_obj.start,
                'end': word_obj.end,
                'confidence': word_obj.confidence,
                'word': word_obj.word,
                'always_capitalized': (
                    word_obj.is_proper_noun 
                    or word_obj.word == 'I'),
                'index': index,
                'punc_after': punc_after,
                'punc_before': punc_before,
            })

            index += 1
            punc_after = False

        return converted_words


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
