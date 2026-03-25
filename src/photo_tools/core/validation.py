from pathlib import Path


def validate_input_dir(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Input path does not exist: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {path}")
