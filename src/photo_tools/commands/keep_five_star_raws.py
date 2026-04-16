import logging
from collections.abc import Callable
from pathlib import Path

from photo_tools.image.metadata import get_exif_metadata, parse_rating
from photo_tools.image.raw_utils import get_matching_jpgs, move_raws_by_rule

logger = logging.getLogger(__name__)

RAW_EXTENSIONS = {".raf"}
JPG_EXTENSIONS = {".jpg", ".jpeg"}

Reporter = Callable[[str, str], None]
RawMatcher = Callable[[Path, list[Path]], bool]


def has_matching_five_star_jpg(
    raw_file: Path,
    jpg_files: list[Path],
) -> bool:
    matching_jpgs = get_matching_jpgs(raw_file, jpg_files)

    for jpg_file in matching_jpgs:
        try:
            metadata = get_exif_metadata(jpg_file)
            rating = parse_rating(metadata)
        except Exception as e:
            logger.debug(
                "Could not read rating for %s (%s)",
                jpg_file.name,
                e,
            )
            continue

        if rating == 5:
            return True

    return False


def keep_five_star_raws(
    raw_dir: str,
    jpg_dir: str,
    report: Reporter,
    dry_run: bool = False,
) -> None:
    move_raws_by_rule(
        raw_dir=raw_dir,
        jpg_dir=jpg_dir,
        destination_dir_name="raws-5-star",
        should_move=has_matching_five_star_jpg,
        report=report,
        dry_run=dry_run,
        existing_warning_message=None,
    )
