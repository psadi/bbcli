# -*- coding: utf-8 -*-
from unittest.mock import patch

from bb.pr.list import list_pull_request


@patch("bb.pr.list.request.get")
@patch("bb.pr.list.cmnd.base_repo", return_value=("project", "repo_name"))
def test_list_pull_request_current(mock_base_repo, mock_get):
    mock_get.return_value = [
        200,
        {
            "values": [
                {
                    "title": "PR Title",
                    "links": {"self": [{"href": "http://example.com"}]},
                    "state": "OPEN",
                    "fromRef": {"repository": {"slug": "repo"}, "displayId": "src"},
                    "toRef": {"displayId": "dst"},
                    "author": {"user": {"displayName": "User"}},
                    "reviewers": [],
                    "properties": {},
                }
            ]
        },
    ]

    list_pull_request("current", False)

    mock_get.assert_called_once()


@patch("bb.pr.list.request.get")
@patch("bb.pr.list.cmnd.base_repo", return_value=("project", "repo_name"))
def test_list_pull_request_all(mock_base_repo, mock_get):
    mock_get.return_value = [
        200,
        {
            "values": [
                {
                    "title": "PR Title",
                    "links": {"self": [{"href": "http://example.com"}]},
                    "state": "OPEN",
                    "fromRef": {"repository": {"slug": "repo"}, "displayId": "src"},
                    "toRef": {"displayId": "dst"},
                    "author": {"user": {"displayName": "User"}},
                    "reviewers": [],
                    "properties": {},
                }
            ]
        },
    ]

    list_pull_request("author", True)

    mock_get.assert_called_once()
