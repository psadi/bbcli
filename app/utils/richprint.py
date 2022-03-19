#-*- coding: utf-8 -*-
""""
    app.utils.richprint
"""
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

console = Console ()

def to_console(header_args: dict, value_args: dict, show_header: bool) -> None:
    """Pretty print to console as a table"""
    table = Table(show_header=show_header, header_style="bold cyan")

    for key, value in header_args.items():
        table.add_column(str(key))

    for key, value in value_args.items():
        table.add_row(str(key),str(value))

    console.print(table)

def markdown_to_console(mark_down: str) -> None:
    """Prettry print markdown to console"""
    mark_down = Markdown(mark_down)
    console.print(mark_down)

def traceback_to_console(*args, **kwargs):
    console.print_exception(max_frames=1, show_locals=True)
