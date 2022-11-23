# -*- coding: utf-8 -*-

import json
from bb.utils import api
from props import Api

property = Api()


def test_test():
    test = api.test(property.bitbucket_host)
    assert (
        test == f"{property.bitbucket_host}/rest/api/latest/inbox/pull-requests/count"
    )
    assert type(test) == str


def test_pull_request_create():
    pull_request_create = api.pull_request_create(
        property.bitbucket_host, property.project, property.repository
    )
    assert (
        pull_request_create
        == f"{property.bitbucket_host}/rest/api/1.0/projects/{property.project}/repos/{property.repository}/pull-requests"
    )
    assert type(pull_request_create) == str


def test_get_repo_info():
    get_repo_info = api.get_repo_info(property.bitbucket_host, property.project)
    assert (
        get_repo_info
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos?start=0&limit=10000"
    )
    assert type(get_repo_info) == str


def test_default_reviewers():
    default_reviewers = api.default_reviewers(
        property.bitbucket_host,
        property.project,
        property.repo_id,
        property.from_branch,
        property.target,
    )
    reviewer_query = f"avatarSize=32&sourceRepoId={property.repo_id}&sourceRefId=refs%2Fheads%2F{property.from_branch.replace('/','%2F')}&targetRepoId={property.repo_id}&targetRefId=refs%2Fheads%2F{property.target.replace('/','%2F')}"
    assert (
        reviewer_query
        == f"avatarSize=32&sourceRepoId=1234&sourceRefId=refs%2Fheads%2Ffeature%2Ftest_branch&targetRepoId=1234&targetRefId=refs%2Fheads%2Fmaster"
    )

    assert type(reviewer_query) == str

    assert (
        default_reviewers
        == f"{property.bitbucket_host}/rest/default-reviewers/latest/projects/{property.project}/repos/repository/reviewers?{reviewer_query}"
    )

    assert type(default_reviewers) == str


def test_pull_request_body():
    pull_request_body = api.pull_request_body(
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

    assert type(pull_request_body) == str


def test_pull_request_difference():
    pull_request_difference = api.pull_request_difference(
        property.bitbucket_host, property.project, property.repository, property.pr_no
    )

    assert (
        pull_request_difference
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}/changes?start=0&limit=1000&changeScope=unreviewed"
    )

    assert type(pull_request_difference) == str


def test_pull_request_info():
    pull_request_info = api.pull_request_info(
        property.bitbucket_host, property.project, property.repository, property.pr_no
    )

    assert (
        pull_request_info
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}"
    )

    assert type(pull_request_info) == str


def test_pull_request_viewer():
    pull_request_viewer = api.pull_request_viewer(
        property.bitbucket_host, property.role
    )

    assert (
        pull_request_viewer
        == f"{property.bitbucket_host}/rest/api/latest/inbox/pull-requests?role={property.role}&avatarSize=64"
    )

    assert type(pull_request_viewer) == str


def test_current_pull_request():
    current_pull_request = api.current_pull_request(
        property.bitbucket_host, property.project, property.repository
    )

    assert (
        current_pull_request
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests"
    )

    assert type(current_pull_request) == str


def test_whoami():
    whoami = api.whoami(property.bitbucket_host)

    assert whoami == f"{property.bitbucket_host}/plugins/servlet/applinks/whoami"
    assert type(whoami) == str


def test_action_pull_request():
    action_pull_request = api.action_pull_request(
        property.bitbucket_host,
        property.project,
        property.repository,
        property.target,
        property.user,
    )

    assert (
        action_pull_request
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.target}/participants/{property.user}?avatarSize=32"
    )
    assert type(action_pull_request) == str


def test_pr_source_branch_delete_check():
    pr_source_branch_delete_check = api.pr_source_branch_delete_check(
        property.bitbucket_host,
        property.project,
        property.repository,
        property.pr_no,
        property.from_branch,
    )

    assert (
        pr_source_branch_delete_check
        == f"{property.bitbucket_host}/rest/pull-request-cleanup/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}?deleteSourceRef={property.from_branch}&retargetDependents={property.from_branch}"
    )
    assert type(pr_source_branch_delete_check) == str


def test_validate_merge():
    validate_merge = api.validate_merge(
        property.bitbucket_host, property.project, property.repository, property.pr_no
    )
    assert (
        validate_merge
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}/merge"
    )
    assert type(validate_merge) == str


def test_merge_config():
    merge_config = api.merge_config(
        property.bitbucket_host, property.project, property.repository
    )

    assert (
        merge_config
        == f"{property.bitbucket_host}/rest/api/latest/projects/{property.project}/repos/{property.repository}/settings/pull-requests"
    )
    assert type(merge_config) == str


def test_get_merge_info():
    get_merge_info = api.get_merge_info(
        property.bitbucket_host, property.project, property.repository, property.target
    )
    assert (
        get_merge_info
        == f"{property.bitbucket_host}/rest/branch-utils/latest/projects/{property.project}/repos/{property.repository}/automerge/path/refs/heads/{property.target}"
    )
    assert type(get_merge_info) == str


def test_pr_merge_body():
    pr_merge_body = api.pr_merge_body(
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

    assert type(pr_merge_body) == str


def test_pr_cleanup():
    pr_cleanup = api.pr_cleanup(
        property.bitbucket_host, property.project, property.repository, property.pr_no
    )
    assert (
        pr_cleanup
        == f"{property.bitbucket_host}/rest/pull-request-cleanup/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}"
    )
    assert type(pr_cleanup) == str


def test_pr_cleanup_body():
    for prop in property.delete_source_branch:
        pr_cleanup_body = api.pr_cleanup_body(prop)
        assert type(prop) == bool
        assert pr_cleanup_body == json.dumps(
            {"deleteSourceRef": prop, "retargetDependents": True}
        )
        assert type(pr_cleanup_body) == str


def test_pr_rebase():
    pr_rebase = api.pr_rebase(
        property.bitbucket_host,
        property.project,
        property.repository,
        property.pr_no,
        property.version,
    )

    assert pr_rebase == [
        json.dumps({"version": property.version}),
        f"{property.bitbucket_host}/rest/git/latest/projects/{property.project}/repos/{property.repository}/pull-requests/{property.pr_no}/rebase",
    ]
    assert type(pr_rebase) == list


def test_delete_branch():
    delete_branch = api.delete_branch(
        property.bitbucket_host,
        property.project,
        property.repository,
        property.from_branch,
    )
    assert delete_branch == [
        json.dumps({"name": f"{property.from_branch}"}),
        f"{property.bitbucket_host}/rest/branch-utils/latest/projects/{property.project}/repos/{property.repository}/branches",
    ]
    assert type(delete_branch) == list
