import json
import os

from converters import converters


class TranscriptConverter:

    def __init__(self, path, format_name):
        self.path = path
        with open(path, 'r') as fin:
            self.words = converters[format_name](json.load(fin))

    def to_json(self):
        return json.dumps(self.words, indent=4)

    def save(self):
        name = f"{os.path.basename(self.path).split('.json')[0]}_processed.json"
        with open(name, 'w') as fout:
            fout.write(self.to_json())
