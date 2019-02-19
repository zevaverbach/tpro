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
- [viraloverlay](https://github.com/zevaverbach/viraloverlay) (JSON)

## Planned

- Word (`.doc`, `.docx`)
- text files
- SRT (subtitles)

# Installation

    pip install tpro

## Non-pip Requirement:  Stanford NER JAR

  - download the .jar [here](https://nlp.stanford.edu/software/CRF-NER.shtml#Download)
  - put these files in in /usr/local/bin/:
    - stanford-ner.jar
    - english.all.3class.distsim.crf.ser.gz
