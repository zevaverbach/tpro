import json

def universal(self):
    return json.dumps(self.converted_words, indent=4)

def vo(self):
    transcript = []

    for word in self.converted_words:
        if word['always_capitalized']:
            word_word = word['word'].title()
        else:
            word_word = word['word']

        transcript.append({
            'start': word['start'],
            'stop': word['end'],
            'text': word_word,
            })

    return json.dumps(transcript, indent=4)

