import allure

from src.api import endpoints
from src.api.helpers import safe_json


@allure.feature("Orders")
@allure.story("Orders list")
class TestOrdersList:

    def test_orders_list_returns_list(self, client):
        resp = client.request("GET", endpoints.ORDERS_LIST)
        assert resp.status_code == 200

        body = safe_json(resp) or {}
        assert "orders" in body
        assert isinstance(body["orders"], list)
