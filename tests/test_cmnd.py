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

from props import Cmnd

from bb.utils import cmnd

property = Cmnd()


def test_is_git_repo():
    is_git_repo = cmnd.is_git_repo()
    cmnd_is_git_repo = cmnd.subprocess_run(property.is_git_repo)

    assert is_git_repo is True
    assert isinstance(is_git_repo, bool)
    assert cmnd_is_git_repo == "true"
    assert isinstance(cmnd_is_git_repo, str)


def test_remote_info():
    remote_info = cmnd.base_repo()
    cmnd_remote_info = cmnd.subprocess_run(property.remote_info)
    if cmnd_remote_info is not None:
        fmt = cmnd_remote_info.splitlines()[0].replace("\t", " ").split(" ")[1].strip()
        assert remote_info == [
            fmt.split("/")[-2],
            fmt.split("/")[-1].split(".")[0],
        ]
    assert len(remote_info) == 2
    assert isinstance(remote_info, list)


def test_title_and_description():
    title_and_description = cmnd.title_and_description()
    tmp = cmnd.subprocess_run(property.commit_message).split("\n")
    assert len(title_and_description) == 2
    assert isinstance(title_and_description, list)
    assert isinstance(title_and_description[0], str)
    assert isinstance(title_and_description[1], str)
    assert isinstance(tmp, list)
    assert title_and_description == [tmp[0], "\n".join(tmp[2:])]
