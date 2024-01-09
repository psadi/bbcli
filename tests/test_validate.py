# -*- coding: utf-8 -*-
from bb.utils.validate import validate_input


def test_validate_input():
    # Test case 1: Valid input
    assert validate_input("hello", "Enter a string", "Invalid input") == "hello"
