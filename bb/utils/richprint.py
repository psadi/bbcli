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
bb.utils.richprint - uses py rich api to pretty print information to console
"""

import sys

from rich.columns import Columns
from rich.console import Console, Group
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from bb.utils.constants import common_vars

# Setting up the console.
console = Console()


def str_print(text: str, style: str) -> None:
    """
    Prints the given text with the specified style.

    Args:
        text (str): The text to be printed.
        style (str): The style to be applied to the text.

    Returns:
        None
    """
    _text = Text(text)
    _text.stylize(style)
    console.print(_text)


def table(header_args: list, value_args: list, show_header: bool) -> Table:
    """
    Generate a rich table using the provided header arguments and value arguments.

    Args:
        header_args (list): A list of tuples containing the column names and styles for the table header.
        value_args (list): A list of tuples containing the row values for the table.
        show_header (bool): A boolean value indicating whether to show the table header.

    Returns:
        Table: A rich Table object representing the generated table.
    """
    _table = Table(show_header=show_header, header_style="bold #2684FF", highlight=True)

    if show_header:
        for i in header_args:
            _table.add_column(str(i[0]), style=str(i[1]))

    for i in value_args:
        _table.add_row(*i)

    return _table


def traceback_to_console():
    """
    Prints the traceback to the console.

    This function uses the `print_exception` method of the `console` object to print the traceback to the console.
    The `show_locals` parameter is set to False to exclude local variables from the printed traceback.
    An extra line is added after the traceback for better readability.
    """
    console.print_exception(show_locals=False, extra_lines=1)


def live_progress(message: str):
    """
    Creates a live progress indicator with a given message.

    Args:
        message (str): The message to be displayed alongside the progress indicator.

    Returns:
        Live: A Live object representing the live progress indicator.

    """
    is_utf8 = sys.stdout.encoding.lower() == "utf-8"
    spin_type = "dots" if is_utf8 else "simpleDots"
    return Live(
        Columns([Spinner(spin_type, style=common_vars.bold_white), message]),
        refresh_per_second=24,
    )


def render_tree(repo_name: str, status: str, data: dict[str, list[tuple]]) -> None:
    """
    Renders a tree structure representing the repository and its status.

    Args:
        repo_name (str): The name of the repository.
        status (str): The status of the repository.
        data (dict[str, list[tuple]]): A dictionary containing the data to be rendered.

    Returns:
        None
    """
    tree = Tree("Root", highlight=True, hide_root=True)
    tree_root = tree.add(
        f"[bold #2684FF]{repo_name}", guide_style=common_vars.bold_white
    )
    containers_node = tree_root.add(
        f"[bold #2684FF]{status}", guide_style=common_vars.bold_white
    )
    containers_node.expanded = True
    for _ in zip(data.keys(), data.values()):
        containers_node.add(Group(f"PR: #{_[0]}", table(_[1], _[1], False)))
    console.print(tree)
