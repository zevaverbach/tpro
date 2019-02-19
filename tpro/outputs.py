import json

def universal_transcript(self):
    return json.dumps(self.converted_words, indent=4)

def viral_overlay(self):
    return json.dumps([{
  'start': word['start'],
  'stop': word['end'],
  'text': word['word'].title() if word['always_capitalized'] else word['word']}

              for word in self.converted_words], indent=4
            )

