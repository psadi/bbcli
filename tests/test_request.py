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

import json
from unittest.mock import MagicMock, patch

import pytest

from bb.utils.request import delete, get, http_response_definitions, post, put


def test_http_response_definitions():
    assert http_response_definitions(200) == "OK"
    assert http_response_definitions(999) == "Unknown Status Code"


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_get_success(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_client.get.return_value = mock_response

    status, data = get("https://example.com")
    assert status == 200
    assert data == {"success": True}


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_get_success_content(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
    mock_response.content = b"some string content"
    mock_client.get.return_value = mock_response

    status, data = get("https://example.com")
    assert status == 200
    assert data == "some string content"


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_get_400_invalid(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"errors": [{"message": "invalid input"}]}
    mock_client.get.return_value = mock_response

    with pytest.raises(ValueError):
        get("https://example.com")


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_get_400_other(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"errors": [{"message": "some other error"}]}
    mock_client.get.return_value = mock_response

    with pytest.raises(ValueError):
        get("https://example.com")


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_get_500(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.get.return_value = mock_response

    with pytest.raises(ValueError):
        get("https://example.com")


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_post_success(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"id": 1}
    mock_client.post.return_value = mock_response

    status, data = post("https://example.com", {"key": "value"})
    assert status == 201
    assert data == {"id": 1}


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_post_success_204(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_client.post.return_value = mock_response

    status, data = post("https://example.com", {"key": "value"})
    assert status == 204
    assert data == {}


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_post_error(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.post.return_value = mock_response

    with pytest.raises(ValueError):
        post("https://example.com", {"key": "value"})


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_put_success(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"updated": True}
    mock_client.put.return_value = mock_response

    status, data = put("https://example.com", {"key": "value"})
    assert status == 200
    assert data == {"updated": True}


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_put_error(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.put.return_value = mock_response

    with pytest.raises(ValueError):
        put("https://example.com", {"key": "value"})


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_delete_success(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_client.request.return_value = mock_response

    status = delete("https://example.com", {"key": "value"})
    assert status == 204


@patch("bb.utils.request._get_client")
@patch("bb.utils.request._get_auth")
def test_delete_error(mock_get_auth, mock_get_client):
    mock_get_auth.return_value = ("user", "token")
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_client.request.return_value = mock_response

    with pytest.raises(ValueError):
        delete("https://example.com", {"key": "value"})


@patch("bb.utils.request._get_auth")
def test_get_no_auth(mock_get_auth):
    import bb.utils.request as request_module

    mock_get_auth.return_value = None
    mock_client = MagicMock()
    request_module._client = mock_client
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}
    mock_client.get.return_value = mock_response

    status, data = get("https://example.com")
    assert status == 200
    assert data == {"success": True}


def test_get_client_reuse():
    import bb.utils.request as request_module

    client1 = request_module._get_client()
    client2 = request_module._get_client()
    assert client1 is client2


def test_get_client_creates_new():
    import bb.utils.request as request_module

    request_module._client = None
    client = request_module._get_client()
    assert client is not None


@patch("bb.utils.ini.is_config_present")
@patch("bb.utils.ini.parse")
def test_get_auth_no_config(mock_parse, mock_is_present):
    import bb.utils.ini as ini_module
    import bb.utils.request as request_module

    ini_module._config_cache = None
    mock_is_present.return_value = False
    auth = request_module._get_auth()
    assert auth is None


@patch("bb.utils.ini.is_config_present")
@patch("bb.utils.ini.parse")
def test_get_auth_with_config(mock_parse, mock_is_present):
    import bb.utils.ini as ini_module
    import bb.utils.request as request_module

    ini_module._config_cache = None
    mock_is_present.return_value = True
    mock_parse.return_value = ["user", "token", "host"]
    auth = request_module._get_auth()
    assert auth == ("user", "token")
