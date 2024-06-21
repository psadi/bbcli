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
bb.utils.request - makes http requests

Defines functions for making HTTP requests (GET, POST, PUT, DELETE) with
error handling and status code interpretation.
"""

from http import HTTPStatus
from json import JSONDecodeError

import httpx

from bb.utils.constants import common_vars
from bb.utils.ini import is_config_present, parse
from bb.utils.richprint import str_print

if is_config_present():
    username, token, _ = parse()


def http_response_definitions(status_code: int) -> str:
    """
    Returns the HTTP response phrase for a given status code.

    Args:
        status_code (int): The HTTP status code.

    Returns:
        str: The HTTP response phrase corresponding to the status code.
             If the status code is not recognized, "Unknown Status Code" is returned.
    """
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Unknown Status Code"


def get(url: str) -> list[int, dict]:
    """
    Sends a GET request to the specified URL and returns the response status code and data.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        list[int, dict]: A list containing the response status code and data. The status code is an integer and the data is a dictionary.

    Raises:
        ValueError: If the request returns a non-200 status code.
    """

    with httpx.Client() as client:
        request = client.get(url, auth=(username, token), timeout=10.0)

    if request.status_code != 200:
        if request.status_code == 400:
            error_message = request.json().get("errors", [{}])[0].get("message", "")
            if "invalid" in error_message.lower():
                str_print(
                    f"Invalid input: {error_message}",
                    common_vars.dim_white,
                )
            else:
                str_print(
                    f"Error: {error_message}",
                    common_vars.dim_white,
                )
        else:
            str_print(
                f"Unexpected error occurred. Status code: {request.status_code}, Message: {http_response_definitions(request.status_code)}",
                common_vars.dim_white,
            )

        raise ValueError(
            f"\n[{request.status_code}] {http_response_definitions(request.status_code)}"
        )

    try:
        data: dict = request.json()
    except JSONDecodeError:
        data: str = request.content.decode()

    return [request.status_code, data]


def post(url: str, body: dict) -> list[int, dict]:
    """
    Send a POST request to the specified URL with the given body.

    Args:
        url (str): The URL to send the request to.
        body (dict): The request body as a dictionary.

    Returns:
        list[int, dict]: A list containing the status code and the response data as a dictionary.

    Raises:
        ValueError: If the request returns a status code other than 200, 201, 204, or 409.
    """
    with httpx.Client() as client:
        request = client.post(
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": common_vars.content_type},
            timeout=10.0,
        )

    if request.status_code not in (200, 201, 204, 409):
        raise ValueError(
            f"\n[{request.status_code}] {http_response_definitions(request.status_code)}"
        )

    json_data: dict = {} if request.status_code == 204 else request.json()
    return [request.status_code, json_data]


def put(url: str, body: dict) -> list[int, dict]:
    """
    Sends a PUT request to the specified URL with the given body.

    Args:
        url (str): The URL to send the request to.
        body (dict): The request body as a dictionary.

    Returns:
        list[int, dict]: A list containing the status code and the response body as a dictionary.

    Raises:
        ValueError: If the request returns a status code other than 200, 403, or 409.

    """
    with httpx.Client() as client:
        request = client.put(
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": common_vars.content_type},
            timeout=10.0,
        )

    if request.status_code not in (200, 403, 409):
        raise ValueError(
            f"\n[{request.status_code}] {http_response_definitions(request.status_code)}"
        )

    return [request.status_code, request.json()]


def delete(url: str, body: dict) -> int:
    """
    Sends a DELETE request to the specified URL with the given request body.

    Args:
        url (str): The URL to send the DELETE request to.
        body (dict): The request body to send along with the DELETE request.

    Returns:
        int: The status code of the DELETE request.

    Raises:
        ValueError: If the DELETE request returns a status code other than 202 or 204.

    """
    with httpx.Client() as client:
        request = client.request(
            "DELETE",
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": common_vars.content_type},
            timeout=10.0,
        )
    if request.status_code not in (202, 204):
        raise ValueError(
            f"\n[{request.status_code}] {http_response_definitions(request.status_code)}"
        )
    return request.status_code
