# -*- coding: utf-8 -*-

"""
    bb.utils.ini - parses .alt ini file
    prompts for setup if not present
"""

import os
import configparser
from pathlib import Path
from xdg import xdg_config_home
from typer import echo, Exit

_XDG_CONFIG_HOME: str = f"{xdg_config_home()}/bb"
BB_CONFIG_FILE: str = f"{_XDG_CONFIG_HOME}/config.ini"


def is_config_present() -> bool:
    """checks if config.ini file is present"""
    return os.path.isfile(BB_CONFIG_FILE)


def _setup(bitbucket_host: str, username: str, token: str) -> None:
    """
    It creates a config file with the given parameters.
    """

    Path(_XDG_CONFIG_HOME).mkdir(parents=True, exist_ok=True)
    Path(BB_CONFIG_FILE).touch(exist_ok=True)

    defaut_config = """[auth]
bitbucket_host=https://bitbucket.<company>.com
username=name
token=xxxxxxxxxxx"""

    with open(BB_CONFIG_FILE, "w", encoding="utf-8") as alt:
        alt.write(defaut_config)

    w_alt = Path(BB_CONFIG_FILE)
    ini = configparser.ConfigParser()
    ini.read(BB_CONFIG_FILE)
    ini.set("auth", "bitbucket_host", bitbucket_host)
    ini.set("auth", "username", username)
    ini.set("auth", "token", token)
    ini.write(w_alt.open("w", encoding="utf-8"))


def parse() -> list:
    """
    It returns the configuration present in .alt file in home directory
    """
    if not os.path.isfile(BB_CONFIG_FILE):
        echo("Configuration required, Try running 'bb auth setup'")
        raise Exit(code=1)

    ini = configparser.ConfigParser()
    ini.read(BB_CONFIG_FILE)
    token = ini.get("auth", "token")
    username = ini.get("auth", "username")
    bitbucket_host = ini.get("auth", "bitbucket_host")
    return [username, token, bitbucket_host]
