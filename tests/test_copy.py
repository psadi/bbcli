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
