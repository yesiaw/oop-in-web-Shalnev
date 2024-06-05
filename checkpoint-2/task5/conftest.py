import pytest
from api import API

@pytest.fixture
def client():
    return API().test_session()
