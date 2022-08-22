# -*- coding: utf-8 -*-

# This is importing the requests library, the echo function from typer, and the Exit function from
# typer.

import json
import requests
from typer import echo
from typer import Exit


def http_response_definitions(status_code: int) -> str:
    """
    HTTP response code validator
    """
    reponse_code_mapping = {
        100: "Continue",
        101: "Switching Protocols",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Time-out",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Request Entity Too Large",
        414: "Request-URI Too Large",
        415: "Unsupported Media Type",
        416: "Requested range not satisfiable",
        417: "Expectation Failed",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Time-out",
        505: "HTTP Version not supported",
    }

    return reponse_code_mapping[status_code]


def get(url: str, username: str, token: str) -> list:
    """
    It makes a get request to the url, with the username and token as authentication.

    """
    with requests.Session() as client:
        response = client.get(url, auth=(username, token), timeout=10)
        if response.status_code == 200:
            response_data = response.json()
        else:
            response_data = json.dumps(
                {"message": http_response_definitions(response.status_code)}
            )
    return [response.status_code, response.json()]


def post(url: str, username: str, token: str, body: dict) -> list:
    """
    This function makes a POST request to the specified URL, using the specified username and token
    for authentication, and the specified body as the request body
    """
    with requests.Session() as client:
        response = client.post(
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": "application/json;charset=UTF-8"},
        )
    if response.status_code not in (200, 201, 204, 409):
        response_data = response.json()
    else:
        response_data = json.dumps(
            {"message": http_response_definitions(response.status_code)}
        )
    return [response.status_code, response.json()]


def put(url: str, username: str, token: str, body: dict) -> list:
    """
    This function makes a PUT request to the specified URL with the specified username and token, and
    returns the status code and response body as a list
    """
    with requests.Session() as client:
        client.put
        response = client.put(
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": "application/json;charset=UTF-8"},
        )
    if response.status_code != 200:
        echo(
            f"\n{response.status_code} - {http_response_definitions(response.status_code)}"
        )
        raise Exit(code=1)
    return [response.status_code, response.json()]


def delete(url: str, username: str, token: str, body: dict) -> int:
    """
    This function sends a DELETE request to the specified URL with the specified username and token,
    and returns the HTTP status code
    """
    with requests.Session() as client:
        response = client.delete(
            url,
            auth=(username, token),
            data=body,
            headers={"content-type": "application/json;charset=UTF-8"},
        )
    if response.status_code != 204:
        echo(
            f"\n{response.status_code} - {http_response_definitions(response.status_code)}"
        )
        raise Exit(code=1)
    return response.status_code
