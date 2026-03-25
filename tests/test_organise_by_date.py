from datetime import datetime

from photo_tools.organise_by_date import organise_by_date


def test_dry_run_does_not_move_files(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    image_file = input_dir / "photo.jpg"
    image_file.write_text("fake image content")

    monkeypatch.setattr(
        "photo_tools.organise_by_date.get_image_date",
        lambda _: __import__("datetime").datetime(2024, 5, 17),
    )

    organise_by_date(str(input_dir), str(output_dir), dry_run=True)

    assert image_file.exists()
    assert not (output_dir / "2024-05-17" / "photo.jpg").exists()

def test_moves_file_into_date_folder(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    image_file = input_dir / "photo.jpg"
    image_file.write_text("fake image content")

    monkeypatch.setattr(
        "photo_tools.organise_by_date.get_image_date",
        lambda _: datetime(2024, 5, 17),
    )

    organise_by_date(str(input_dir), str(output_dir), dry_run=False)

    moved_file = output_dir / "2024-05-17" / "photo.jpg"

    assert not image_file.exists()
    assert moved_file.exists()