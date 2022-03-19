#-*- coding: utf-8 -*-
""""
    app.utils.api
"""
import json

def test(bitbucket_host: str) -> str:
    """API string to validate connection, checks user inbox"""
    return f"{bitbucket_host}/rest/api/latest/inbox/pull-requests/count"

def pull_request_create(bitbucket_host: str, project: str, repository: str) -> str:
    """Returns the pull request API to create pull requests"""
    return f"{bitbucket_host}/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests"

def get_repo_info(bitbucket_host: str, project: str) -> str:
    """Returns the project repository information"""
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos?start=0&limit=10000"

def default_reviewers(bitbucket_host: str, project: str, repo_id: str, from_branch: str, target: str) -> str:
    """Retuens the api to validate default reviewrs in a repository"""
    reviewer_query = f"avatarSize=32&sourceRepoId={repo_id}&sourceRefId=refs%2Fheads%2F{from_branch.replace('/','%2F')}&targetRepoId={repo_id}&targetRefId=refs%2Fheads%2F{target.replace('/','%2F')}"
    return f"{bitbucket_host}/rest/default-reviewers/latest/projects/{project}/repos/repository/reviewers?{reviewer_query}"

def pull_request_body(title_and_description: str, from_branch: str, repository: str, project: str, target: str, reviewers: list) -> dict:
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
    """Retuens the diff API to check in a given pull request"""
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{pr_number}/changes?start=0&limit=1000&changeScope=unreviewed"

def pull_request_delete(bitbucket_host: str, project: str, repository: str, target: str) -> str:
    """Retuens the api to delete pull request"""
    return f"{bitbucket_host}/rest/api/latest/projects/{project}/repos/{repository}/pull-requests/{target}"

def pull_request_viewer(bitbucket_host: str, role: str) -> str:
    """Returns api for either reviewer or author role"""
    return f"{bitbucket_host}/rest/api/latest/inbox/pull-requests?role={role}&avatarSize=64&withAttributes=true&state=OPEN&order=oldest"
