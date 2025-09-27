"""Batch transcribe WAV audio files using OpenAI Whisper.

Usage:
    python transcribe_whisper.py /path/to/folder

If no folder is provided, the script will prompt for one.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

import whisper


def find_audio_files(directory: Path) -> list[Path]:
    """Return all WAV files in *directory* (non-recursive).

    The files are returned in alphabetical order for predictable output.
    """
    return sorted(directory.glob("*.wav"))


def transcribe_file(model: "whisper.Whisper", audio_path: Path) -> Path:
    """Transcribe *audio_path* to a UTF-8 text file next to the audio file."""
    result = model.transcribe(str(audio_path), fp16=False)
    output_path = audio_path.with_suffix(".txt")
    output_path.write_text(result["text"], encoding="utf-8")
    return output_path


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe every WAV file in a folder using OpenAI Whisper"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        help="Folder containing WAV files to transcribe",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)

    directory = args.directory
    if directory is None:
        directory_input = input("Enter the path to the folder with WAV files: ").strip()
        directory = Path(directory_input)

    directory = directory.expanduser().resolve()
    if not directory.exists() or not directory.is_dir():
        print(f"Error: '{directory}' is not a valid directory.", file=sys.stderr)
        return 1

    print("Loading the Whisper model ('small.en')...")
    model = whisper.load_model("small.en")
    print("Model loaded.")

    audio_files = find_audio_files(directory)
    if not audio_files:
        print(f"Error: No .wav files found in '{directory}'")
        print("Please check that the path is correct and the folder contains .wav files.")
        return 1

    print(f"Found {len(audio_files)} audio file(s) to transcribe.")
    print("-" * 20)

    for audio_path in audio_files:
        print(f"Transcribing '{audio_path.name}'...")
        output_path = transcribe_file(model, audio_path)
        print(f"-> Transcription saved to '{output_path.name}'")
        print("-" * 20)

    print("All files have been transcribed. ✨")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
