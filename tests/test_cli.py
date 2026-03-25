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