from PIL import Image

from photo_tools.image.optimisation import resize_to_max_width


def test_does_not_resize_when_width_is_within_limit():
    img = Image.new("RGB", (1200, 800))

    result = resize_to_max_width(img, max_width=2500)

    assert result.size == img.size


def test_resizes_image_with_simple_ratio():
    img = Image.new("RGB", (4000, 2000))  # 2:1 ratio

    result = resize_to_max_width(img, max_width=2000)

    assert result.size == (2000, 1000)
