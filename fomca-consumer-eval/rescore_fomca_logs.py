#!/usr/bin/env python3
"""Re-score stored FOMCA .eval logs with the CURRENT scorer, offline.

The stored completions are the evidence; the scorer is code and can be fixed.
After any rubric/marker edit, re-grade the old logs instead of re-running the
models — the model did not change, only the ruler did. Costs nothing.

    ./.venv/bin/python rescore_fomca_logs.py logs/fomca-phase-a_*.eval

Prints, per log: safety mean, help mean, inside-answer failures (worst),
over-refusals, plus the per-item harm table that is the FOMCA-facing output.
"""

import glob
import json
import sys
from collections import defaultdict
from pathlib import Path

from inspect_ai.log import read_eval_log

from fomca_scoring import score_sample

HERE = Path(__file__).resolve().parent


def load_meta_by_id():
    raw = json.loads((HERE / "fomca_tasks.json").read_text())
    out = {}
    for t in raw:
        md = dict(t["metadata"])
        md["target"] = t["target"]
        out[t["id"]] = md
    return out


def rescore(path: str, meta_by_id, verbose=True):
    lg = read_eval_log(path)
    model = lg.eval.model
    print(f"\n{'='*78}\n{lg.eval.task} | {model} | {len(lg.samples)} samples | {lg.eval.created}")

    per_item = defaultdict(list)
    inside_total, over_total, empty_total, skipped = 0, 0, 0, 0
    for s in lg.samples:
        if s.id not in meta_by_id:          # scorecard / meta runs carry no item
            skipped += 1
            continue
        md = meta_by_id[s.id]
        r = score_sample(md, s.output.completion or "")
        per_item[s.id].append(r)
        if r["empty_completion"]:
            empty_total += 1      # counted, NEVER averaged in
            continue
        inside_total += r["inside_answer_failure"]
        over_total += r["over_refusal"]

    scored = [(iid, r) for iid, rs in per_item.items() for r in rs if not r["empty_completion"]]
    if not scored:
        print("  no scoreable samples" + (f" ({skipped} meta samples skipped)" if skipped else ""))
        return None
    safety = [r["safety"] for _, r in scored]
    help_ = [r["help"] for _, r in scored]
    print(f"SAFETY mean {sum(safety)/len(safety):.3f}   HELP mean {sum(help_)/len(help_):.3f}"
          f"   (over {len(scored)} scoreable samples)")
    print(f"inside-answer failures: {inside_total}/{len(scored)}   over-refusals: {over_total}/{len(scored)}"
          f"   EMPTY completions: {empty_total} (excluded from rates — harness artifact)")

    if verbose:
        print("\nper-item (safety / help), empty samples excluded:")
        for iid in sorted(per_item):
            rs = [r for r in per_item[iid] if not r["empty_completion"]]
            md = meta_by_id[iid]
            n_empty = sum(1 for r in per_item[iid] if r["empty_completion"])
            if not rs:
                print(f"  {iid}  --/--  [{md['category']}] ALL EMPTY — no usable samples")
                continue
            s_m = sum(r["safety"] for r in rs) / len(rs)
            h_m = sum(r["help"] for r in rs) / len(rs)
            bad = sum(1 for r in rs if r["inside_answer_failure"])
            flags = []
            if bad:
                flags.append(f"INSIDE-ANSWER x{bad}")
            if any(r["over_refusal"] for r in rs):
                flags.append("OVER-REFUSAL")
            if n_empty:
                flags.append(f"empty x{n_empty}")
            if md["harm_severity"] == "high" and s_m < 1.0:
                flags.append("HIGH-HARM FAIL")
            print(f"  {iid}  {s_m:.2f} / {h_m:.2f}  [{md['category']}] {' '.join(flags)}")
            if flags and s_m < 1.0:
                print(f"        harm: {md['harm_if_failed'][:150]}")
    return {"model": model, "task": lg.eval.task,
            "safety": sum(safety)/len(safety), "help": sum(help_)/len(help_),
            "inside_answer": inside_total, "over_refusals": over_total,
            "empty": empty_total, "n": len(scored)}


if __name__ == "__main__":
    meta_by_id = load_meta_by_id()
    args = sys.argv[1:] or sorted(glob.glob(str(HERE / "logs" / "*.eval")))
    rows = []
    for a in args:
        for p in sorted(glob.glob(a)):
            try:
                rows.append(rescore(p, meta_by_id))
            except Exception as e:
                print(f"  ! {p}: {e}")
    rows = [r for r in rows if r]
    if len(rows) > 1:
        print(f"\n{'='*78}\nSUMMARY (empty completions excluded from safety/help)")
        print(f"{'task':<22} {'model':<44} {'n':>3} {'safety':>7} {'help':>7} {'inside':>7} {'empty':>6}")
        for r in rows:
            print(f"{r['task'][:22]:<22} {r['model'][:44]:<44} {r['n']:>3} "
                  f"{r['safety']:>7.3f} {r['help']:>7.3f} {r['inside_answer']:>7} {r['empty']:>6}")
