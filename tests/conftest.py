import pytest
@pytest.fixture(scope='session')
def get_host():
    yield 'http://host.docker.internal:8000'

