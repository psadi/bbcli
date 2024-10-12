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

"""
bb.utils.api - contains the API model for Bitbucket server
"""

import json

from typer import Exit

from bb.utils.ini import is_config_present, parse


class BitbucketAPI:
    def __init__(self, bitbucket_host: str):
        """
        Initializes a new instance of the API class.

        Args:
            bitbucket_host (str): The host URL of the Bitbucket server.
        """
        self.bitbucket_host = bitbucket_host

    def api_project_url(self, path: str) -> str:
        """
        Generates the URL for the given project path.

        Args:
            path (str): The project path.

        Returns:
            str: The generated URL for the project.
        """
        return f"{self.bitbucket_host}{path}"

    def test(self) -> str:
        """
        This method returns the API project URL for retrieving the count of pull requests in the inbox.

        :return: A string representing the API project URL for retrieving the count of pull requests in the inbox.
        """
        return self.api_project_url("/rest/api/latest/inbox/pull-requests/count")

    def pull_request_create(self, project: str, repository: str) -> str:
        """
        Creates a new pull request for the specified project and repository.

        Args:
            project (str): The name of the project.
            repository (str): The name of the repository.

        Returns:
            str: The URL of the newly created pull request.
        """
        return self.api_project_url(
            f"/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests"
        )

    def get_repo_info(self, project: str) -> str:
        """
        Retrieves the API URL for getting repository information for a given project.

        Args:
            project (str): The project key or ID.

        Returns:
            str: The API URL for getting repository information.
        """
        return self.api_project_url(
            f"/rest/api/latest/projects/{project}/repos?start=0&limit=10000"
        )

    def default_reviewers(
        self, project: str, repo_id: str, from_branch: str, target: str
    ) -> str:
        """
        Get the default reviewers for a given project, repository, source branch, and target branch.

        Args:
            project (str): The project key or ID.
            repo_id (str): The repository ID.
            from_branch (str): The source branch.
            target (str): The target branch.

        Returns:
            str: The URL for retrieving the default reviewers.
        """
        reviewer_query = f"avatarSize=32&sourceRepoId={repo_id}&sourceRefId=refs%2Fheads%2F{from_branch.replace('/', '%2F')}&targetRepoId={repo_id}&targetRefId=refs%2Fheads%2F{target.replace('/', '%2F')}"
        return self.api_project_url(
            f"/rest/default-reviewers/latest/projects/{project}/repos/repository/reviewers?{reviewer_query}"
        )

    def pull_request_body(
        self,
        title: str,
        description: str,
        from_branch: str,
        repository: str,
        project: str,
        target: str,
        reviewers: list,
    ) -> str:
        """
        Generate the JSON body for creating a pull request.

        Args:
            title (str): The title of the pull request.
            description (str): The description of the pull request.
            from_branch (str): The source branch of the pull request.
            repository (str): The name of the repository.
            project (str): The key of the project.
            target (str): The target branch of the pull request.
            reviewers (list): A list of reviewers for the pull request.

        Returns:
            str: The JSON body for creating a pull request.
        """
        return json.dumps(
            {
                "title": title,
                "description": description,
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
        """
        Retrieves the difference URL for a specific pull request.

        Args:
            project (str): The project key or ID.
            repository (str): The repository slug or ID.
            pr_number (str): The pull request number.

        Returns:
            str: The URL for the pull request difference.
        """
        return self.api_project_url(
            f"/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{pr_number}/changes?start=0&limit=1000&changeScope=unreviewed"
        )

    def pull_request_info(self, project: str, repository: str, _id: str) -> str:
        """
        Retrieves the URL for the pull request with the given project, repository, and ID.

        Args:
            project (str): The name of the project.
            repository (str): The name of the repository.
            _id (str): The ID of the pull request.

        Returns:
            str: The URL of the pull request.
        """
        return self.api_project_url(
            f"/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{_id}"
        )

    def pull_request_viewer(self, role: str) -> str:
        """
        Returns the URL for viewing pull requests in the inbox with the specified role.

        Args:
            role (str): The role of the user viewing the pull requests.

        Returns:
            str: The URL for viewing pull requests in the inbox with the specified role.
        """
        return self.api_project_url(
            f"/rest/api/latest/inbox/pull-requests?role={role}&avatarSize=64"
        )

    def current_pull_request(self, project: str, repository: str) -> str:
        """
        Returns the URL for the current pull request of the specified project and repository.

        Args:
            project (str): The name of the project.
            repository (str): The name of the repository.

        Returns:
            str: The URL of the current pull request.

        """
        return self.api_project_url(
            f"/rest/api/latest/projects/{project}/repos/{repository}/pull-requests"
        )

    def whoami(self) -> str:
        """
        Retrieves the user information from the API.

        Returns:
            str: The URL for retrieving the user information.
        """
        return self.api_project_url("/plugins/servlet/applinks/whoami")

    def action_pull_request(
        self, project: str, repository: str, target: int, user_id: str
    ) -> str:
        """
        Generates the URL for the pull request action.

        Args:
            project (str): The project key or ID.
            repository (str): The repository slug or ID.
            target (int): The pull request ID.
            user_id (str): The user ID.

        Returns:
            str: The URL for the pull request action.
        """
        return self.api_project_url(
            f"/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{target}/participants/{user_id}?avatarSize=32"
        )

    def pr_source_branch_delete_check(
        self, project: str, repository: str, _id: str, delete_source_branch: str
    ) -> str:
        """
        Generates the URL for checking if a pull request source branch can be deleted.

        Args:
            project (str): The project key or ID.
            repository (str): The repository slug or ID.
            _id (str): The ID of the pull request.
            delete_source_branch (str): Indicates whether the source branch should be deleted.

        Returns:
            str: The URL for checking if the source branch can be deleted.
        """
        return self.api_project_url(
            f"/rest/pull-request-cleanup/latest/projects/{project}/repos/{repository}/pull-requests/{_id}?deleteSourceRef={delete_source_branch}&retargetDependents={delete_source_branch}"
        )

    def validate_merge(self, project: str, repository: str, _id: str) -> str:
        """
        Validates the merge of a pull request in the specified project and repository.

        Args:
            project (str): The project key or ID.
            repository (str): The repository slug or ID.
            _id (str): The ID of the pull request.

        Returns:
            str: The URL for validating the merge of the pull request.
        """
        return self.api_project_url(
            f"/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{_id}/merge"
        )

    def merge_config(self, project: str, repository: str) -> str:
        """
        Generates the API URL for merging the configuration of a specific project and repository.

        Args:
            project (str): The name of the project.
            repository (str): The name of the repository.

        Returns:
            str: The API URL for merging the configuration.
        """
        return self.api_project_url(
            f"/rest/api/latest/projects/{project}/repos/{repository}/settings/pull-requests"
        )

    def get_merge_info(self, project: str, repository: str, target_branch: str) -> str:
        """
        Retrieves the merge information for a given project, repository, and target branch.

        Args:
            project (str): The name of the project.
            repository (str): The name of the repository.
            target_branch (str): The name of the target branch.

        Returns:
            str: The URL for retrieving the merge information.

        """
        return self.api_project_url(
            f"/rest/branch-utils/latest/projects/{project}/repos/{repository}/automerge/path/refs/heads/{target_branch}"
        )

    def pr_merge_body(
        self,
        project: str,
        repository: str,
        _id: str,
        from_branch: str,
        target_branch: str,
    ) -> str:
        """
        Generate the merge body for a pull request.

        Args:
            project (str): The name of the project.
            repository (str): The name of the repository.
            _id (str): The ID of the pull request.
            from_branch (str): The name of the source branch.
            target_branch (str): The name of the target branch.

        Returns:
            str: The merge body as a JSON string.
        """
        return json.dumps(
            {
                "autoSubject": False,
                "message": f"Merge pull request #{_id} in {project}/{repository} from {from_branch} to {target_branch}",
            }
        )

    def pr_cleanup(self, project: str, repository: str, _id: str) -> str:
        """
        Returns the URL for cleaning up a pull request.

        Args:
            project (str): The project name.
            repository (str): The repository name.
            _id (str): The ID of the pull request.

        Returns:
            str: The URL for cleaning up the pull request.
        """
        return self.api_project_url(
            f"/rest/pull-request-cleanup/latest/projects/{project}/repos/{repository}/pull-requests/{_id}"
        )

    def pr_cleanup_body(self, delete_retarget: bool) -> str:
        """
        Generates the JSON body for cleaning up a pull request.

        Args:
            delete_retarget (bool): Indicates whether to delete the source reference and retarget dependents.

        Returns:
            str: The JSON body for cleaning up a pull request.
        """
        return json.dumps(
            {
                "deleteSourceRef": delete_retarget,
                "retargetDependents": delete_retarget,
            }
        )

    def pr_rebase(self, project: str, repository: str, _id: str, version: int) -> list:
        """
        Rebase a pull request.

        Args:
            project (str): The project key or ID.
            repository (str): The repository slug or ID.
            _id (str): The ID of the pull request.
            version (int): The version of the pull request.

        Returns:
            list: A list containing the JSON representation of the version and the API URL for the rebase.
        """
        return [
            json.dumps({"version": version}),
            self.api_project_url(
                f"/rest/git/latest/projects/{project}/repos/{repository}/pull-requests/{_id}/rebase"
            ),
        ]

    def delete_branch(self, project: str, repository: str, source_branch: str) -> list:
        """
        Deletes a branch in a Bitbucket repository.

        Args:
            project (str): The project key or ID.
            repository (str): The repository slug or ID.
            source_branch (str): The name of the branch to delete.

        Returns:
            list: A list containing the JSON representation of the branch to delete and the API URL for deleting the branch.

        """
        return [
            json.dumps({"name": f"{source_branch}"}),
            self.api_project_url(
                f"/rest/branch-utils/latest/projects/{project}/repos/{repository}/branches"
            ),
        ]

    def delete_repo(self, project: str, repo: str) -> str:
        """
        Deletes a repository in the specified project.

        Args:
            project (str): The project key or ID.
            repo (str): The repository slug or ID.

        Returns:
            str: The API URL for deleting the repository.
        """
        return self.api_project_url(f"/rest/api/latest/projects/{project}/repos/{repo}")

    def create_repo(self, project: str) -> str:
        """
        Creates a new repository in the specified project.

        Args:
            project (str): The name of the project where the repository will be created.

        Returns:
            str: The URL of the newly created repository.

        """
        return self.api_project_url(f"/rest/api/latest/projects/{project}/repos")


def load_bitbucket_api() -> BitbucketAPI:
    """
    Loads the Bitbucket API by reading the configuration data and returning an instance of BitbucketAPI.

    Raises:
        ValueError: If the configuration is not present or if the number of configuration items is not 3.

    Returns:
        BitbucketAPI: An instance of the BitbucketAPI class.
    """
    if not is_config_present():
        raise ValueError("Configuration not present")

    config_data = parse()
    if len(config_data) != 3:
        raise ValueError(f"Expected 3 configuration items, got {len(config_data)}")

    return BitbucketAPI(config_data[2])


try:
    bitbucket_api = load_bitbucket_api()
except ValueError:
    bitbucket_api = None
    Exit(code=1)
