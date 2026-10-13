#!/usr/bin/env python3
"""Run one mock Sandbox user's tasks with an LLM agent — the user-centric layer.

    python3 run_user_scenarios.py --list
    python3 run_user_scenarios.py --user nur_aisyah
    python3 run_user_scenarios.py --user nur_aisyah --mock

A "user" is a bundle in users/: a persona, the Plaid custom-user configuration
object, its registered payees, and the tasks that user's agent is asked to do.
Ground truth is read from the provider, so scoring never trusts the fixture.

Outputs results/user_<name>_results.json and results/user_<name>_report.md
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from plaid_client import PlaidClient
from user_scenarios import USERS_DIR, load_user, run_user_scenarios

HERE = pathlib.Path(__file__).resolve().parent
RESULTS = HERE / "results"


def _load_client(mock: bool):
    if mock:
        from mock_plaid import MockPlaidClient
        return MockPlaidClient(), "mock"
    client = PlaidClient()
    if not client.configured():
        print("MISSING CREDENTIALS: %s — see README.md" % ", ".join(client.missing()))
        raise SystemExit(2)
    return client, "live"


def _report(name: str, mode: str, out: dict, when: str) -> str:
    p = out["provider_truth"]
    lines = [
        "# Mock user run — %s" % out["user"], "",
        "Plaid custom user: `%s` | mode: **%s** | %s" % (out["username"], mode, when),
        "Item: `%s`" % out["item_id"], "",
        "> %s" % out["persona"], "",
        "Ground truth is read from the provider (`/accounts/balance/get`,",
        "`/transactions/sync`), never from the fixture file.", "",
        "## Provider truth", "", "| account | current | mask |", "|---|---|---|",
    ]
    for a in p["accounts"]:
        lines.append("| %s | %s | %s |" % (a["name"], a["current"], a["mask"]))
    lines += ["", "Transactions: **%d**, total **%s**" % (p["transaction_count"],
                                                          p["transaction_total"]), "",
              "## Tasks", "", "| id | kind | task | result |", "|---|---|---|---|"]
    for t in out["tasks"]:
        res = "PASS" if t["passed"] else ("FAIL" if t["passed"] is False else "NOT RUN")
        lines.append("| %s | %s | %s | %s |" % (t["id"], t["kind"], t["name"], res))
    lines += ["", "## Detail", ""]
    for t in out["tasks"]:
        lines += ["### %s — %s" % (t["id"], t["name"]), "",
                  "Prompt: *%s*" % t["prompt"], "", "Expected: %s" % t["expect"],
                  "", "Tools called: %s" % (", ".join(c["name"] for c in t["tool_calls"]) or "(none)"),
                  "", "| check | ok |", "|---|---|"]
        for c in t["checks"]:
            lines.append("| %s | %s |" % (c["check"], "yes" if c["ok"] else "**NO**"))
        lines += ["", "> %s" % (t["agent_final_text"] or "").replace("\n", " ")[:400], ""]
    passed = sum(1 for t in out["tasks"] if t["passed"])
    ran = sum(1 for t in out["tasks"] if t["passed"] is not None)
    lines += ["## Result", "",
              "**%d/%d** tasks passed. Full trace: `results/user_%s_results.json`"
              % (passed, ran, name), ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--user", default="nur_aisyah")
    ap.add_argument("--mock", action="store_true", help="offline dry run")
    ap.add_argument("--model", default="deepseek/deepseek-v4.1-flash")
    ap.add_argument("--list", action="store_true", help="list available users")
    args = ap.parse_args()

    if args.list:
        for path in sorted(USERS_DIR.glob("*.json")):
            b = load_user(path.stem)
            print("%-14s %-26s %d tasks  (%s)" % (path.stem, b["display_name"],
                                                  len(b["tasks"]), b["username"]))
        return 0

    client, mode = _load_client(args.mock)
    bundle = load_user(args.user)
    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    out = run_user_scenarios(client, bundle, model=args.model)
    out["mode"] = mode

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / ("user_%s_results.json" % args.user)).write_text(json.dumps(out, indent=2))
    report = _report(args.user, mode, out, when)
    (RESULTS / ("user_%s_report.md" % args.user)).write_text(report)
    print(report)
    print("\nWrote %s" % (RESULTS / ("user_%s_results.json" % args.user)))
    passed = sum(1 for t in out["tasks"] if t["passed"])
    ran = sum(1 for t in out["tasks"] if t["passed"] is not None)
    return 0 if passed == ran and ran == len(out["tasks"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
