import logging
from collections.abc import Callable
from pathlib import Path

from photo_tools.image.raw_utils import get_matching_jpgs, move_raws_by_rule

logger = logging.getLogger(__name__)

Reporter = Callable[[str, str], None]
RawMatcher = Callable[[Path, list[Path]], bool]


def has_matching_jpg(
    raw_file: Path,
    jpg_files: list[Path],
) -> bool:
    return bool(get_matching_jpgs(raw_file, jpg_files))


def clean_unpaired_raws(
    raw_dir: str,
    jpg_dir: str,
    report: Reporter,
    dry_run: bool = False,
) -> None:
    move_raws_by_rule(
        raw_dir=raw_dir,
        jpg_dir=jpg_dir,
        destination_dir_name="raws-to-delete",
        should_move=lambda raw_file, jpg_files: (
            not has_matching_jpg(
                raw_file,
                jpg_files,
            )
        ),
        report=report,
        dry_run=dry_run,
        existing_warning_message=None,
    )
