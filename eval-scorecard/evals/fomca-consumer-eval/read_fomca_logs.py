#!/usr/bin/env python3
"""Read a FOMCA .eval log and print per-item scores with explanations.

    ./.venv/bin/python read_fomca_logs.py logs/<file>.eval

Never hand-type a number out of the Inspect display — read it from the log.
"""

import glob
import sys
from pathlib import Path

from inspect_ai.log import read_eval_log

HERE = Path(__file__).resolve().parent


def report(path: str, verbose: bool = True):
    lg = read_eval_log(path)
    print(f"\n=== {lg.eval.task} | model: {lg.eval.model} | samples: {len(lg.samples)} "
          f"| created: {lg.eval.created}")
    keys = []
    for s in lg.samples:
        for k in s.scores:
            if k not in keys:
                keys.append(k)
    means = {}
    for k in keys:
        vals = [s.scores[k].value for s in lg.samples if k in s.scores]
        means[k] = sum(vals) / len(vals) if vals else float("nan")
    print("means: " + " | ".join(f"{k} {means[k]:.3f}" for k in keys))

    for s in lg.samples:
        row = " ".join(f"{k}={s.scores[k].value:g}" for k in keys if k in s.scores)
        print(f"  {s.id:<10} {row}")
        if verbose:
            for k in keys:
                if k in s.scores:
                    print(f"        [{k}] {s.scores[k].explanation}")
            comp = (s.output.completion or "").replace("\n", " ")
            print(f"        [out] {comp[:300]}")
    return means


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = sorted(glob.glob(str(HERE / "logs" / "*.eval")))
        if not args:
            sys.exit("no .eval files found")
    for a in args:
        for p in glob.glob(a):
            report(p)
