from collections.abc import Callable

import typer

Reporter = Callable[[str, str], None]


def make_reporter(verbose: bool) -> Reporter:
    def report(level: str, message: str) -> None:
        if level == "warning":
            typer.secho(message, fg=typer.colors.YELLOW, err=True)
        elif level == "summary":
            typer.echo(message)
        elif level == "info" and verbose:
            typer.echo(message)

    return report
