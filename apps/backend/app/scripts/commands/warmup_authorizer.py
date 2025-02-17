import click
import simplejson as json
from boto3 import Session
from rich.console import Console

import os

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
    "-f",
    "--function_name",
    required=True,
    help="""
    Authorizer lambda function name to warm up
    """,
)
def warmup_authorizer(
    profile: str,
    function_name: str,
) -> None:
    """
    Example script to warm up an authorizer lambda function

    Example Usage:
        warmup-authorizer -p eph-dev -f lambda-function-name
    """

    session = Session(profile_name=profile)
    client = session.client("lambda")

    try:
        client.get_function(FunctionName=function_name)
    except Exception as e:
        console.print(f"[red]Could not find lambda function:[/red] {function_name}")
        console.print(e)
        return

    console.print(f"[blue]Warming up lambda function:[/blue] {function_name}")

    response = client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps({"warmer": True}),
    )
    console.print(response)
