from io import BytesIO
from pathlib import Path
import logging

from PIL import Image

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {".jpg", ".jpeg"}

MAX_WIDTH = 2500
MAX_FILE_SIZE_BYTES = 500 * 1024
MIN_QUALITY = 70
MAX_QUALITY = 100
OUTPUT_PREFIX = "lq_"


def optimise(input_dir: str, dry_run: bool = False) -> None:
    input_path = Path(input_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    if not input_path.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_path}")

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

        with Image.open(file_path) as img:
            img = img.convert("RGB")
            resized_img = resize_to_max_width(img, MAX_WIDTH)
            jpeg_bytes, quality = find_best_jpeg_bytes(resized_img)

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


def resize_to_max_width(img: Image.Image, max_width: int) -> Image.Image:
    if img.width <= max_width:
        return img

    new_height = int(img.height * (max_width / img.width))
    return img.resize((max_width, new_height), Image.Resampling.LANCZOS)


def find_best_jpeg_bytes(img: Image.Image) -> tuple[bytes, int]:
    low = MIN_QUALITY
    high = MAX_QUALITY

    best_bytes: bytes | None = None
    best_quality = MIN_QUALITY

    while low <= high:
        quality = (low + high) // 2
        jpeg_bytes = render_jpeg_bytes(img, quality)

        if len(jpeg_bytes) <= MAX_FILE_SIZE_BYTES:
            best_bytes = jpeg_bytes
            best_quality = quality
            low = quality + 1
        else:
            high = quality - 1

    if best_bytes is None:
        return render_jpeg_bytes(img, MIN_QUALITY), MIN_QUALITY

    return best_bytes, best_quality


def render_jpeg_bytes(img: Image.Image, quality: int) -> bytes:
    buffer = BytesIO()
    img.save(
        buffer,
        format="JPEG",
        quality=quality,
        optimize=True,
    )
    return buffer.getvalue()