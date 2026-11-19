#!/usr/bin/env python3
"""Build the FOMCA consumer-harm eval dataset from items/*.json.

One source of truth (the 10 per-item files, each independently reviewable),
three machine formats out. Asserts the schema programmatically and prints the
real counts from the real file — never describes them from memory.

    python3 build_fomca_dataset.py
"""

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEMS = HERE / "items"

REQUIRED_ITEM_KEYS = {"id", "input", "target", "metadata"}
REQUIRED_META_KEYS = {
    "category", "title", "language", "difficulty", "consumer_scenario",
    "expected_behaviour", "good_answer", "failure_signature", "what_it_catches",
    "must_include", "must_not_include", "safe_actions", "require_any_of",
    "harm_if_failed", "harm_severity", "probe_question", "verification_criteria",
    "regulator_reference", "placeholder_notice",
}
VALID_TARGETS = {"refuse", "warn", "answer"}
VALID_SEVERITY = {"high", "medium", "low"}

CSV_FIELDS = [
    "id", "category", "language", "difficulty", "target", "harm_severity",
    "title", "prompt", "expected_behaviour", "failure_signature",
    "what_it_catches", "harm_if_failed", "must_include", "must_not_include",
    "regulator_reference", "placeholder_notice",
]


def load_items():
    paths = sorted(ITEMS.glob("FOMCA-*.json"))
    if not paths:
        sys.exit(f"No item files found under {ITEMS}")
    items, problems = [], []
    for p in paths:
        d = json.loads(p.read_text())
        missing = REQUIRED_ITEM_KEYS - set(d)
        if missing:
            problems.append(f"{p.name}: missing item keys {sorted(missing)}")
        meta = d.get("metadata", {})
        missing_meta = REQUIRED_META_KEYS - set(meta)
        if missing_meta:
            problems.append(f"{p.name}: missing metadata keys {sorted(missing_meta)}")
        if d.get("target") not in VALID_TARGETS:
            problems.append(f"{p.name}: target {d.get('target')!r} not in {VALID_TARGETS}")
        if meta.get("harm_severity") not in VALID_SEVERITY:
            problems.append(f"{p.name}: harm_severity {meta.get('harm_severity')!r} invalid")
        for lst in ("must_include", "must_not_include", "require_any_of", "safe_actions"):
            if not isinstance(meta.get(lst), list):
                problems.append(f"{p.name}: metadata.{lst} must be a list")
        items.append(d)
    if problems:
        sys.exit("SCHEMA CHECK FAILED:\n  " + "\n  ".join(problems))

    ids = [i["id"] for i in items]
    if len(set(ids)) != len(ids):
        sys.exit(f"Duplicate ids: {ids}")
    items.sort(key=lambda i: i["id"])
    return items


def write_outputs(items):
    (HERE / "fomca_tasks.json").write_text(json.dumps(items, indent=2) + "\n")
    with (HERE / "fomca_tasks.jsonl").open("w") as f:
        for it in items:
            f.write(json.dumps(it) + "\n")
    with (HERE / "fomca_tasks.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        for it in items:
            m = it["metadata"]
            w.writerow({
                "id": it["id"], "category": m["category"], "language": m["language"],
                "difficulty": m["difficulty"], "target": it["target"],
                "harm_severity": m["harm_severity"], "title": m["title"],
                "prompt": it["input"], "expected_behaviour": m["expected_behaviour"],
                "failure_signature": m["failure_signature"],
                "what_it_catches": m["what_it_catches"],
                "harm_if_failed": m["harm_if_failed"],
                "must_include": " | ".join(m["must_include"]),
                "must_not_include": " | ".join(m["must_not_include"]),
                "regulator_reference": m["regulator_reference"],
                "placeholder_notice": m["placeholder_notice"],
            })


def report(items):
    def tally(key, get):
        counts = {}
        for it in items:
            counts[get(it)] = counts.get(get(it), 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: str(kv[0])))

    print(f"items: {len(items)}  ids: {', '.join(i['id'] for i in items)}")
    for label, get in [
        ("target", lambda i: i["target"]),
        ("category", lambda i: i["metadata"]["category"]),
        ("language", lambda i: i["metadata"]["language"]),
        ("difficulty", lambda i: i["metadata"]["difficulty"]),
        ("harm_severity", lambda i: i["metadata"]["harm_severity"]),
    ]:
        print(f"{label}: {tally(label, get)}")
    ph = [i["id"] for i in items if i["metadata"]["placeholder_notice"]]
    print(f"placeholder_notice=true: {len(ph)}/{len(items)} -> {', '.join(ph)}")
    print("----- REVIEW TABLE -----")
    for i in items:
        m = i["metadata"]
        print(f"{i['id']} | {i['target']:<6} | d{m['difficulty']} | {m['harm_severity']:<6} | "
              f"{m['language']:<9} | {m['category']}")
        print(f"        {m['title']}")


if __name__ == "__main__":
    items = load_items()
    write_outputs(items)
    report(items)
    print("\nwrote: fomca_tasks.json, fomca_tasks.jsonl, fomca_tasks.csv")
