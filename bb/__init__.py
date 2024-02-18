# -*- coding: utf-8 -*-
"""
bb: a cli for bitbucket.
"""

import typer

from bb.__version__ import __version__ as version
from bb.auth import _auth
from bb.pr import _pr
from bb.repo import _repo
from bb.utils.helper import state
from bb.utils.richprint import console


def version_callback(value: bool) -> None:
    """
    Prints the version of bb and exits the program.
    """
    if value:
        console.print(f"bb version: {version}")
        raise typer.Exit(code=0)


def setup() -> typer.Typer:
    _bb = typer.Typer(
        add_completion=False,
        epilog="Source Code: https://github.com/psadi/bbcli",
        help="Work seamlessly with Bitbucket from the command line.",
        no_args_is_help=True,
    )

    _bb.add_typer(_pr, name="pr", help="Manage pull requests")
    _bb.add_typer(_auth, name="auth", help="Authenticate bb and git with Bitbucket")
    _bb.add_typer(_repo, name="repo", help="Work with BitBucket repositories")

    return _bb


_bb = setup()


@_bb.callback()
def callback(
    verbose: bool = False,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    """
    Entry point for the bb CLI. Handles global flags like --verbose and --version.
    """
    if verbose:
        state["verbose"] = True
