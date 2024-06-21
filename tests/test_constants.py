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

from bb.utils.constants import CommonVars


def test_common_vars():
    common_vars: CommonVars = CommonVars()

    # Test attribute values
    assert common_vars.bold_red == "bold red"
    assert common_vars.bold_white == "bold white"
    assert common_vars.id_cannot_be_none == "id cannot be none"
    assert common_vars.not_a_git_repo == "Not a git repository"
    assert common_vars.skip_prompt == "skip confirmation prompt"
    assert common_vars.content_type == "application/json;charset=UTF-8"
    assert common_vars.dim_white == "dim white"
    assert common_vars.state == {"verbose": False}

    # Test attribute types
    assert isinstance(common_vars.bold_red, str)
    assert isinstance(common_vars.bold_white, str)
    assert isinstance(common_vars.id_cannot_be_none, str)
    assert isinstance(common_vars.not_a_git_repo, str)
    assert isinstance(common_vars.skip_prompt, str)
    assert isinstance(common_vars.content_type, str)
    assert isinstance(common_vars.dim_white, str)
    assert isinstance(common_vars.state, dict)
