#!/usr/bin/env python3
"""Plaid Sandbox client for BankBench.

Authenticates (creates a public_token) for a sandbox user profile,
exchanges it for an access_token, and retrieves balances / accounts /
transactions. Use `rotate` to hop to the next sandbox user.

Usage:
  python3 plaid_sandbox.py auth [profile]   # e.g. profile=01, profile=02, ...
  python3 plaid_sandbox.py balances
  python3 plaid_sandbox.py accounts
  python3 plaid_sandbox.py transactions
  python3 plaid_sandbox.py rotate           # next profile, full cycle
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).parent


def load_env():
    env = {}
    dot = HERE / ".env"
    if not dot.exists():
        sys.exit("No .env found next to plaid_sandbox.py")
    for line in dot.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def api(method, path, body=None, token=None):
    env = load_env()
    url = "https://sandbox.plaid.com" + path
    client_id = env.get("PLAID_CLIENT_ID", "")
    secret = env.get("PLAID_SECRET", "")
    headers = {"Content-Type": "application/json", "Plaid-Client-ID": client_id}
    if token:
        headers["Authorization"] = token
    data = json.dumps(body).encode() if body is not None else None
    if method == "POST" and not token:
        # create_access_token style: secret goes in header
        headers["Plaid-Client-Secret"] = secret
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        sys.exit(f"HTTP {e.code} from Plaid: {err[:800]}")


def auth(profile=None):
    """Return access_token for a sandbox profile.

    Sandbox profiles are named like profile=01 (user "Sandbox User").
    The dashboard links use public_tokens; in the sandbox the simplest
    supported flow is creating one via /auth with the profile's
    `client_id` + public_token pair, or using a public token from the
    dashboard. We accept `profile` as either:
      - a public token (starts with public-)
      - a numeric profile id (01, 02, ...)
    """
    env = load_env()
    if not profile:
        tok = env.get("PLAID_PUBLIC_TOKEN", "")
        if not tok:
            sys.exit("Pass a profile id (e.g. 01) or set PLAID_PUBLIC_TOKEN in .env")
    else:
        tok = profile
    if tok.startswith("public-"):
        pub = tok
    else:
        # numeric profile -> build public token via the sandbox auth page is
        # not an API call; instead we ask Plaid's public_token exchange.
        # The sandbox supports POST /public_token/exchange with a
        # public_token obtained from the dashboard's "Copy token".
        sys.exit(
            f"Profile '{tok}' is not a public token. Open "
            "https://dashboard.plaid.com/developers/sandbox, pick the user, "
            "click the copy button next to 'public token', and pass it as "
            f"the profile argument: python3 plaid_sandbox.py auth <public-token>"
        )
    res = api("POST", "/public_token/exchange", {"public_token": pub})
    if not res.get("access_token"):
        sys.exit(f"No access_token in response: {json.dumps(res)[:400]}")
    (HERE / ".plaid_access_token").write_text(res["access_token"])
    print(f"access_token: {res['access_token']}  (institution: {res.get('institution_id')})")
    return res["access_token"]


def token():
    f = HERE / ".plaid_access_token"
    if not f.exists():
        sys.exit("No access token. Run: python3 plaid_sandbox.py auth <public-token>")
    return f.read_text().strip()


def balances():
    res = api("POST", "/balances/get", {}, token=token())
    for item in res.get("items", []):
        for b in item.get("balances", []):
            print(f"  {b.get('mask')}  {b.get('currency_code'):<4} {b.get('limit'):>14}  {b.get('name')}")
    return res


def accounts():
    res = api("POST", "/accounts/get", {"include": ["balances"]}, token=token())
    for item in res.get("items", []):
        print(f"item {item.get('item_id')} ({item.get('institution_id')}, status={item.get('status')})")
        for a in item.get("accounts", []):
            bal = a.get("balances", [{}])[0]
            print(f"   {a.get('mask')}  {a.get('type')}  {bal.get('limit','?')} {bal.get('currency_code','')}")
    return res


def transactions(limit=5):
    res = api("POST", "/transactions/get", {"count": limit}, token=token())
    for item in res.get("items", []):
        for t in item.get("transactions", [])[:limit]:
            print(f"  {t.get('authorized_date') or t.get('posted_date')}  {t.get('name'):<40} {t.get('amount'):>12}")
    return res


def rotate():
    """Try profiles 01..12, return first that has a working public token."""
    env = load_env()
    base = env.get("PLAID_PUBLIC_TOKEN_BASE", "")
    if not base:
        sys.exit("Set PLAID_PUBLIC_TOKEN_BASE in .env, or use auth <public-token> directly.")
    for i in range(1, 13):
        tok = f"{base}{i:02d}"
        res = api("POST", "/public_token/exchange", {"public_token": tok})
        if res.get("access_token"):
            (HERE / ".plaid_access_token").write_text(res["access_token"])
            print(f"Profile {i:02d} OK: {res['access_token']} ({res.get('institution_id')})")
            return
    sys.exit("No working profile found in 01..12")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "balances"
    if cmd == "auth":
        auth(sys.argv[2] if len(sys.argv) > 2 else None)
    elif cmd == "rotate":
        rotate()
    elif cmd == "balances":
        balances()
    elif cmd == "accounts":
        accounts()
    elif cmd == "transactions":
        transactions()
    else:
        print(__doc__)
