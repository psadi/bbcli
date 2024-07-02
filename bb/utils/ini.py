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
bb.utils.ini - parses .alt ini file
prompts for setup if not present
"""

import configparser
import os
from pathlib import Path
from typing import List, Tuple


def config_path() -> Tuple[str, str]:
    """
    Returns the path to the configuration directory and the configuration file.

    :return: A tuple containing the path to the configuration directory and the configuration file.
    :rtype: Tuple[str, str]
    """
    home: str = str(Path.home())
    config_dir: str = os.path.join(home, ".config", "bb")
    config_file: str = os.path.join(config_dir, "config.ini")
    return (config_dir, config_file)


XDG_CONFIG_HOME, BB_CONFIG_FILE = config_path()


def is_config_present() -> bool:
    """
    Check if the BB_CONFIG_FILE is present.

    Returns:
        bool: True if the BB_CONFIG_FILE is present, False otherwise.
    """
    return os.path.isfile(BB_CONFIG_FILE)


def auth_setup(bitbucket_host: str, username: str, token: str) -> None:
    """
    Set up authentication for Bitbucket CLI.

    Args:
        bitbucket_host (str): The Bitbucket host URL.
        username (str): The username for authentication.
        token (str): The authentication token.

    Returns:
        None
    """
    Path(XDG_CONFIG_HOME).mkdir(parents=True, exist_ok=True)
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


def parse() -> List[str]:
    """
    Parses the configuration file and retrieves the authentication details.

    Returns:
        A list containing the username, token, and Bitbucket host.

    Raises:
        ValueError: If the configuration file does not exist.
    """

    if not os.path.isfile(BB_CONFIG_FILE):
        raise ValueError("Configuration required, Try running 'bb auth setup'")

    ini = configparser.ConfigParser()
    ini.read(BB_CONFIG_FILE)
    token = ini.get("auth", "token")
    username = ini.get("auth", "username")
    bitbucket_host = ini.get("auth", "bitbucket_host")
    return [username, token, bitbucket_host]
