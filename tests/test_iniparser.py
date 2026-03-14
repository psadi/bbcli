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

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from props import Ini

from bb.utils.ini import auth_setup, config_path, parse

property = Ini()


def test_parse():
    if property.BB_CONFIG_FILE:
        _parse = parse()
        assert isinstance(_parse, list)
        assert len(_parse) == 3
        for i in _parse:
            assert isinstance(i, str)


def test_parse_missing_config():
    import bb.utils.ini as ini_module

    original_file = ini_module.BB_CONFIG_FILE
    ini_module.BB_CONFIG_FILE = "/nonexistent/config.ini"
    try:
        with pytest.raises(ValueError, match="Configuration required"):
            parse()
    finally:
        ini_module.BB_CONFIG_FILE = original_file


def test_config_path():
    config_dir, config_file = config_path()
    assert config_dir == os.path.join(str(Path.home()), ".config", "bb")
    assert config_file == os.path.join(config_dir, "config.ini")


@patch.dict(os.environ, {"XDG_CONFIG_HOME": tempfile.gettempdir()})
def test_auth_setup():
    import importlib

    import bb.utils.ini as ini_module

    with tempfile.TemporaryDirectory() as tmpdir:
        test_config_file = os.path.join(tmpdir, "bb", "config.ini")
        old_config = ini_module.BB_CONFIG_FILE
        old_xdg = ini_module.XDG_CONFIG_HOME
        ini_module.BB_CONFIG_FILE = test_config_file
        ini_module.XDG_CONFIG_HOME = os.path.join(tmpdir, "bb")
        try:
            auth_setup("https://bitbucket.example.com", "testuser", "testtoken")
            assert os.path.isfile(test_config_file)
            with open(test_config_file) as f:
                content = f.read()
                assert "testuser" in content
                assert "testtoken" in content
                assert "bitbucket.example.com" in content
        finally:
            ini_module.BB_CONFIG_FILE = old_config
            ini_module.XDG_CONFIG_HOME = old_xdg
            import bb.utils.api as api_module

            importlib.reload(api_module)
