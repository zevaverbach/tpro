from ..converter import TranscriptConverter




class GentleConverter(TranscriptConverter):

    name = 'gentle'

    def __init__(self, path):
        super().__init__(path)

    def get_word_objects(self, json_data):
        return json_data['words']

    def get_words(self, word_objects):
        return [self.get_word_word(w)
                for w in word_objects]

    @staticmethod
    def get_word_start(word_object):
        return word_object['start']

    @staticmethod
    def get_word_end(word_object):
        return word_object['end']

    @staticmethod
    def get_word_confidence(word_object):
        return 1

    @staticmethod
    def get_word_word(word_object):
        return word_object['alignedWord']

    def convert_words(self, word_objects, words, tagged_words=None):
        converted_words = []
        punc_before = False
        punc_after = False
        num_words = len(words)

        for i, w in enumerate(word_objects):
            word_obj = self.get_word_object(w, i, tagged_words, word_objects)

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

