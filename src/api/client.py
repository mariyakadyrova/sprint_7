import allure
import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = self._url(path)

        with allure.step(f"{method} {path}"):
            resp = self.session.request(method=method, url=url, timeout=15, **kwargs)


            try:
                allure.attach(str(kwargs.get("json") or kwargs.get("data")), "request_body", allure.attachment_type.TEXT)
            except Exception:
                pass

            allure.attach(f"status={resp.status_code}\n{resp.text}", "response", allure.attachment_type.TEXT)
            return resp
