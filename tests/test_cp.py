# -*- coding: utf-8 -*-

from bb.utils import cp
from props import Cp

property = Cp()


def test_copy_to_clipboard():
    copy_to_clipboard = cp.copy_to_clipboard(property.url)
    assert copy_to_clipboard == None
