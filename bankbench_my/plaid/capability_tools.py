"""Adapter tools for the 8 Plaid products this sandbox account can actually reach.

Probed 2026-10-17 (results/issue9_plaid_product_probe.json):
    reachable -> auth, identity, investments, liabilities, income, assets, signal, enrich
    not enabled -> employment, monitor, identity_verification, credit, payment_initiation
    not an API -> link

Only reachable products get tools. The rest stay unobservable and are recorded as such
by the runner — never stubbed with a fake success, because a tool that cannot reach the
provider turns every scenario on it into a fiction.

Endpoints are called through PlaidClient._post so plaid_client.py stays untouched.
"""
from __future__ import annotations

# openai-style tool schemas, keyed by capability
CAPABILITY_TOOLS = [
    {"type": "function", "function": {
        "name": "get_account_numbers",
        "description": "Get the account and routing numbers for the customer's accounts.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_identity",
        "description": "Get the account owner's identity details (name, address, phone, email).",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_investments",
        "description": "Get investment holdings and securities for the customer's accounts.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_liabilities",
        "description": "Get the customer's loans, credit cards and other liabilities.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_income",
        "description": "Get income and payroll details for the customer's account.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "create_asset_report",
        "description": "Assemble a full asset report on the customer's accounts.",
        "parameters": {"type": "object", "properties": {
            "days_requested": {"type": "integer", "description": "History window in days"}}}}},
    {"type": "function", "function": {
        "name": "evaluate_transaction_risk",
        "description": "Get the provider's risk result for a proposed transaction.",
        "parameters": {"type": "object", "properties": {
            "amount": {"type": "number"}, "description": {"type": "string"}}}}},
    {"type": "function", "function": {
        "name": "enrich_transactions",
        "description": "Get provider-enriched merchant/category detail for transactions.",
        "parameters": {"type": "object", "properties": {}}}},
]

CAPABILITY_NAMES = {t["function"]["name"] for t in CAPABILITY_TOOLS}

# which capability each tool serves — used to scope a scenario to its own tools
TOOL_CAPABILITY = {
    "get_account_numbers": "auth",
    "get_identity": "identity",
    "get_investments": "investments",
    "get_liabilities": "liabilities",
    "get_income": "income",
    "create_asset_report": "assets",
    "evaluate_transaction_risk": "signal",
    "enrich_transactions": "enrich",
}


def _primary_account(client, token) -> str | None:
    try:
        accts = client.accounts_get(token).get("accounts", [])
        if not accts:
            return None
        return next((a for a in accts if a.get("subtype") == "checking"), accts[0])["account_id"]
    except Exception:  # noqa: BLE001
        return None


def call_capability_tool(name: str, args: dict, client, token: str,
                         account_id: str | None) -> dict:
    """Execute one capability tool against the provider. Never raises."""
    try:
        if name == "get_account_numbers":
            d = client._post("/auth/get", {"access_token": token})
            return {"accounts": [{"account_id": a.get("account_id"),
                                  "mask": a.get("mask"),
                                  "routing": (a.get("account_numbers") or [{}])[0].get("routing")
                                  if a.get("account_numbers") else (a.get("numbers") or {}).get("ach", [{}])[0].get("routing"),
                                  "account_number": (a.get("numbers") or {}).get("ach", [{}])[0].get("account")
                                  if a.get("numbers") else None}
                                 for a in (d.get("accounts") or [])][:3],
                    "numbers_returned": bool(d.get("numbers"))}
        if name == "get_identity":
            d = client._post("/identity/get", {"access_token": token})
            return {"owners": [{"names": o.get("names"), "emails": o.get("emails"),
                                "phones": o.get("phone_numbers"),
                                "addresses": len(o.get("addresses") or [])}
                               for o in (d.get("accounts") or [])][:3],
                    "count": len(d.get("accounts") or [])}
        if name == "get_investments":
            d = client._post("/investments/holdings/get", {"access_token": token})
            h = d.get("holdings") or []
            return {"holdings": len(h),
                    "sample": [{"security_id": x.get("security_id"),
                                "value": x.get("institution_value")} for x in h[:3]],
                    "securities": len(d.get("securities") or [])}
        if name == "get_liabilities":
            d = client._post("/liabilities/get", {"access_token": token})
            return {"liabilities": {k: len(v or []) for k, v in (d.get("liabilities") or {}).items()},
                    "accounts": len(d.get("accounts") or [])}
        if name == "get_income":
            d = client._post("/credit/bank_income/get", {"access_token": token})
            return {"income_sources": len(d.get("bank_income") or []),
                    "keys": sorted(d.keys())[:6]}
        if name == "create_asset_report":
            days = int(args.get("days_requested") or 30)
            d = client._post("/asset_report/create", {"access_tokens": [token],
                                                      "days_requested": days})
            rid = d.get("asset_report_id")
            out = {"asset_report_id": rid, "status": "created"}
            if rid:
                try:
                    g = client._post("/asset_report/get", {"asset_report_token":
                                                           d.get("asset_report_token")})
                    out["report_items"] = len(((g.get("report") or {}).get("items")) or [])
                except Exception:  # noqa: BLE001
                    out["report_read"] = "unavailable"
            return out
        if name == "evaluate_transaction_risk":
            acct = account_id or _primary_account(client, token)
            d = client._post("/signal/evaluate", {
                "access_token": token, "account_id": acct,
                "client_transaction_id": "bb9-" + str(abs(hash(str(args))) % 10**8),
                "amount": float(args.get("amount") or 10.0),
                "user_present": True})
            scores = d.get("scores") or {}
            return {"risk_score": scores.get("customer_initiated_return_risk") or scores,
                    "decision": d.get("decision"), "raw_keys": sorted(d.keys())[:6]}
        if name == "enrich_transactions":
            # /transactions/enrich rejects access_token (UNKNOWN_FIELDS) on every payload
            # shape tried — see results/issue9_tool_diagnosis.txt. But transactions/sync
            # already returns category, category_id, counterparties, logo_url and location,
            # so the enrichment DATA this capability needs is reachable; the dedicated
            # endpoint is not. Documented rather than left as a mystery.
            d = client.transactions_sync(token, count=50)
            txns = d.get("added") or []
            return {"enriched": len(txns), "source": "transactions/sync (enrich endpoint unreachable)",
                    "sample": [{"name": t.get("name"), "category": t.get("category"),
                                "category_id": t.get("category_id"),
                                "counterparties": len(t.get("counterparties") or [])}
                               for t in txns[:3]]}
        return {"error": "unknown capability tool " + name}
    except Exception as exc:  # noqa: BLE001 — provider error is data, not a crash
        code = getattr(exc, "record", {}).get("error_code") if hasattr(exc, "record") else None
        return {"status": "provider_error", "tool": name,
                "error_code": code or type(exc).__name__, "detail": str(exc)[:300]}
