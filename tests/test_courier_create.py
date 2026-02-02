import allure
import pytest

from src.api.helpers import make_courier_payload, create_courier, safe_json


@allure.feature("Courier")
@allure.story("Create courier")
class TestCourierCreate:

    def test_courier_can_be_created(self, created_courier):
        payload, resp = created_courier

        assert resp.status_code == 201
        body = safe_json(resp)
        assert body == {"ok": True}

    def test_cannot_create_two_identical_couriers(self, client):
        payload = make_courier_payload()

        resp1 = create_courier(client, payload)
        assert resp1.status_code == 201

        resp2 = create_courier(client, payload)
        from src.api.constants import COURIER_DUPLICATE_ERROR

        assert resp2.status_code == 409  # ожидаем конфликт

        body = safe_json(resp2) or {}
        assert body.get("message") == COURIER_DUPLICATE_ERROR

    # проверяем, что пришла ошибка

    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_requires_all_required_fields(self, client, missing_field):
        payload = make_courier_payload()
        payload.pop(missing_field)

        resp = create_courier(client, payload)
        assert resp.status_code == 400

        body = safe_json(resp) or {}
        assert "message" in body
