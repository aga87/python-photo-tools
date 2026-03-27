import functools
from typing import Callable, ParamSpec, TypeVar

import typer

P = ParamSpec("P")
R = TypeVar("R")


# Decorator to handle common CLI errors and present clean messages to the user.
# Keeps core logic free of CLI concerns
def handle_cli_errors(func: Callable[P, R]) -> Callable[P, R]:
    # Preserve original function metadata so Typer can correctly parse arguments
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except (FileNotFoundError, NotADirectoryError) as e:
            typer.echo(f"Error: {e}")
            raise typer.Exit(code=1)

    return wrapper
