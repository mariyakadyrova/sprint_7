import allure
import pytest

from src.api import endpoints
from src.api.helpers import safe_json


def base_order_payload():
    return {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-02-02",
        "comment": "Saske, come back to Konoha",
    }


@allure.feature("Orders")
@allure.story("Create order")
class TestOrdersCreate:

    @pytest.mark.parametrize(
        "color_value",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None,   # цвет не указан
        ],
    )
    def test_create_order_with_color_variants_returns_track(self, client, color_value):
        payload = base_order_payload()
        if color_value is not None:
            payload["color"] = color_value

        resp = client.request("POST", endpoints.ORDERS_CREATE, json=payload)
        assert resp.status_code == 201

        body = safe_json(resp) or {}
        assert "track" in body
        assert isinstance(body["track"], int)
