import typer

from photo_tools.core.dependencies import validate_feature
from photo_tools.exceptions import MissingDependencyError
from photo_tools.logging_config import setup_logging
from photo_tools.optimise import optimise
from photo_tools.organise_by_date import organise_by_date
from photo_tools.organise_by_type import organise_by_type
from photo_tools.soft_delete_unpaired_raws import soft_delete_unpaired_raws

app = typer.Typer(help="CLI tools for organising and optimising photography workflows.")


@app.callback()
def main() -> None:
    try:
        # validate dependencies needed globally (if any)
        validate_feature("exif")
    except MissingDependencyError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


setup_logging()


@app.command("organise-by-date")
def organise_by_date_cmd(
    input_dir: str = typer.Argument(
        ...,
        help="Directory containing input images",
    ),
    output_dir: str = typer.Argument(
        ...,
        help="Directory where organised images will be saved",
    ),
    suffix: str | None = typer.Option(
        None,
        "--suffix",
        help="Optional suffix appended to folder names (e.g. location)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without moving files",
    ),
) -> None:
    """Organise images into folders based on capture date."""
    organise_by_date(input_dir, output_dir, suffix, dry_run)


@app.command("organise-by-type")
def organise_by_type_cmd(
    input_dir: str = typer.Argument(
        ...,
        help="Directory containing images to organise by type (JPG and RAF supported)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without moving files",
    ),
) -> None:
    """Organise images into 'jpgs' and 'raws' folders (supports .jpg/.jpeg and .raf)."""
    organise_by_type(input_dir, dry_run)


@app.command(
    "soft-delete-unpaired-raws",
    help="Move RAW files without a matching JPG (by filename) to 'raws-to-delete'.",
)
def soft_delete_unpaired_raws_cmd(
    raw_dir: str = typer.Argument(
        ...,
        help="Directory containing RAW files.",
    ),
    jpg_dir: str = typer.Argument(
        ...,
        help="Directory containing JPG files used for matching.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show which RAW files would be moved without making changes.",
    ),
) -> None:
    soft_delete_unpaired_raws(raw_dir, jpg_dir, dry_run)


@app.command(
    "optimise",
    help="Resize JPG images to max 2500px width and compress to ≤500KB using quality "
    "70-100, saving as prefixed copies.",
)
def optimise_cmd(
    input_dir: str = typer.Argument(
        ...,
        help="Directory containing JPG images to optimise.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show resulting size and quality without writing files.",
    ),
) -> None:
    optimise(input_dir, dry_run)


if __name__ == "__main__":
    app()
