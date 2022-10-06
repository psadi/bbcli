# -*- coding: utf-8 -*-

import pyperclip as pc


def copy_to_clipboard(url: str) -> None:
    """
    Copy the pull request to user clipboard for convenience
    """
    try:
        pc.copy(url)
        pc.paste()
    except Exception:  # Dosent work on VM's so we skip the exception if not available
        pass
