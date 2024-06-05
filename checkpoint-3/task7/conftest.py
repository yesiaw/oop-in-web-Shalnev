import pytest

from api import API

@pytest.fixture
def api() -> API:
    return API()

@pytest.fixture
def client(api: API):
    return api.test_session()
