# -*- coding: utf-8 -*-

"""
utils.validate - consists of validation functions
"""

from typing import Any, Callable

from typer import Exit, prompt

from bb.utils import constants, request, richprint
from bb.utils.api import bitbucket_api


def validate_config() -> None:
    """
    calls the `api.test` function, If the response code is not 200,
    prints exception and return non-zero exit code
    """
    try:
        message = f"Validating connection with '{bitbucket_api.bitbucket_host}' ... "
        with richprint.live_progress(message) as live:
            response = request.get(bitbucket_api.test())
            if response[0] == 200:
                live.update(richprint.console.print("OK", style="bold green"))
    except Exception as err:
        raise ValueError(err) from err


def validate_input(_input: Any, expected: str, error: str) -> str:
    """
    validates the input, raise the error if the value is not as expected
    """

    def checker():
        if not isinstance(_input, (str)):
            raise ValueError(error)

        if _input is None or _input.lower() == "none":
            raise ValueError(error)

    checker()

    if not _input:
        _input: str = prompt(f"? {expected}")
        checker()

    return _input


def error_tip() -> None:
    """
    reusable error message across mainstream commands
    """
    richprint.console.print(
        "\n💻 Try running 'bb --verbose [OPTIONS] COMMAND [ARGS]' to debug",
        style="dim white",
    )


def error_handler(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as err:
            richprint.console.print(f"{err}", style="bold red")
            if constants.vars.state["verbose"]:
                richprint.traceback_to_console()
            else:
                error_tip()
            Exit(code=1)

    return wrapper
