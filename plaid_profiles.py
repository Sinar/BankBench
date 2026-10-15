#!/usr/bin/env python3
"""Plaid Sandbox multi-profile client (official plaid-python v45 SDK).

Each "user profile" = a Plaid sandbox test-user credential. The SDK handles
routing + the pinned 2020-09-14 API version. Sandbox maps any live institution
to the simulated test bank, so the test-user login is what differentiates profiles.

Usage:
  python3 plaid_profiles.py list          # profile catalog
  python3 plaid_profiles.py <profile>     # one profile: item -> balances
  python3 plaid_profiles.py all           # balances for every profile
"""
import os
import sys
from pathlib import Path

import plaid
from plaid.api.plaid_api import PlaidApi
from plaid.api_client import ApiClient
from plaid.configuration import Configuration
from plaid.exceptions import ApiException
from plaid.model.sandbox_public_token_create_request import (
    SandboxPublicTokenCreateRequest as SP,
)
from plaid.model.sandbox_public_token_create_request_options import (
    SandboxPublicTokenCreateRequestOptions as OPT,
)
from plaid.model.item_public_token_exchange_request import (
    ItemPublicTokenExchangeRequest as EX,
)
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest as BAL
from plaid.model.accounts_balance_get_request_options import (
    AccountsBalanceGetRequestOptions as BLO,
)
from plaid.model.accounts_get_request import AccountsGetRequest as ACCT
from plaid.model.transactions_get_request import TransactionsGetRequest as TXN
from plaid.model.products import Products

HERE = Path(__file__).parent


def load_env():
    env = {}
    for line in (HERE / ".env").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


ENV = load_env()
CID = ENV["PLAID_CLIENT_ID"]
SEC = ENV["PLAID_SECRET"]
API_HOST = plaid.Environment.Sandbox  # 'https://sandbox.plaid.com'
api = PlaidApi(ApiClient(Configuration(host=API_HOST)))

# Sandbox test bank: any live catalog institution maps to the simulated bank.
INSTITUTION_ID = os.environ.get("PLAID_TEST_INSTITUTION", "ins_128026")

PROFILES = {
    "good":    {"username": "user_good",    "note": "clean login"},
    "mfa":     {"username": "user_mfa",     "note": "needs MFA (123456)"},
    "mfa_sms": {"username": "user_mfa_sms", "note": "needs SMS MFA"},
    "bad":     {"username": "user_bad",     "note": "wrong password"},
    "locked":  {"username": "user_locked",  "note": "account locked"},
    "update":  {"username": "user_update",  "note": "account-update flow"},
}
PASSWORD = "passw0rd"


def _call(fn, req):
    try:
        return fn(req)
    except ApiException as e:
        body = getattr(e, "body", None) or getattr(e, "reason", "")
        return {"_error": str(e.status), "body": (str(body)[:400])}


def make_item(profile):
    c = PROFILES[profile]
    opts = OPT(override_username=c["username"], override_password=PASSWORD)
    req = SP(
        institution_id=INSTITUTION_ID,
        initial_products=[Products("auth"), Products("transactions")],
        client_id=CID,
        secret=SEC,
        options=opts,
    )
    r = _call(api.sandbox_public_token_create, req)
    if "_error" in r:
        return r
    pub = r.public_token
    ex = _call(api.item_public_token_exchange, EX(public_token=pub, client_id=CID, secret=SEC))
    if "_error" in ex:
        return ex
    return {"access_token": ex.access_token}


def balances(access_token):
    import datetime
    since = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
    opts = BLO(min_last_updated_datetime=since)
    return _call(
        api.accounts_balance_get,
        BAL(access_token=access_token, client_id=CID, secret=SEC, options=opts),
    )


def accounts(access_token):
    return _call(api.accounts_get, ACCT(access_token=access_token, client_id=CID, secret=SEC))


def run(profile):
    c = PROFILES[profile]
    print(f"\n=== {profile}  ({c['note']})  user={c['username']} ===")
    item = make_item(profile)
    if "_error" in item:
        print(f"  item create: ERROR {item['_error']}  {item['body']}")
        return None
    at = item["access_token"]
    print(f"  access_token: {at[:24]}...")
    b = balances(at)
    if "_error" in b:
        print(f"  balances: ERROR {b['_error']}  {b['body']}")
        return None
    accounts_ = getattr(b, "accounts", None)
    if accounts_ is None:
        print("  balances: got response but no accounts (raw:", b.to_dict(), ")")
        return None
    for acct in accounts_:
        mask = str(getattr(acct, "mask", "?"))
        name = str(getattr(acct, "name", "?"))
        subtype = str(getattr(acct, "subtype", "?"))
        bal = getattr(acct, "balances", None)
        if bal is None:
            print(f"    {mask}  {name:<18}  (no balance data)")
            continue
        avail = getattr(bal, "available", None)
        curr = getattr(bal, "current", None)
        cur = str(getattr(bal, "iso_currency_code", "?") or "?")
        avail_s = f"{avail:>12}" if avail is not None else f"{'-':>12}"
        curr_s = f"{curr:>12}" if curr is not None else f"{'-':>12}"
        print(f"    {mask}  {name:<18} {subtype:<10} avail {avail_s}  current {curr_s}  {cur}")
    return at


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        print(f"institution: {INSTITUTION_ID}  host: {API_HOST}")
        for name, c in PROFILES.items():
            print(f"  {name:<8} {c['username']:<13} -> {c['note']}")
    elif cmd == "all":
        for name in PROFILES:
            run(name)
    elif cmd in PROFILES:
        run(cmd)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
