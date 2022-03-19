#-*- coding: utf-8 -*-
""""
    app.scripts.diff
"""
from app.utils import request
from app.utils import iniparser
from app.utils import richprint

def show_diff(url: str) -> None:
    """
        display the diff from remote pull request to the console
        applicable for create and delete actions
    """

    username, token, bitbucket_host = iniparser.parse()
    response = request.get_response(url, username, token)[1]['values']

    header = {
        "TYPE": ['dim'],
        "CONTENT": ['dim']
    }

    value_args = {}

    for i in response:
        value_args.update({i['type'] : i['path']['toString']})

    richprint.to_console(header, value_args, True)
