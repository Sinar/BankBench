#!/usr/bin/env python3
"""Resolve a suite key from suites/registry.json into shell variables.

Keeps the registry as the single source of truth so run_eval.sh does not carry
its own duplicate copy of the suite list (duplicate lists drift).

    python3 resolve_suite.py --suite fomca --format shell
    python3 resolve_suite.py --list
"""

import argparse
import json
import shlex
import sys
from pathlib import Path

REGISTRY = Path(__file__).resolve().parent.parent / "suites" / "registry.json"


def load():
    return json.loads(REGISTRY.read_text())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--format", choices=["shell", "json", "human"], default="human")
    args = ap.parse_args()

    reg = load()
    suites = reg["suites"]

    if args.list:
        for key, s in suites.items():
            needs = ", ".join(s.get("needs") or []) or "nothing extra"
            tag = "local" if s["kind"] == "local" else "inspect_evals"
            print(f"{key:<24} [{tag:<13}] {s['display']}")
            print(f"{'':<24} needs: {needs}")
        return

    if not args.suite:
        ap.error("--suite is required (or use --list)")
    if args.suite not in suites:
        sys.exit(f"unknown suite {args.suite!r}. Known: {', '.join(suites)}")

    s = dict(suites[args.suite])
    s["key"] = args.suite
    s["default"] = reg.get("default")

    if args.format == "json":
        print(json.dumps(s, indent=2))
        return

    if args.format == "shell":
        # shell-safe: values are quoted, and absent values become empty strings
        for k in ("kind", "dir", "task", "log_dir", "display", "assessment",
                  "oracle_mock", "naive_mock"):
            print(f"SUITE_{k.upper()}={shlex.quote(str(s.get(k) or ''))}")
        print(f"SUITE_NEEDS={shlex.quote('; '.join(s.get('needs') or []))}")
        print(f"SUITE_CAVEAT={shlex.quote(str(s.get('caveat') or ''))}")
        print(f"SUITE_QUESTIONS={shlex.quote(str(s.get('questions') or ''))}")
        return

    print(f"{s['display']}")
    print(f"  key        : {s['key']}")
    print(f"  kind       : {s['kind']}")
    print(f"  task       : {s['task']}")
    print(f"  questions  : {s.get('questions')}")
    print(f"  languages  : {', '.join(s.get('languages') or [])}")
    print(f"  tests      : {s.get('what_it_tests')}")
    print(f"  good for   : {s.get('good_for')}")
    print(f"  needs      : {', '.join(s.get('needs') or []) or 'nothing extra'}")
    print(f"  assessment : {s.get('assessment') or 'none — third-party grade not yet written'}")
    print(f"  caveat     : {s.get('caveat')}")


if __name__ == "__main__":
    main()
