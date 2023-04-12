# -*- coding: utf-8 -*-

"""
    bb.utils.request - makes http requests
"""

from http import HTTPStatus
from json import JSONDecodeError

import httpx

from bb.utils.richprint import str_print

content_type: str = "application/json;charset=UTF-8"


def http_response_definitions(status_code: int) -> str:
    """
    HTTP response code validator
    """
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Unknown Status Code"


def get(url: str, username: str, token: str) -> list:
    """
    It makes a get request to the url, with the username and token as authentication.
    """
    with httpx.Client() as client:
        request = client.get(url, auth=(username, token))

    if request.status_code != 200:
        if request.status_code == 400:
            str_print(f"Message: {request.json()['errors'][0]['message']}", "dim white")

        raise ValueError(
            f"\n[{request.status_code}] {http_response_definitions(request.status_code)}"
        )

    try:
        data: dict = request.json()
    except JSONDecodeError:
        data: str = request.content.decode()

    return [request.status_code, data]


def post(url: str, username: str, token: str, body: dict) -> list:
    """
    This function makes a POST request to the specified URL, using the specified username and token
    for authentication, and the specified body as the request body

    """
    with httpx.Client() as client:
        request = client.post(
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": content_type},
        )

    if request.status_code not in (200, 201, 204, 409):
        raise ValueError(
            f"\n[{request.status_code}] {http_response_definitions(request.status_code)}"
        )

    if request.status_code == 204:
        json_data: dict = {}
    else:
        json_data: dict = request.json()

    return [request.status_code, json_data]


def put(url: str, username: str, token: str, body: dict) -> list:
    """
    This function makes a PUT request to the specified URL
    with the specified username and token and returns the status code
    and response body as a list
    """
    with httpx.Client() as client:
        request = client.put(
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": content_type},
        )
    if request.status_code != 200:
        raise ValueError(
            f"\n[{request.status_code}] {http_response_definitions(request.status_code)}"
        )
    return [request.status_code, request.json()]


def delete(url: str, username: str, token: str, body: dict) -> int:
    """
    This function sends a DELETE request to the specified URL with the specified username and token,
    and returns the HTTP status code
    """
    with httpx.Client() as client:
        request = client.request(
            "DELETE",
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": content_type},
        )
    if request.status_code != 204:
        raise ValueError(
            f"\n[{request.status_code}] {http_response_definitions(request.status_code)}"
        )
    return request.status_code
