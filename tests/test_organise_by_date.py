from datetime import datetime

from photo_tools.organise_by_date import organise_by_date


def noop_report(level: str, message: str) -> None:
    pass


def test_dry_run_does_not_move_files(tmp_path, monkeypatch):
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

    organise_by_date(
        str(input_dir),
        str(output_dir),
        report=noop_report,
        dry_run=True,
    )

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

    organise_by_date(
        str(input_dir),
        str(output_dir),
        report=noop_report,
        dry_run=False,
    )

    moved_file = output_dir / "2024-05-17" / "photo.jpg"

    assert not image_file.exists()
    assert moved_file.exists()


def test_skips_unsupported_files(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    supported_file = input_dir / "photo.jpg"
    unsupported_file = input_dir / "notes.txt"

    supported_file.write_text("fake image content")
    unsupported_file.write_text("not an image")

    monkeypatch.setattr(
        "photo_tools.organise_by_date.get_image_date",
        lambda _: datetime(2024, 5, 17),
    )

    organise_by_date(
        str(input_dir),
        str(output_dir),
        report=noop_report,
        dry_run=False,
    )

    moved_file = output_dir / "2024-05-17" / "photo.jpg"

    assert moved_file.exists()
    assert unsupported_file.exists()
    assert not (output_dir / "2024-05-17" / "notes.txt").exists()


def test_skips_files_with_missing_date_metadata(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    image_file = input_dir / "photo.jpg"
    image_file.write_text("fake image content")

    monkeypatch.setattr(
        "photo_tools.organise_by_date.get_image_date",
        lambda _: (_ for _ in ()).throw(ValueError("No DateTimeOriginal")),
    )

    organise_by_date(
        str(input_dir),
        str(output_dir),
        report=noop_report,
        dry_run=False,
    )

    assert image_file.exists()
    assert not any(output_dir.rglob("*"))


def test_moves_files_into_separate_date_folders(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    first_file = input_dir / "first.jpg"
    second_file = input_dir / "second.jpg"

    first_file.write_text("fake image content")
    second_file.write_text("fake image content")

    dates = {
        "first.jpg": datetime(2024, 5, 17),
        "second.jpg": datetime(2024, 5, 18),
    }

    monkeypatch.setattr(
        "photo_tools.organise_by_date.get_image_date",
        lambda file_path: dates[file_path.name],
    )

    organise_by_date(
        str(input_dir),
        str(output_dir),
        report=noop_report,
        dry_run=False,
    )

    assert (output_dir / "2024-05-17" / "first.jpg").exists()
    assert (output_dir / "2024-05-18" / "second.jpg").exists()
    assert not first_file.exists()
    assert not second_file.exists()


def test_skips_file_when_destination_already_exists(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    target_dir = output_dir / "2024-05-17"

    input_dir.mkdir()
    target_dir.mkdir(parents=True)

    source_file = input_dir / "photo.jpg"
    existing_file = target_dir / "photo.jpg"

    source_file.write_text("new file")
    existing_file.write_text("existing file")

    monkeypatch.setattr(
        "photo_tools.organise_by_date.get_image_date",
        lambda _: datetime(2024, 5, 17),
    )

    organise_by_date(
        str(input_dir),
        str(output_dir),
        report=noop_report,
        dry_run=False,
    )

    assert source_file.exists()
    assert existing_file.exists()
    assert existing_file.read_text() == "existing file"


def test_handles_empty_input_directory(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"

    input_dir.mkdir()
    output_dir.mkdir()

    organise_by_date(
        str(input_dir),
        str(output_dir),
        report=noop_report,
        dry_run=False,
    )

    assert not any(output_dir.iterdir())
