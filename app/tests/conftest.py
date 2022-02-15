import pytest
import os

from main import create_app
from requests.auth import _basic_auth_str

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def header():
    API_USERNAME = os.getenv('LOWDEFY_SECRET_API_USERNAME', '')
    API_PASSWORD = os.getenv('LOWDEFY_SECRET_API_PASSWORD', '')

    return {
        'Authorization': _basic_auth_str(API_USERNAME, API_PASSWORD)
    }

@pytest.fixture
def client(app):
    return app.test_client()