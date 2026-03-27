import logging
import shutil
from pathlib import Path

from photo_tools.core.validation import validate_input_dir

logger = logging.getLogger(__name__)

RAW_EXTENSIONS = {".raf"}
JPG_EXTENSIONS = {".jpg", ".jpeg"}


def clean_unpaired_raws(
    raw_dir: str,
    jpg_dir: str,
    dry_run: bool = False,
) -> None:
    raw_path = Path(raw_dir)
    jpg_path = Path(jpg_dir)
    trash_dir = raw_path / "raws-to-delete"

    validate_input_dir(raw_path)
    validate_input_dir(jpg_path)

    jpg_files = [
        f
        for f in jpg_path.iterdir()
        if f.is_file() and f.suffix.lower() in JPG_EXTENSIONS
    ]

    for raw_file in raw_path.iterdir():
        if not raw_file.is_file():
            continue

        if raw_file.suffix.lower() not in RAW_EXTENSIONS:
            continue

        raw_stem = raw_file.stem.lower()

        has_match = any(jpg.name.lower().startswith(raw_stem) for jpg in jpg_files)

        if has_match:
            logger.debug(f"Keeping {raw_file.name} (matched JPG)")
            continue

        target_file = trash_dir / raw_file.name

        if target_file.exists():
            logger.info(f"Skipping (already moved): {target_file.name}")
            continue

        if dry_run:
            logger.info(f"[DRY RUN] Would move {raw_file.name} → {trash_dir}")
            continue

        trash_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(raw_file), str(target_file))
        logger.info(f"Moved {raw_file.name} → {trash_dir}")
