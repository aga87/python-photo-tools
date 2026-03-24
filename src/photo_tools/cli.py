import typer
from photo_tools.organise_by_date import organise_by_date
from photo_tools.organise_by_type import organise_by_type
from photo_tools.soft_delete_unpaired_raws import soft_delete_unpaired_raws
from photo_tools.optimise import optimise
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

@app.command("soft-delete-unpaired-raws")
def soft_delete_unpaired_raws_cmd(
    raw_dir: str,
    jpg_dir: str,
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without moving files",
    ),
) -> None:
    soft_delete_unpaired_raws(raw_dir, jpg_dir, dry_run)

@app.command("optimise")
def optimise_cmd(
    input_dir: str,
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    optimise(input_dir, dry_run)

if __name__ == "__main__":
    app()