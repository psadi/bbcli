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

from dataclasses import dataclass, field


@dataclass(frozen=True, order=True)
class Api:
    bitbucket_host: str = "http://picolo.box:7990"
    project: str = "test-project"
    repository: str = "test-repo"
    repo_id: str = "1234"
    from_branch: str = "feature/test_branch"
    target: str = "master"
    title_and_description: list[str, str] = field(
        default_factory=lambda: [
            "pull request title",
            "pull request description",
        ]
    )
    reviewers: list[str] = field(default_factory=lambda: ["test"])
    pr_no: int = 1
    role: str = "author"
    user: str = "test"
    delete_source_branch: list[bool, bool] = field(
        default_factory=lambda: [True, False]
    )
    version: int = 0


@dataclass(frozen=True, order=True)
class Cmnd:
    is_git_repo: str = "git rev-parse --is-inside-work-tree"
    remote_info: str = "git remote -v"
    commit_message: str = "git log --format=%B -n 1"
    from_branch: str = "git rev-parse --abbrev-ref HEAD"


@dataclass(frozen=True, order=True)
class Cp:
    url: str = "https://test-url.com"


class Ini:
    import os
    from platform import system
    from typing import Dict

    _XDG_CONFIG_HOME: str = os.path.expanduser("~")

    platform_config: Dict[str, dict] = {
        "Windows": f"{_XDG_CONFIG_HOME}\\.config\\bb\\config.ini",
        "Linux": f"{_XDG_CONFIG_HOME}/.config/bb/config.ini",
        "Darwin": f"{_XDG_CONFIG_HOME}/.config/bb/config.ini",
    }

    BB_CONFIG_FILE: str = platform_config.get(system(), "n/a")
