from photo_tools.separate_raws import separate_raws


def noop_report(level: str, message: str) -> None:
    pass


def test_dry_run_does_not_move_raw_files(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    raw_file = input_dir / "photo.raf"
    raw_file.write_text("fake raw content")

    separate_raws(
        str(input_dir),
        report=noop_report,
        dry_run=True,
    )

    assert raw_file.exists()
    assert not (input_dir / "raws" / "photo.raf").exists()


def test_moves_raw_file_into_raws_folder(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    raw_file = input_dir / "photo.raf"
    raw_file.write_text("fake raw content")

    separate_raws(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    moved_file = input_dir / "raws" / "photo.raf"

    assert not raw_file.exists()
    assert moved_file.exists()


def test_leaves_non_raw_files_in_place(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    jpg_file = input_dir / "photo.jpg"
    txt_file = input_dir / "notes.txt"

    jpg_file.write_text("fake jpg content")
    txt_file.write_text("notes")

    separate_raws(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    assert jpg_file.exists()
    assert txt_file.exists()
    assert not (input_dir / "raws" / "photo.jpg").exists()
    assert not (input_dir / "raws" / "notes.txt").exists()


def test_moves_only_raw_files(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    raw_file = input_dir / "photo.raf"
    jpg_file = input_dir / "photo.jpg"

    raw_file.write_text("fake raw content")
    jpg_file.write_text("fake jpg content")

    separate_raws(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    assert (input_dir / "raws" / "photo.raf").exists()
    assert jpg_file.exists()
    assert not raw_file.exists()


def test_skips_file_when_destination_already_exists(tmp_path):
    input_dir = tmp_path / "input"
    raws_dir = input_dir / "raws"

    input_dir.mkdir()
    raws_dir.mkdir()

    source_file = input_dir / "photo.raf"
    existing_file = raws_dir / "photo.raf"

    source_file.write_text("new raw")
    existing_file.write_text("existing raw")

    separate_raws(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    assert source_file.exists()
    assert existing_file.exists()
    assert existing_file.read_text() == "existing raw"


def test_handles_empty_input_directory(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    separate_raws(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    assert not any(input_dir.iterdir())


def test_ignores_nested_directories(tmp_path):
    input_dir = tmp_path / "input"
    nested_dir = input_dir / "nested"

    input_dir.mkdir()
    nested_dir.mkdir()

    nested_raw = nested_dir / "photo.raf"
    nested_raw.write_text("fake raw content")

    separate_raws(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    assert nested_raw.exists()
    assert not (input_dir / "raws" / "photo.raf").exists()
