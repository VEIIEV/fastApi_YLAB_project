import os
from pathlib import Path

import pytest
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope='session')
def get_host():
    yield 'http://' + os.getenv('HOST_FOR_TEST') + ':8000'
