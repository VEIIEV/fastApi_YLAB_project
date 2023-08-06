import pytest
import requests
from requests import Response

# чекер, если меню ещё не создано, то создаем и сохраняем его
# если создано, то используем, без создания очередного меню
MENU = None


@pytest.fixture(scope='module')
def create_menu_for_test(get_host):
    global MENU
    if MENU:
        return MENU
    else:
        url = get_host + '/api/v1/menus'
        body = {
            'title': 'My menu 1',
            'description': 'My menu description 1'
        }
        response: Response = requests.post(url=url, json=body)
        MENU = response.json()
    yield MENU
    url = url + '/' + MENU['id']
    requests.delete(url)
    print('create_menu_for_test fixture finalized')


@pytest.fixture()
def create_submenu_for_test(get_host, create_menu_for_test):
    # создаем сабменю
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus'
    body = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response: Response = requests.post(url=url, json=body)
    yield response.json()
    # удаляем сабменю
    url = url + '/' + response.json()['id']
    requests.delete(url)
    print('create_submenu_for_test fixture finalized')


# Положительные тесты

def test_get_all_submenu(get_host, create_menu_for_test):
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus'
    print(url)
    response: Response = requests.get(url=url)
    assert response.status_code == 200, 'check for status code'


def test_get_submenu_by_id(get_host, create_menu_for_test, create_submenu_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id
    print(url)
    response: Response = requests.get(url=url)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'


def test_create_submenu(get_host, create_menu_for_test):
    # создаем субменю
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus'
    body = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response: Response = requests.post(url=url, json=body)
    assert response.status_code == 201, 'check for status code'
    assert response.json()['title'] == body['title'], 'check for retrieved submenu(title) accordance'
    assert response.json()['description'] == body['description'], 'check for retrieved submenu(description) accordance'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'
    # удаляем сабменю
    url = url + '/' + response.json()['id']
    requests.delete(url)


def test_update_submenu_by_id(get_host, create_menu_for_test, create_submenu_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id
    body = {
        'title': 'My submenu 1',
        'description': 'updated description'
    }
    response: Response = requests.patch(url=url, json=body)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['description'] == body['description'], 'check for retrieved submenu(description) accordance'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'


def test_delete_submenu_by_id(get_host, create_menu_for_test, create_submenu_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id
    response: Response = requests.delete(url=url)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['message'] == 'The submenu has been deleted', 'checking for message content'
