# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest

from bb.pr.review import review_pull_request


@patch("bb.pr.review.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.review.bitbucket_api.whoami", return_value="whoami_url")
@patch("bb.pr.review.get", return_value=[200, "username"])
@patch("bb.pr.review.put", return_value=[200, {}])
def test_review_pull_request(mock_put, mock_get, mock_whoami, mock_base_repo):
    review_pull_request(1, "approve")
    assert mock_get.call_count == 1
    assert mock_put.call_count == 1


@patch("bb.pr.review.base_repo", return_value=("project", "repo_name"))
@patch("bb.pr.review.bitbucket_api.whoami", return_value="whoami_url")
@patch("bb.pr.review.get", return_value=[200, "username"])
@patch("bb.pr.review.put", return_value=[409, {}])
def test_review_pull_request_error(mock_put, mock_get, mock_whoami, mock_base_repo):
    with pytest.raises(
        ValueError,
        match="Cannot perform action on PR. Possibly due to outdated PR state.",
    ):
        review_pull_request(1, "approve")
