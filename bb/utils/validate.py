# -*- coding: utf-8 -*-

"""
utils.validate - consists of validation functions
"""

from typer import prompt
from bb.utils import ini, api, request, richprint


state: dict = {"verbose": False}


def validate_config():
    """
    calls the `api.test` function, If the response code is not 200,
    prints exception and return non-zero exit code
    """
    try:
        username, token, bitbucket_host = ini.parse()
        message = f"Validating connection with '{bitbucket_host}'... "
        with richprint.live_progress(message) as live:
            response = request.get(api.test(bitbucket_host), username, token)
            if response[0] == 200:
                live.update(richprint.console.print("OK", style="bold green"))
    except Exception as err:
        richprint.console.print("ERROR", style="bold red")
        raise err


def validate_input(_input: any, expected: str, error: str) -> str:
    """
    validates the input, raise the error if the value is not as expected
    """
    if not _input:
        _input: str = prompt(f"? {expected}")

    if _input is None or _input.lower() == "none":
        raise ValueError(error)

    return _input


def error_tip() -> None:
    """
    reusable error message across mainstream commands
    """
    richprint.console.print(
        "\n💻 Try running 'bb --verbose [OPTIONS] COMMAND [ARGS]' to debug",
        style="dim white",
    )
