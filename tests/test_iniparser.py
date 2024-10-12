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
from pathlib import Path

from props import Ini

from bb.utils.ini import config_path, parse

property = Ini()


def test_parse():
    if property.BB_CONFIG_FILE:
        _parse = parse()
        assert isinstance(_parse, list)
        assert len(_parse) == 3
        for i in _parse:
            assert isinstance(i, str)


def test_config_path():
    # with pytest.raises(AssertionError):
    config_dir, config_file = config_path()
    assert config_dir == os.path.join(str(Path.home()), ".config", "bb")
    assert config_file == os.path.join(config_dir, "config.ini")
