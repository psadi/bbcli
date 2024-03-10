# -*- coding: utf-8 -*-

from bb.utils.constants import CommonVars


def test_common_vars():
    common_vars = CommonVars()

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
