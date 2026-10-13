#!/usr/bin/env python3
"""BankBench-MY x Plaid Sandbox - six-eval first pass (GitHub issue Sinar/BankBench#3).

  3 capability evals  CAP-1..3   can the target act on a real banking API?
  3 AI-safety evals   SAF-1..3   does it attempt / complete a forbidden action?

Usage:
    python3 run_plaid_evals.py --preflight     # access check only
    python3 run_plaid_evals.py                 # full run (needs PLAID_CLIENT_ID / PLAID_SECRET)
    python3 run_plaid_evals.py --mock          # offline dry run, no keys, tags results mode=mock

Outputs:
    results/plaid_eval_results.json    evidence, one record per eval
    results/plaid_eval_report.md       human-readable report

Secrets live only in the environment (repo .env, gitignored). Nothing here
writes a client_id, secret or access_token to disk.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from capability_evals import run_capability_evals
from plaid_client import PlaidClient, redact
from safety_evals import run_safety_evals, selfcheck

HERE = pathlib.Path(__file__).resolve().parent
RESULTS = HERE / "results"


def _load_client(mock: bool):
    if mock:
        from mock_plaid import MockPlaidClient
        return MockPlaidClient(), "mock"
    client = PlaidClient()
    if not client.configured():
        print("MISSING CREDENTIALS: %s" % ", ".join(client.missing()))
        print("Put them in %s (gitignored):" % (HERE.parents[1] / ".env"))
        print("  PLAID_CLIENT_ID=...\n  PLAID_SECRET=...\n  PLAID_ENV=sandbox")
        print("Get them at https://dashboard.plaid.com/developers/keys (Sandbox tab).")
        print("Dry run without keys: python3 run_plaid_evals.py --mock")
        raise SystemExit(2)
    return client, "live"


def _verdict(r: dict) -> str:
    if r.get("verdict"):
        return r["verdict"]
    return "PASS" if r.get("passed") else "FAIL"


def _summary(rows: list[dict]) -> str:
    out = ["| eval | kind | name | result | observed |", "|---|---|---|---|---|"]
    for r in rows:
        out.append("| %s | %s | %s | %s | %s |" % (
            r["id"], r["kind"], r.get("name", ""), _verdict(r),
            (r.get("observed") or r.get("verdict") or "")[:70]))
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mock", action="store_true", help="offline dry run, no credentials")
    ap.add_argument("--preflight", action="store_true", help="access check only")
    ap.add_argument("--model", default="deepseek/deepseek-v4.1-flash")
    args = ap.parse_args()

    client, mode = _load_client(args.mock)
    started = datetime.now(timezone.utc)
    caps = run_capability_evals(client)

    token = (caps[0].get("context") or {}).get("access_token")
    account_id = ((caps[1].get("context") or {}).get("primary_account_id")
                  or (caps[2].get("context") or {}).get("primary_account_id"))

    if args.preflight:
        print("PREFLIGHT (%s)" % mode)
        for r in caps:
            print("  %-4s %-28s %s" % ("PASS" if r["passed"] else "FAIL",
                                       r["name"], r.get("observed")))
        print("\nAPI calls made: %d" % len(client.calls))
        for c in client.calls:
            print("  %-34s ok=%s %sms %s" % (c["endpoint"], c["ok"], c.get("ms"),
                                             c.get("error_code") or ""))
        return 0 if all(r["passed"] for r in caps) else 1

    safs, note = run_safety_evals(client, token, account_id, model=args.model)
    checks = selfcheck()

    RESULTS.mkdir(exist_ok=True)
    payload = {
        "harness": "bankbench_my/plaid",
        "issue": "https://github.com/Sinar/BankBench/issues/3",
        "mode": mode,
        "started_utc": started.isoformat(),
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "env": {"client_id": redact(getattr(client, "client_id", "")) if mode == "live" else "(mock)",
                "base_url": getattr(client, "base_url", "(mock)"),
                "agent_model": args.model, "safety_note": note},
        "api_calls": client.calls,
        "scorer_selfcheck": checks,
        "capability": caps,
        "safety": safs,
    }
    (RESULTS / "plaid_eval_results.json").write_text(json.dumps(payload, indent=2))

    rows = caps + safs
    cap_pass = sum(1 for r in caps if r["passed"])
    saf_ran = [r for r in safs if r["passed"] is not None]
    saf_pass = sum(1 for r in saf_ran if r["passed"])

    lines = [
        "# BankBench-MY x Plaid Sandbox - six-eval first pass", "",
        "Issue: https://github.com/Sinar/BankBench/issues/3 | mode: **%s**" % mode,
        "Run: %s" % started.strftime("%Y-%m-%d %H:%M UTC"),
        "Agent under test: OpenRouter `%s` (see agent.py)" % args.model, "",
        "## Scoreboard", "", _summary(rows), "",
        "## Result", "",
        "- Capability: **%d/3** passed." % cap_pass,
        "- AI safety: **%d/%d** run passed." % (saf_pass, len(saf_ran)),
        "- Scorer self-check: **%d/%d** synthetic cases classified correctly (%s)"
        % (sum(1 for c in checks if c["ok"]), len(checks),
           ", ".join("%s=%s" % (c["case"], "ok" if c["ok"] else "WRONG") for c in checks)),
    ]
    if note:
        lines += ["- Safety evals note: `%s`" % note]
    lines += ["", "## Evidence", "",
              "Every eval's tool calls, provider-state delta and agent final text are in",
              "`results/plaid_eval_results.json`. Layer B (`observable: false`) means the",
              "provider ledger could not be read - reported as unknown, never reconstructed.", ""]
    (RESULTS / "plaid_eval_report.md").write_text("\n".join(lines))

    print("\n".join(lines))
    print("\nWrote %s" % (RESULTS / "plaid_eval_results.json"))
    return 0 if cap_pass == 3 and saf_pass == len(saf_ran) else 1


if __name__ == "__main__":
    raise SystemExit(main())
