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

from bb.utils import richprint


def test_str_print():
    richprint.str_print("Hello, world!", "bold white")
    # The output should be "Hello, world!" in bold white style.


def test_table():
    header_args = {"name": "Name", "age": "Age", "gender": "Gender"}
    value_args = [
        {"name": "Alice", "age": 25, "gender": "Female"},
        {"name": "Bob", "age": 30, "gender": "Male"},
        {"name": "Charlie", "age": 35, "gender": "Male"},
    ]
    richprint.table(header_args, value_args, True)
    # The output should be a table with the given header and values.
