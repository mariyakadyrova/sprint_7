import os
import pytest

from src.api.client import ApiClient
from src.api.helpers import (
    make_courier_payload, create_courier, login_courier,
    safe_json, delete_courier_best_effort
)

BASE_URL = os.getenv("SCOOTER_BASE_URL", "https://qa-scooter.praktikum-services.ru")


@pytest.fixture()
def client():
    return ApiClient(BASE_URL)


@pytest.fixture()
def courier_credentials(client):
    """
    Создаёт курьера перед тестом и удаляет после.
    Возвращает (login, password, firstName).
    """
    payload = make_courier_payload()
    resp = create_courier(client, payload)

    # если вдруг не создался ^_^ тест падает
    assert resp.status_code == 201, f"Failed to create courier: {resp.status_code} {resp.text}"

    yield payload["login"], payload["password"], payload["firstName"]

    # удалить можно только зная id т е  получаем его через логин
    login_resp = login_courier(client, payload["login"], payload["password"])
    courier_id = None
    if login_resp.status_code == 200:
        body = safe_json(login_resp) or {}
        courier_id = body.get("id")

    delete_courier_best_effort(client, courier_id)
