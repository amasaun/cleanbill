import click
import simplejson as json
from boto3 import Session
from rich.console import Console

from src.repositories.idp_repository import IDPRepository
from src.services.idp_service import IDPService

console = Console()


@click.command()
@click.option(
    "-p",
    "--profile",
    default="eph-dev",
    help="""
    AWS Profile to connect with
    """,
)
@click.option(
    "-t",
    "--table",
    required=True,
    help="""
    Table to retrieve items from
    """,
)
@click.option(
    "-u",
    "--url",
    required=True,
    help="""
    URL for an IDP.
    """,
)
def look_up_idp(
    profile: str,
    table: str,
    url: str,
) -> None:
    """
    Example script that scans add table

    Example Usage:
        lookup-idp -p eph-dev -t table_name -u http://idp
    """
    console.print(f"[blue]Using Profile:[/blue] [red]{profile}[/red]")
    session = Session(profile_name=profile)
    ddb_table = session.resource("dynamodb").Table(table)
    service = IDPService(repository=IDPRepository(table=ddb_table))

    idp_item = service.get_idp_by_url(url)

    console.print(f"[blue]Scanning data on:[/blue] [red]{table}[/red]")

    console.print_json(idp_item.json())
