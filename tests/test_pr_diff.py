# -*- coding: utf-8 -*-
from unittest.mock import patch

from bb.pr.diff import show_diff


@patch("bb.pr.diff.cmnd.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.diff.request.get")
@patch("bb.pr.diff.cmnd.show_git_diff")
@patch("bb.pr.diff.richprint.console.print")
@patch("bb.pr.diff.richprint.table")
def test_show_diff(
    mock_table, mock_print, mock_show_git_diff, mock_get, mock_base_repo
):
    mock_get.side_effect = [
        [
            200,
            {
                "fromHash": "abcdef1234567890",
                "toHash": "1234567890abcdef",
                "values": [{"path": {"toString": "file.txt"}, "type": "ADD"}],
            },
        ],
        [
            200,
            {
                "id": 1,
                "title": "Test Title",
                "fromRef": {"displayId": "src"},
                "toRef": {"displayId": "dst"},
            },
        ],
    ]

    show_diff("1")

    assert mock_get.call_count == 2
    mock_print.assert_called()
    mock_table.assert_called()
