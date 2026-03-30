import typer
from dotenv import load_dotenv

from photo_tools.cli_support.cli_errors import handle_cli_errors
from photo_tools.cli_support.cli_reporter import make_reporter
from photo_tools.commands.clean_unpaired_raws import clean_unpaired_raws
from photo_tools.commands.optimise import optimise
from photo_tools.commands.organise_by_date import organise_by_date
from photo_tools.commands.separate_raws import separate_raws
from photo_tools.core.dependencies import validate_feature
from photo_tools.exceptions import MissingDependencyError
from photo_tools.logging_config import setup_logging

app = typer.Typer(help="CLI tools for organising and optimising photography workflows.")


load_dotenv()
setup_logging()


@app.callback()
def main() -> None:
    try:
        # validate dependencies needed globally (if any)
        validate_feature("exif")
    except MissingDependencyError as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@app.command("by-date")
@handle_cli_errors
def organise_by_date_cmd(
    input_dir: str = typer.Argument(
        ...,
        help="Directory containing input images.",
    ),
    output_dir: str = typer.Argument(
        ...,
        help="Directory where organised images will be saved.",
    ),
    suffix: str | None = typer.Option(
        None,
        "--suffix",
        help="Optional suffix appended to folder names (e.g. location).",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without moving files.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show per-file output.",
    ),
) -> None:
    """Organise images into folders based on capture date."""
    organise_by_date(
        input_dir=input_dir,
        output_dir=output_dir,
        report=make_reporter(verbose),
        suffix=suffix,
        dry_run=dry_run,
    )


@app.command(
    "raws",
    help="Move RAW images into a 'raws' folder",
)
@handle_cli_errors
def separate_raws_cmd(
    input_dir: str = typer.Argument(
        ...,
        help="Directory containing images from which RAW files should be separated.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without moving files.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show per-file output.",
    ),
) -> None:
    """Move RAW images into a 'raws' folder."""
    separate_raws(
        input_dir=input_dir,
        report=make_reporter(verbose),
        dry_run=dry_run,
    )


@app.command(
    "clean-raws",
    help="Move RAW files without matching JPGs to 'raws-to-delete'.",
)
@handle_cli_errors
def clean_unpaired_raws_cmd(
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
        help="Preview changes without moving files.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show per-file output.",
    ),
) -> None:
    clean_unpaired_raws(
        raw_dir=raw_dir,
        jpg_dir=jpg_dir,
        report=make_reporter(verbose),
        dry_run=dry_run,
    )


@app.command(
    "optimise",
    help="Resize JPG images to max 2500px width and compress to ≤500KB using quality "
    "70-100, saving as prefixed copies.",
)
@handle_cli_errors
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
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show per-file output.",
    ),
) -> None:
    optimise(
        input_dir=input_dir,
        report=make_reporter(verbose),
        dry_run=dry_run,
    )


if __name__ == "__main__":
    app()
