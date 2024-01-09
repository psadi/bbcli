# -*- coding: utf-8 -*-

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
