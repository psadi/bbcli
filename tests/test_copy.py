# -*- coding: utf-8 -*-
from unittest.mock import patch

from bb.pr.copy import copy_pull_request
from bb.utils.api import bitbucket_api


@patch("bb.pr.copy.cmnd.base_repo")
@patch("bb.pr.copy.request.get")
@patch("bb.pr.copy.cmnd.cp_to_clipboard")
def test_copy_pull_request(mock_cp_to_clipboard, mock_get, mock_base_repo):
    # Arrange
    mock_base_repo.return_value = ("project", "repository")
    mock_get.return_value = [None, {"links": {"self": [{"href": "test_url"}]}}]

    # Act
    copy_pull_request("123")

    # Assert
    mock_base_repo.assert_called_once()
    mock_get.assert_called_once_with(
        bitbucket_api.pull_request_info("project", "repository", "123")
    )
    mock_cp_to_clipboard.assert_called_once_with("test_url")
