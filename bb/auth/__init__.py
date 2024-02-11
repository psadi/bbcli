# -*- coding: utf-8 -*-

"""
bb: auth - validates and configures the auth details
"""

import typer

from bb.utils.helper import error_handler, validate_config
from bb.utils.ini import BB_CONFIG_FILE, auth_setup, is_config_present, parse
from bb.utils.richprint import console

_auth: typer.Typer = typer.Typer(add_completion=False, no_args_is_help=True)
bold_red: str = "bold red"


@_auth.command()
def setup() -> None:
    """Configure bbcli to work with bitbucket"""

    @error_handler
    def _setup() -> None:
        if is_config_present():
            console.print(
                "Configuration file found, Run 'bb auth status' for more information"
            )
        else:
            auth_setup(
                typer.prompt(
                    "> bitbucket_host",
                ),
                typer.prompt("> username"),
                typer.prompt("> token", hide_input=True),
            )
            typer.echo(
                f"Configuration written at '{BB_CONFIG_FILE}',"
                + "Please re-run 'bb auth test' to validate"
            )

    _setup()


@_auth.command()
def test() -> None:
    """Test configuration & connection"""

    @error_handler
    def _test() -> None:
        validate_config()

    _test()


@_auth.command()
def status(token: bool = typer.Option(False, help="Display auth token")) -> None:
    """View authentication config status"""

    @error_handler
    def _status(token: bool) -> None:
        if not is_config_present():
            raise ValueError("Configuration missing, run 'bb auth setup'")

        hcm: str = "[bold green]:heavy_check_mark:[/bold green]"
        console.print(
            f"{hcm} Configuration found at [bold cyan]{BB_CONFIG_FILE}[/bold cyan]"
        )
        username, _token, bitbucket_host = parse()
        console.print(
            f"{hcm} Will connect to [bold]{bitbucket_host}[/bold] as [bold]{username}[/bold]"
        )
        console.print(f"{hcm} Token: {_token if token else '*' * len(_token)}")

    _status(token)
