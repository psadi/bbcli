# -*- coding: utf-8 -*-
# pylint: disable=W0613

"""
    bb.utils.richprint - uses py rich api to pretty print information to console
"""

import sys
from rich.console import Console, Group
from rich.table import Table
from rich.spinner import Spinner
from rich.columns import Columns
from rich.live import Live
from rich.text import Text
from rich.tree import Tree

# Setting up the console.
console = Console()

bold_white: str = "bold white"


def str_print(text: str, style: str) -> None:
    """
    Sytlize text with rich Text lib and output to console
    """
    _text = Text(text)
    _text.stylize(style)
    console.print(_text)


def table(header_args: list, value_args: list, show_header: bool) -> Table:
    """
    Pretty print to console as a table
    The function takes three arguments:

    - `header_args`: a dictionary of header arguments
    - `value_args`: a dictionary of value arguments
    - `show_header`: a boolean to show the header
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
    It prints the traceback to the console
    """
    console.print_exception()


def live_progress(message: str):
    """
    It takes a string and returns a Live object that displays a spinner and the string
    """
    is_utf8 = sys.stdout.encoding.lower() == "utf-8"
    spin_type = "dots" if is_utf8 else "simpleDots"
    return Live(
        Columns([Spinner(spin_type, style=bold_white), message]),
        refresh_per_second=20,
    )


def render_tree(repo_name: str, status: str, header: list, data: list) -> None:
    """
    utilised by bb show, catagorize pr's based on state and render a tree
    """
    tree = Tree("Root", highlight=True, hide_root=True)
    tree_root = tree.add(f"[bold #2684FF]{repo_name}", guide_style=bold_white)
    containers_node = tree_root.add(f"[bold #2684FF]{status}", guide_style=bold_white)
    containers_node.expanded = True
    for _ in data:
        containers_node.add(Group("Pull Request Details", table(header, _, True)))
    console.print(tree)
