import pytest
import httpx
from bb.utils.request import get, post, put, delete


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
        post(url, "username", "password", data)


# def test_put_error():
#     url = "https://example.com"
#     data = {"key": "value"}
#     with pytest.raises(ValueError):
#         put(url, "username", "password", data)


def test_delete_error():
    url = "https://example.com"
    data = {"key": "value"}
    with pytest.raises(ValueError):
        delete(url, "username", "password", data)
