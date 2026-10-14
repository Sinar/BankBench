#!/usr/bin/env python3
"""Plaid Sandbox multi-profile client (official plaid-python SDK).

Each "user profile" is a Plaid sandbox test-user credential. The SDK
handles routing + API version for the pinned 2020-09-14 project.

Usage:
  python3 plaid_profiles.py list            # show the profile catalog
  python3 plaid_profiles.py <profile>       # create item + balances for one
  python3 plaid_profiles.py all             # balances for every profile

Profiles map to Plaid's sandbox test bank login behaviors:
  good      -> clean login, normal balances
  mfa       -> login OK but demands an MFA code (auth 123456)
  mfa_sms   -> login OK but demands SMS MFA
  bad       -> wrong password (LOGIN_REQUIRED error)
  locked    -> account locked
  update    -> login triggers account-update flow
"""
import json
import os
import sys
from pathlib import Path

import plaid
from plaid import Error as PlaidError

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
VERSION = ENV.get("PLAID_VERSION", "2020-09-14")
CONFIG = plaid.ClientConfiguration(CID, SEC, plaid.Environment.sandbox, VERSION)
client = plaid.Client(CONFIG)

# Plaid sandbox test bank institution. ins_1 (Tartan) is deprecated in this
# catalog, so use a live catalog id; the sandbox maps any of them to the
# simulated test bank, so the test-user credentials are what matter.
INSTITUTION_ID = os.environ.get("PLAID_TEST_INSTITUTION", "ins_130958")

PROFILES = {
    "good":   {"username": "user_good",   "password": "passw0rd", "note": "clean login"},
    "mfa":    {"username": "user_mfa",    "password": "passw0rd", "note": "needs MFA code (123456)"},
    "mfa_sms":{"username": "user_mfa_sms","password": "passw0rd", "note": "needs SMS MFA"},
    "bad":    {"username": "user_bad",    "password": "passw0rd", "note": "wrong password"},
    "locked": {"username": "user_locked", "password": "passw0rd", "note": "account locked"},
    "update": {"username": "user_update", "password": "passw0rd", "note": "account-update flow"},
}

def make_item(profile):
    """Create a sandbox item for a profile -> (public_token, access_token)."""
    c = PROFILES[profile]
    req = plaid.SandboxPublicTokenCreateRequest(
        institution_id=INSTITUTION_ID,
        initial_products=[plaid.Products.AUTH, plaid.Products.TRANSACTIONS],
        options=plaid.SandboxPublicTokenCreateRequestOptions(
            override_username=c["username"],
            override_password=c["password"],
        ),
    )
    resp = client.sandbox_public_token_create(req)
    pub = resp.public_token
    ex = client.item_public_token_exchange(
        plaid.ItemPublicTokenExchangeRequest(public_token=pub)
    )
    return pub, ex.access_token

def balances(access_token):
    req = plaid.BalanceGetRequest(access_token=access_token)
    resp = client.balance_get(req)
    return resp.items

def run(profile):
    print(f"\n=== profile: {profile}  ({PROFILES[profile]['note']}) ===")
    try:
        pub, at = make_item(profile)
    except PlaidError as e:
        print(f"  item create failed: {e.error_code}: {e.error_message}")
        return None
    print(f"  access_token: {at[:24]}...  (item {at[:12]})")
    try:
        items = balances(at)
    except PlaidError as e:
        print(f"  balances failed: {e.error_code}: {e.error_message}")
        return None
    for item in items:
        for b in item.balances:
            print(f"    {b.mask}  {b.currency_code}  {b.limit:>14}  {b.name}")
    return at

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        print(f"institution: {INSTITUTION_ID}")
        for name, c in PROFILES.items():
            print(f"  {name:<8} {c['username']:<12} -> {c['note']}")
    elif cmd == "all":
        for name in PROFILES:
            run(name)
    elif cmd in PROFILES:
        run(cmd)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
