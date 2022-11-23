# -*- coding: utf-8 -*-
# pylint: disable=W0703

"""
    bb.utils.cp - copies the received url to clipboard
"""

import pyperclip as pc
from bb.utils.richprint import str_print


def copy_to_clipboard(url: str) -> None:
    """
    Copy the pull request to user clipboard for convenience
    """
    try:
        pc.copy(url)
        pc.paste()
        str_print(
            "Tip: Pull request url is copied to clipboard ('ctrl+v' to paste)",
            "dim white",
        )

    except Exception:  # Dosent work on VM's so we skip the exception if not available
        pass
