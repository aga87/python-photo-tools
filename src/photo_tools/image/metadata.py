import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def get_exif_metadata(file_path: Path) -> Dict[str, Any]:
    result = subprocess.run(
        ["exiftool", "-json", str(file_path)],
        capture_output=True,
        text=True,
        check=True,
    )

    data = json.loads(result.stdout)

    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        raise ValueError("Invalid EXIF data format")

    return data[0]


def get_image_date(file_path: Path) -> datetime:
    exif_data = get_exif_metadata(file_path)

    for key in ["DateTimeOriginal", "CreateDate", "ModifyDate"]:
        value = exif_data.get(key)
        if value:
            return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

    raise ValueError("No usable date field found")
