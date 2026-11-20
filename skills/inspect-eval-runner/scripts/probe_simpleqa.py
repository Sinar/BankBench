"""Inspect a SimpleQA log: what was asked, what the model said, how the grader marked it.

Run before quoting any SimpleQA number. A model-graded Scorer is a Scorer like
any other, and the whole point of the gate is that a marking bug looks exactly
like a model failure.
"""
import glob
import sys

from inspect_ai.log import read_eval_log

pat = sys.argv[1] if len(sys.argv) > 1 else "logs/*simpleqa*.eval"
lg = read_eval_log(sorted(glob.glob(pat))[-1])

print(f"task   : {lg.eval.task}")
print(f"model  : {lg.eval.model}")
print(f"samples: {len(lg.samples)}")

# what scorers exist, and the aggregate
names = sorted({k for s in lg.samples for k in s.scores})
print(f"scorers: {names}")

for s in lg.samples:
    print("\n" + "=" * 74)
    print(f"ID: {s.id}")
    print(f"Q : {(s.input if isinstance(s.input, str) else str(s.input))[:300]}")
    print(f"TARGET (answer key): {s.target}")
    ans = (s.output.completion or "(EMPTY)")
    print(f"A : {ans[:600]}")
    for name in names:
        if name not in s.scores:
            continue
        sc = s.scores[name]
        print(f"  [{name}] value={sc.value!r}")
        if sc.explanation:
            print(f"      why: {sc.explanation[:500]}")
        if sc.metadata:
            print(f"      meta: {str(sc.metadata)[:300]}")
