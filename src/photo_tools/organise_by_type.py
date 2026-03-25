from pathlib import Path
import shutil
import logging

from photo_tools.core.validation import validate_input_dir

logger = logging.getLogger(__name__)

RAW_EXTENSIONS = {".raf"}
JPG_EXTENSIONS = {".jpg", ".jpeg"}


def organise_by_type(input_dir: str, dry_run: bool = False) -> None:
    input_path = Path(input_dir)

    validate_input_dir(input_path)

    raws_dir = input_path / "raws"
    jpgs_dir = input_path / "jpgs"

    for file_path in input_path.iterdir():
        if not file_path.is_file():
            continue

        ext = file_path.suffix.lower()

        if ext in RAW_EXTENSIONS:
            target_dir = raws_dir
        elif ext in JPG_EXTENSIONS:
            target_dir = jpgs_dir
        else:
            logger.debug(f"Skipping (unsupported): {file_path.name}")
            continue

        target_file = target_dir / file_path.name

        if target_file.exists():
            logger.info(f"Skipping (already exists): {target_file.name}")
            continue

        if dry_run:
            logger.info(f"[DRY RUN] Would move {file_path.name} → {target_dir}")
            continue

        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(target_file))
        logger.info(f"Moved {file_path.name} → {target_dir}")