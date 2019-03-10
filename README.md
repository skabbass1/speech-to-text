`speech-to-text` is a script which provides functionality to convert an audio file to a transcribed text document using `Google Cloud Speech`

Specifically, the script exposes functionality to:

1. Convert an MP3 file to a WAV file which could later be used for audio editing or for transcription.
2. Upload a large audio file to `Google Cloud Store` for processing by the `Google Cloud Speech` service.
3. Check the status of a transcription operation.

# Usage
```
speech-to-text.py --help
Usage: speech-to-text.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

  Commands:
  mp3-to-wav
  transcribe-audio
  transcription-status
  upload-audio
```

