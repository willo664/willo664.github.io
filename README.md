# Whisper Batch Transcription Utility

This repository provides a flexible utility to batch-transcribe audio and video files using the [OpenAI Whisper](https://github.com/openai/whisper) models. It supports parallel processing, automatic audio extraction, and customizable output options to streamline large transcription jobs.

## Requirements

### System Dependencies
- **FFmpeg** (required for processing video files or non-WAV audio formats)
  - Windows: `winget install ffmpeg` or follow an official installation guide
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt update && sudo apt install ffmpeg`

### Python Dependencies
- Python 3.9+
- `openai-whisper`
- `tqdm`

Install the Python dependencies:

```bash
pip install -U openai-whisper tqdm
```

## Usage

Basic usage transcribes every supported media file in the provided directory:

```bash
python transcribe_whisper.py /path/to/your/media_folder/
```

If you omit the folder path, the script will prompt you to enter one. The script scans the directory (non-recursively) for supported audio and video files, transcribes each one, and writes a matching `.txt` file to the chosen output directory.

### Advanced Options

```bash
python transcribe_whisper.py /path/to/media \
    --output_dir /path/to/transcripts \
    --model medium.en \
    --jobs 4
```

- `--output_dir`: Directory to save transcript files. Defaults to the input directory.
- `--model`: Whisper model to use (e.g., `tiny`, `base`, `small.en`, `medium`, `large`). Defaults to `small.en`.
- `--jobs`: Number of files to process in parallel. Defaults to the number of CPU cores.

### Notes

- The first run downloads the selected Whisper model. Subsequent runs reuse the cached model.
- Processing non-WAV files requires FFmpeg to be installed and available on your `PATH`.
- Progress updates include a live progress bar and per-file status messages.
