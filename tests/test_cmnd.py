# -*- coding: utf-8 -*-

from bb.utils import cmnd
from props import Cmnd

property = Cmnd()


def test_is_git_repo():
    is_git_repo = cmnd.is_git_repo()
    cmnd_is_git_repo = cmnd.subprocess_run(property.is_git_repo)

    assert is_git_repo == True
    assert type(is_git_repo)
    assert cmnd_is_git_repo == "true"
    assert type(cmnd_is_git_repo) == str


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
    assert type(remote_info) == list


def test_title_and_description():
    title_and_description = cmnd.title_and_description()
    tmp = cmnd.subprocess_run(property.commit_message).split("\n")
    assert len(title_and_description) == 2
    assert type(title_and_description) == list
    assert type(title_and_description[0]) == str
    assert type(title_and_description[1]) == str
    assert type(tmp) == list
    assert title_and_description == [tmp[0], "\n".join(tmp[2:])]
