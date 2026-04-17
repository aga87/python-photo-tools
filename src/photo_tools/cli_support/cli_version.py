from importlib.metadata import PackageNotFoundError, version

import typer


def get_version() -> str:
    try:
        return version("photo-tools-cli")
    except PackageNotFoundError:
        return "unknown"


def version_callback(value: bool) -> None:
    if not value:
        return

    typer.echo(get_version())
    raise typer.Exit()
