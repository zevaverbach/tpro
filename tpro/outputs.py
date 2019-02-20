import json

def universal_transcript(self, pretty=False):
    return json.dumps(self.converted_words, indent=4 if pretty else None)

def viral_overlay(self, pretty=False):
    return json.dumps([{
  'start': word['start'],
  'stop': word['end'],
  'text': word['word'].title() if word['always_capitalized'] else word['word']}

              for word in self.converted_words], indent=4 if pretty else None
            )

