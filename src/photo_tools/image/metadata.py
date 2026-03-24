from pathlib import Path
from datetime import datetime
from PIL import Image, ExifTags


def get_exif_metadata(file_path: Path) -> dict:
    with Image.open(file_path) as img:
        exif = img._getexif()

        if not exif:
            raise ValueError("No EXIF data")

        return {
            ExifTags.TAGS.get(tag): value
            for tag, value in exif.items()
        }


def get_image_date(file_path: Path) -> datetime:
    exif_data = get_exif_metadata(file_path)

    date_str = exif_data.get("DateTimeOriginal")

    if not date_str:
        raise ValueError("No DateTimeOriginal")

    date_str = date_str.strip(" \x00")

    return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")