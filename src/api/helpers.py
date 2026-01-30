import random
import string
from typing import Dict, Optional

from src.api import endpoints


def _rand_str(n: int = 10) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(n))


def make_courier_payload() -> Dict[str, str]:
    return {
        "login": _rand_str(10),
        "password": _rand_str(10),
        "firstName": _rand_str(10),
    }


def safe_json(resp):
    try:
        return resp.json()
    except Exception:
        return None


def create_courier(client, payload: Dict[str, str]):
    # Важно: в requests лучше отправлять json=payload, а не data=payload
    return client.request("POST", endpoints.COURIER_CREATE, json=payload)


def login_courier(client, login: str, password: str):
    return client.request("POST", endpoints.COURIER_LOGIN, json={"login": login, "password": password})


def delete_courier_best_effort(client, courier_id: Optional[int]):
    """
    В учебном API удаление иногда отличается реализацией.
    Мы делаем best-effort: если ручка есть — удалим, если нет — не завалим тест.
    """
    if not courier_id:
        return

    path = endpoints.COURIER_DELETE_BY_ID.format(courier_id=courier_id)
    try:
        client.request("DELETE", path)
    except Exception:
        # cleanup не должен ломать тест-ран
        pass
