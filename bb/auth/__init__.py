# -*- coding: utf-8 -*-

############################################################################
# Bitbucket CLI (bb): Work seamlessly with Bitbucket from the command line
#
# Copyright (C) 2022  P S, Adithya (psadi) (ps.adithya@icloud.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
############################################################################

"""
bb: auth - validates and configures the auth details

Defines commands to configure, test, and view the authentication status for
a Bitbucket CLI tool.
"""

import typer

from bb.utils.helper import error_handler, validate_config
from bb.utils.ini import (
    BB_CONFIG_FILE,
    XDG_CONFIG_HOME,
    auth_setup,
    is_config_present,
    parse,
)
from bb.utils.richprint import console

_auth: typer.Typer = typer.Typer(add_completion=False, no_args_is_help=True)


@_auth.command(help="Configure bbcli to work with Bitbucket")
def setup() -> None:
    """
    The `setup` function checks for a configuration file and sets up authentication if not found.

    Args:
    -   :param: The `setup` function does not take any parameters
    Raises:
    -   :raises: This function does not raise any exceptions
    Returns:
    -   :rtype: None
    """

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
            console.print(
                f"\nConfiguration written at [yellow]'{BB_CONFIG_FILE}'[/yellow]\nPlease re-run [yellow]`bb auth test`[/yellow] to validate\n"
            )

    _setup()


@_auth.command(help="Test configuration & connection")
def test() -> None:
    """
    The function `test` contains an inner function `_test` that checks for the presence of configuration
    and validates it.

    Args:
    -   :param: The `test` function does not take any parameters
    Raises:
    -   :raises: This function does not raise any exceptions
    Returns:
    -   :rtype: None
    """

    @error_handler
    def _test() -> None:
        if not is_config_present():
            raise ValueError("Configuration missing, run 'bb auth setup'")
        validate_config()

    _test()


@_auth.command(help="View authentication config status")
def status(token: bool = typer.Option(False, help="Display auth token")) -> None:
    """
    Displays the status of the authentication token and related configuration
    information for a Bitbucket connection.

    Args:
    -   :param token: The `token` parameter in the `status` function is a boolean type with a default value
        of `False`. It is used to determine whether the authentication token should be displayed or masked
        when the function is called
    -   :type token: bool
    Raises:
    -   :raises: This function does not raise any exceptions
    Returns:
    -   :rtype: None
    """

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


@_auth.command(help="Reset authentication configuration")
def reset() -> None:
    """
    The function `reset` contains an inner function `_reset` that resets the configuration file.

    Args:
    -   :param: The `reset` function does not take any parameters
    Raises:
    -   :raises: This function does not raise any exceptions
    Returns:
    -   :rtype: None
    """

    @error_handler
    def _reset() -> None:
        console.print(
            f"\nThis will delete,\n\n- File: [yellow]{BB_CONFIG_FILE}[/yellow]\n- Directory: [yellow]{XDG_CONFIG_HOME}[/yellow]\n"
        )
        if (
            typer.prompt(
                "Are you sure you want to reset the configuration? (y/n)", default="n"
            )
            == "y"
        ):
            import os

            if os.path.exists(BB_CONFIG_FILE):
                os.remove(BB_CONFIG_FILE)

            if os.path.exists(XDG_CONFIG_HOME):
                os.rmdir(XDG_CONFIG_HOME)

            console.print(
                "\nConfiguration reset successfully, please run [yellow]`bb auth setup`[/yellow] to configure again\n"
            )

    _reset()
