# -*- coding: utf-8 -*-
"""
bb: a cli for bitbucket.
"""

import typer
from bb.pr import _pr
from bb.auth import _auth
from bb.repo import _repo
from bb.utils.validate import state
from bb.utils.richprint import console
from bb import __version__

_bb = typer.Typer(
    add_completion=False,
    epilog="Source Code: https://github.com/psadi/bbcli",
)


def version_callback(value: bool) -> None:
    """
    returns the docstring of the current module (`__doc__`)
    and exits the program.
    """
    if value:
        console.print(f"bb version: {__version__.__version__}")
        raise typer.Exit(code=0)


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


_bb.add_typer(_pr, name="pr", help="Manage pull requests")
_bb.add_typer(
    _auth,
    name="auth",
    help="Authenticate bb and git with Bitbucket",
)
_bb.add_typer(_repo, name="repo", help="Work with BitBucket repositories")
