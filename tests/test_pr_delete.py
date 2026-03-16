# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest

from bb.pr.delete import delete_pull_request


@patch("bb.pr.delete.show_diff")
@patch("bb.pr.delete.cmnd.base_repo", return_value=("project", "repo_name"))
@patch(
    "bb.pr.delete.request.get",
    return_value=[
        200,
        {
            "id": 1,
            "state": "OPEN",
            "title": "Title",
            "fromRef": {"displayId": "src"},
            "toRef": {"displayId": "dst"},
            "version": 1,
            "links": {"self": [{"href": "url"}]},
        },
    ],
)
@patch("bb.pr.delete.request.delete", return_value=204)
@patch("bb.pr.delete.confirm", return_value=True)
@patch("bb.pr.delete.richprint.console.print")
def test_delete_pull_request(
    mock_print, mock_confirm, mock_delete, mock_get, mock_base_repo, mock_show_diff
):
    delete_pull_request(["1", "2"], True, False)

    # 2 requests per ID (one for get version, one for delete) -> 2 ids * 2 = 4
    # Wait, GET is 1 per ID. Delete is 1 per ID.
    assert mock_get.call_count == 2
    assert mock_delete.call_count == 2
    mock_print.assert_called()


@patch("bb.pr.delete.show_diff")
@patch("bb.pr.delete.cmnd.base_repo", return_value=("project", "repo_name"))
@patch(
    "bb.pr.delete.request.get",
    return_value=[
        200,
        {
            "id": 1,
            "state": "OPEN",
            "title": "Title",
            "fromRef": {"displayId": "src"},
            "toRef": {"displayId": "dst"},
            "version": 1,
            "links": {"self": [{"href": "url"}]},
        },
    ],
)
@patch("bb.pr.delete.request.delete", return_value=409)
@patch("bb.pr.delete.confirm", return_value=True)
@patch("bb.pr.delete.richprint.console.print")
def test_delete_pull_request_error(
    mock_print, mock_confirm, mock_delete, mock_get, mock_base_repo, mock_show_diff
):
    with pytest.raises(ValueError):
        delete_pull_request(["1"], True, False)

    assert mock_get.call_count == 1
    assert mock_delete.call_count == 1
    mock_print.assert_called()


@patch("bb.pr.delete.show_diff")
@patch("bb.pr.delete.cmnd.base_repo", return_value=("project", "repo_name"))
@patch(
    "bb.pr.delete.request.get",
    return_value=[
        200,
        {
            "id": 1,
            "state": "OPEN",
            "title": "Title",
            "fromRef": {"displayId": "src"},
            "toRef": {"displayId": "dst"},
            "version": 1,
            "links": {"self": [{"href": "url"}]},
        },
    ],
)
@patch("bb.pr.delete.request.delete", return_value=204)
@patch("bb.pr.delete.confirm", return_value=False)
@patch("bb.pr.delete.richprint.console.print")
def test_delete_pull_request_no_confirm(
    mock_print, mock_confirm, mock_delete, mock_get, mock_base_repo, mock_show_diff
):
    delete_pull_request(["1"], False, False)

    assert mock_get.call_count == 1
    assert mock_delete.call_count == 0
    mock_print.assert_called()


@patch("bb.pr.delete.show_diff")
@patch("bb.pr.delete.cmnd.base_repo", return_value=("project", "repo_name"))
@patch(
    "bb.pr.delete.request.get",
    return_value=[
        200,
        {
            "id": 1,
            "state": "OPEN",
            "title": "Title",
            "fromRef": {"displayId": "src"},
            "toRef": {"displayId": "dst"},
            "version": 1,
            "links": {"self": [{"href": "url"}]},
        },
    ],
)
@patch("bb.pr.delete.request.delete", return_value=204)
@patch("bb.pr.delete.confirm", return_value=True)
@patch("bb.pr.delete.richprint.console.print")
def test_delete_pull_request_with_diff(
    mock_print, mock_confirm, mock_delete, mock_get, mock_base_repo, mock_show_diff
):
    delete_pull_request(["1"], False, True)

    assert mock_get.call_count == 1
    assert mock_delete.call_count == 1
    mock_show_diff.assert_called_once()
