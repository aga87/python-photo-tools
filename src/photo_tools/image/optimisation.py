from PIL import Image


def resize_to_max_width(img: Image.Image, max_width: int) -> Image.Image:
    if img.width <= max_width:
        return img

    new_height = int(img.height * (max_width / img.width))
    return img.resize((max_width, new_height), Image.Resampling.LANCZOS)
