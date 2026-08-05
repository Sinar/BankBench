#!/usr/bin/env python3
"""Check whether held-out BankBench-MY prompts (or close paraphrases) already
appear in OLMo's public Dolma training mixture -- if so, the S-04 "held-out"
re-eval claim is contaminated and needs a caveat.

TODO: replace the naive substring check with an actual n-gram overlap /
embedding-similarity search against the Dolma index once provenance_audit.py
has a real manifest wired in.

Run:
  python contamination_check.py
"""
import json
from pathlib import Path

HELDOUT = Path(__file__).resolve().parents[1] / "data" / "sft_heldout.jsonl"
OUT = Path(__file__).resolve().parent / "contamination_report.json"


def main():
    if not HELDOUT.exists():
        raise SystemExit(f"{HELDOUT} missing -- run data/prepare_bankbench_sft.py first")

    heldout = [json.loads(l) for l in HELDOUT.read_text().splitlines() if l.strip()]

    report = {
        "stage": "s04",
        "heldout_tasks_checked": len(heldout),
        "status": "TODO-implement-real-overlap-search",
        "note": (
            "Placeholder -- wire this to provenance_audit.py's Dolma manifest once "
            "downloaded, and run an n-gram or embedding overlap search per held-out "
            "prompt. Until then, treat the S-04 held-out claim as unverified for "
            "contamination, same caveat level as S-02's."
        ),
    }
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
