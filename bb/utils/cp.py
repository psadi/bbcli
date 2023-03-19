# -*- coding: utf-8 -*-

"""
    bb.utils.cp - copies the received url to clipboard
"""

import tkinter as tk
from bb.utils.richprint import str_print


def copy_to_clipboard(url: str) -> None:
    """
    Copy the pull request to user clipboard for convenience
    """
    try:
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(url)
        root.update()  # required for clipboard to be updated
        str_print(
            "Tip: Pull request url is copied to clipboard ('ctrl+v' to paste)",
            "dim white",
        )
    except tk.TclError:
        # Dosent work on VM's so we skip the exception if not available
        pass
