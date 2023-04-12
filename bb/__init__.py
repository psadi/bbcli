# -*- coding: utf-8 -*-
"""
bb: a cli for bitbucket.
"""

import typer

from bb import __version__
from bb.auth import _auth
from bb.pr import _pr
from bb.repo import _repo
from bb.utils.richprint import console
from bb.utils.validate import state


def setup() -> typer.Typer:
    _bb = typer.Typer(
        add_completion=False, epilog="Source Code: https://github.com/psadi/bbcli"
    )

    _bb.add_typer(_pr, name="pr", help="Manage pull requests")
    _bb.add_typer(_auth, name="auth", help="Authenticate bb and git with Bitbucket")
    _bb.add_typer(_repo, name="repo", help="Work with BitBucket repositories")

    return _bb


_bb = setup()


def version_callback(value: bool) -> None:
    """
    returns the docstring of the current module (`__doc__`)
    and exits the program.
    """
    if value:
        console.print(f"bb version: {__version__.__version__}")
        typer.Exit(code=0)


@_bb.callback()
def callback(
    verbose: bool = False,
    version: bool = typer.Option(None, "--version", callback=version_callback),
):
    """
    Work seamlessly with Bitbucket from the command line.
    """
    if verbose:
        state["verbose"] = True
