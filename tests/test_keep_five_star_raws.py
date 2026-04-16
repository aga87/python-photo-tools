import photo_tools.commands.keep_five_star_raws as keep_starred_module
from photo_tools.commands.keep_five_star_raws import keep_five_star_raws


def noop_report(level: str, message: str) -> None:
    pass


def test_dry_run_does_not_move_raw_when_matching_jpg_has_5_stars(
    tmp_path,
    monkeypatch,
):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    jpg_file = jpg_dir / "photo.jpg"

    raw_file.write_text("fake raw content")
    jpg_file.write_text("fake jpg content")

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        lambda file_path: {"Rating": "5"},
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=True,
    )

    assert raw_file.exists()
    assert not (raw_dir / "raws-5-star" / "photo.raf").exists()


def test_moves_raw_when_matching_jpg_has_5_stars(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    jpg_file = jpg_dir / "photo.jpg"

    raw_file.write_text("fake raw content")
    jpg_file.write_text("fake jpg content")

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        lambda file_path: {"Rating": "5"},
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    moved_file = raw_dir / "raws-5-star" / "photo.raf"

    assert not raw_file.exists()
    assert moved_file.exists()


def test_keeps_raw_when_matching_jpg_does_not_have_5_stars(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    jpg_file = jpg_dir / "photo.jpg"

    raw_file.write_text("fake raw content")
    jpg_file.write_text("fake jpg content")

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        lambda file_path: {"Rating": "4"},
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    assert raw_file.exists()
    assert jpg_file.exists()
    assert not (raw_dir / "raws-5-star" / "photo.raf").exists()


def test_keeps_raw_when_no_matching_jpg_exists(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    other_jpg = jpg_dir / "other.jpg"

    raw_file.write_text("fake raw content")
    other_jpg.write_text("fake jpg content")

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        lambda file_path: {"Rating": "5"},
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    assert raw_file.exists()
    assert not (raw_dir / "raws-5-star" / "photo.raf").exists()


def test_moves_raw_when_matching_jpg_starts_with_same_stem_and_has_5_stars(
    tmp_path,
    monkeypatch,
):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    jpg_file = jpg_dir / "photo_edit.jpg"

    raw_file.write_text("fake raw content")
    jpg_file.write_text("fake jpg content")

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        lambda file_path: {"Rating": "5"},
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    assert not raw_file.exists()
    assert (raw_dir / "raws-5-star" / "photo.raf").exists()


def test_moves_only_raw_files_with_matching_5_star_jpgs(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    starred_raw = raw_dir / "starred.raf"
    unstarred_raw = raw_dir / "unstarred.raf"

    starred_jpg = jpg_dir / "starred.jpg"
    unstarred_jpg = jpg_dir / "unstarred.jpg"

    starred_raw.write_text("starred raw")
    unstarred_raw.write_text("unstarred raw")
    starred_jpg.write_text("starred jpg")
    unstarred_jpg.write_text("unstarred jpg")

    def fake_get_exif_metadata(file_path):
        if file_path.name == "starred.jpg":
            return {"Rating": "5"}
        return {"Rating": "3"}

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        fake_get_exif_metadata,
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    assert not starred_raw.exists()
    assert (raw_dir / "raws-5-star" / "starred.raf").exists()

    assert unstarred_raw.exists()
    assert not (raw_dir / "raws-5-star" / "unstarred.raf").exists()


def test_ignores_non_raw_files_in_raw_directory(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    jpg_file = raw_dir / "photo.jpg"
    txt_file = raw_dir / "notes.txt"
    rated_jpg = jpg_dir / "photo.jpg"

    jpg_file.write_text("fake jpg content")
    txt_file.write_text("notes")
    rated_jpg.write_text("rated jpg")

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        lambda file_path: {"Rating": "5"},
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    assert jpg_file.exists()
    assert txt_file.exists()
    assert not (raw_dir / "raws-5-star" / "photo.jpg").exists()
    assert not (raw_dir / "raws-5-star" / "notes.txt").exists()


def test_skips_file_when_destination_already_exists(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"
    keep_dir = raw_dir / "raws-5-star"

    raw_dir.mkdir()
    jpg_dir.mkdir()
    keep_dir.mkdir()

    source_file = raw_dir / "photo.raf"
    existing_file = keep_dir / "photo.raf"
    jpg_file = jpg_dir / "photo.jpg"

    source_file.write_text("new raw")
    existing_file.write_text("existing raw")
    jpg_file.write_text("fake jpg")

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        lambda file_path: {"Rating": "5"},
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    assert source_file.exists()
    assert existing_file.exists()
    assert existing_file.read_text() == "existing raw"


def test_handles_empty_directories(tmp_path):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

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

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    assert nested_raw.exists()
    assert not (raw_dir / "raws-5-star" / "photo.raf").exists()


def test_keeps_raw_when_rating_cannot_be_read(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raws"
    jpg_dir = tmp_path / "jpgs"

    raw_dir.mkdir()
    jpg_dir.mkdir()

    raw_file = raw_dir / "photo.raf"
    jpg_file = jpg_dir / "photo.jpg"

    raw_file.write_text("fake raw content")
    jpg_file.write_text("fake jpg content")

    def fake_get_exif_metadata(file_path):
        raise ValueError("bad metadata")

    monkeypatch.setattr(
        keep_starred_module,
        "get_exif_metadata",
        fake_get_exif_metadata,
    )

    keep_five_star_raws(
        str(raw_dir),
        str(jpg_dir),
        report=noop_report,
        dry_run=False,
    )

    assert raw_file.exists()
    assert not (raw_dir / "raws-5-star" / "photo.raf").exists()
