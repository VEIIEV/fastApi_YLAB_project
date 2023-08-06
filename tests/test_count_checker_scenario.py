import requests
from requests import Response


def test_counter_scenario(get_host):
    url = get_host + '/api/v1/menus'
    body = {
        'title': 'My menu 1',
        'description': 'My menu description 1'
    }
    response_menu: Response = requests.post(url=url, json=body)
    assert response_menu.status_code == 201, 'check for menu creation status code'

    menu_id = response_menu.json()['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus'
    body = {
        'title': 'My submenu 1',
        'description': 'My submenu description 1'
    }
    response_submenu: Response = requests.post(url=url, json=body)
    assert response_submenu.status_code == 201, 'check for submenu creation status code'

    submenu_id = response_submenu.json()['id']
    url = get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id + '/dishes'
    body = {
        'title': 'My dish 1',
        'description': 'My dish description 1',
        'price': '12.50'
    }
    response_first_dish: Response = requests.post(url=url, json=body)
    assert response_first_dish.status_code == 201, 'check for first dish creation status code'

    body = {
        'title': 'My dish 2',
        'description': 'My dish description 2',
        'price': '7.33'
    }
    response_second_dish: Response = requests.post(url=url, json=body)
    assert response_second_dish.status_code == 201, 'check for first dish creation status code'

    checker_for_menu: Response = requests.get(get_host + '/api/v1/menus/' + menu_id)
    assert checker_for_menu.status_code == 200, 'check for counter with 1sub, 2dish'
    assert checker_for_menu.json()['submenus_count'] == 1
    assert checker_for_menu.json()['dishes_count'] == 2

    checker_for_submenu: Response = requests.get(url=get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id)
    assert checker_for_submenu.status_code == 200, 'check for counter with  2dish'
    assert checker_for_submenu.json()['dishes_count'] == 2

    requests.delete(url=get_host + '/api/v1/menus/' + menu_id + '/submenus/' + submenu_id)

    assert requests.get(response_menu.url).status_code == 200
    assert requests.get(response_submenu.url).status_code == 200
    checker_for_menu: Response = requests.get(get_host + '/api/v1/menus/' + menu_id)
    assert checker_for_menu.status_code == 200
    assert checker_for_menu.json()['submenus_count'] == 0, 'check for counter with emptiness'

    requests.delete(get_host + '/api/v1/menus/' + menu_id)
    assert requests.get(response_menu.url).json() == [], 'check clear db'
