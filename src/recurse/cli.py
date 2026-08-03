import logging
from typing import Annotated

from typer import Option, Typer

main = Typer(help="Main CLI entrypoint.", pretty_exceptions_enable=False, no_args_is_help=True)


@main.callback()
def main_callback() -> None:
    """Keep subcommands addressable by name, even while there is only one of them."""


@main.command(name="hello")
def hello_command(
    name: Annotated[str, Option(help="Name to greet")] = "world",
    debug: Annotated[bool, Option("--debug", help="Enable debug logging")] = False,
) -> None:
    """Print a hello message."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    print(f"Hello, {name}!")


if __name__ == "__main__":
    main()
