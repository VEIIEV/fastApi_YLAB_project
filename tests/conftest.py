import pytest
@pytest.fixture(scope='session')
def get_host():
    yield 'http://localhost:8000'

