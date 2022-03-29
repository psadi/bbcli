# -*- coding: utf-8 -*-
""""
    app.scripts.view
"""

from typer import echo
from app.utils import iniparser
from app.utils import api
from app.utils import request


def validate():
    username, token, bitbucket_host = iniparser.parse()
    echo(f"\u1405 Validating connection with '{bitbucket_host}'...")
    reponse = request.get_response(api.test(bitbucket_host), username, token)
    if reponse[0] == 200:
        echo('\u2705 OK')
