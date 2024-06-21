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

import json

from props import Api

from bb.utils.api import bitbucket_api

property = Api()


def test_test():
    test = bitbucket_api.test()
    assert (
        test == f"{property.bitbucket_host}/rest/api/latest/inbox/pull-requests/count"
    )
    assert isinstance(test, str)


def test_pull_request_create():
    pull_request_create = bitbucket_api.pull_request_create(
        property.project, property.repository
    )
    assert (
        pull_request_create
        == f"{property.bitbucket_host}/rest/api/1.0/projects/{property.project}/repos/{property.repository}/pull-requests"
    )
    assert isinstance(pull_request_create, str)


def test_get_repo_info():
    get_repo_info = bitbucket_api.get_repo_info(property.project)
    assert (
        get_repo_info
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos?start=0&limit=10000"
    )
    assert isinstance(get_repo_info, str)


def test_default_reviewers():
    default_reviewers = bitbucket_api.default_reviewers(
        property.project,
        property.repo_id,
        property.from_branch,
        property.target,
    )
    reviewer_query = f"avatarSize=32&sourceRepoId={property.repo_id}&sourceRefId=refs%2Fheads%2F{property.from_branch.replace('/','%2F')}&targetRepoId={property.repo_id}&targetRefId=refs%2Fheads%2F{property.target.replace('/','%2F')}"
    assert (
        reviewer_query
        == "avatarSize=32&sourceRepoId=1234&sourceRefId=refs%2Fheads%2Ffeature%2Ftest_branch&targetRepoId=1234&targetRefId=refs%2Fheads%2Fmaster"
    )

    assert isinstance(reviewer_query, str)

    assert (
        default_reviewers
        == f"{property.bitbucket_host}/rest/default-reviewers/latest/projects/{property.project}/repos/repository/reviewers?{reviewer_query}"
    )

    assert isinstance(default_reviewers, str)


def test_pull_request_body():
    pull_request_body = bitbucket_api.pull_request_body(
        property.title_and_description,
        property.from_branch,
        property.repository,
        property.project,
        property.target,
        property.reviewers,
    )

    assert pull_request_body == json.dumps(
        {
            "title": property.title_and_description[0],
            "description": property.title_and_description[1],
            "state": "OPEN",
            "open": "true",
            "closed": "false",
            "fromRef": {
                "id": "refs/heads/" + property.from_branch,
                "repository": {
                    "slug": property.repository,
                    "name": property.repository,
                    "project": {"key": property.project},
                },
            },
            "toRef": {
                "id": "refs/heads/" + property.target,
                "repository": {
                    "slug": property.repository,
                    "name": property.repository,
                    "project": {"key": property.project},
                },
            },
            "locked": "false",
            "reviewers": property.reviewers,
        }
    )

    assert isinstance(pull_request_body, str)


def test_pull_request_difference():
    pull_request_difference = bitbucket_api.pull_request_difference(
        property.project, property.repository, property.pr_no
    )

    assert (
        pull_request_difference
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}/changes?start=0&limit=1000&changeScope=unreviewed"
    )

    assert isinstance(pull_request_difference, str)


def test_pull_request_info():
    pull_request_info = bitbucket_api.pull_request_info(
        property.project, property.repository, property.pr_no
    )

    assert (
        pull_request_info
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}"
    )

    assert isinstance(pull_request_info, str)


def test_pull_request_viewer():
    pull_request_viewer = bitbucket_api.pull_request_viewer(property.role)

    assert (
        pull_request_viewer
        == f"{property.bitbucket_host}/rest/api/latest/inbox/pull-requests?role={property.role}&avatarSize=64"
    )

    assert isinstance(pull_request_viewer, str)


def test_current_pull_request():
    current_pull_request = bitbucket_api.current_pull_request(
        property.project, property.repository
    )

    assert (
        current_pull_request
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests"
    )

    assert isinstance(current_pull_request, str)


def test_whoami():
    whoami = bitbucket_api.whoami()

    assert whoami == f"{property.bitbucket_host}/plugins/servlet/applinks/whoami"
    assert isinstance(whoami, str)


def test_action_pull_request():
    action_pull_request = bitbucket_api.action_pull_request(
        property.project,
        property.repository,
        property.target,
        property.user,
    )

    assert (
        action_pull_request
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.target}/participants/{property.user}?avatarSize=32"
    )
    assert isinstance(action_pull_request, str)


def test_pr_source_branch_delete_check():
    pr_source_branch_delete_check = bitbucket_api.pr_source_branch_delete_check(
        property.project,
        property.repository,
        property.pr_no,
        property.from_branch,
    )

    assert (
        pr_source_branch_delete_check
        == f"{property.bitbucket_host}/rest/pull-request-cleanup/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}?deleteSourceRef={property.from_branch}&retargetDependents={property.from_branch}"
    )
    assert isinstance(pr_source_branch_delete_check, str)


def test_validate_merge():
    validate_merge = bitbucket_api.validate_merge(
        property.project, property.repository, property.pr_no
    )
    assert (
        validate_merge
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}/merge"
    )
    assert isinstance(validate_merge, str)


def test_merge_config():
    merge_config = bitbucket_api.merge_config(property.project, property.repository)

    assert (
        merge_config
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/settings/pull-requests"
    )
    assert isinstance(merge_config, str)


def test_get_merge_info():
    get_merge_info = bitbucket_api.get_merge_info(
        property.project, property.repository, property.target
    )
    assert (
        get_merge_info
        == f"{property.bitbucket_host}/rest/branch-utils/latest/projects/{property.project}/repos/{property.repository}/automerge/path/refs/heads/{property.target}"
    )
    assert isinstance(get_merge_info, str)


def test_pr_merge_body():
    pr_merge_body = bitbucket_api.pr_merge_body(
        property.project,
        property.repository,
        property.pr_no,
        property.from_branch,
        property.target,
    )

    assert pr_merge_body == json.dumps(
        {
            "autoSubject": False,
            "message": f"Merge pull request #{property.pr_no} in {property.project}/{property.repository} from {property.from_branch} to {property.target}",
        }
    )

    assert isinstance(pr_merge_body, str)


def test_pr_cleanup():
    pr_cleanup = bitbucket_api.pr_cleanup(
        property.project, property.repository, property.pr_no
    )
    assert (
        pr_cleanup
        == f"{property.bitbucket_host}/rest/pull-request-cleanup/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}"
    )
    assert isinstance(pr_cleanup, str)


def test_pr_cleanup_body():
    for prop in property.delete_source_branch:
        pr_cleanup_body = bitbucket_api.pr_cleanup_body(prop)
        assert isinstance(prop, bool)
        assert pr_cleanup_body == json.dumps(
            {"deleteSourceRef": prop, "retargetDependents": prop}
        )
        assert isinstance(pr_cleanup_body, str)


def test_pr_rebase():
    pr_rebase = bitbucket_api.pr_rebase(
        property.project,
        property.repository,
        property.pr_no,
        property.version,
    )

    assert pr_rebase == [
        json.dumps({"version": property.version}),
        f"{property.bitbucket_host}/rest/git/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}/rebase",
    ]
    assert isinstance(pr_rebase, list)


def test_delete_branch():
    delete_branch = bitbucket_api.delete_branch(
        property.project,
        property.repository,
        property.from_branch,
    )
    assert delete_branch == [
        json.dumps({"name": f"{property.from_branch}"}),
        f"{property.bitbucket_host}/rest/branch-utils/latest/projects/{property.project}/repos/{property.repository}/branches",
    ]
    assert isinstance(delete_branch, list)


def test_delete_repo():
    delete_repo = bitbucket_api.delete_repo(property.project, property.repository)
    assert (
        delete_repo
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}"
    )

    assert isinstance(delete_repo, str)


def test_create_repo():
    create_repo = bitbucket_api.create_repo(property.project)
    assert (
        create_repo
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos"
    )

    assert isinstance(create_repo, str)
