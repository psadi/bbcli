#-*- coding: utf-8 -*-
"""
bbcli: a comman line utility that can manage pull requests in bitbucket.
"""

from enum import Enum
from typing import List, Optional
import typer
from app import __doc__
from app.scripts.create import create_pull_request
from app.scripts.delete import delete_pull_request
from app.scripts.test import validate
from app.scripts.show import show_pull_request
from app.scripts.review import review_pull_request
from app.scripts.merge import merge_pull_request
from app.scripts.diff import get_diff_url
from app.utils import command
from app.utils.richprint import traceback_to_console, console

app = typer.Typer()
state = {"verbose": False}

def version_callback(value: bool):
    if value: 
        console.print(__doc__)
        raise typer.Exit()

@app.callback()
def callback(
    verbose: bool = False,
    version: Optional[bool] = typer.Option(None, "--version", callback=version_callback)
):
    """
    run: "bb docs --help" for more information
    """
    if verbose: state["verbose"] = True


@app.command()
def create(
    target: str = typer.Option("", help="target branch name"),
    yes: bool  = typer.Option(False, help="skip yes/no prompt"),
    diff: bool  = typer.Option(False, help="show diff after raising pull request")
):
    """create pull request"""
    try:
        if command.is_git_repo() is True:
            if not target:
                target = typer.prompt("Target Branch")
            create_pull_request(target, yes, diff)
        else:
            typer.echo("\u274C Not a git repository")
            typer.Exit(code=1)
    except Exception:
        if state['verbose']: traceback_to_console(Exception)

@app.command()
def delete(
    id: Optional[List[int]] = typer.Option(None, help="pull request number(s) to delete"),
    yes: bool  = typer.Option(False, help="skip yes/no prompt"),
    diff: bool  = typer.Option(False, help="show diff before deleting pull request")
):
    """delete pull request(s) by id(s)"""
    try:
        if command.is_git_repo() is True:
            if not id:
                id = typer.prompt("Pull request number(s)")
            delete_pull_request(id, yes, diff)
        else:
            typer.echo("\u274C Not a git repository")
            typer.Exit(code=1)
    except Exception:
        if state['verbose']: traceback_to_console(Exception)

class Role(str, Enum):
    """roles choice enum"""
    author = "author"
    reviewer = "reviewer"
    current = "current"
    # participant = "participant"

@app.command()
def show(
    role: Role = Role.current.value,
    all: bool = typer.Option(False, help="show all pull request(s) based on selected role")
):
    #TO-DO: patterns: str   = typer.Option("repository patterrns, absolute (or) regex")
    """show pull request(s) authored & reviewing"""
    try:
        if command.is_git_repo() is True:
            show_pull_request(role.value, all)
        else:
            typer.echo("\u274C Not a git repository")
            typer.Exit(code=1)
    except Exception:
        if state['verbose']: traceback_to_console(Exception)

@app.command()
def test():
    """validate setup, if any issues found manual setup will be prompted"""
    try:
        validate()
    except Exception:
        if state['verbose']: traceback_to_console(Exception)

class Action(str, Enum):
    """review enum choices"""
    approve = "approve"
    unapprove = "unapprove"
    needs_work = "needs_work"
    none = "none"

@app.command()
def review(
    id: int = typer.Option("", help="pull request number to review"),
    action: Action = Action.none.value
):
    """review pull request by id"""
    try:
        if action.value != 'none':
            review_pull_request(id, action.value)
        else:
            typer.echo("Action cannot be none")
            raise(typer.Exit(code=1))
    except Exception:
        if state['verbose']: traceback_to_console(Exception)

@app.command()
def merge(
    id: int = typer.Option("", help="pull request number to merge"),
    deleteSourceBranch: bool = typer.Option(False, help="deletes source branch after merge")
):
    try:
        merge_pull_request(id, deleteSourceBranch)
    except Exception:
        if state['verbose']: traceback_to_console(Exception)

@app.command()
def merge(
    id: int = typer.Option("", help="pull request number to merge"),
    delete_source_branch: bool = typer.Option(False, help="deletes source branch after merge"),
    rebase: bool = typer.Option(False, help="rebase source branch with target before merge"),
    yes: bool  = typer.Option(False, help="skip yes/no prompt")
):
    """merge pull request by id"""
    try:
        merge_pull_request(id, delete_source_branch, rebase, yes)
    except Exception:
        if state['verbose']: traceback_to_console(Exception)

@app.command()
def diff(
    id: int = typer.Option("", help="pull request number to show diff"),
):
    """merges pull request by id"""
    try:
        get_diff_url(id)
    except Exception:
        if state['verbose']: traceback_to_console(Exception)