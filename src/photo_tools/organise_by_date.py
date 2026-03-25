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
) -> None:
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    validate_input_dir(input_path)

    output_path.mkdir(parents=True, exist_ok=True)

    for file_path in input_path.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            logger.debug(f"Skipping (not an image): {file_path.name}")
            continue

        try:
            date = get_image_date(file_path)

            # 1. Build folder: YYYY-MM-DD suffix
            folder_name = date.strftime("%Y-%m-%d")

            if suffix:
                cleaned_suffix = suffix.strip()
                if cleaned_suffix:
                    folder_name = f"{folder_name} {cleaned_suffix}"

            target_dir = output_path / folder_name

            # 2. Ensure directory exists
            if dry_run:
                logger.info(f"[DRY RUN] Would ensure directory exists: {target_dir}")
            else:
                target_dir.mkdir(parents=True, exist_ok=True)

            # 3. Move file
            target_file = target_dir / file_path.name

            if target_file.exists():
                logger.info(f"Skipping (already exists): {target_file.name}")
                continue

            if dry_run:
                logger.info(f"[DRY RUN] Would move {file_path.name} → {target_dir}")
            else:
                shutil.move(str(file_path), str(target_file))
                logger.info(f"Moved {file_path.name} → {target_dir}")

        except Exception as e:
            logger.debug(f"Skipping {file_path.name}: {e}")
