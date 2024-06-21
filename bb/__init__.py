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
bb: a cli for bitbucket.
"""

import typer

from bb.__version__ import __version__ as version
from bb.auth import _auth
from bb.pr import _pr
from bb.repo import _repo
from bb.utils.constants import common_vars
from bb.utils.richprint import console


def version_callback(value: bool) -> None:
    """
    Prints the version of bb and exits the program if the value is True.

    Parameters:
        value (bool): A boolean value indicating whether to print the version or not.

    Returns:
        None
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
    This function is a callback function that sets the verbosity level and version information.

    Args:
        verbose (bool, optional): A boolean indicating whether to enable verbose mode. Defaults to False.
        version (bool, optional): A boolean indicating whether to display the version information. Defaults to None.

    Returns:
        None
    """
    if verbose:
        common_vars.state["verbose"] = True
