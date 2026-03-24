import typer
from photo_tools.organise_by_date import organise_by_date
from photo_tools.logging_config import setup_logging
import shutil

if not shutil.which("exiftool"):
    raise RuntimeError("exiftool is required but not installed")

app = typer.Typer()

setup_logging()


@app.command("organise-by-date")
def organise_by_date_cmd(input: str, output: str) -> None:
    organise_by_date(input, output)


if __name__ == "__main__":
    app()