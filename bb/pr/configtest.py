# -*- coding: utf-8 -*-

# Importing the `echo` and `Exit` functions from the `typer` module, and the `iniparser`,
# `api`, `request`, and `richprint` modules from the `bb.utils` package.
from bb.utils import iniparser, api, request, richprint


def validate():
    """
    calls the `api.test` function, If the response code is not 200,
    prints exception and return non-zero exit code
    """
    try:
        username, token, bitbucket_host = iniparser.parse()
        message = f"Validating connection with '{bitbucket_host}'... "
        with richprint.live_progress(message) as live:
            response = request.get(api.test(bitbucket_host), username, token)
            if response[0] == 200:
                live.update(richprint.console.print("OK", style="bold green"))
    except Exception as err:
        richprint.console.print("ERROR", style="bold red")
        raise err
