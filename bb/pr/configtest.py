#-*- coding: utf-8 -*-

# Importing the `echo` and `Exit` functions from the `typer` module, and the `iniparser`,
# `api`, `request`, and `richprint` modules from the `bb.utils` package.
from typer import Exit
from bb.utils import (
    iniparser,
    api,
    request,
    richprint
)

def validate():
    """
    It prints a message, then calls the `api.test` function, which returns a URL. It then calls the
    `request.get_response` function, which returns a tuple of the HTTP response code and the response
    body. If the response code is not 200, it prints an error message and exits with a non-zero exit
    code
    """
    username, token, bitbucket_host = iniparser.parse()
    message = f"Validating connection with '{bitbucket_host}'... "
    with richprint.live_progress((message)) as live:
        reponse = request.get_response(api.test(bitbucket_host), username, token)
        if reponse[0] == 200:
            live.update(richprint.console.print('OK', style='bold green'))
        else:
            live.update(richprint.console.print(f"ERROR", style='bold red'))
            raise Exit(code=1)
