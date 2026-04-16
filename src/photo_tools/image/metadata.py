import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


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


def parse_rating(metadata: dict[str, str]) -> int | None:
    rating_keys = (
        "XMP:Rating",
        "Rating",
        "XMP-xmp:Rating",
    )

    for key in rating_keys:
        value = metadata.get(key)

        if value in (None, ""):
            continue

        try:
            rating = int(str(value).strip())

            logger.debug(
                "Parsed rating %s from metadata key '%s'",
                rating,
                key,
            )

            return rating

        except ValueError:
            logger.warning(
                "Invalid rating value '%s' found in key '%s'",
                value,
                key,
            )
            return None

    logger.debug("No rating metadata found")

    return None
