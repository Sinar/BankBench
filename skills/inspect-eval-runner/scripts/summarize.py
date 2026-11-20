#!/usr/bin/env python3
"""Summarise + analyse eval results in plain language.

The analysis half of the pipeline. Reads every .eval log in a directory and
answers the three questions a non-technical reader actually has:

    1. What ran?            (which task, which model, how many questions)
    2. How did it score?    (one row per scorer, per run)
    3. What failed, and why does it matter?   (item-level, plain-language harm)

    python3 summarize.py logs/
    python3 summarize.py logs/ --suite ../suites/fomca-consumer-eval
    python3 summarize.py logs/ --json

Design note for agents: this uses `read_eval_log` directly rather than
`inspect_ai.analysis`, because the per-item harm text lives in the suite's own
item files and the two tables wanted here are small. For heavier cross-log work
(score distributions, model leaderboards, outlier hunting) use
`inspect_ai.analysis` from a REPL instead — see the SKILL.md routing table.

TWO HONESTY RULES ARE ENFORCED HERE:
  * Empty completions are counted and EXCLUDED from the rates. A blank answer
    is a harness fault (reasoning tokens ate max_tokens, a 404, a dropped
    stream) — never report it as a model failure.
  * Every item row carries the consequence in plain language, so a failure is
    legible to someone who will never read a scorer.
"""

import argparse
import glob
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from inspect_ai.log import read_eval_log


def load_item_meta(suite_dir: Path):
    """id -> metadata, from the suite's built items file (or items/*.json)."""
    meta = {}
    built = list(suite_dir.glob("*tasks.json")) + list(suite_dir.glob("**/*tasks.json"))
    for b in built:
        try:
            for t in json.loads(b.read_text()):
                md = dict(t.get("metadata", {}))
                md["target"] = t.get("target")
                md.setdefault("input", t.get("input", ""))
                meta[t["id"]] = md
        except Exception:
            pass
    if meta:
        return meta
    for p in sorted(suite_dir.glob("items/*.json")):
        try:
            t = json.loads(p.read_text())
            md = dict(t.get("metadata", {}))
            md["target"] = t.get("target")
            md.setdefault("input", t.get("input", ""))
            meta[t["id"]] = md
        except Exception:
            pass
    return meta


def summarise(log_path, item_meta):
    lg = read_eval_log(log_path)
    scorer_names = []
    for s in lg.samples:
        for k in s.scores:
            if k not in scorer_names:
                scorer_names.append(k)

    per_scorer = defaultdict(list)
    per_item = defaultdict(lambda: defaultdict(list))
    labels = defaultdict(list)
    empty = 0
    for s in lg.samples:
        blank = not (s.output.completion or "").strip()
        if blank:
            empty += 1
        for name in scorer_names:
            if name not in s.scores:
                continue
            v = s.scores[name].value
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                # A LABEL score — e.g. the grade, or SimpleQA's 'C'/'I'.
                # Never averaged here and never reported as a failure: coercing
                # a label to 0.00 invents a model failure. Suites with label
                # scores report their aggregate metrics instead (see below).
                labels[name].append(str(v))
                continue
            n = float(v)
            per_item[s.id][name].append((n, blank))
            if not blank:
                per_scorer[name].append(n)

    # Aggregate metrics Inspect already recorded (accuracy, stderr, ...). This is
    # the ONLY correct source for suites whose scorer emits labels: inspect_evals
    # computes 0.44 from 'C'/'I', and we must read that rather than average the
    # strings ourselves. `results.metrics` is deprecated; prefer `results.scores`.
    aggregates = {}
    res = getattr(lg, "results", None)
    if res is not None:
        try:
            for entry in (getattr(res, "scores", None) or []):
                nm = getattr(entry, "name", None) or getattr(entry, "scorer", None)
                metrics = getattr(entry, "metrics", None) or {}
                vals = {}
                for mk, mv in metrics.items():
                    v = getattr(mv, "value", mv)
                    if isinstance(v, (int, float)):
                        vals[mk] = float(v)
                if nm and vals:
                    aggregates[nm] = vals
        except Exception:
            pass
    if not aggregates:
        for mk, mv in (getattr(res, "metrics", None) or {}).items():
            v = getattr(mv, "value", mv)
            if isinstance(v, (int, float)):
                aggregates.setdefault("__all__", {})[mk] = float(v)

    return {
        "file": Path(log_path).name,
        "task": lg.eval.task,
        "model": lg.eval.model,
        "created": str(lg.eval.created)[:19],
        "n_samples": len(lg.samples),
        "n_scored": len(lg.samples) - empty,
        "n_empty": empty,
        "means": {k: (sum(v) / len(v) if v else float("nan")) for k, v in per_scorer.items()},
        "labels": {k: sorted(set(v)) for k, v in labels.items()},
        "label_counts": {k: dict(sorted(Counter(v).items())) for k, v in labels.items()},
        "aggregates": aggregates,
        "per_item": {i: {k: v for k, v in d.items()} for i, d in per_item.items()},
        "status": str(getattr(lg, "status", "")),
    }


def print_run(r, item_meta):
    print(f"\n{'='*74}")
    print(f"{r['task']}  |  {r['model']}")
    print(f"{'='*74}")
    print(f"  when            : {r['created']}")
    print(f"  questions run   : {r['n_samples']}")
    if r["n_empty"]:
        print(f"  usable answers  : {r['n_scored']}   "
              f"({r['n_empty']} empty — HARNESS fault, excluded from the rates below)")
    print()
    print("  HOW IT SCORED  (0.0 = worst, 1.0 = best)")
    for name, m in r["means"].items():
        bar = "#" * int(round(m * 20))
        print(f"    {name:<24} {m:.3f}  {bar}")
    agg = r.get("aggregates") or {}
    # Suites whose scorer emits labels ('C'/'I', "Category E") have no per-sample
    # number to average. Report the aggregate metric Inspect computed instead of
    # inventing one — and show the raw label counts so the split is visible.
    for name, vals in r.get("labels", {}).items():
        counts = r.get("label_counts", {}).get(name, {})
        dist = "  ".join(f"{k}={v}" for k, v in counts.items())
        print(f"    {name:<24} label scores  {dist}")
        for mk, mv in (agg.get(name) or {}).items():
            print(f"      {mk:<22} {mv:.3f}")
    for name, vals in agg.items():
        if name == "__all__" or name in r.get("labels", {}):
            continue
        line = "  ".join(f"{mk}={mv:.3f}" for mk, mv in vals.items())
        print(f"    {name:<24} {line}")
    print()

    # item-level: anything not perfect on any scorer, worst first
    bad = []
    for iid, sc in r["per_item"].items():
        for name, vals in sc.items():
            usable = [v for v, blank in vals if not blank]
            if not usable:
                continue
            m = sum(usable) / len(usable)
            if m < 1.0:
                bad.append((m, iid, name, len(usable) - sum(1 for v in usable if v == 1.0)))
    if bad:
        print("  WHAT DID NOT GO PERFECTLY  (and why it matters)")
        seen = set()
        for m, iid, name, nbad in sorted(bad):
            md = item_meta.get(iid, {})
            key = (iid, name)
            if key in seen:
                continue
            seen.add(key)
            sev = (md.get("harm_severity") or "?").upper()
            print(f"    {iid}  {name} = {m:.2f}   [{sev} harm]  "
                  f"{md.get('category', '')}")
            if md.get("title"):
                print(f"        {md['title']}")
            if md.get("harm_if_failed"):
                print(f"        consequence: {md['harm_if_failed'][:180]}")
        print()
    elif r["means"]:
        print("  Every question scored full marks on every scorer.\n")
        print("  Read that with suspicion rather than relief: a set that passes")
        print("  everything is not discriminating. Re-run with --epochs 3 and read")
        print("  a few answers by hand before believing it.\n")
    else:
        # Label-scored suite: `per_item` is empty because there is no per-sample
        # number, so the "everything passed" branch above must NOT be reachable.
        # It previously was, and cheerfully reported full marks for a run where
        # 14 of 25 answers were wrong.
        print("  This suite marks with LABELS, not numbers, so there is no")
        print("  per-question number to average. The split under HOW IT SCORED")
        print("  above IS the result — and it is emphatically not an all-pass.")
        print("  Open the viewer to read the individual answers and why each was")
        print("  marked the way it was.\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="?", default="logs", help="log dir or glob")
    ap.add_argument("--suite", help="suite dir, for plain-language item text")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="write the summary as markdown here")
    args = ap.parse_args()

    item_meta = load_item_meta(Path(args.suite)) if args.suite else {}
    paths = sorted(glob.glob(str(Path(args.logs) / "*.eval"))) or sorted(glob.glob(args.logs))
    if not paths:
        sys.exit(f"No .eval logs found at {args.logs!r}. Run the eval first.")

    runs = []
    for p in paths:
        try:
            runs.append(summarise(p, item_meta))
        except Exception as e:
            print(f"  ! skipped {p}: {e}")

    if args.json:
        print(json.dumps(runs, indent=2, default=str))
        return

    print("EVAL RESULT SUMMARY")
    print(f"logs read: {len(runs)}   from: {args.logs}")
    if item_meta:
        print(f"item text: {len(item_meta)} questions loaded from {args.suite}")

    print(f"\n{'RUN':<44} {'MODEL':<38} {'Q':>4} {'EMPTY':>6}  SCORES")
    for r in sorted(runs, key=lambda x: x["created"]):
        parts = [f"{k}={v:.2f}" for k, v in r["means"].items()]
        if not parts:
            # label-scored suite: show the aggregate metric instead of nothing
            for _nm, vals in (r.get("aggregates") or {}).items():
                parts += [f"{mk}={mv:.2f}" for mk, mv in vals.items()]
        print(f"{r['task'][:44]:<44} {r['model'][:38]:<38} {r['n_scored']:>4} "
              f"{r['n_empty']:>6}  {'  '.join(parts)}")

    for r in runs:
        print_run(r, item_meta)

    print("=" * 74)
    print("NEXT: open the interactive viewer for transcripts and per-question detail:")
    print(f"    inspect view --log-dir {args.logs}")
    print("=" * 74)


if __name__ == "__main__":
    main()
