import logging
from pathlib import Path

from PIL import Image

from photo_tools.core.validation import validate_input_dir
from photo_tools.image.optimisation import optimise_jpeg, resize_to_max_width

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {".jpg", ".jpeg"}

MAX_WIDTH = 2500
MAX_FILE_SIZE_BYTES = 500 * 1024
MIN_QUALITY = 70
MAX_QUALITY = 100
OUTPUT_PREFIX = "lq_"


def optimise(input_dir: str, dry_run: bool = False) -> None:
    input_path = Path(input_dir)

    validate_input_dir(input_path)

    for file_path in input_path.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            logger.debug(f"Skipping (not a supported image): {file_path.name}")
            continue

        if file_path.name.startswith(OUTPUT_PREFIX):
            logger.debug(f"Skipping (already optimised): {file_path.name}")
            continue

        output_path = file_path.with_name(f"{OUTPUT_PREFIX}{file_path.name}")

        with Image.open(file_path) as original_img:
            img = original_img.convert("RGB")
            resized_img = resize_to_max_width(img, MAX_WIDTH)
            jpeg_bytes, quality = optimise_jpeg(resized_img, MAX_FILE_SIZE_BYTES)

        size_kb = len(jpeg_bytes) // 1024

        if dry_run:
            logger.info(
                f"[DRY RUN] Would optimise {file_path.name} → {output_path.name} "
                f"(quality={quality}, size={size_kb} KB)"
            )
            continue

        output_path.write_bytes(jpeg_bytes)

        logger.info(
            f"Optimised {file_path.name} → {output_path.name} "
            f"(quality={quality}, size={size_kb} KB)"
        )
