from pathlib import Path

RAW_EXTENSIONS = {
    ".cr2",
    ".cr3",
    ".nef",
    ".arw",
    ".raf",
    ".orf",
    ".rw2",
    ".dng",
    ".pef",
    ".srw",
    ".x3f",
}

JPG_EXTENSIONS = {".jpg", ".jpeg"}


def is_raw(file_path: Path) -> bool:
    return file_path.is_file() and file_path.suffix.lower() in RAW_EXTENSIONS


def is_jpg(file_path: Path) -> bool:
    return file_path.is_file() and file_path.suffix.lower() in JPG_EXTENSIONS
