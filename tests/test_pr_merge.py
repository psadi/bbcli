# -*- coding: utf-8 -*-
from unittest.mock import MagicMock, patch

import pytest

from bb.pr.merge import (
    delete_branch,
    merge_pr,
    merge_pull_request,
    pr_source_branch_delete_check,
    rebase_pr,
    show_merge_stats,
    validate_automerge_conditions,
    validate_pr_source_branch_delete_check,
)


@patch("bb.pr.merge.request.get")
def test_pr_source_branch_delete_check(mock_get):
    mock_get.return_value = [200, []]
    pr_source_branch_delete_check("proj", "repo", "1", True)

    mock_get.return_value = [200, [{"error": "exists"}]]
    with pytest.raises(ValueError):
        pr_source_branch_delete_check("proj", "repo", "1", True)


@patch("bb.pr.merge.request.get")
def test_validate_pr_source_branch_delete_check(mock_get):
    mock_get.return_value = [
        200,
        {"canMerge": True, "conflicted": False, "outcome": "CLEAN"},
    ]
    validate_pr_source_branch_delete_check("proj", "repo", "1")

    mock_get.return_value = [
        200,
        {"canMerge": False, "conflicted": True, "outcome": "CONFLICTED"},
    ]
    with pytest.raises(ValueError):
        validate_pr_source_branch_delete_check("proj", "repo", "1")


@patch("bb.pr.merge.request.get")
def test_validate_automerge_conditions(mock_get):
    mock_get.side_effect = [
        [
            200,
            {
                "fromRef": {"displayId": "src"},
                "toRef": {"displayId": "dst"},
                "version": 1,
            },
        ],
        [200, {"status": {"id": "NO_PATH"}}],
    ]

    pr_info, merge_info, src, dst, ver = validate_automerge_conditions(
        "proj", "repo", "1"
    )
    assert src == "src"
    assert dst == "dst"
    assert ver == 1


def test_show_merge_stats():
    show_merge_stats({"status": {"id": "NO_PATH", "available": False}}, "src", "dst")
    show_merge_stats(
        {
            "status": {"id": "PROCEED", "available": True},
            "path": [{"displayId": "dst"}],
        },
        "src",
        "dst",
    )
    with pytest.raises(ValueError):
        show_merge_stats(
            {"status": {"id": "UNKNOWN", "available": False}}, "src", "dst"
        )


@patch("bb.pr.merge.request.post")
def test_rebase_pr(mock_post):
    rebase_pr("proj", "repo", "1", 1)
    mock_post.assert_called_once()


@patch("bb.pr.merge.request.post")
@patch("bb.pr.merge.request.delete")
@patch("bb.pr.merge.cmnd.checkout_and_pull")
@patch("bb.pr.merge.cmnd.delete_local_branch")
def test_delete_branch(mock_del_local, mock_checkout, mock_delete, mock_post):
    delete_branch("proj", "repo", "1", "src", "dst")
    mock_post.assert_called_once()
    mock_delete.assert_called_once()
    mock_checkout.assert_called_once()
    mock_del_local.assert_called_once()


@patch("bb.pr.merge.request.post")
def test_merge_pr(mock_post):
    mock_live = MagicMock()
    mock_post.return_value = [200, {"state": "MERGED"}]
    assert merge_pr(mock_live, "proj", "repo", "1", ("src", "dst", 1)) == 200

    mock_post.return_value = [409, {"errors": [{"message": "fail"}]}]
    assert merge_pr(mock_live, "proj", "repo", "1", ("src", "dst", 1)) == 409


@patch("bb.pr.merge.cmnd.base_repo", return_value=("proj", "repo"))
@patch("bb.pr.merge.pr_source_branch_delete_check")
@patch("bb.pr.merge.validate_pr_source_branch_delete_check")
@patch("bb.pr.merge.validate_automerge_conditions")
@patch("bb.pr.merge.show_merge_stats")
@patch("bb.pr.merge.confirm", return_value=True)
@patch("bb.pr.merge.rebase_pr")
@patch("bb.pr.merge.merge_pr", return_value=200)
@patch("bb.pr.merge.delete_branch")
def test_merge_pull_request(
    mock_delete_branch,
    mock_merge_pr,
    mock_rebase_pr,
    mock_confirm,
    mock_show_merge_stats,
    mock_validate_automerge,
    mock_validate_delete,
    mock_delete_check,
    mock_base_repo,
):
    mock_validate_automerge.return_value = (
        {"links": {"self": [{"href": "url"}]}},
        {},
        "src",
        "dst",
        1,
    )

    merge_pull_request("1", True, True, True)

    mock_rebase_pr.assert_called_once()
    mock_merge_pr.assert_called_once()
    mock_delete_branch.assert_called_once()
