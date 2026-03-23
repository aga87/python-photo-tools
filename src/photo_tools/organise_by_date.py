from pathlib import Path

IMAGE_EXTENSIONS = {
    ".jpg", 
    ".jpeg",
    ".raf", # Fujifilm RAW
}

def organise_by_date(input_dir: str, output_dir: str) -> None:
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    if not input_path.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_path}")

    # Ensure intermediate output directory exists (for year/month structure)
    output_path.mkdir(parents=True, exist_ok=True)

    for file_path in input_path.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            print(f"Skipping (not an image): {file_path.name}")
            continue

        # TODO: EXIF date extraction
        print(f"Processing image: {file_path.name}")