from PIL import Image

from photo_tools.optimise import MAX_WIDTH, optimise


def noop_report(level: str, message: str) -> None:
    pass


def test_dry_run_does_not_create_output(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    img_path = input_dir / "photo.jpg"
    Image.new("RGB", (1000, 1000)).save(img_path)

    optimise(
        str(input_dir),
        report=noop_report,
        dry_run=True,
    )

    assert img_path.exists()
    assert not (input_dir / "lq_photo.jpg").exists()


def test_creates_optimised_file(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    img_path = input_dir / "photo.jpg"
    Image.new("RGB", (1000, 1000)).save(img_path)

    optimise(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    output = input_dir / "lq_photo.jpg"

    assert img_path.exists()
    assert output.exists()


def test_skips_unsupported_files(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    txt_file = input_dir / "notes.txt"
    txt_file.write_text("hello")

    optimise(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    assert txt_file.exists()
    assert not (input_dir / "lq_notes.txt").exists()


def test_skips_already_optimised_files(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    img_path = input_dir / "lq_photo.jpg"
    Image.new("RGB", (1000, 1000)).save(img_path)

    optimise(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    assert img_path.exists()
    assert not (input_dir / "lq_lq_photo.jpg").exists()


def test_output_image_width_is_capped(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    img_path = input_dir / "photo.jpg"
    Image.new("RGB", (4000, 2000)).save(img_path)

    optimise(
        str(input_dir),
        report=noop_report,
        dry_run=False,
    )

    output = input_dir / "lq_photo.jpg"

    with Image.open(output) as img:
        assert img.width <= MAX_WIDTH
