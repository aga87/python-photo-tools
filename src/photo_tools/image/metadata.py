import json
import subprocess
from datetime import datetime
from pathlib import Path


def get_exif_metadata(file_path: Path) -> dict:
    result = subprocess.run(
        ["exiftool", "-json", str(file_path)],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)

    if not data or not data[0]:
        raise ValueError("No EXIF data")

    return data[0]


def get_image_date(file_path: Path) -> datetime:
    exif_data = get_exif_metadata(file_path)

    for key in ["DateTimeOriginal", "CreateDate", "ModifyDate"]:
        value = exif_data.get(key)
        if value:
            return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

    raise ValueError("No usable date field found")
