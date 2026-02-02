import os
import pytest

from src.api.client import ApiClient
from src.api.helpers import (
    make_courier_payload,
    create_courier,
    login_courier,
    safe_json,
    delete_courier_best_effort,
)

BASE_URL = os.getenv("SCOOTER_BASE_URL", "https://qa-scooter.praktikum-services.ru")


@pytest.fixture()
def client():
    return ApiClient(BASE_URL)


@pytest.fixture()
def created_courier(client):
    payload = make_courier_payload()
    create_resp = create_courier(client, payload)

    yield payload, create_resp

    # получаем id через логин и удаляем
    courier_id = None
    login_resp = login_courier(client, payload.get("login"), payload.get("password"))
    if login_resp.status_code == 200:
        courier_id = (safe_json(login_resp) or {}).get("id")

    delete_courier_best_effort(client, courier_id)
