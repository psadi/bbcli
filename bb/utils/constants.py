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


vars = CommonVars()
