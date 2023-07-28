import decimal
import json

from starlette.testclient import TestClient
from httpx import Response
from python_code.main import app
from python_code.models.dish_model import Dish

client = TestClient(app)


class Mes:
    message: str

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return {'message': self.message}


def test_ping():
    response: Response = client.get('/')
    assert response.status_code == 200
    ob = Mes(**response.json())
    assert isinstance(ob, type(Mes()))
    assert ob.__str__() == {"message": "Hello World"}


def test_create_dish():
    content = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50"
    }
    content = json.dumps(content)
    response: Response = client.post(
        '/api/v1/menus/d7cb2206-bc41-4b05-8b55-08180951a7db/submenus/d7cb2206-bc41-4b05-8b55-08180951a7db/dishes',
        content=content)

    assert response.status_code == '201'


def test_check_dish_existence():
    response: Response = client.get("/check/dish/title")
    assert isinstance(response.json(), type(Dish))
