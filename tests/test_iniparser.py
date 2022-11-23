# -*- coding: utf-8 -*-

from bb.utils import iniparser
from props import IniParser

property = IniParser()


def test_parse():
    if property.altfile:
        _parse = iniparser.parse()
        assert type(_parse) == list
        assert len(_parse) == 3
        for i in _parse:
            assert type(i) == str
