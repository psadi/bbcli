#-*- coding: utf-8 -*-
""""
    app.utils.richprint
"""
from rich.console import (
    Console,
    Text
)
from rich.markdown import Markdown
from rich.table import Table
from rich.spinner import Spinner
from rich.columns import Columns
from rich.live import Live

console = Console ()
text = Text()
live = Live()

def to_console(header_args: dict, value_args: dict, show_header: bool) -> None:
    """Pretty print to console as a table"""
    table = Table(show_header=show_header, header_style="bold #2684FF", highlight=True)

    for key, value in header_args.items():
        table.add_column(str(key), style=str(value))

    for key, value in value_args.items():
        table.add_row(str(key),str(value))

    console.print(table)

def markdown_to_console(mark_down: str) -> None:
    """Prettry print markdown to console"""
    mark_down = Markdown(mark_down)
    console.print(mark_down)

def traceback_to_console(*args, **kwargs):
    console.print_exception(max_frames=1, show_locals=True)

def spinner_progress(message: str) -> tuple:
    return Columns(
        [Spinner('dots', style="bold white"), message]
    )

def live_progress(message: str):
    return Live(spinner_progress(message), refresh_per_second=4)
