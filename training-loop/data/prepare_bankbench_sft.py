#!/usr/bin/env python3
"""BankBench-MY tasks -> SFT (prompt, completion) pairs, with a held-out split.

Reads the existing eval task set (not re-collected) and produces:
  data/sft_train.jsonl     -- held-in tasks, used for fine-tuning
  data/sft_heldout.jsonl   -- held-out tasks, used ONLY for before/after re-eval

Run:
  python prepare_bankbench_sft.py --n-heldout 5 --seed 42
"""
import argparse
import json
import random
from pathlib import Path

BANKBENCH_PATH = Path(__file__).resolve().parents[3] / "make-me-pay-eval" / "bankbench-20-tasks.json"
OUT_DIR = Path(__file__).resolve().parent


def build_target_refusal(task: dict) -> str:
    """Safe-refusal-with-explanation template used as the SFT completion target.

    NOTE: this is a structural template, NOT a graded transcript. The data/README
    calls for swapping these in for YOUR OWN best BankBench-MY run transcripts
    (Cetavals C/D refusals from an actual eval run) so the fine-tune learns your
    graded style rather than a generic refusal. Until those run logs exist, this
    template keeps the SFT file functional for a dry-run / pipeline sanity check.
    """
    category = (task.get("metadata") or {}).get("category", "adversarial request")
    title = (task.get("metadata") or {}).get("title", "")
    return (
        "I can't help with that request as described. "
        f"It looks like a {category} scenario ({title}), and acting on it could put your "
        "money or account at risk. I'll keep standard verification and confirmation steps "
        "in place rather than bypass them. If you believe this is a legitimate request, "
        "please confirm the details through your bank's official app or a verified channel "
        "and I can walk you through the safe steps."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-heldout", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--bankbench-path", type=Path, default=BANKBENCH_PATH)
    args = ap.parse_args()

    tasks = json.loads(args.bankbench_path.read_text())
    if isinstance(tasks, dict):
        tasks = tasks.get("tasks", tasks.get("samples", []))

    random.Random(args.seed).shuffle(tasks)
    heldout, train = tasks[: args.n_heldout], tasks[args.n_heldout :]

    def write(path: Path, rows: list[dict]):
        with path.open("w") as f:
            for t in rows:
                prompt = t.get("prompt") or t.get("input") or t.get("scenario")
                completion = build_target_refusal(t)
                f.write(json.dumps({"prompt": prompt, "completion": completion, "task_id": t.get("id")}) + "\n")

    write(OUT_DIR / "sft_train.jsonl", train)
    write(OUT_DIR / "sft_heldout.jsonl", heldout)
    print(f"train={len(train)} heldout={len(heldout)} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
