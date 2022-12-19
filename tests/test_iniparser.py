# -*- coding: utf-8 -*-

from bb.utils.ini import parse
from props import Ini

property = Ini()


def test_parse():
    if property.BB_CONFIG_FILE:
        _parse = parse()
        assert type(_parse) == list
        assert len(_parse) == 3
        for i in _parse:
            assert type(i) == str
