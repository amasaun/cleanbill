import os
import sys

import click
from rich.console import Console

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__),
        ),
    ),
)

from scripts.commands.lookup_idp import look_up_idp
from scripts.commands.warmup_authorizer import warmup_authorizer

console = Console()


@click.group()
def cli() -> None:
    pass


cli.add_command(look_up_idp)
cli.add_command(warmup_authorizer)

if __name__ == "__main__":
    console.print("[magenta]Service CLI")
    cli()
