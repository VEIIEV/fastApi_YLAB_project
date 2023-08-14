import pytest
from httpx import AsyncClient, Response

# чекер, если меню ещё не создано, то создаем и сохраняем его
# если создано, то используем, без создания очередного меню
MENU = None


@pytest.fixture(scope='module')
async def create_menu_for_test(get_host, async_client: AsyncClient):
    global MENU
    url = get_host + '/api/v1/menus'
    if not MENU:
        body = {
            'title': 'My menu 1',
            'description': 'My menu description 1'
        }
        response: Response = await async_client.post(url=url, json=body)
        MENU = response.json()
    print(MENU)
    yield MENU
    url = url + '/' + MENU['id']
    await async_client.delete(url)


@pytest.fixture(scope='function')
async def create_submenu_for_test(get_host, create_menu_for_test, async_client: AsyncClient):
    # создаем сабменю
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/dishes'
    body = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response: Response = await async_client.post(url=url, json=body)
    print(response)
    yield response.json()
    # удаляем сабменю
    url = url + '/' + response.json()['id']
    await async_client.delete(url)


# Положительные тесты

async def test_get_all_submenu(get_host, create_menu_for_test, async_client: AsyncClient):
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/dishes'
    print(url)
    response: Response = await async_client.get(url=url)
    assert response.status_code == 200, 'check for status code'


async def test_get_submenu_by_id(get_host, create_menu_for_test, create_submenu_for_test, async_client: AsyncClient):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/dishes/' + submenu_id
    print(url)
    response: Response = await async_client.get(url=url)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'


async def test_create_submenu(get_host, create_menu_for_test, async_client: AsyncClient):
    # создаем субменю
    menu_id = create_menu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/dishes'
    body = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response: Response = await async_client.post(url=url, json=body)
    assert response.status_code == 201, 'check for status code'
    assert response.json()['title'] == body['title'], 'check for retrieved submenu(title) accordance'
    assert response.json()['description'] == body['description'], 'check for retrieved submenu(description) accordance'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'
    # удаляем сабменю
    url = url + '/' + response.json()['id']
    await async_client.delete(url)


async def test_update_submenu_by_id(get_host, create_menu_for_test, create_submenu_for_test, async_client: AsyncClient):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/dishes/' + submenu_id
    body = {
        'title': 'My submenu 1',
        'description': 'updated description'
    }
    response: Response = await async_client.patch(url=url, json=body)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['description'] == body['description'], 'check for retrieved submenu(description) accordance'
    assert response.json()['dishes_count'] is not None, 'check for  "dishes_count" field existence'


async def test_delete_submenu_by_id(get_host, create_menu_for_test, create_submenu_for_test, async_client: AsyncClient):
    menu_id = create_menu_for_test['id']
    submenu_id = create_submenu_for_test['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/dishes/' + submenu_id
    response: Response = await async_client.delete(url=url)
    assert response.status_code == 200, 'check for status code'
    assert response.json()['message'] == 'The submenu has been deleted', 'checking for message content'
