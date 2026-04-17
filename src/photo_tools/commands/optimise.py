import logging
from collections.abc import Callable
from pathlib import Path

from PIL import Image

from photo_tools.core.validation import validate_input_dir
from photo_tools.image.file_types import is_jpg
from photo_tools.image.optimisation import optimise_jpeg, resize_to_max_width

logger = logging.getLogger(__name__)


MAX_WIDTH = 2500
MAX_FILE_SIZE_BYTES = 500 * 1024
MIN_QUALITY = 70
MAX_QUALITY = 100
OUTPUT_PREFIX = "lq_"

Reporter = Callable[[str, str], None]


def optimise(
    input_dir: str,
    report: Reporter,
    dry_run: bool = False,
) -> None:
    input_path = Path(input_dir)

    validate_input_dir(input_path)

    optimised_count = 0
    dry_run_count = 0
    failed_count = 0

    for file_path in input_path.iterdir():
        if not is_jpg(file_path):
            logger.debug("Skipping (not a supported image): %s", file_path.name)
            continue

        if file_path.name.startswith(OUTPUT_PREFIX):
            logger.debug("Skipping (already optimised): %s", file_path.name)
            continue

        output_path = file_path.with_name(f"{OUTPUT_PREFIX}{file_path.name}")

        try:
            with Image.open(file_path) as original_img:
                img = original_img.convert("RGB")
                resized_img = resize_to_max_width(img, MAX_WIDTH)
                jpeg_bytes, quality = optimise_jpeg(
                    resized_img,
                    MAX_FILE_SIZE_BYTES,
                )
        except Exception as e:
            failed_count += 1
            report("warning", f"Skipping {file_path.name}: could not optimise image")
            logger.debug("Reason: %s", e)
            continue

        size_kb = len(jpeg_bytes) // 1024

        if dry_run:
            dry_run_count += 1
            report(
                "info",
                f"[DRY RUN] Would optimise {file_path.name} -> {output_path.name} "
                f"(quality={quality}, size={size_kb} KB)",
            )
            continue

        output_path.write_bytes(jpeg_bytes)
        optimised_count += 1

        report(
            "info",
            f"Optimised {file_path.name} -> {output_path.name} "
            f"(quality={quality}, size={size_kb} KB)",
        )

    if dry_run:
        report("summary", f"Dry run complete: would optimise {dry_run_count} file(s)")
    else:
        report("summary", f"Optimised {optimised_count} file(s)")

    if failed_count:
        report("warning", f"Skipped {failed_count} file(s): could not optimise image")
