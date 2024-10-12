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

from typing import Dict


class CommonVars:
    """Common variables used throughout the application"""

    bold_red: str = "bold red"
    bold_white: str = "bold white"
    id_cannot_be_none: str = "id cannot be none"
    not_a_git_repo: str = "Not a git repository"
    skip_prompt: str = "skip confirmation prompt"
    content_type: str = "application/json;charset=UTF-8"
    dim_white: str = "dim white"
    state: Dict[str, bool] = {"verbose": False}
    repo_cant_be_none: str = "repository can't be none"
    project_name_of_repo: str = "project name of the repository"
    project_name: str = "Project name"
    repository_name: str = "Repository Name"
    project_cant_be_none: str = "project can't be none"
    timeout: float = 10.0


common_vars: CommonVars = CommonVars()
