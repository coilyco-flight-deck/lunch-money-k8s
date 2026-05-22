"""Lunch Money API client - v1 and v2, token from env or SSM, thin httpx wrapper."""

import os
import time

import boto3
import httpx

# v1 is the stable public beta. v2 is open alpha, recommended for new projects.
API_BASES = {
    "v1": "https://dev.lunchmoney.app/v1",
    "v2": "https://api.lunchmoney.dev/v2",
}
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


def _resolve_api() -> tuple[str, str]:
    """Pick API version and base URL from env. v1 unless LUNCH_MONEY_API_VERSION=v2."""
    version = os.environ.get("LUNCH_MONEY_API_VERSION", "v1").lower()
    if version not in API_BASES:
        version = "v1"
    base = os.environ.get("LUNCH_MONEY_API_BASE", API_BASES[version])
    return version, base


class LunchMoney:
    """Lunch Money API client. Defaults to v1; v2 is selectable and best-effort."""

    def __init__(self) -> None:
        self.version, base = _resolve_api()
        token = _load_token()
        self._http = httpx.Client(
            base_url=base,
            headers={"Authorization": f"Bearer {token}"},
            timeout=30.0,
        )

    # v2 renamed two resource paths. Everything else shares the v1 path shape.
    @property
    def _assets_path(self) -> str:
        return "/manual_accounts" if self.version == "v2" else "/assets"

    @property
    def _budgets_path(self) -> str:
        return "/summary" if self.version == "v2" else "/budgets"

    def _send(self, method: str, path: str, **kwargs):
        """Issue a request, backing off on 429 per the Retry-After header."""
        for attempt in range(MAX_RETRIES):
            resp = self._http.request(method, path, **kwargs)
            if resp.status_code == 429 and attempt < MAX_RETRIES - 1:
                wait = float(resp.headers.get("Retry-After", 2**attempt))
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json() if resp.content else {}
        raise RuntimeError(f"{method} {path} still rate-limited after {MAX_RETRIES} retries")

    def _get(self, path: str, **params):
        return self._send("GET", path, params={k: v for k, v in params.items() if v is not None})

    def _put(self, path: str, payload: dict) -> dict:
        return self._send("PUT", path, json=payload)

    def _post(self, path: str, payload: dict) -> dict:
        return self._send("POST", path, json=payload)

    def _delete(self, path: str, **params) -> dict:
        return self._send("DELETE", path, params={k: v for k, v in params.items() if v})

    def _get_list(self, path: str, **params) -> list:
        """GET an endpoint that returns a bare JSON array."""
        data = self._get(path, **params)
        return data if isinstance(data, list) else []

    @staticmethod
    def _unwrap(data, *keys: str) -> list:
        """Pull the list out of a wrapped response, tolerating v1/v2 key names."""
        if isinstance(data, list):
            return data
        for key in keys:
            if isinstance(data, dict) and isinstance(data.get(key), list):
                return data[key]
        return []

    # --- user ---
    def me(self) -> dict:
        return self._get("/me")

    # --- categories ---
    def categories(self) -> list[dict]:
        return self._unwrap(self._get("/categories"), "categories")

    def category(self, category_id: int) -> dict:
        return self._get(f"/categories/{category_id}")

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

    def create_category_group(self, name: str, category_ids: list[int]) -> dict:
        return self._post("/categories/group", {"name": name, "category_ids": category_ids})

    def add_to_category_group(self, group_id: int, category_ids: list[int]) -> dict:
        return self._post(f"/categories/group/{group_id}/add", {"category_ids": category_ids})

    def update_category(self, category_id: int, fields: dict) -> dict:
        return self._put(f"/categories/{category_id}", fields)

    def delete_category(self, category_id: int, force: bool = False) -> dict:
        suffix = "/force" if force else ""
        return self._delete(f"/categories/{category_id}{suffix}")

    # --- tags ---
    def tags(self) -> list:
        return self._get_list("/tags")

    # --- transactions ---
    def transactions(self, start_date: str, end_date: str, **filters) -> list[dict]:
        data = self._get("/transactions", start_date=start_date, end_date=end_date, **filters)
        return self._unwrap(data, "transactions")

    def transaction(self, transaction_id: int) -> dict:
        return self._get(f"/transactions/{transaction_id}")

    def insert_transactions(self, transactions: list[dict], **options) -> dict:
        payload = {"transactions": transactions}
        payload.update({k: v for k, v in options.items() if v is not None})
        return self._post("/transactions", payload)

    def update_transaction(self, transaction_id: int, fields: dict) -> dict:
        return self._put(f"/transactions/{transaction_id}", {"transaction": fields})

    def split_transaction(self, transaction_id: int, splits: list[dict]) -> dict:
        return self._put(f"/transactions/{transaction_id}", {"split": splits})

    def unsplit_transactions(self, parent_ids: list[int]) -> dict:
        return self._post("/transactions/unsplit", {"parent_ids": parent_ids})

    def set_category(self, transaction_id: int, category_id: int) -> dict:
        return self.update_transaction(transaction_id, {"category_id": category_id})

    def transaction_group(self, transaction_id: int) -> dict:
        return self._get("/transactions/group", transaction_id=transaction_id)

    def create_transaction_group(self, payload: dict) -> dict:
        return self._post("/transactions/group", payload)

    def delete_transaction_group(self, transaction_id: int) -> dict:
        return self._delete(f"/transactions/group/{transaction_id}")

    # --- recurring ---
    def recurring_items(self, start_date: str, end_date: str) -> list:
        return self._get_list("/recurring_items", start_date=start_date, end_date=end_date)

    # --- budgets (v2: /summary) ---
    def budgets(self, start_date: str, end_date: str) -> list:
        return self._get_list(self._budgets_path, start_date=start_date, end_date=end_date)

    def upsert_budget(
        self, start_date: str, category_id: int, amount: float, currency: str
    ) -> dict:
        return self._put(
            self._budgets_path,
            {
                "start_date": start_date,
                "category_id": category_id,
                "amount": amount,
                "currency": currency,
            },
        )

    def remove_budget(self, start_date: str, category_id: int) -> dict:
        return self._delete(self._budgets_path, start_date=start_date, category_id=category_id)

    # --- assets / manual accounts (v2: /manual_accounts) ---
    def assets(self) -> list[dict]:
        return self._unwrap(self._get(self._assets_path), "assets", "manual_accounts")

    def create_asset(self, payload: dict) -> dict:
        return self._post(self._assets_path, payload)

    def update_asset(self, asset_id: int, fields: dict) -> dict:
        return self._put(f"{self._assets_path}/{asset_id}", fields)

    # --- plaid accounts ---
    def plaid_accounts(self) -> list[dict]:
        return self._unwrap(self._get("/plaid_accounts"), "plaid_accounts")

    def trigger_plaid_fetch(self) -> dict:
        return self._post("/plaid_accounts/fetch", {})

    # --- crypto ---
    def crypto(self) -> list[dict]:
        return self._unwrap(self._get("/crypto"), "crypto")

    def update_crypto(self, crypto_id: int, fields: dict) -> dict:
        return self._put(f"/crypto/manual/{crypto_id}", fields)
