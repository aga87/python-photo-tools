import logging
import shutil
from pathlib import Path

from photo_tools.core.validation import validate_input_dir

logger = logging.getLogger(__name__)

RAW_EXTENSIONS = {".raf"}


def separate_raws(input_dir: str, dry_run: bool = False) -> None:
    input_path = Path(input_dir)

    validate_input_dir(input_path)

    raws_dir = input_path / "raws"

    for file_path in input_path.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in RAW_EXTENSIONS:
            logger.debug(f"Skipping (not RAW): {file_path.name}")
            continue

        target_file = raws_dir / file_path.name

        if target_file.exists():
            logger.info(f"Skipping (already exists): {target_file.name}")
            continue

        if dry_run:
            logger.info(f"[DRY RUN] Would move {file_path.name} → {raws_dir}")
            continue

        raws_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(target_file))
        logger.info(f"Moved {file_path.name} → {raws_dir}")
