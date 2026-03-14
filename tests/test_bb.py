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

from bb import _bb

runner = CliRunner()


def test_version():
    result = runner.invoke(_bb, ["--version"])
    assert result.exit_code == 0
    assert "bb version:" in result.stdout


def test_verbose():
    from bb.utils.constants import common_vars

    result = runner.invoke(_bb, ["--verbose", "pr", "--help"])
    assert result.exit_code == 0
    assert common_vars.state["verbose"] is True
