#-*- coding: utf-8 -*-

# Importing the from_branch function from the bb.utils.command module.
import json

def test(bitbucket_host: str) -> str:
    """
    > This function returns a string that is the API endpoint for the user's inbox

    :param bitbucket_host: The hostname of your Bitbucket instance
    :type bitbucket_host: str
    :return: The string of the API call to check the user's inbox.
    """
    return f"{bitbucket_host}/rest/api/latest/inbox/pull-requests/count"

def pull_request_create(bitbucket_host: str, project: str, repository: str) -> str:
    """
    It returns the pull request API to create pull requests

    :param bitbucket_host: The hostname of your Bitbucket instance
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: The name of the repository you want to create a pull request for
    :type repository: str
    :return: The pull request API to create pull requests
    """
    return f"{bitbucket_host}/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests"

def get_repo_info(bitbucket_host: str, project: str) -> str:
    """
    `Returns the project repository information`

    :param bitbucket_host: The hostname of your Bitbucket instance
    :type bitbucket_host: str
    :param project: The project name
    :type project: str
    :return: The project repository information
    """
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos?start=0&limit=10000"

def default_reviewers(bitbucket_host: str, project: str, repo_id: str, from_branch: str, target: str) -> str:
    """
    > Returns the api to validate default reviewrs in a repository

    :param bitbucket_host: The hostname of your Bitbucket instance
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repo_id: The repository id of the repository you want to get the default reviewers for
    :type repo_id: str
    :param from_branch: The branch you're merging from
    :type from_branch: str
    :param target: The branch you want to merge to
    :type target: str
    :return: The api to validate default reviewrs in a repository
    """
    reviewer_query = f"avatarSize=32&sourceRepoId={repo_id}&sourceRefId=refs%2Fheads%2F{from_branch.replace('/','%2F')}&targetRepoId={repo_id}&targetRefId=refs%2Fheads%2F{target.replace('/','%2F')}"
    return f"{bitbucket_host}/rest/default-reviewers/latest/projects/{project}/repos/repository/reviewers?{reviewer_query}"

def pull_request_body(title_and_description: str, from_branch: str, repository: str, project: str, target: str, reviewers: list) -> dict:
    """
    It creates a pull request from the branch `from_branch` to the branch `target` in the repository
    `repository` in the project `project` with the title and description `title_and_description` and the
    reviewers `reviewers`

    :param title_and_description: The title and description of the pull request
    :type title_and_description: str
    :param from_branch: The branch you want to merge from
    :type from_branch: str
    :param repository: The name of the repository you want to create the pull request in
    :type repository: str
    :param project: The project key of the project you want to create the pull request in
    :type project: str
    :param target: The branch you want to merge into
    :type target: str
    :param reviewers: list of reviewers
    :type reviewers: list
    :return: A dictionary of the payload to create a pull request.
    """
    """Payload to create pull request"""
    return json.dumps({
        "title": title_and_description,
        "description": title_and_description,
        "state": "OPEN",
        "open": "true",
        "closed": "false",
        "fromRef": {
            "id": 'refs/heads/' + from_branch,
            "repository": {
                "slug": repository,
                "name": repository,
                "project": {
                    "key": project
                }
            }
        },
        "toRef": {
            "id": 'refs/heads/' + target,
            "repository": {
                "slug": repository,
                "name": repository,
                "project": {
                    "key": project
                }
            }
        },
        "locked": "false",
        "reviewers": reviewers
    })

def pull_request_diffrence(bitbucket_host: str, project: str, repository: str, pr_number: int) -> str:
    """
    > Returns the diff API to check in a given pull request

    :param bitbucket_host: The hostname of your Bitbucket instance
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: The name of the repository
    :type repository: str
    :param pr_number: The pull request number
    :type pr_number: int
    :return: The diff API to check in a given pull request
    """
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{pr_number}/changes?start=0&limit=1000&changeScope=unreviewed"

def pull_request_info(bitbucket_host: str, project: str, repository: str, id: int) -> str:
    """
    It returns a URL for a Bitbucket pull request

    :param bitbucket_host: The hostname of your Bitbucket server
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: the name of the repository
    :type repository: str
    :param id: The ID of the pull request
    :type id: int
    :return: A string
    """
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{id}"

def pull_request_viewer(bitbucket_host: str, role: str) -> str:
    """
    It returns the api for either reviewer or author role.

    :param bitbucket_host: The hostname of your Bitbucket instance
    :type bitbucket_host: str
    :param role: The role of the user in the pull request. Can be either REVIEWER or AUTHOR
    :type role: str
    :return: A string
    """
    return f"{bitbucket_host}/rest/api/latest/inbox/pull-requests?role={role}&avatarSize=64"

def current_pull_request(bitbucket_host: str, project: str, repository: str) -> str:
    """
    It returns the URL of the current pull request

    :param bitbucket_host: The hostname of your Bitbucket server
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: the name of the repository
    :type repository: str
    :return: The URL for the current pull request.
    """
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos/{repository}/pull-requests"

def whoami(bitbucket_host: str) -> str:
    """
    It returns a string of who the current user is

    :param bitbucket_host: The hostname of your Bitbucket server
    :type bitbucket_host: str
    :return: The response is a JSON object with the following keys:
    """
    return f"{bitbucket_host}/plugins/servlet/applinks/whoami"

def action_pull_request(bitbucket_host: str, project: str, repository: str, target: int,user_id: str) -> str:
    """
    `action_pull_request` returns a URL to the Bitbucket API endpoint for a pull request participant

    :param bitbucket_host: The hostname of your Bitbucket server
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: the name of the repository
    :type repository: str
    :param target: the pull request id
    :type target: int
    :param user_id: The user id of the user you want to add to the pull request
    :type user_id: str
    :return: A list of all the pull requests for a given repository.
    """
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{target}/participants/{user_id}?avatarSize=32"

def pr_source_branch_delete_check(bitbucket_host: str, project: str, repository: str, id: int, delete_source_branch:str) -> str:
    """
    `pr_source_branch_delete_check` is a function that takes in a Bitbucket host, project, repository,
    pull request ID, and a boolean value for whether or not to delete the source branch, and returns a
    URL that can be used to check if the source branch can be deleted.

    :param bitbucket_host: The hostname of your Bitbucket server
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: the name of the repository
    :type repository: str
    :param id: The ID of the pull request you want to delete
    :type id: int
    :param delete_source_branch: true/false
    :type delete_source_branch: str
    :return: The response is a JSON object with the following fields:
    """
    return f"{bitbucket_host}/rest/pull-request-cleanup/latest/projects/{project}/repos/{repository}/pull-requests/{id}?deleteSourceRef={delete_source_branch}&retargetDependents={delete_source_branch}"

def validate_merge(bitbucket_host: str, project: str, repository: str, id: int) -> str:
    """
    It takes a Bitbucket host, a project, a repository, and a pull request ID, and returns a URL that
    can be used to validate the merge of the pull request

    :param bitbucket_host: The hostname of your Bitbucket server
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: the name of the repository
    :type repository: str
    :param id: The ID of the pull request
    :type id: int
    :return: The URL for the merge request.
    """
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{id}/merge"

def merge_config(bitbucket_host: str, project: str, repository: str) -> str:
    """
    It takes a Bitbucket host, a project, and a repository and returns a URL for the pull request
    settings of that repository

    :param bitbucket_host: The hostname of your Bitbucket instance
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: The name of the repository
    :type repository: str
    :return: The URL for the pull request settings for a given repository.
    """
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos/{repository}/settings/pull-requests"

def get_merge_info(bitbucket_host: str, project: str, repository: str, target_branch) -> str:
    """
    > This function returns the URL for the Bitbucket API endpoint that will return the merge info for a
    given branch

    :param bitbucket_host: The hostname of your Bitbucket instance
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: the name of the repository you want to merge into
    :type repository: str
    :param target_branch: The branch you want to merge into
    :return: The URL for the merge info
    """
    return f"{bitbucket_host}/rest/branch-utils/latest/projects/{project}/repos/{repository}/automerge/path/refs/heads/{target_branch}"

def pr_merge_body(project: str, repository: str, id: int, from_branch: str, target_branch: str) -> dict:
    """
    It takes the project, repository, pull request id, from branch, and target branch and returns a JSON
    object that contains the message to be used when merging the pull request

    :param project: The project name
    :type project: str
    :param repository: The name of the repository you want to merge the PR into
    :type repository: str
    :param id: The ID of the pull request
    :type id: int
    :param from_branch: The branch you want to merge into the target_branch
    :type from_branch: str
    :param target_branch: The branch you want to merge into
    :type target_branch: str
    :return: A dictionary with the key "autoSubject" and the value False, and the key "message" and the
    value "Merge pull request #{id} in {project}/{repository} from {from_branch} to {target_branch}"
    """
    return json.dumps({
        "autoSubject": False,
        "message": f"Merge pull request #{id} in {project}/{repository} from {from_branch} to {target_branch}"
    })

def pr_cleanup(bitbucket_host: str, project: str, repository: str, id: int) -> str:
    """
    It returns a URL for the Bitbucket REST API endpoint for the pull request cleanup plugin

    :param bitbucket_host: The hostname of your Bitbucket server
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: the name of the repository
    :type repository: str
    :param id: The ID of the pull request
    :type id: int
    :return: A list of all the pull requests for a given repository.
    """
    return f"{bitbucket_host}/rest/pull-request-cleanup/latest/projects/{project}/repos/{repository}/pull-requests/{id}"

def pr_cleanup_body(delete_source_branch: bool) -> dict:
    """
    It returns a dictionary that contains a JSON string that contains a dictionary that contains a
    boolean

    :param delete_source_branch: If true, the source branch will be deleted after the PR is merged
    :type delete_source_branch: bool
    :return: A dictionary with the key "deleteSourceRef" and the value of the delete_source_branch
    parameter.
    """
    return json.dumps({
        "deleteSourceRef": delete_source_branch ,
        "retargetDependents": True
    })

def pr_rebase(bitbucket_host: str, project: str, repository: str, id: int, version: int) -> list:
    """
    It returns a list of two elements, the first being a JSON string, and the second being a URL

    :param bitbucket_host: The hostname of your Bitbucket server
    :type bitbucket_host: str
    :param project: The project key
    :type project: str
    :param repository: the name of the repository
    :type repository: str
    :param id: The ID of the pull request
    :type id: int
    :param version: The version of the pull request
    :type version: int
    :return: A list of two elements. The first element is a JSON string that contains the version of the
    pull request. The second element is the URL to the pull request.
    """
    return [json.dumps({"version": version}), f"{bitbucket_host}/rest/git/latest/projects/{project}/repos/{repository}/pull-requests/{id}/rebase"]
