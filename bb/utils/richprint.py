#-*- coding: utf-8 -*-

# Importing the rich library and setting up the console.
import sys
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.table import Table
from rich.spinner import Spinner
from rich.columns import Columns
from rich.live import Live
from rich.text import Text
from rich.tree import Tree

# Setting up the console.
console = Console ()

def str_print(text: str, style: str) -> None:
    _text = Text(text)
    _text.stylize(style)
    console.print(_text)

def table(header_args: list, value_args: list, show_header: bool) -> None:
    """
    > Pretty print to console as a table

    The function takes three arguments:

    - `header_args`: a dictionary of header arguments
    - `value_args`: a dictionary of value arguments
    - `show_header`: a boolean to show the header

    The function returns `None`

    :param header_args: A dictionary of the header names and their styles
    :type header_args: dict
    :param value_args: This is the data that you want to display in the table
    :type value_args: dict
    :param show_header: If True, the header will be shown
    :type show_header: bool
    """
    _table = Table(show_header=show_header, header_style="bold #2684FF", highlight=True)

    if show_header:
        for i in header_args:
            _table.add_column(str(i[0]), style=str(i[1]))

    for i in value_args:
        _table.add_row(*i)

    return _table

def markdown_to_console(mark_down: str) -> None:
    """
    `Prettry print markdown to console`

    And here's a longer description:

    > This function takes a markdown string and prints it to the console

    :param mark_down: str
    :type mark_down: str
    """
    mark_down = Markdown(mark_down)
    console.print(mark_down)

def traceback_to_console(*args, **kwargs):
    """
    It prints the traceback to the console
    """
    console.print_exception(max_frames=1, show_locals=True)

# def spinner_progress(message: str) -> tuple:
#     """
#     It returns a Columns object that contains a Spinner object and a message

#     :param message: The message to display next to the spinner
#     :type message: str
#     :return: A tuple of a Columns object with a Spinner object and a message string.
#     """
#     return

def live_progress(message: str):
    """
    It takes a string and returns a Live object that displays a spinner and the string

    :param message: The message to display
    :type message: str
    :return: A Live object with a spinner_progress function
    """
    is_utf8 = sys.stdout.encoding.lower() == "utf-8"
    spin_type = "dots" if is_utf8 else "simpleDots"
    return Live(
        Columns([Spinner(spin_type, style="bold white"), message]),
        refresh_per_second=20
    )

def render_tree(repo_name: str, status: str, header: list, data: list):
    tree = Tree("Root", highlight=True, hide_root=True)
    tree_root = tree.add(f"[bold #2684FF]{repo_name}", guide_style="bold white")
    # tree_root.add(Group(status))
    # tree_root.add(Group(to_console(hf"eader, data, False)))
    containers_node = tree_root.add(
        f"[bold #2684FF]{status}", guide_style="bold white"
    )
    containers_node.expanded = True

    containers_node.add(Group("Pull Request Details", table(header, data, True)))
    console.print(tree)