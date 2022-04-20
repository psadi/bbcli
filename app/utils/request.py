#-*- coding: utf-8 -*-
""""
    app.utils.request
"""

import requests
from typer import echo
from typer import Exit

def http_response_definitions(status_code: int) -> str:
    """"HTTP response code validator"""
    reponse_code_mapping =  {
        100 : "Continue",
        101 : "Switching Protocols",
        200 : "OK",
        201 : "Created",
        202 : "Accepted",
        203 : "Non-Authoritative Information",
        204 : "No Content",
        205 : "Reset Content",
        206 : "Partial Content",
        300 : "Multiple Choices",
        301 : "Moved Permanently",
        302 : "Found",
        303 : "See Other",
        304 : "Not Modified",
        305 : "Use Proxy",
        307 : "Temporary Redirect",
        400 : "Bad Request",
        401 : "Unauthorized",
        402 : "Payment Required",
        403 : "Forbidden",
        404 : "Not Found",
        405 : "Method Not Allowed",
        406 : "Not Acceptable",
        407 : "Proxy Authentication Required",
        408 : "Request Time-out",
        409 : "Conflict",
        410 : "Gone",
        411 : "Length Required",
        412 : "Precondition Failed",
        413 : "Request Entity Too Large",
        414 : "Request-URI Too Large",
        415 : "Unsupported Media Type",
        416 : "Requested range not satisfiable",
        417 : "Expectation Failed",
        500 : "Internal Server Error",
        501 : "Not Implemented",
        502 : "Bad Gateway",
        503 : "Service Unavailable",
        504 : "Gateway Time-out",
        505 : "HTTP Version not supported"
    }

    for key, value in reponse_code_mapping.items():
        if key == status_code:
            return value

def get_response(url: str, username: str, token: str) -> list:
    """
        get request method, needs the url, username and token
        returns the statecode and output as json
    """
    request = requests.get(url, auth=(username, token), timeout=10)
    if request.status_code == 200:
        return [request.status_code, request.json()]
    elif request.status_code == 400:
        echo(f"\u274C {request.status_code} - {request.json()['errors'][0]['message']}")
        raise Exit(code=1)
    else:
        echo(f"\n\u274C {request.status_code} - {http_response_definitions(request.status_code)}")
        raise Exit(code=1)

def post_request(url: str, username: str, token: str, body: dict) -> list:
    """
        post request method, needs the url, body, username and token
        returns the statecode and output as json
    """
    request = requests.post(url, auth=(username, token), data=body, headers={
                      "content-type": "application/json;charset=UTF-8"})
    if request.status_code in (200, 201, 409):
        return [request.status_code, request.json()]
    elif request.status_code == 204:
        return request.status_code
    else:
        echo(f"\n\u274C {request.status_code} - {http_response_definitions(request.status_code)}")
        raise Exit(code=1)

def put_request(url: str, username: str, token: str, body: dict) -> list:
    """
        post request method, needs the url, body, username and token
        returns the statecode and output as json
    """
    request = requests.put(url, auth=(username, token), data=body, headers={
                      "content-type": "application/json;charset=UTF-8"})
    if request.status_code == 200:
        return [request.status_code, request.json()]
    else:
        echo(f"\n\u274C {request.status_code} - {http_response_definitions(request.status_code)}")
        raise Exit(code=1)

def delete_request(url: str, username: str, token: str, body: dict) -> int:
    """
        delete request method, needs the url, body, username and token
        returns the statecode and output as json
    """
    request = requests.delete(url, auth=(username, token), data=body, headers={
        "content-type": "application/json;charset=UTF-8"})
    if request.status_code == 204:
        return request.status_code
    else:
        echo(f"\n\u274C  {request.status_code} - {http_response_definitions(request.status_code)}")
        raise Exit(code=1)
