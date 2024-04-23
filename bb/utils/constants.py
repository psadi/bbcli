# -*- coding: utf-8 -*-

from typing import Dict


class CommonVars:
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


common_vars: CommonVars = CommonVars()
