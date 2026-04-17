from pathlib import Path

import pytest

from photo_tools.image.raw_utils import is_jpg, is_raw


@pytest.mark.parametrize(
    ("filename"),
    [
        "image.cr2",
        "image.CR2",
        "image.cr3",
        "image.nef",
        "image.NeF",
        "image.arw",
        "image.raf",
        "image.orf",
        "image.rw2",
        "image.dng",
        "image.pef",
        "image.srw",
        "image.x3f",
    ],
)
def test_is_raw_returns_true_for_supported_raw_files(
    tmp_path: Path,
    filename: str,
) -> None:
    file_path = tmp_path / filename
    file_path.touch()

    assert is_raw(file_path) is True


@pytest.mark.parametrize(
    ("filename"),
    [
        "image.jpg",
        "image.jpeg",
        "image.png",
        "image.txt",
        "image",
    ],
)
def test_is_raw_returns_false_for_non_raw_files(
    tmp_path: Path,
    filename: str,
) -> None:
    file_path = tmp_path / filename
    file_path.touch()

    assert is_raw(file_path) is False


def test_is_raw_returns_false_for_directory(tmp_path: Path) -> None:
    dir_path = tmp_path / "image.cr2"
    dir_path.mkdir()

    assert is_raw(dir_path) is False


def test_is_raw_returns_false_for_non_existing_path(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.cr2"

    assert is_raw(file_path) is False


@pytest.mark.parametrize(
    ("filename"),
    [
        "image.jpg",
        "image.jpeg",
        "image.JPG",
        "image.JPEG",
    ],
)
def test_is_jpg_returns_true_for_supported_jpg_files(
    tmp_path: Path,
    filename: str,
) -> None:
    file_path = tmp_path / filename
    file_path.touch()

    assert is_jpg(file_path) is True


@pytest.mark.parametrize(
    ("filename"),
    [
        "image.cr2",
        "image.nef",
        "image.png",
        "image.txt",
        "image",
    ],
)
def test_is_jpg_returns_false_for_non_jpg_files(
    tmp_path: Path,
    filename: str,
) -> None:
    file_path = tmp_path / filename
    file_path.touch()

    assert is_jpg(file_path) is False


def test_is_jpg_returns_false_for_directory(tmp_path: Path) -> None:
    dir_path = tmp_path / "image.jpg"
    dir_path.mkdir()

    assert is_jpg(dir_path) is False


def test_is_jpg_returns_false_for_non_existing_path(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.jpg"

    assert is_jpg(file_path) is False
