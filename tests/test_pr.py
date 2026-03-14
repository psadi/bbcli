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

from unittest.mock import patch

from typer.testing import CliRunner

from bb.pr import _pr

runner = CliRunner()


@patch(
    "bb.utils.helper.prompt",
    side_effect=lambda text, default="", show_default=True: default,
)
@patch("bb.pr.create_pull_request")
@patch("bb.pr.is_git_repo", return_value=True)
@patch("bb.utils.cmnd.title_and_description", return_value=["Test Title", "Test Desc"])
def test_create(mock_title_desc, mock_is_git, mock_create_pr, mock_prompt):
    result = runner.invoke(_pr, ["create", "--target", "main", "--yes"])
    assert result.exit_code == 0
    mock_create_pr.assert_called_once()

    result = runner.invoke(
        _pr, ["create", "--target", "main", "--yes", "--diff", "--rebase"]
    )
    assert result.exit_code == 0
    assert mock_create_pr.call_count == 2


@patch("bb.utils.helper.prompt", return_value="1")
@patch("bb.pr.delete_pull_request")
@patch("bb.utils.cmnd.is_git_repo", return_value=True)
def test_delete(mock_is_git, mock_delete_pr, mock_prompt):
    result = runner.invoke(_pr, ["delete", "--id", "1", "--yes"])
    assert result.exit_code == 0
    mock_delete_pr.assert_called_once_with(["1"], True, False)


@patch("bb.utils.helper.prompt", return_value="1")
@patch("bb.pr.copy_pull_request")
@patch("bb.utils.cmnd.is_git_repo", return_value=True)
def test_copy(mock_is_git, mock_copy_pr, mock_prompt):
    result = runner.invoke(_pr, ["copy", "--id", "1"])
    assert result.exit_code == 0
    mock_copy_pr.assert_called_once_with("1")


@patch("bb.utils.helper.prompt", return_value="1")
@patch("bb.pr.show_diff")
@patch("bb.utils.cmnd.is_git_repo", return_value=True)
def test_diff(mock_is_git, mock_show_diff, mock_prompt):
    result = runner.invoke(_pr, ["diff", "--id", "1"])
    assert result.exit_code == 0
    mock_show_diff.assert_called_once_with("1")


@patch("bb.pr.list_pull_request")
@patch("bb.utils.cmnd.is_git_repo", return_value=True)
def test_list(mock_is_git, mock_list_pr):
    result = runner.invoke(_pr, ["list"])
    assert result.exit_code == 0
    mock_list_pr.assert_called_once_with("current", False)


@patch("bb.utils.helper.prompt", return_value="1")
@patch("bb.pr.merge_pull_request")
@patch("bb.utils.cmnd.is_git_repo", return_value=True)
def test_merge(mock_is_git, mock_merge_pr, mock_prompt):
    result = runner.invoke(_pr, ["merge", "--id", "1", "--yes"])
    assert result.exit_code == 0
    mock_merge_pr.assert_called_once_with("1", False, False, True)


@patch("bb.utils.helper.prompt", side_effect=["1", "approve"])
@patch("bb.pr.review_pull_request")
@patch("bb.utils.cmnd.is_git_repo", return_value=True)
def test_review(mock_is_git, mock_review_pr, mock_prompt):
    result = runner.invoke(_pr, ["review", "--id", "1", "--action", "approve"])
    assert result.exit_code == 0
    mock_review_pr.assert_called_once_with("1", "approve")


@patch("bb.utils.helper.prompt", return_value="1")
@patch("bb.pr.view_pull_request")
@patch("bb.utils.cmnd.is_git_repo", return_value=True)
def test_view(mock_is_git, mock_view_pr, mock_prompt):
    result = runner.invoke(_pr, ["view", "--id", "1"])
    assert result.exit_code == 0
    mock_view_pr.assert_called_once_with("1", False)
