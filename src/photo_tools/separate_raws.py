import logging
import shutil
from pathlib import Path

from photo_tools.core.validation import validate_input_dir

logger = logging.getLogger(__name__)

RAW_EXTENSIONS = {".raf"}

OUTPUT_DIR = "raws"


def separate_raws(
    input_dir: str,
    dry_run: bool = False,
    verbose: bool = False,
) -> None:
    input_path = Path(input_dir)

    validate_input_dir(input_path)

    raws_dir = input_path / OUTPUT_DIR

    # For the summary
    moved_count = 0
    dry_run_count = 0
    skipped_existing_count = 0

    for file_path in input_path.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in RAW_EXTENSIONS:
            logger.debug(f"Skipping (not RAW): {file_path.name}")
            continue

        target_file = raws_dir / file_path.name

        if target_file.exists():
            skipped_existing_count += 1
            logger.warning(f"Skipping {file_path.name}: already exists in {OUTPUT_DIR}")
            continue

        if dry_run:
            dry_run_count += 1
            if verbose:
                logger.info(f"[DRY RUN] Would move {file_path.name} -> {raws_dir}")
            continue

        raws_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(target_file))
        moved_count += 1

        if verbose:
            logger.info(f"Moved {file_path.name} -> {raws_dir}")

    # Summary (always)

    if dry_run:
        logger.info(f"Dry run complete: would move {dry_run_count} file(s)")
    else:
        logger.info(f"Moved {moved_count} file(s)")

    if skipped_existing_count:
        logger.warning(
            f"Skipped {skipped_existing_count} file(s): already exist in raws"
        )