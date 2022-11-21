# -*- coding: utf-8 -*-

"""
    bb.utils.iniparser - parses .alt ini file
    prompts for setup if not present
"""

import os
import configparser
from pathlib import Path
from typer import prompt, echo, Exit

# Creating a file called .alt in the home directory.
altfile = os.path.expanduser("~") + "/.alt"


def setup(bitbucket_host: str, username: str, token: str) -> None:
    """
    It creates a config file with the given parameters.
    """
    defaut_config = """[default]
bitbucket_host=https://bitbucket.<company>.com
username=name
token=xxxxxxxxxxx"""

    with open(altfile, "w", encoding="utf-8") as alt:
        alt.write(defaut_config)

    w_alt = Path(altfile)
    ini = configparser.ConfigParser()
    ini.read(altfile)
    ini.set("default", "bitbucket_host", bitbucket_host)
    ini.set("default", "username", username)
    ini.set("default", "token", token)
    ini.write(w_alt.open("w", encoding="utf-8"))


def parse() -> list:
    """
    It returns the configuration present in .alt file in home directory
    """
    if not os.path.isfile(altfile):
        if (
            prompt(
                f"* No '.alt' found at '{altfile}'\n* Do you wish to setup one ?"
            ).lower()
            == "y"
        ):
            echo("")
            setup(prompt("> bitbucket_host"), prompt("> username"), prompt("> token"))
            echo("")
            echo(
                f"'.alt' file written @ '{altfile}', Please re-run 'bb test' to validate"
            )
            Exit(code=0)
        else:
            echo("'.alt' configuration is required")
            raise Exit(code=1)

    ini = configparser.ConfigParser()
    ini.read(altfile)
    token = ini.get("default", "token")
    username = ini.get("default", "username")
    bitbucket_host = ini.get("default", "bitbucket_host")
    return [username, token, bitbucket_host]
