import logging
import shutil
from pathlib import Path

from photo_tools.core.validation import validate_input_dir
from photo_tools.image.metadata import get_image_date

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".raf",
}


def organise_by_date(
    input_dir: str,
    output_dir: str,
    suffix: str | None = None,
    dry_run: bool = False,
    verbose: bool = False,
) -> None:
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    validate_input_dir(input_path)

    # For the summary 
    moved_count = 0
    dry_run_count = 0
    skipped_missing_date_count = 0
    skipped_existing_count = 0

    cleaned_suffix = suffix.strip() if suffix and suffix.strip() else None

    for file_path in input_path.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            logger.debug(f"Skipping unsupported file: {file_path.name}")
            continue

        try:
            date = get_image_date(file_path)
        except Exception as e:
            skipped_missing_date_count += 1
            logger.warning(f"Skipping {file_path.name}: could not read capture date")
            logger.debug(f"Reason: {e}")
            continue

        folder_name = date.strftime("%Y-%m-%d")
        if cleaned_suffix:
            folder_name = f"{folder_name} {cleaned_suffix}"

        target_dir = output_path / folder_name
        target_file = target_dir / file_path.name

        if target_file.exists():
            skipped_existing_count += 1
            logger.warning(f"Skipping {file_path.name}: destination already exists")
            continue

        if dry_run:
            dry_run_count += 1
            if verbose:
                logger.info(
                    f"[DRY RUN] Would move {file_path.name} -> {target_dir}"
                )
            continue

        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(target_file))
        moved_count += 1

        if verbose:
            logger.info(f"Moved {file_path.name} -> {target_dir}")

    # Summary (always shown)

    if dry_run:
        logger.info(f"Dry run complete: would move {dry_run_count} file(s)")
    else:
        logger.info(f"Moved {moved_count} file(s)")

    if skipped_missing_date_count:
        logger.warning(
            f"Skipped {skipped_missing_date_count} file(s): could not read capture date"
        )

    if skipped_existing_count:
        logger.warning(
            f"Skipped {skipped_existing_count} file(s): destination already exists"
        )