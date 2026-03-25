from datetime import datetime

from typer.testing import CliRunner

from photo_tools.cli import app

runner = CliRunner()


def test_missing_dependency(monkeypatch):
    def fake_which(_):
        return None

    monkeypatch.setattr("shutil.which", fake_which)

    result = runner.invoke(app, ["organise-by-date", "in", "out"])

    assert result.exit_code == 1
    assert "Error:" in result.output
    assert "required but not installed" in result.output

def test_dependency_check_passes(monkeypatch):
    def fake_which(_):
        return "/usr/bin/fake-exiftool"

    monkeypatch.setattr("shutil.which", fake_which)

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_organise_by_date_command_moves_file(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    image_file = input_dir / "photo.jpg"
    image_file.write_text("fake image content")

    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/fake-exiftool")
    monkeypatch.setattr(
        "photo_tools.organise_by_date.get_image_date",
        lambda _: datetime(2024, 5, 17),
    )

    result = runner.invoke(
        app,
        ["organise-by-date", str(input_dir), str(output_dir)],
    )

    assert result.exit_code == 0
    assert not image_file.exists()
    assert (output_dir / "2024-05-17" / "photo.jpg").exists()



def test_organise_by_date_command_dry_run_does_not_move_file(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    image_file = input_dir / "photo.jpg"
    image_file.write_text("fake image content")

    monkeypatch.setattr("shutil.which", lambda _: "/usr/bin/fake-exiftool")
    monkeypatch.setattr(
        "photo_tools.organise_by_date.get_image_date",
        lambda _: datetime(2024, 5, 17),
    )

    result = runner.invoke(
        app,
        ["organise-by-date", str(input_dir), str(output_dir), "--dry-run"],
    )

    assert result.exit_code == 0
    assert image_file.exists()
    assert not (output_dir / "2024-05-17" / "photo.jpg").exists()