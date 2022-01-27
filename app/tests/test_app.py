import pytest

def test_app(client):
    assert client.get("/").data.find(b"App-version") >= 0