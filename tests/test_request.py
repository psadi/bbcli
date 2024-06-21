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

import httpx
import pytest

from bb.utils.request import delete, post


@pytest.fixture
def client():
    with httpx.Client() as client:
        yield client


def test_get(client):
    url = "https://example.com"
    response = client.get(url)
    assert response.status_code == 200


def test_post(client):
    url = "https://example.com"
    data = {"key": "value"}
    response = client.post(url, json=data)
    assert response.status_code == 200


def test_post_error():
    url = "https://example.com"
    data = {"key": "value"}
    with pytest.raises(ValueError):
        post(url, data)


# def test_put_error():
#     url = "https://example.com"
#     data = {"key": "value"}
#     with pytest.raises(ValueError):
#         put(url, data)


def test_delete_error():
    url = "https://example.com"
    data = {"key": "value"}
    with pytest.raises(ValueError):
        delete(url, data)
