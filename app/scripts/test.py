#-*- coding: utf-8 -*-
""""
    app.scripts.view
"""

from typer import echo
from app.utils import (
    iniparser,
    api,
    request,
    richprint
)

def validate():
    username, token, bitbucket_host = iniparser.parse()
    message = f"Validating connection with '{bitbucket_host}'..."
    with richprint.live_progress((message)):
        reponse = request.get_response(api.test(bitbucket_host), username, token)
    if reponse[0] == 200:
        echo('\u2705 OK')
