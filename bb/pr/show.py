# -*- coding: utf-8 -*-

# Importing the modules from the bb.utils package.
from typer import Exit

from bb.utils import api, cmnd, iniparser, request, richprint


def to_richprint(repo_name: str, pr_repo_dict: dict, header: dict) -> None:
    """
    This function takes in a repository name, a dictionary of pull requests, and a header dictionary
    and prints the data to the console
    """
    for status, data in pr_repo_dict.items():
        richprint.render_tree(repo_name, status, header, data)


def show_pull_request(role: str, all: bool) -> None:
    """
    Shows the list of pull requests authored and pull requests reviewing
    """

    username, token, bitbucket_host = iniparser.parse()
    if role == "current":
        project, repository = cmnd.base_repo()
        request_url = api.current_pull_request(bitbucket_host, project, repository)
    else:
        request_url = api.pull_request_viewer(bitbucket_host, role)

    with richprint.live_progress(f"Fetching Pull Requests ({role}) ..."):
        response = request.get(request_url, username, token)
    repository = cmnd.base_repo()[1]

    repo_dict = {}
    if (response[0]) == 200 and (len(response[1]["values"]) > 0):
        for pr in response[1]["values"]:
            repo = f"{pr['fromRef']['repository']['slug']}"
            if repo not in repo_dict.keys():
                repo_dict.update({repo: {}})
                if pr["state"] not in repo_dict[repo].values():
                    repo_dict.update({repo: {pr["state"]: []}})
            _list = []
            _list.append(("Tittle", pr["title"]))
            _list.append(("From Branch", pr["fromRef"]["displayId"]))
            _list.append(("To Branch", pr["toRef"]["displayId"]))
            _list.append(("URL", pr["links"]["self"][0]["href"]))
            repo_dict[repo][pr["state"]].append(_list)

        header = [("SUMMARY", "yellow"), ("DESCRIPTION", "white")]

        for repo_name, pr_repo_dict in repo_dict.items():
            if repo_name.lower() == repository.lower() and not all:
                to_richprint(repo_name, pr_repo_dict, header)
            elif all:
                to_richprint(repo_name, pr_repo_dict, header)
            else:
                raise Exit(code=0)
