# -*- coding: utf-8 -*-

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


@dataclass(frozen=True, order=True)
class Ini:
    import os

    _XDG_CONFIG_HOME: str = os.path.expanduser("~") + "/.config/bb"
    BB_CONFIG_FILE: str = f"{_XDG_CONFIG_HOME}/config.ini"
