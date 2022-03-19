#-*- coding: utf-8 -*-
""""
    app.utils.iniparser
"""

import os
import configparser
from pathlib import Path

from typer import Exit, prompt
from typer import echo

altfile = os.path.expanduser('~') + '/.alt'

def setup(bitbucket_host: str, username: str, token: str) -> None:
    defaut_config = """[default]
bitbucket_host=https://bitbucket.<company>.com
username=name
token=xxxxxxxxxxx"""

    with open(altfile, 'w') as alt:
        alt.write(defaut_config)

    w_alt = Path(altfile)
    ini = configparser.ConfigParser()
    ini.read(altfile)
    ini.set('default','bitbucket_host',bitbucket_host)
    ini.set('default','username',username)
    ini.set('default','token',token)
    ini.write(w_alt.open('w'))

def parse() -> list:
    """Returns the configuration present in .alt file in home directory"""
    if os.path.isfile(altfile):
        ini = configparser.ConfigParser()
        ini.read(altfile)
        token = ini.get('default', 'token')
        username = ini.get('default', 'username')
        bitbucket_host = ini.get('default', 'bitbucket_host')
        return [username, token, bitbucket_host]
    elif prompt(f"\u274C No .alt found at '{altfile}'\n\U0001F4A1 Do you want to setup").lower() == 'y':
        echo('')
        setup(prompt("\u1405 bitbucket_host"), prompt("\u1405 username"), prompt("\u1405 token"))
        echo('')
        echo(f"\u2705 .alt file written @ '{altfile}', Please run 'bb test' to validate")
        raise Exit(code=0)
    else:
        echo("\u274C .alt configuration is required")
        echo("\U0001F4A1 Please run 'bb docs --option setup' for more help")
        raise Exit(code=1)
