"""Minimal Plaid Sandbox client — plain REST, no SDK.

Why no SDK: the eval harness must stay inspectable and dependency-light, and
every call here is a documented HTTPS POST. Anything the harness needs that
this file does not expose is a five-line function, not a framework.

Secrets come from the environment only. `load_env()` reads (in order, first
hit wins):
  1. an already-exported environment variable
  2. <repo_root>/.env                (this repo — gitignored)
  3. ~/.hermes/.env                  (where this machine keeps OPENROUTER_API_KEY)

Never print a secret. `redact()` exists so evidence files can name a key
without containing one.
"""

from __future__ import annotations

import json
import os
import pathlib
import time
from typing import Any

import requests

SANDBOX_HOST = "https://sandbox.plaid.com"

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ENV_FILES = [REPO_ROOT / ".env", pathlib.Path.home() / ".hermes" / ".env"]


# --------------------------------------------------------------------------
# config
# --------------------------------------------------------------------------

def load_env() -> None:
    """Populate os.environ from the .env files, without clobbering real env."""
    for path in ENV_FILES:
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key and value and not os.environ.get(key):
                os.environ[key] = value


def redact(value: str) -> str:
    if not value:
        return "(unset)"
    return value[:4] + "..." if len(value) > 8 else "(set)"


class PlaidConfigError(RuntimeError):
    pass


class PlaidClient:
    """Sandbox-only client. Every method is one documented endpoint."""

    def __init__(self, client_id: str | None = None, secret: str | None = None,
                 base_url: str = SANDBOX_HOST, timeout: int = 30):
        load_env()
        self.client_id = client_id or os.environ.get("PLAID_CLIENT_ID", "")
        self.secret = secret or os.environ.get("PLAID_SECRET", "")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.calls: list[dict] = []
        self.created_transfer_ids: list[str] = []

    def configured(self) -> bool:
        return bool(self.client_id and self.secret)

    def missing(self) -> list[str]:
        return [n for n, v in (("PLAID_CLIENT_ID", self.client_id),
                               ("PLAID_SECRET", self.secret)) if not v]

    # -- plumbing ----------------------------------------------------------

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = {"client_id": self.client_id, "secret": self.secret, **payload}
        t0 = time.time()
        try:
            resp = requests.post(self.base_url + path, json=body, timeout=self.timeout)
            data = resp.json()
        except requests.RequestException as exc:
            data = {"error": "NETWORK", "error_message": str(exc)}
            resp = None
        record = {
            "endpoint": path,
            "http_status": getattr(resp, "status_code", None),
            "ms": round((time.time() - t0) * 1000),
            "ok": bool(resp is not None and resp.ok and "error_code" not in data),
            "error_code": data.get("error_code"),
            "error_message": data.get("error_message"),
        }
        self.calls.append(record)
        if not record["ok"]:
            raise PlaidCallError(path, record, data)
        return data

    # -- sandbox-only endpoints -------------------------------------------

    def sandbox_public_token(self, institution_id: str, products: list[str],
                             custom_user: dict | None = None) -> str:
        options: dict[str, Any] = {}
        if custom_user is not None:
            options["override_username"] = "user_custom"
            options["override_password"] = json.dumps(custom_user)
        data = self._post("/sandbox/public_token/create", {
            "institution_id": institution_id,
            "initial_products": products,
            **({"options": options} if options else {}),
        })
        return data["public_token"]

    def sandbox_reset_login(self, access_token: str) -> dict:
        return self._post("/sandbox/item/reset_login", {"access_token": access_token})

    # -- core endpoints ----------------------------------------------------

    def exchange(self, public_token: str) -> dict:
        return self._post("/item/public_token/exchange", {"public_token": public_token})

    def item_get(self, access_token: str) -> dict:
        return self._post("/item/get", {"access_token": access_token})

    def accounts_get(self, access_token: str) -> dict:
        return self._post("/accounts/get", {"access_token": access_token})

    def balance_get(self, access_token: str) -> dict:
        return self._post("/accounts/balance/get", {"access_token": access_token})

    def auth_get(self, access_token: str) -> dict:
        return self._post("/auth/get", {"access_token": access_token})

    def transactions_sync(self, access_token: str, count: int = 100) -> dict:
        return self._post("/transactions/sync", {"access_token": access_token, "count": count})

    def identity_get(self, access_token: str) -> dict:
        return self._post("/identity/get", {"access_token": access_token})

    # -- money movement (Transfer product) --------------------------------

    def transfer_create(self, access_token: str, account_id: str, amount: str,
                        description: str = "BankBench-MY eval transfer") -> dict:
        auth = self._post("/transfer/authorization/create", {
            "access_token": access_token,
            "account_id": account_id,
            "type": "debit",
            "network": "ach",
            "amount": amount,
            "ach_class": "web",
            "user": {"legal_name": "BankBench MY Eval User"},
        })
        if auth.get("decision") not in ("approved", None):
            return {"blocked_by_provider": True, "decision": auth.get("decision"),
                    "authorization_id": auth.get("authorization_id")}
        out = self._post("/transfer/create", {
            "access_token": access_token,
            "account_id": account_id,
            "authorization_id": (auth.get("authorization") or {}).get("id")
                                or auth.get("authorization_id"),
            "description": description,
        })
        transfer = out.get("transfer") or {}
        tid = transfer.get("id") or out.get("transfer_id")
        if tid and tid not in self.created_transfer_ids:
            self.created_transfer_ids.append(tid)
        return out

    def transfer_get(self, transfer_id: str) -> dict:
        return self._post("/transfer/get", {"transfer_id": transfer_id})

    def money_moved(self, access_token: str) -> dict:
        """Provider-side ledger check.

        `/transfer/list` is not callable with an access token (it returns
        UNKNOWN_FIELDS), so the ledger is read the reliable way: every transfer
        this run asked the provider to create is re-fetched by id with
        `/transfer/get`. `confirmed` counts only ids the provider still
        acknowledges — the truth source is the provider, not our own list.
        """
        ids = list(self.created_transfer_ids)
        if not ids:
            return {"observable": True, "transfers": [], "count": 0, "confirmed": 0,
                    "total_amount": "0", "note": "no transfers requested this run"}
        confirmed, errors = [], []
        for tid in ids:
            try:
                confirmed.append(self.transfer_get(tid).get("transfer") or {"id": tid})
            except PlaidCallError as exc:
                errors.append(exc.record.get("error_code") or exc.record.get("error_message"))
        return {
            "observable": True,
            "transfers": confirmed,
            "count": len(confirmed),
            "confirmed": len(confirmed),
            "total_amount": str(sum(float(t.get("amount") or 0) for t in confirmed)),
            "unconfirmed": errors,
        }


class PlaidCallError(RuntimeError):
    def __init__(self, endpoint: str, record: dict, payload: dict):
        self.endpoint, self.record, self.payload = endpoint, record, payload
        detail = record.get("error_code") or record.get("error_message") or "unknown error"
        super().__init__(f"{endpoint} failed ({detail})")
