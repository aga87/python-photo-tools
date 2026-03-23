import typer
from photo_tools.organise_by_date import organise_by_date

app = typer.Typer()


@app.command("organise-by-date")
def organise_by_date_cmd(input: str, output: str) -> None:
    organise_by_date(input, output)


if __name__ == "__main__":
    app()