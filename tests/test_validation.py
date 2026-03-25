import pytest

from photo_tools.core.validation import validate_input_dir


def test_validate_input_dir_raises_when_path_does_not_exist(tmp_path):
    missing_path = tmp_path / "missing"

    with pytest.raises(FileNotFoundError, match="Input path does not exist"):
        validate_input_dir(missing_path)


def test_validate_input_dir_raises_when_path_is_not_a_directory(tmp_path):
    file_path = tmp_path / "file.txt"
    file_path.write_text("not a directory")

    with pytest.raises(NotADirectoryError, match="Input path is not a directory"):
        validate_input_dir(file_path)