# Whisper Batch Transcription

This repository provides a small utility to batch-transcribe WAV audio files using the [OpenAI Whisper](https://github.com/openai/whisper) `small.en` model.

## Requirements

- Python 3.9+
- `openai-whisper`

Install the dependency:

```bash
pip install -U openai-whisper
```

## Usage

```bash
python transcribe_whisper.py /path/to/your/wav_folder/
```

If you omit the folder path, the script will prompt you to enter one. The script transcribes every `.wav` file in the directory (non-recursively) and creates a matching `.txt` file for each audio file containing the transcription.

The first time you run the script, Whisper will download the `small.en` model (~1.4 GB). Subsequent runs will re-use the cached model.
