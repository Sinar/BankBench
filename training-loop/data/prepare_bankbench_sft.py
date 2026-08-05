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
    """TODO: replace with the actual refusal-with-explanation you want the model to learn.

    For now this is a template stub -- swap in real graded transcripts (Cetavals A-D)
    from your BankBench-MY run logs where the model scored well (grade C/D refusals),
    rather than hand-writing a generic refusal for every task. Using YOUR OWN best
    transcripts as targets is what makes this fine-tune meaningful instead of generic.
    """
    return (
        "I can't help with that request as described. "
        f"[TODO: fill in a real graded refusal transcript for task id={task.get('id', '?')} "
        "from an existing BankBench-MY run log, not this placeholder.]"
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
