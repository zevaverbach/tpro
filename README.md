# tpro

Transcript Processing! `tpro` takes JSON-formatted transcripts produced by
various speech-to-text services and converts them to various standardized
formats.

# Installation and Usage

## Non-pip Requirement:  Stanford NER JAR

  - download and unzip [this](https://nlp.stanford.edu/software/stanford-ner-2018-10-16.zip)
  - put these files in in /usr/local/bin/:
    - stanford-ner.jar
    - classifiers/english.all.3class.distsim.crf.ser.gz
  - you might have to [update Java](https://askubuntu.com/questions/508546/howto-upgrade-java-on-ubuntu-14-04-lts) on Linux

## Pip

    $ pip install tpro

## Usage

    $ tpro --help

    Usage: tpro [OPTIONS] JSON_PATH_OR_DATA [amazon|gentle|speechmatics]
            [universal_transcript|viral_overlay]

    Options:
      -s, --save TEXT  save to file
      --help           Show this message and exit.

### Example

    $ tpro '{

        "job": {
          "lang": "en",
          "user_id": 2152310,
          "name": "recording.mp4",
          "duration": 7,
          "created_at": "Mon Nov 12 14:57:06 2018",
          "id": 9871364
        },
        "speakers": [
          {
            "duration": "6.87",
            "confidence": null,
            "name": "M2",
            "time": "5.98"
          }
        ],
        "words": [
          {
            "duration": "0.13",
            "confidence": "0.670",
            "name": "Hello",
            "time": "5.98"
          },
          {
            "duration": "0.45",
            "confidence": "1.000",
            "name": "there",
            "time": "6.14"
          }
      ]
      
    }' speechmatics universal_transcript

    [
        {
            "start": 5.98,
            "end": 6.11,
            "confidence": 0.67,
            "word": "Hello",
            "always_capitalized": false,
            "punc_after": false,
            "punc_before": false
        },
        {
            "start": 6.14,
            "end": 6.59,
            "confidence": 1.0,
            "word": "there",
            "always_capitalized": false,
            "punc_after": false,
            "punc_before": false
        }
    ]

    $

# STT Services

- [Speechmatics](https://www.speechmatics.com/)
- [Amazon Transcribe](https://aws.amazon.com/transcribe/)
- [Gentle](https://github.com/lowerquality/gentle)

## Planned

- [Watson](https://www.ibm.com/watson/services/speech-to-text/) 
- [Google Speech](https://cloud.google.com/speech-to-text/)
- [Mozilla's new open-source STT thing](https://github.com/mozilla/DeepSpeech)

# Output Formats

- [Universal Transcript](https://gist.github.com/zevaverbach/d2b7a19397607677878aa3268fda1002#example) (JSON)
- [viraloverlay](https://github.com/zevaverbach/viraloverlay#json-transcript-format) (JSON)

## Planned

- Word (`.doc`, `.docx`)
- text files
- SRT (subtitles)
