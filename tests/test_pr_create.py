# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest

from bb.pr.create import create_pull_request, gather_facts


@patch("bb.pr.create.request.get")
@patch("bb.pr.create.richprint.table")
@patch("bb.pr.create.richprint.console.print")
def test_gather_facts(mock_print, mock_table, mock_get):
    # Mocking requests
    mock_get.side_effect = [
        [200, {"values": [{"name": "repo_name", "id": 123}]}],
        [200, [{"name": "Reviewer 1"}, {"name": "Reviewer 2"}]],
    ]

    reviewers = gather_facts(
        "target_branch",
        "source_branch",
        "project",
        "repo_name",
        "Test Title",
        "Test Description",
    )

    assert len(reviewers) == 2
    assert reviewers[0]["user"]["name"] == "Reviewer 1"
    assert mock_get.call_count == 2
    mock_table.assert_called_once()
    mock_print.assert_called_once()


@patch("bb.pr.create.cmnd.from_branch", return_value="source_branch")
@patch("bb.pr.create.cmnd.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.create.gather_facts", return_value=[{"user": {"name": "Reviewer 1"}}])
@patch("bb.pr.create.confirm", return_value=True)
@patch("bb.pr.create.request.post")
@patch("bb.pr.create.cmnd.cp_to_clipboard")
@patch("bb.pr.create.show_diff")
def test_create_pull_request(
    mock_show_diff,
    mock_cp,
    mock_post,
    mock_confirm,
    mock_gather,
    mock_base_repo,
    mock_from_branch,
):
    mock_post.return_value = [
        201,
        {"links": {"self": [{"href": "http://example.com/pr/1"}]}},
    ]

    create_pull_request("target_branch", True, False, False, "Title", "Desc")

    mock_post.assert_called_once()
    mock_cp.assert_called_once_with("http://example.com/pr/1")


@patch("bb.pr.create.cmnd.from_branch", return_value="source_branch")
@patch("bb.pr.create.cmnd.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.create.gather_facts", return_value=[{"user": {"name": "Reviewer 1"}}])
@patch("bb.pr.create.confirm", return_value=True)
@patch("bb.pr.create.request.post")
@patch("bb.pr.create.cmnd.cp_to_clipboard")
@patch("bb.pr.create.show_diff")
def test_create_pull_request_conflict(
    mock_show_diff,
    mock_cp,
    mock_post,
    mock_confirm,
    mock_gather,
    mock_base_repo,
    mock_from_branch,
):
    mock_post.return_value = [
        409,
        {
            "errors": [
                {
                    "message": "Conflict",
                    "existingPullRequest": {
                        "links": {"self": [{"href": "http://example.com/pr/2"}]}
                    },
                }
            ]
        },
    ]

    create_pull_request("target_branch", True, False, False, "Title", "Desc")

    mock_post.assert_called_once()
    mock_cp.assert_called_once_with("http://example.com/pr/2")


@patch("bb.pr.create.cmnd.from_branch", return_value="source_branch")
@patch("bb.pr.create.cmnd.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.create.gather_facts", return_value=[{"user": {"name": "Reviewer 1"}}])
@patch("bb.pr.create.confirm", return_value=True)
@patch("bb.pr.create.cmnd.git_rebase")
@patch("bb.pr.create.request.post")
@patch("bb.pr.create.cmnd.cp_to_clipboard")
@patch("bb.pr.create.show_diff")
def test_create_pull_request_rebase(
    mock_show_diff,
    mock_cp,
    mock_post,
    mock_rebase,
    mock_confirm,
    mock_gather,
    mock_base_repo,
    mock_from_branch,
):
    mock_post.return_value = [
        201,
        {"links": {"self": [{"href": "http://example.com/pr/1"}]}},
    ]

    create_pull_request("target_branch", True, False, True, "Title", "Desc")
    mock_rebase.assert_called_once_with("target_branch")


@patch("bb.pr.create.cmnd.from_branch", return_value="main")
def test_create_pull_request_same_branch(mock_from_branch):
    with pytest.raises(ValueError, match="Source & target cannot be the same"):
        create_pull_request("main", True, False, False, "Title", "Desc")


@patch("bb.pr.create.request.get")
@patch("bb.pr.create.richprint.table")
@patch("bb.pr.create.richprint.console.print")
def test_gather_facts_no_repo(mock_print, mock_table, mock_get):
    mock_get.side_effect = [
        [200, {"values": []}],
    ]

    reviewers = gather_facts(
        "target_branch",
        "source_branch",
        "project",
        "repo_name",
        "Test Title",
        "Test Description",
    )

    assert reviewers == []
    mock_table.assert_called_once()
