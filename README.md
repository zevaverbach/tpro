# tpro

Transcript Processing!  `tpro` takes JSON-formatted transcripts produced by
various speech-to-text services and converts them to various standardized
formats.

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

# Installation

    pip install tpro

## Non-pip Requirement:  Stanford NER JAR

  - download and unzip [this](https://nlp.stanford.edu/software/stanford-ner-2018-10-16.zip)
  - put these files in in /usr/local/bin/:
    - stanford-ner.jar
    - classifiers/english.all.3class.distsim.crf.ser.gz
  - on Ubuntu you might have to [update Java](https://askubuntu.com/questions/508546/howto-upgrade-java-on-ubuntu-14-04-lts)
