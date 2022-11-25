# -*- coding: utf-8 -*-

"""
    bb.pr.show lists all pr is current repo
    can also show all pr's authored/revewing either in current repo
    or all repos
"""

from bb.utils import api, cmnd, iniparser, request, richprint


def to_richprint(repo_name: str, pr_repo_dict: dict, header: list) -> None:
    """
    This function takes in a repository name, a dictionary of pull requests, and a header dictionary
    and prints the data to the console
    """
    for status, data in pr_repo_dict.items():
        richprint.render_tree(repo_name, status, header, data)


def construct_repo_dict(role_info: list) -> dict:
    """
    parses the role info (reviewer/author), constructs a dict that can be sent to
    richprint tree view
    """
    repo_dict: dict = {}
    if (role_info[0]) == 200 and (len(role_info[1]["values"]) > 0):
        for _pr in role_info[1]["values"]:
            repo = f"{_pr['fromRef']['repository']['slug']}"
            if repo not in repo_dict:
                repo_dict.update({repo: {}})
                if _pr["state"] not in repo_dict[repo].values():
                    repo_dict.update({repo: {_pr["state"]: []}})
            _list = [
                ("Tittle", _pr["title"]),
                (
                    "Description",
                    _pr["description"] if "description" in _pr.keys() else "-",
                ),
                ("From Branch", _pr["fromRef"]["displayId"]),
                ("To Branch", _pr["toRef"]["displayId"]),
                ("URL", _pr["links"]["self"][0]["href"]),
            ]
            repo_dict[repo][_pr["state"]].append(_list)
    return repo_dict


def show_pull_request(role: str, _all: bool) -> None:
    """
    Shows the list of pull requests authored and pull requests reviewing
    """
    username, token, bitbucket_host = iniparser.parse()
    project, repository = cmnd.base_repo()
    request_url = api.current_pull_request(bitbucket_host, project, repository)
    if role != "current":
        request_url = api.pull_request_viewer(bitbucket_host, role)

    with richprint.live_progress(f"Fetching Pull Requests ({role}) ..."):
        role_info: list = request.get(request_url, username, token)
        repo_dict: dict = construct_repo_dict(role_info)
        header = [("SUMMARY", "yellow"), ("DESCRIPTION", "white")]

        for repo_name, pr_repo_dict in repo_dict.items():
            if repo_name.lower() == repository.lower() and not _all:
                to_richprint(repo_name, pr_repo_dict, header)
                break

            to_richprint(repo_name, pr_repo_dict, header)
