#!/usr/bin/env python3
"""Assemble smoke_benign.jsonl -- benign banking-domain requests used to check
for over-refusal after fine-tuning (S-02's second metric alongside compliance).

Source: Banking77 (or similar) from Kaggle, downloaded via download_kaggle.sh,
optionally passed through AdaptationAI to reframe as banking-agent-style
requests rather than raw intent-classification strings.

Run:
  python build_smoke_test.py --n 30
"""
import argparse
import csv
import json
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent / "raw" / "banking77"
OUT_PATH = Path(__file__).resolve().parent / "smoke_benign.jsonl"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30)
    args = ap.parse_args()

    if not RAW_DIR.exists():
        raise SystemExit(f"{RAW_DIR} missing -- run ./download_kaggle.sh first")

    csv_files = list(RAW_DIR.glob("*.csv"))
    if not csv_files:
        raise SystemExit(f"No CSV found in {RAW_DIR} -- check download_kaggle.sh output")

    rows = []
    with csv_files[0].open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            text_col = next((k for k in row if "text" in k.lower()), list(row.keys())[0])
            rows.append(row[text_col])
            if len(rows) >= args.n:
                break

    # TODO: run these through AdaptationAI to reframe as banking-agent-directed
    # requests (e.g. "What's my card limit?" -> "Hi, can you check my card limit
    # for me please?") rather than using raw intent-classification strings as-is.

    with OUT_PATH.open("w") as f:
        for text in rows:
            f.write(json.dumps({"prompt": text}) + "\n")

    print(f"Wrote {len(rows)} benign smoke-test prompts to {OUT_PATH}")


if __name__ == "__main__":
    main()
