from io import BytesIO

from PIL import Image


def resize_to_max_width(img: Image.Image, max_width: int) -> Image.Image:
    if img.width <= max_width:
        return img

    new_height = int(img.height * (max_width / img.width))
    return img.resize((max_width, new_height), Image.Resampling.LANCZOS)


# Binary search to find the highest JPEG quality that produces a file
# within the maximum allowed size. Assumes file size increases with quality.
def optimise_jpeg(
    img: Image.Image,
    max_file_size_bytes: int,
    min_quality: int = 70,
    max_quality: int = 100,
) -> tuple[bytes, int]:
    """
    Binary search to find the highest JPEG quality that produces a file
    within the maximum allowed size.
    """

    low = min_quality
    high = max_quality

    best_bytes: bytes | None = None
    best_quality = min_quality

    while low <= high:
        quality = (low + high) // 2
        jpeg_bytes = encode_jpeg(img, quality)

        if len(jpeg_bytes) <= max_file_size_bytes:
            best_bytes = jpeg_bytes
            best_quality = quality
            low = quality + 1
        else:
            high = quality - 1

    if best_bytes is None:
        jpeg_bytes = encode_jpeg(img, min_quality)
        return jpeg_bytes, min_quality

    return best_bytes, best_quality


# Encode a PIL Image into JPEG bytes in memory using the given quality.
# This is used to evaluate the resulting file size without writing to disk.
# `quality` controls compression (higher = better quality, larger size).
def encode_jpeg(img: Image.Image, quality: int) -> bytes:
    buffer = BytesIO()
    img.save(
        buffer,
        format="JPEG",
        quality=quality,
        optimize=True,
    )
    return buffer.getvalue()
