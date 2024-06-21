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

from typer.testing import CliRunner

from bb.pr import _pr

runner = CliRunner()


def test_create():
    result = runner.invoke(_pr, ["create", "--target", "main", "--yes"])
    assert result.exit_code == 0
    result = runner.invoke(
        _pr, ["create", "--target", "main", "--yes", "--diff", "--rebase"]
    )
    assert result.exit_code == 0


def test_delete():
    result = runner.invoke(_pr, ["delete", "--id", "0", "--yes"])
    assert result.exit_code == 0


def test_copy():
    result = runner.invoke(_pr, ["copy", "--id", "0"])
    assert result.exit_code == 0


def test_diff():
    result = runner.invoke(_pr, ["diff", "--id", "0"])
    assert result.exit_code == 0


def test_list():
    result = runner.invoke(_pr, ["list"])
    assert result.exit_code == 0


def test_merge():
    result = runner.invoke(_pr, ["merge", "--id", "0", "--yes"])
    assert result.exit_code == 0


def test_review():
    result = runner.invoke(_pr, ["review", "--id", "0"])
    assert result.exit_code == 0


def test_view():
    result = runner.invoke(_pr, ["view", "--id", "0"])
    assert result.exit_code == 0
