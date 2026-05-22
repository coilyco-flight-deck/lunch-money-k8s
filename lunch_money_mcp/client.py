"""Lunch Money API client - token from SSM, thin httpx wrapper."""

import os
import time

import boto3
import httpx

API_BASE = "https://dev.lunchmoney.app/v1"
SSM_TOKEN_PATH = "/coilysiren/lunchmoney/api-token"
MAX_RETRIES = 5


def _load_token() -> str:
    """Token from LUNCH_MONEY_TOKEN env var, else an AWS SSM SecureString.

    The SSM path defaults to SSM_TOKEN_PATH, overridable with LUNCH_MONEY_SSM_PATH.
    """
    env = os.environ.get("LUNCH_MONEY_TOKEN")
    if env:
        return env
    ssm = boto3.client("ssm", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    path = os.environ.get("LUNCH_MONEY_SSM_PATH", SSM_TOKEN_PATH)
    resp = ssm.get_parameter(Name=path, WithDecryption=True)
    return resp["Parameter"]["Value"]


class LunchMoney:
    """Minimal Lunch Money v1 API client."""

    def __init__(self) -> None:
        token = _load_token()
        self._http = httpx.Client(
            base_url=API_BASE,
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0,
        )

    def _send(self, method: str, path: str, **kwargs):
        """Issue a request, backing off on 429 per the Retry-After header."""
        for attempt in range(MAX_RETRIES):
            resp = self._http.request(method, path, **kwargs)
            if resp.status_code == 429 and attempt < MAX_RETRIES - 1:
                wait = float(resp.headers.get("Retry-After", 2**attempt))
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        raise RuntimeError(f"{method} {path} still rate-limited after {MAX_RETRIES} retries")

    def _get(self, path: str, **params):
        clean = {k: v for k, v in params.items() if v is not None}
        return self._send("GET", path, params=clean)

    def _put(self, path: str, payload: dict) -> dict:
        return self._send("PUT", path, json=payload)

    def _post(self, path: str, payload: dict) -> dict:
        return self._send("POST", path, json=payload)

    def transactions(self, start_date: str, end_date: str) -> list[dict]:
        data = self._get("/transactions", start_date=start_date, end_date=end_date)
        return data.get("transactions", [])

    def categories(self) -> list[dict]:
        return self._get("/categories").get("categories", [])

    def budgets(self, start_date: str, end_date: str) -> list[dict]:
        return self._get("/budgets", start_date=start_date, end_date=end_date)

    def create_category(
        self, name: str, is_income: bool = False, exclude_from_totals: bool = False
    ) -> dict:
        return self._post(
            "/categories",
            {
                "name": name,
                "is_income": is_income,
                "exclude_from_budget": False,
                "exclude_from_totals": exclude_from_totals,
            },
        )

    def set_category(self, transaction_id: int, category_id: int) -> dict:
        return self._put(
            f"/transactions/{transaction_id}",
            {"transaction": {"category_id": category_id}},
        )
