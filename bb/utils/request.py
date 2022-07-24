#-*- coding: utf-8 -*-

# This is importing the requests library, the echo function from typer, and the Exit function from
# typer.
import httpx
import requests
from typer import echo
from typer import Exit

def http_response_definitions(status_code: int) -> str:
    """
    HTTP response code validator

    :param status_code: The HTTP response code you want to validate
    :type status_code: int
    :return: The value of the key that matches the status code.
    """
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
    It makes a get request to the url, with the username and token as authentication.

    :param url: The URL of the API endpoint you want to call
    :type url: str
    :param username: The username of the user you want to use to access the API
    :type username: str
    :param token: The token you generated in the previous step
    :type token: str
    :return: The statecode and output as json
    """
    with httpx.Client() as client:
        request = client.get(url, auth=(username, token), timeout=10)
    if request.status_code == 200:
        return [request.status_code, request.json()]
    elif request.status_code == 400:
        echo(f"{request.status_code} - {request.json()['errors'][0]['message']}")
        raise Exit(code=1)
    else:
        echo(f"\n{request.status_code} - {http_response_definitions(request.status_code)}")
        raise Exit(code=1)

def post_request(url: str, username: str, token: str, body: dict) -> list:
    """
    > This function makes a POST request to the specified URL, using the specified username and token
    for authentication, and the specified body as the request body

    :param url: The URL of the API endpoint you're trying to access
    :type url: str
    :param username: The username of the user you want to use to make the request
    :type username: str
    :param token: The token you generated in the previous step
    :type token: str
    :param body: dict
    :type body: dict
    :return: A list of the status code and the json response.
    """
    with httpx.Client() as client:
        request = client.post(url, auth=(username, token), data=body, headers={
                      "content-type": "application/json;charset=UTF-8"})
    if request.status_code not in (200, 201, 204, 409):
        echo(f"\n{request.status_code} - {http_response_definitions(request.status_code)}")
        raise Exit(code=1)

    return [request.status_code, request.json()]


def put_request(url: str, username: str, token: str, body: dict) -> list:
    """
    > This function makes a PUT request to the specified URL with the specified username and token, and
    returns the status code and response body as a list

    :param url: The URL of the API endpoint you're trying to access
    :type url: str
    :param username: The username of the user you want to authenticate as
    :type username: str
    :param token: The token you got from the previous step
    :type token: str
    :param body: dict
    :type body: dict
    :return: A list containing the status code and the json response.
    """
    with httpx.Client() as client:
        request = client.put(url, auth=(username, token), data=body, headers={
                      "content-type": "application/json;charset=UTF-8"})
    if request.status_code != 200:
        echo(f"\n{request.status_code} - {http_response_definitions(request.status_code)}")
        raise Exit(code=1)
    return [request.status_code, request.json()]


def delete_request(url: str, username: str, token: str, body: dict) -> int:
    """
    > This function sends a DELETE request to the specified URL with the specified username and token,
    and returns the HTTP status code

    :param url: The URL of the API endpoint you want to hit
    :type url: str
    :param username: The username of the user you want to authenticate as
    :type username: str
    :param token: The token you generated in the previous step
    :type token: str
    :param body: dict
    :type body: dict
    :return: The status code of the request.
    """
    # with httpx.Client() as client:
    request = requests.delete(url, auth=(username, token), data=body, headers={
    "content-type": "application/json;charset=UTF-8"})
    if request.status_code != 204:
        echo(f"\n{request.status_code} - {http_response_definitions(request.status_code)}")
        raise Exit(code=1)
    return request.status_code
