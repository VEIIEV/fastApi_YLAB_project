import asyncio
import os
from pathlib import Path

import httpx
import pytest
from dotenv import load_dotenv
from httpx import AsyncClient

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


@pytest.fixture(scope='session')
def get_host():
    yield 'http://' + os.getenv('HOST_FOR_TEST') + ':8000'
    print('session fixture finallized')


@pytest.fixture(scope='session')
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client


# нужно что бы области видимости фикстур нормально отрабатывали
@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
