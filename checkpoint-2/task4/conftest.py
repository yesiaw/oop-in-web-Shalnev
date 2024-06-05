import pytest
from web_framework import WebFramework as API

@pytest.fixture
def create_api():
    return API()

@pytest.fixture
def create_client(create_api):
    return create_api.create_test_session()
