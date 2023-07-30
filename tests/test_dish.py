import pytest

import requests
from requests import Response

# чекер -> если меню ещё не создано, то создаем и сохраняем его
# если создано, то используем, без создания очередного меню
MENU = None
SUBMENU = None


@pytest.fixture(scope='module')
def create_menu_for_test(get_host):
    global MENU
    if MENU:
        return MENU
    else:
        url = get_host + '/api/v1/menus'
        body = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response: Response = requests.post(url=url, json=body)
        MENU = response.json()
        yield MENU
        url = url + '/' + MENU['id']
        requests.delete(url)


@pytest.fixture(scope='module')
def create_submenu_for_test(get_host, create_menu_for_test):
    global SUBMENU
    if SUBMENU:
        return SUBMENU
    else:
        menu_id = create_menu_for_test['id']
        url = get_host + '/api/v1/menus/' + menu_id + '/submenus'
        body = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response: Response = requests.post(url=url, json=body)
        SUBMENU = response.json()
    yield SUBMENU
    url = url + '/' + SUBMENU['id']
    requests.delete(url)


@pytest.fixture()
def create_dish_for_test(get_host, create_menu_for_test, create_submenu_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    body = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    response: Response = requests.post(url=url, json=body)
    yield response.json()
    url = url + '/' + response.json()['id']
    requests.delete(url)


def test_get_all_dishes(get_host, create_menu_for_test, create_submenu_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    response: Response = requests.get(url=url)
    assert response.status_code == 200, "check for status code"


def test_get_dish_by_id(get_host,
                        create_menu_for_test,
                        create_submenu_for_test,
                        create_dish_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    dish_id = create_dish_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id + '/dishes/' + dish_id
    response: Response = requests.get(url=url)
    assert response.status_code == 200, "check for status code"


def test_create_dish(get_host, create_menu_for_test, create_submenu_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    body = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    response: Response = requests.post(url=url, json=body)
    assert response.status_code == 201, "check for status code"
    assert response.json()['title'] == body['title'], 'check for retrieved submenu(title) accordance'
    assert response.json()['description'] == body['description'], 'check for retrieved submenu(description) accordance'
    # кста, этот тест нашёл ошибку, оказывается у меня округлялись значения в большую строну где-то
    assert response.json()['price'] == body['price'], 'check for retrieved submenu(price) accordance'
    url = url + '/' + response.json()['id']
    requests.delete(url)


def test_update_dish(get_host, create_menu_for_test, create_submenu_for_test, create_dish_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    dish_id = create_dish_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id + '/dishes/' + dish_id
    body = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    response: Response = requests.patch(url=url, json=body)
    assert response.status_code == 200, "check for status code"
    assert response.json()['title'] == body['title'], 'check for retrieved submenu(title) accordance'
    assert response.json()['description'] == body['description'], 'check for retrieved submenu(description) accordance'
    assert response.json()['price'] == body['price'], 'check for retrieved submenu(price) accordance'


def test_delete_dish(get_host, create_menu_for_test, create_submenu_for_test, create_dish_for_test):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    dish_id = create_dish_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id + '/dishes/' + dish_id
    response: Response = requests.delete(url=url)
    assert response.status_code == 200, "check for status code"
    assert response.json()['message'] == "The dish has been deleted", 'checking for message content'
