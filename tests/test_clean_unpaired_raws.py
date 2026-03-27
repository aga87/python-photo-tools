from photo_tools.clean_unpaired_raws import clean_unpaired_raws


def test_dry_run_does_not_move_unpaired_raw_files(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    raw_file.write_text("fake raw content")

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=True)

    assert raw_file.exists()
    assert not (raw_dir / "raws-to-delete" / "photo.raf").exists()


def test_moves_unpaired_raw_file_into_raws_to_delete_folder(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    raw_file.write_text("fake raw content")

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=False)

    moved_file = raw_dir / "raws-to-delete" / "photo.raf"

    assert not raw_file.exists()
    assert moved_file.exists()


def test_keeps_raw_file_when_matching_jpg_exists(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    jpg_file = jpg_dir / "photo.jpg"

    raw_file.write_text("fake raw content")
    jpg_file.write_text("fake jpg content")

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=False)

    assert raw_file.exists()
    assert jpg_file.exists()
    assert not (raw_dir / "raws-to-delete" / "photo.raf").exists()


def test_keeps_raw_file_when_matching_jpg_starts_with_same_stem(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    jpg_file = jpg_dir / "photo_edit.jpg"

    raw_file.write_text("fake raw content")
    jpg_file.write_text("fake jpg content")

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=False)

    assert raw_file.exists()
    assert not (raw_dir / "raws-to-delete" / "photo.raf").exists()


def test_moves_only_unpaired_raw_files(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    matched_raw = raw_dir / "matched.raf"
    unmatched_raw = raw_dir / "unmatched.raf"
    matching_jpg = jpg_dir / "matched.jpg"

    matched_raw.write_text("matched raw")
    unmatched_raw.write_text("unmatched raw")
    matching_jpg.write_text("matching jpg")

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=False)

    assert matched_raw.exists()
    assert not unmatched_raw.exists()
    assert (raw_dir / "raws-to-delete" / "unmatched.raf").exists()


def test_ignores_non_raw_files_in_raw_directory(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    jpg_file = raw_dir / "photo.jpg"
    txt_file = raw_dir / "notes.txt"

    jpg_file.write_text("fake jpg content")
    txt_file.write_text("notes")

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=False)

    assert jpg_file.exists()
    assert txt_file.exists()
    assert not (raw_dir / "raws-to-delete" / "photo.jpg").exists()
    assert not (raw_dir / "raws-to-delete" / "notes.txt").exists()


def test_skips_file_when_destination_already_exists(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"
    trash_dir = raw_dir / "raws-to-delete"

    raw_dir.mkdir()
    jpg_dir.mkdir()
    trash_dir.mkdir()

    source_file = raw_dir / "photo.raf"
    existing_file = trash_dir / "photo.raf"

    source_file.write_text("new raw")
    existing_file.write_text("existing raw")

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=False)

    assert source_file.exists()
    assert existing_file.exists()
    assert existing_file.read_text() == "existing raw"


def test_handles_empty_directories(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=False)

    assert not any(raw_dir.iterdir())


def test_ignores_nested_directories(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"
    nested_dir = raw_dir / "nested"

    raw_dir.mkdir()
    jpg_dir.mkdir()
    nested_dir.mkdir()

    nested_raw = nested_dir / "photo.raf"
    nested_raw.write_text("fake raw content")

    clean_unpaired_raws(str(raw_dir), str(jpg_dir), dry_run=False)

    assert nested_raw.exists()
    assert not (raw_dir / "raws-to-delete" / "photo.raf").exists()