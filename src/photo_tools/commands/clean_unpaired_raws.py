import logging
import shutil
from collections.abc import Callable
from pathlib import Path

from photo_tools.core.validation import validate_input_dir

logger = logging.getLogger(__name__)

RAW_EXTENSIONS = {".raf"}
JPG_EXTENSIONS = {".jpg", ".jpeg"}

Reporter = Callable[[str, str], None]


def clean_unpaired_raws(
    raw_dir: str,
    jpg_dir: str,
    report: Reporter,
    dry_run: bool = False,
) -> None:
    raw_path = Path(raw_dir)
    jpg_path = Path(jpg_dir)
    trash_dir = raw_path / "raws-to-delete"

    validate_input_dir(raw_path)
    validate_input_dir(jpg_path)

    moved_count = 0
    dry_run_count = 0
    skipped_existing_count = 0

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
            logger.debug("Keeping %s (matched JPG)", raw_file.name)
            continue

        target_file = trash_dir / raw_file.name

        if target_file.exists():
            skipped_existing_count += 1
            report(
                "warning",
                f"Skipping {raw_file.name}: already in raws-to-delete",
            )
            continue

        if dry_run:
            dry_run_count += 1
            report(
                "info",
                f"[DRY RUN] Would move {raw_file.name} -> {trash_dir}",
            )
            continue

        trash_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(raw_file), str(target_file))
        moved_count += 1

        report("info", f"Moved {raw_file.name} -> {trash_dir}")

    # Summary

    if dry_run:
        report("summary", f"Dry run complete: would move {dry_run_count} file(s)")
    else:
        report("summary", f"Moved {moved_count} file(s)")

    if skipped_existing_count:
        report(
            "warning",
            f"Skipped {skipped_existing_count} file(s): "
            "already exist in raws-to-delete",
        )
