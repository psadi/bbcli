# -*- coding: utf-8 -*-
"""
bb.utils.api - contains the API model for Bitbucket server
"""

import json

from typer import Exit

from bb.utils.ini import is_config_present, parse


class BitbucketAPI:
    def __init__(self, bitbucket_host: str):
        self.bitbucket_host = bitbucket_host

    def _api_url(self, path: str) -> str:
        return f"{self.bitbucket_host}{path}"

    def test(self) -> str:
        return self._api_url("/rest/api/latest/inbox/pull-requests/count")

    def pull_request_create(self, project: str, repository: str) -> str:
        return self._api_url(
            f"/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests"
        )

    def get_repo_info(self, project: str) -> str:
        return self._api_url(
            f"/rest/api/latest/projects/{project}/repos?start=0&limit=10000"
        )

    def default_reviewers(
        self, project: str, repo_id: str, from_branch: str, target: str
    ) -> str:
        reviewer_query = f"avatarSize=32&sourceRepoId={repo_id}&sourceRefId=refs%2Fheads%2F{from_branch.replace(
            '/', '%2F')}&targetRepoId={repo_id}&targetRefId=refs%2Fheads%2F{target.replace('/', '%2F')}"
        return self._api_url(
            f"/rest/default-reviewers/latest/projects/{
                project}/repos/repository/reviewers?{reviewer_query}"
        )

    def pull_request_body(
        self,
        title_and_description: str,
        from_branch: str,
        repository: str,
        project: str,
        target: str,
        reviewers: list,
    ) -> str:
        return json.dumps(
            {
                "title": title_and_description[0],
                "description": title_and_description[1],
                "state": "OPEN",
                "open": "true",
                "closed": "false",
                "fromRef": {
                    "id": f"refs/heads/{from_branch}",
                    "repository": {
                        "slug": repository,
                        "name": repository,
                        "project": {"key": project},
                    },
                },
                "toRef": {
                    "id": f"refs/heads/{target}",
                    "repository": {
                        "slug": repository,
                        "name": repository,
                        "project": {"key": project},
                    },
                },
                "locked": "false",
                "reviewers": reviewers,
            }
        )

    def pull_request_difference(
        self, project: str, repository: str, pr_number: str
    ) -> str:
        return self._api_url(
            f"/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{
                pr_number}/changes?start=0&limit=1000&changeScope=unreviewed"
        )

    def pull_request_info(self, project: str, repository: str, _id: str) -> str:
        return self._api_url(
            f"/rest/api/latest/projects/{project}/repos/{
                repository}/pull-requests/{_id}"
        )

    def pull_request_viewer(self, role: str) -> str:
        return self._api_url(
            f"/rest/api/latest/inbox/pull-requests?role={role}&avatarSize=64"
        )

    def current_pull_request(self, project: str, repository: str) -> str:
        return self._api_url(
            f"/rest/api/latest/projects/{project}/repos/{
                repository}/pull-requests"
        )

    def whoami(self) -> str:
        return self._api_url("/plugins/servlet/applinks/whoami")

    def action_pull_request(
        self, project: str, repository: str, target: int, user_id: str
    ) -> str:
        return self._api_url(
            f"/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{
                target}/participants/{user_id}?avatarSize=32"
        )

    def pr_source_branch_delete_check(
        self, project: str, repository: str, _id: str, delete_source_branch: str
    ) -> str:
        return self._api_url(
            f"/rest/pull-request-cleanup/latest/projects/{project}/repos/{repository}/pull-requests/{
                _id}?deleteSourceRef={delete_source_branch}&retargetDependents={delete_source_branch}"
        )

    def validate_merge(self, project: str, repository: str, _id: str) -> str:
        return self._api_url(
            f"/rest/api/latest/projects/{project}/repos/{
                repository}/pull-requests/{_id}/merge"
        )

    def merge_config(self, project: str, repository: str) -> str:
        return self._api_url(
            f"/rest/api/latest/projects/{project}/repos/{
                repository}/settings/pull-requests"
        )

    def get_merge_info(self, project: str, repository: str, target_branch: str) -> str:
        return self._api_url(
            f"/rest/branch-utils/latest/projects/{project}/repos/{
                repository}/automerge/path/refs/heads/{target_branch}"
        )

    def pr_merge_body(
        self,
        project: str,
        repository: str,
        _id: str,
        from_branch: str,
        target_branch: str,
    ) -> str:
        return json.dumps(
            {
                "autoSubject": False,
                "message": f"Merge pull request #{_id} in {project}/{repository} from {from_branch} to {target_branch}",
            }
        )

    def pr_cleanup(self, project: str, repository: str, _id: str) -> str:
        return self._api_url(
            f"/rest/pull-request-cleanup/latest/projects/{
                project}/repos/{repository}/pull-requests/{_id}"
        )

    def pr_cleanup_body(self, delete_retarget: bool) -> str:
        return json.dumps(
            {
                "deleteSourceRef": delete_retarget,
                "retargetDependents": delete_retarget,
            }
        )

    def pr_rebase(self, project: str, repository: str, _id: str, version: int) -> list:
        return [
            json.dumps({"version": version}),
            self._api_url(
                f"/rest/git/latest/projects/{project}/repos/{
                    repository}/pull-requests/{_id}/rebase"
            ),
        ]

    def delete_branch(self, project: str, repository: str, source_branch: str) -> list:
        return [
            json.dumps({"name": f"{source_branch}"}),
            self._api_url(
                f"/rest/branch-utils/latest/projects/{
                    project}/repos/{repository}/branches"
            ),
        ]

    def delete_repo(self, project: str, repo: str) -> str:
        return self._api_url(f"/rest/api/latest/projects/{project}/repos/{repo}")

    def create_repo(self, project: str) -> str:
        return self._api_url(f"/rest/api/latest/projects/{project}/repos")


def load_bitbucket_api() -> BitbucketAPI:
    if not is_config_present():
        raise ValueError()

    config_data = parse()
    if len(config_data) != 3:
        raise ValueError()

    return BitbucketAPI(config_data[2])


try:
    bitbucket_api = load_bitbucket_api()
except ValueError:
    bitbucket_api = None
    Exit(code=1)
