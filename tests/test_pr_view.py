# -*- coding: utf-8 -*-
from unittest.mock import patch

from bb.pr.view import view_pull_request


@patch("bb.pr.view.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.view.get")
def test_view_pull_request(mock_get, mock_base_repo):
    mock_get.return_value = [
        200,
        {
            "id": "1",
            "title": "Test Title",
            "description": "Test Desc",
            "fromRef": {"displayId": "src"},
            "toRef": {"displayId": "dst"},
            "state": "OPEN",
            "author": {
                "user": {
                    "displayName": "User",
                    "emailAddress": "test@test.com",
                    "name": "usr",
                }
            },
            "reviewers": [],
            "links": {"self": [{"href": "url"}]},
        },
    ]

    view_pull_request("1", False)

    mock_get.assert_called_once()


@patch("bb.pr.view.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.view.get")
@patch("bb.pr.view.webbrowser.open_new")
def test_view_pull_request_web(mock_webbrowser, mock_get, mock_base_repo):
    mock_get.return_value = [
        200,
        {"id": "1", "links": {"self": [{"href": "http://example.com"}]}},
    ]

    view_pull_request("1", True)

    mock_get.assert_called_once()
    mock_webbrowser.assert_called_once_with("http://example.com")


@patch("bb.pr.view.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.view.get")
@patch("bb.pr.view.webbrowser.open_new", return_value=False)
def test_view_pull_request_web_error(mock_webbrowser, mock_get, mock_base_repo):
    mock_get.return_value = [
        200,
        {"id": "1", "links": {"self": [{"href": "http://example.com"}]}},
    ]

    view_pull_request("1", True)

    mock_get.assert_called_once()
    mock_webbrowser.assert_called_once_with("http://example.com")
