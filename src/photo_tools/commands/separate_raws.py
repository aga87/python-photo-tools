import logging
import shutil
from collections.abc import Callable
from pathlib import Path

from photo_tools.core.validation import validate_input_dir
from photo_tools.image.file_types import is_raw

logger = logging.getLogger(__name__)

OUTPUT_DIR = "raws"

Reporter = Callable[[str, str], None]


def separate_raws(
    input_dir: str,
    report: Reporter,
    dry_run: bool = False,
) -> None:
    input_path = Path(input_dir)

    validate_input_dir(input_path)

    raws_dir = input_path / OUTPUT_DIR

    moved_count = 0
    dry_run_count = 0
    skipped_existing_count = 0

    for file_path in input_path.iterdir():
        if not is_raw(file_path):
            logger.debug("Skipping (not RAW): %s", file_path.name)
            continue

        target_file = raws_dir / file_path.name

        if target_file.exists():
            skipped_existing_count += 1
            report(
                "warning",
                f"Skipping {file_path.name}: already exists in {OUTPUT_DIR}",
            )
            continue

        if dry_run:
            dry_run_count += 1
            report(
                "info",
                f"[DRY RUN] Would move {file_path.name} -> {raws_dir}",
            )
            continue

        raws_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(target_file))
        moved_count += 1

        report("info", f"Moved {file_path.name} -> {raws_dir}")

    # Summary

    if dry_run:
        report("summary", f"Dry run complete: would move {dry_run_count} file(s)")
    else:
        report("summary", f"Moved {moved_count} file(s)")

    if skipped_existing_count:
        report(
            "warning",
            f"Skipped {skipped_existing_count} file(s): already exist in raws",
        )
