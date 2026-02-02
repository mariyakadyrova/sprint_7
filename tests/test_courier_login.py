import allure
import pytest

from src.api.helpers import login_courier, safe_json


@allure.feature("Courier")
@allure.story("Login courier")
class TestCourierLogin:

    def test_courier_can_login_and_returns_id(self, client, courier_credentials):
        login, password, _ = courier_credentials
        resp = login_courier(client, login, password)

        assert resp.status_code == 200
        body = safe_json(resp) or {}
        assert "id" in body
        assert isinstance(body["id"], int)

    @pytest.mark.parametrize(
        "payload",
        [
            {"login": "some_login"},                 # нет password
            {"password": "some_password"},           # нет login
            {},                                      # ничего нет
        ],
    )
    def test_login_requires_all_required_fields(self, client, payload):
        resp = client.request("POST", "/api/v1/courier/login", json=payload)
        assert resp.status_code == 400

        body = safe_json(resp) or {}
        assert "message" in body

    def test_login_fails_with_wrong_password(self, client, courier_credentials):
        login, password, _ = courier_credentials
        resp = login_courier(client, login, password + "x")

        assert resp.status_code in (400, 404)
        body = safe_json(resp) or {}
        assert "message" in body

    def test_login_fails_for_nonexistent_user(self, client):
        resp = login_courier(client, "no_such_user_123", "no_such_pass_123")

        assert resp.status_code in (400, 404)
        body = safe_json(resp) or {}
        assert "message" in body
