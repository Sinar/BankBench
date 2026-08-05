#!/usr/bin/env python3
"""Diff Tinker's fine-tune result against the local S-02 LoRA result.

Run:
  python compare_to_s02.py
"""
import json
from pathlib import Path

S02_RESULTS = Path(__file__).resolve().parents[1] / "s02-finetune" / "results.json"
TINKER_LOG = Path(__file__).resolve().parent / "tinker_run_log.json"
OUT = Path(__file__).resolve().parent / "comparison.json"


def main():
    if not S02_RESULTS.exists():
        raise SystemExit(f"{S02_RESULTS} missing -- finish S-02 before comparing")
    if not TINKER_LOG.exists():
        raise SystemExit(f"{TINKER_LOG} missing -- run finetune_tinker.py first")

    s02 = json.loads(S02_RESULTS.read_text())
    tinker = json.loads(TINKER_LOG.read_text())

    comparison = {
        "stage": "s03",
        "local_loop": {"heldout_refusal_rate": s02.get("finetuned", {}).get("heldout_refusal_rate")},
        "tinker_loop": tinker,  # TODO: shape once finetune_tinker.py's real output format is known
        "note": "TODO: fill in qualitative diff -- what Tinker abstracted away vs. what it still required you to specify",
    }
    OUT.write_text(json.dumps(comparison, indent=2))
    print(json.dumps(comparison, indent=2))


if __name__ == "__main__":
    main()
