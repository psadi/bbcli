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
utils.validate - consists of validation functions
"""

from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

from typer import Exit, prompt

from bb.utils import constants, request, richprint
from bb.utils.api import bitbucket_api

P = ParamSpec("P")
T = TypeVar("T")


def validate_config() -> None:
    """
    Validates the connection with the Bitbucket API.

    This function sends a test request to the Bitbucket API to check if the connection is valid.
    If the response status code is 200, it prints "OK" in bold green to indicate a successful connection.

    Raises:
        ValueError: If an error occurs during the validation process.

    """
    try:
        message = f"Validating connection with '{bitbucket_api.bitbucket_host}' ... "
        with richprint.live_progress(message) as live:
            response = request.get(bitbucket_api.test())
            if response[0] == 200:
                live.update(richprint.console.print("OK", style="bold green"))
    except Exception as err:
        raise ValueError(err) from err


def validate_input(
    _input: Any, expected: str, error: str, default: str = "", optional: bool = False
) -> str:
    """
    Validates the input value based on the expected type and error message.

    Args:
        _input (Any): The input value to be validated.
        expected (str): The expected type of the input value.
        error (str): The error message to be raised if the input value is invalid.

    Raises:
        ValueError: If the input value is not of the expected type or is None.

    Returns:
        str: The validated input value.
    """

    check = 0

    def checker():
        if not isinstance(_input, (str)):
            raise ValueError(error)

        if (
            _input is None
            or _input.lower() == "none"
            or _input == ""
            and check == 1
            and not optional
        ):
            raise ValueError(error)

    checker()

    if not _input:
        _input: str = prompt(
            f"? {expected}",
            default=default,
            show_default=default != "",
        )

        check += 1

        checker()

    return _input


def error_tip() -> None:
    """
    Prints an error tip message.

    This function prints a message with a suggestion to run a command with verbose mode
    to help with debugging.

    Args:
        None

    Returns:
        None
    """
    richprint.console.print(
        "\n💻 Try running 'bb --verbose [OPTIONS] COMMAND [ARGS]' to debug",
        style="dim white",
    )


def error_handler(func: Callable[P, T]) -> Callable[P, T]:
    """
    Decorator function that handles exceptions raised by the decorated function.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.

    Raises:
        Exit: If an exception is raised by the decorated function.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            richprint.console.print(f"{err}", style="bold red")
            if constants.common_vars.state["verbose"]:
                richprint.traceback_to_console()
            else:
                error_tip()
            Exit(code=1)

    return wrapper
