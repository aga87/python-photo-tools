import typer
from photo_tools.organise_by_date import organise_by_date
from photo_tools.organise_by_type import organise_by_type
from photo_tools.logging_config import setup_logging
import shutil

if not shutil.which("exiftool"):
    raise RuntimeError("exiftool is required but not installed")

app = typer.Typer()

setup_logging()

@app.command("organise-by-date")
def organise_by_date_cmd(
    input: str,
    output: str,
    suffix: str | None = typer.Option(None),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without moving files",
    ),
) -> None:
    organise_by_date(input, output, suffix, dry_run)

@app.command("organise-by-type")
def organise_by_type_cmd(
    input: str,
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    organise_by_type(input, dry_run)

if __name__ == "__main__":
    app()