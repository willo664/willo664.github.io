"""Batch transcribe audio and video files using OpenAI Whisper."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from pathlib import Path
from typing import Iterable

import whisper
from tqdm import tqdm

SUPPORTED_EXTENSIONS = [
    ".wav",
    ".mp3",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
]

# Each worker process maintains its own cache of loaded models
_MODEL_CACHE: dict[str, whisper.Whisper] = {}


def find_media_files(directory: Path) -> list[Path]:
    """Return all supported media files in *directory* (non-recursive)."""

    files: list[Path] = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(directory.glob(f"*{ext}"))
    return sorted(files)


def is_ffmpeg_installed() -> bool:
    """Return True if FFmpeg is available on the current PATH."""

    try:
        subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_to_wav(media_path: Path, temp_dir: Path) -> Path:
    """Convert *media_path* to a mono 16 kHz WAV file stored in *temp_dir*."""

    wav_path = temp_dir / f"{media_path.stem}_{uuid.uuid4().hex}.wav"
    command = [
        "ffmpeg",
        "-i",
        str(media_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(wav_path),
    ]
    subprocess.run(command, check=True, capture_output=True)
    return wav_path


def process_file(
    media_path: Path,
    model_name: str,
    output_dir: Path,
    temp_dir: Path,
) -> tuple[Path, str]:
    """Transcribe a single media file and return the status."""

    if model_name not in _MODEL_CACHE:
        _MODEL_CACHE[model_name] = whisper.load_model(model_name)
    model = _MODEL_CACHE[model_name]

    audio_to_transcribe = media_path
    cleanup_path: Path | None = None

    if media_path.suffix.lower() != ".wav":
        try:
            audio_to_transcribe = convert_to_wav(media_path, temp_dir)
            cleanup_path = audio_to_transcribe
        except subprocess.CalledProcessError as exc:  # pragma: no cover - ffmpeg failure details
            error = exc.stderr.decode(errors="ignore") if exc.stderr else str(exc)
            return media_path, f"FFmpeg failed: {error}"

    result = model.transcribe(str(audio_to_transcribe), fp16=False)

    output_path = output_dir / media_path.with_suffix(".txt").name
    output_path.write_text(result["text"], encoding="utf-8")

    if cleanup_path and cleanup_path.exists():
        cleanup_path.unlink()

    return media_path, "Success"


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe media files in a folder using OpenAI Whisper.",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        help="Folder containing media files to transcribe.",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default=None,
        help="Directory to save transcript files. Defaults to the input directory.",
    )
    parser.add_argument(
        "--model",
        default="small.en",
        help="Whisper model to use (e.g., tiny, base, small.en, medium, large).",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=os.cpu_count() or 1,
        help="Number of files to transcribe in parallel. Defaults to CPU core count.",
    )
    return parser.parse_args(argv)


def prompt_for_directory() -> Path:
    directory_input = input("Enter the path to the folder with media files: ").strip()
    return Path(directory_input)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)

    input_dir = args.directory or prompt_for_directory()
    input_dir = input_dir.expanduser().resolve()

    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' is not a valid directory.", file=sys.stderr)
        return 1

    output_dir = args.output_dir or input_dir
    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    media_files = find_media_files(input_dir)
    if not media_files:
        print(f"No supported media files found in '{input_dir}'.")
        print("Please add audio or video files and run the script again.")
        return 1

    needs_ffmpeg = any(path.suffix.lower() != ".wav" for path in media_files)
    if needs_ffmpeg and not is_ffmpeg_installed():
        print(
            "Error: FFmpeg is required to process non-WAV files but was not found in PATH.",
            file=sys.stderr,
        )
        print("Install FFmpeg and try again.", file=sys.stderr)
        return 1

    jobs = max(1, args.jobs)

    print(f"Found {len(media_files)} media file(s) to transcribe.")
    print(f"Using model: {args.model}")
    print(f"Parallel jobs: {jobs}")

    process_func = partial(
        process_file,
        model_name=args.model,
        output_dir=output_dir,
    )

    if jobs == 1:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            for media_path in tqdm(media_files, desc="Transcribing", unit="file"):
                _, status = process_func(media_path=media_path, temp_dir=temp_path)
                if status != "Success":
                    print(f"Failed to process {media_path.name}: {status}", file=sys.stderr)
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            process_with_temp = partial(process_func, temp_dir=temp_path)
            with ProcessPoolExecutor(max_workers=jobs) as executor:
                futures = [executor.submit(process_with_temp, path) for path in media_files]
                for future in tqdm(
                    as_completed(futures),
                    total=len(media_files),
                    desc="Transcribing",
                    unit="file",
                ):
                    media_path, status = future.result()
                    if status != "Success":
                        print(f"Failed to process {media_path.name}: {status}", file=sys.stderr)

    print("\nAll files have been transcribed. ✨")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
