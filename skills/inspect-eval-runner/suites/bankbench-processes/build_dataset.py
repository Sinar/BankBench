#!/usr/bin/env python3
"""Build the BankBench process-safety dataset from items.json.

Asserts the schema AND the two properties this suite claims: a balanced
risk/control split, and a declared mode + agentic flag on every item. If either
claim breaks, the build fails rather than shipping a quietly unbalanced set.

    python3 build_dataset.py
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "items.json"

VALID_TARGETS = {"block", "escalate", "allow"}
VALID_MODES = {"model_only", "model_plus_tools", "full_agent_system"}
REQUIRED_META = {
    "category", "title", "mode", "agentic", "language", "difficulty",
    "process_control", "expected_behaviour", "what_it_catches", "safe_actions",
    "require_any_of", "must_include", "must_not_include", "control_pair",
    "harm_if_failed", "harm_severity", "unbiased_note", "regulator_reference",
    "placeholder_notice",
}
CSV_FIELDS = [
    "id", "category", "target", "mode", "agentic", "language", "difficulty",
    "harm_severity", "title", "prompt", "process_control", "expected_behaviour",
    "control_pair", "harm_if_failed", "unbiased_note", "regulator_reference",
    "placeholder_notice",
]


def load():
    data = json.loads(SRC.read_text())
    meta, items = data["_meta"], data["items"]
    problems = []

    for it in items:
        iid = it.get("id", "?")
        if it.get("target") not in VALID_TARGETS:
            problems.append(f"{iid}: target {it.get('target')!r} not in {VALID_TARGETS}")
        m = it.get("metadata", {})
        missing = REQUIRED_META - set(m)
        if missing:
            problems.append(f"{iid}: missing metadata {sorted(missing)}")
        if m.get("mode") not in VALID_MODES:
            problems.append(f"{iid}: mode {m.get('mode')!r} not in {VALID_MODES}")
        if not isinstance(m.get("agentic"), bool):
            problems.append(f"{iid}: agentic must be true/false, got {m.get('agentic')!r}")
        for k in ("must_include", "must_not_include", "require_any_of", "safe_actions"):
            if not isinstance(m.get(k), list):
                problems.append(f"{iid}: metadata.{k} must be a list")

    ids = [i["id"] for i in items]
    if len(set(ids)) != len(ids):
        problems.append(f"duplicate ids: {ids}")

    # --- the two claims this suite makes, checked mechanically ------------
    risky = [i for i in items if i["target"] in ("block", "escalate")]
    control = [i for i in items if i["target"] == "allow"]
    if len(risky) != len(control):
        problems.append(
            f"UNBALANCED: {len(risky)} risk vs {len(control)} control. The paired-control "
            f"design is the suite's anti-bias mechanism and requires an equal split."
        )
    paired = {i["metadata"].get("control_pair") for i in items}
    for i in items:
        cp = i["metadata"].get("control_pair")
        if not cp:
            problems.append(f"{i['id']}: no control_pair — every item must be paired")
        elif cp not in ids:
            problems.append(f"{i['id']}: control_pair {cp!r} does not exist")

    if problems:
        sys.exit("SCHEMA/BALANCE CHECK FAILED:\n  " + "\n  ".join(problems))
    return meta, items, risky, control


def build(meta, items):
    (HERE / "bankbench_tasks.json").write_text(json.dumps(items, indent=2) + "\n")
    with (HERE / "bankbench_tasks.jsonl").open("w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    with (HERE / "bankbench_tasks.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for it in items:
            m = it["metadata"]
            w.writerow({
                "id": it["id"], "category": m["category"], "target": it["target"],
                "mode": m["mode"], "agentic": m["agentic"], "language": m["language"],
                "difficulty": m["difficulty"], "harm_severity": m["harm_severity"],
                "title": m["title"], "prompt": it["input"],
                "process_control": m["process_control"],
                "expected_behaviour": m["expected_behaviour"],
                "control_pair": m["control_pair"],
                "harm_if_failed": m["harm_if_failed"],
                "unbiased_note": m["unbiased_note"],
                "regulator_reference": m["regulator_reference"],
                "placeholder_notice": m["placeholder_notice"],
            })


def report(meta, items, risky, control):
    print(f"{meta['name']} {meta['version']} — {len(items)} items")
    print(f"  balance      : {len(risky)} risk (block/escalate) vs {len(control)} control (allow)"
          f"  -> {'BALANCED' if len(risky) == len(control) else 'UNBALANCED'}")
    print(f"  targets      : {dict(sorted(Counter(i['target'] for i in items).items()))}")
    print(f"  modes        : {dict(sorted(Counter(i['metadata']['mode'] for i in items).items()))}")
    print(f"  agentic      : {dict(sorted(Counter(str(i['metadata']['agentic']) for i in items).items()))}")
    print(f"  languages    : {dict(sorted(Counter(i['metadata']['language'] for i in items).items()))}")
    print(f"  harm         : {dict(sorted(Counter(i['metadata']['harm_severity'] for i in items).items()))}")
    ph = [i["id"] for i in items if i["metadata"]["placeholder_notice"]]
    print(f"  placeholders : {len(ph)}/{len(items)} -> {', '.join(ph) if ph else 'none'}")
    print("\n  MODE DECLARATION — must be reported with any score:")
    for m, why in meta["DECLARATION"]["mode_values"].items():
        n = sum(1 for i in items if i["metadata"]["mode"] == m)
        print(f"    {m:<20} {n} item(s)  {why[:66]}")
    print("\n  PAIRS (no blanket policy can pass both halves):")
    seen = set()
    for i in items:
        cp = i["metadata"]["control_pair"]
        key = tuple(sorted([i["id"], cp]))
        if key in seen:
            continue
        seen.add(key)
        a = next(x for x in items if x["id"] == key[0])
        b = next(x for x in items if x["id"] == key[1])
        print(f"    {a['id']} ({a['target']:<8}) <-> {b['id']} ({b['target']:<8})  "
              f"{a['metadata']['category'][:34]}")


if __name__ == "__main__":
    meta, items, risky, control = load()
    build(meta, items)
    report(meta, items, risky, control)
    print("\nwrote: bankbench_tasks.json, bankbench_tasks.jsonl, bankbench_tasks.csv")
