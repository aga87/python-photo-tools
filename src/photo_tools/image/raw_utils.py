import logging
import shutil
from collections.abc import Callable
from pathlib import Path

from photo_tools.core.validation import validate_input_dir

logger = logging.getLogger(__name__)

RAW_EXTENSIONS = {".raf"}
JPG_EXTENSIONS = {".jpg", ".jpeg"}

Reporter = Callable[[str, str], None]
RawMatcher = Callable[[Path, list[Path]], bool]


def move_raws_by_rule(
    raw_dir: str,
    jpg_dir: str,
    destination_dir_name: str,
    should_move: RawMatcher,
    report: Reporter,
    dry_run: bool = False,
    existing_warning_message: str | None = None,
) -> None:
    raw_path = Path(raw_dir)
    jpg_path = Path(jpg_dir)
    destination_dir = raw_path / destination_dir_name

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

        if not should_move(raw_file, jpg_files):
            continue

        target_file = destination_dir / raw_file.name

        if target_file.exists():
            skipped_existing_count += 1
            report(
                "warning",
                existing_warning_message
                or f"Skipping {raw_file.name}: already in {destination_dir_name}",
            )
            continue

        if dry_run:
            dry_run_count += 1
            report(
                "info",
                f"[DRY RUN] Would move {raw_file.name} -> {destination_dir}",
            )
            continue

        destination_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(raw_file), str(target_file))
        moved_count += 1
        report("info", f"Moved {raw_file.name} -> {destination_dir}")

    if dry_run:
        report("summary", f"Dry run complete: would move {dry_run_count} file(s)")
    else:
        report("summary", f"Moved {moved_count} file(s)")

    if skipped_existing_count:
        report(
            "warning",
            f"Skipped {skipped_existing_count} file(s): "
            f"already exist in {destination_dir_name}",
        )


def get_matching_jpgs(
    raw_file: Path,
    jpg_files: list[Path],
) -> list[Path]:
    raw_stem = raw_file.stem.lower()

    return [jpg for jpg in jpg_files if jpg.name.lower().startswith(raw_stem)]
