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

import pytest

from bb.utils.helper import validate_input


def test_validate_input():
    # Test case 1: Valid input
    assert validate_input("hello", "Enter a string", "Invalid input") == "hello"

    # Test case 2: Invalid input
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(123, "Enter a string", "Invalid input")

    # Test case 3: Empty input
    # with pytest.raises(ValueError, match="Invalid input"):
    #     validate_input("", "Enter a string", "Invalid input")

    # Test case 4: None input
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(None, "Enter a string", "Invalid input")

    # Test case 5: Valid input with different prompt and error message
    assert (
        validate_input("test", "Enter another string", "Different error message")
        == "test"
    )

    # Test case 6: Input with leading and trailing spaces
    assert validate_input(" hello ", "Enter a string", "Invalid input") == " hello "

    # Test case 7: Input with special characters
    assert validate_input("@#$$%", "Enter a string", "Invalid input") == "@#$$%"

    # Test case 8: Numeric string input
    assert validate_input("12345", "Enter a string", "Invalid input") == "12345"

    # Test case 9: Input is a boolean
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(True, "Enter a string", "Invalid input")

    # Test case 10: Input is a list
    with pytest.raises(ValueError, match="Invalid input"):
        validate_input(["hello"], "Enter a string", "Invalid input")
