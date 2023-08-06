import pytest
import requests
from _pytest.fixtures import FixtureRequest
from requests import Response

# пример написания тестов с помощью библиотек  starlette, httpx
# from starlette.testclient import TestClient
# from httpx import Response
# from python_code.main import app
# client = TestClient(app)
# def test_ping():
#     response: Response = client.get('/')
#     assert response.status_code == 200
#     ob = Mes(**response.json())
#     assert isinstance(ob, type(Mes()))
#     assert ob.__str__() == {"message": "Hello World"}


@pytest.fixture(scope='function')
def create_menu_for_test(get_host):
    url = get_host + '/api/v1/menus'
    body = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response: Response = requests.post(url=url, json=body)
    yield response.json()
    url = url + '/' + response.json()['id']
    requests.delete(url)
    print('create_menu_for_test fixture finalized')


# Положительные тесты
def test_get_all_menu(get_host):
    url = get_host + '/api/v1/menus'
    response: Response = requests.get(url=url)
    assert response.status_code == 200, 'check for status code'


def test_get_menu_by_id(get_host, create_menu_for_test):
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id
    response: Response = requests.get(url=url)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['id'] == create_menu_for_test['id'], 'check for retrieved menu(id) accordance'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'
    assert response.json()['submenus_count'] is not None, 'check for  "submenus_count" field existence'


def test_create_menu(get_host, request: FixtureRequest):
    url = get_host + '/api/v1/menus'
    body = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response: Response = requests.post(url=url, json=body)
    assert response.status_code == 201, 'check for status code'
    assert response.json()['title'] == body['title'], 'check for retrieved menu(id) accordance'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'
    assert response.json()['submenus_count'] is not None, 'check for  "submenus_count" field existence'

    url = get_host + '/api/v1/menus/' + response.json()['id']
    requests.delete(url)


def test_update_menu_by_id(get_host, create_menu_for_test):
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id
    body = {
        'title': 'My menu 2',
        'description': 'updated description'
    }
    response: Response = requests.patch(url, json=body)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['description'] == body['description'], 'check for retrieved menu(id) accordance'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'
    assert response.json()['submenus_count'] is not None, 'check for  "submenus_count" field existence'


def test_delete_menu_by_id(get_host, create_menu_for_test):
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id
    response: Response = requests.delete(url)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['message'] == 'The menu has been deleted', 'checking for message content'
