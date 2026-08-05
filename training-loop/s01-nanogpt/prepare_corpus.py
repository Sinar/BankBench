#!/usr/bin/env python3
"""Build a tiny character-level corpus for nanoGPT from-scratch training.

Mixes: BankBench-MY prompt text (for domain flavor) + a Kaggle BM/Manglish
text sample (../../data/raw/malay-corpus/*, once downloaded via
../../data/download_kaggle.sh) + Shakespeare as filler if the corpus is too
small to train on meaningfully (nanoGPT needs a few hundred KB minimum to
not immediately overfit).

Run:
  python prepare_corpus.py --out corpus.txt
"""
import argparse
import json
from pathlib import Path

BANKBENCH_PATH = Path(__file__).resolve().parents[3] / "make-me-pay-eval" / "bankbench-20-tasks.json"
MALAY_CORPUS_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "malay-corpus"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("corpus.txt"))
    args = ap.parse_args()

    chunks = []

    if BANKBENCH_PATH.exists():
        tasks = json.loads(BANKBENCH_PATH.read_text())
        if isinstance(tasks, dict):
            tasks = tasks.get("tasks", tasks.get("samples", []))
        for t in tasks:
            text = t.get("prompt") or t.get("input") or t.get("scenario") or ""
            if text:
                chunks.append(text)

    if MALAY_CORPUS_DIR.exists():
        for p in MALAY_CORPUS_DIR.glob("**/*.txt"):
            chunks.append(p.read_text(errors="ignore"))
    else:
        print(f"WARNING: {MALAY_CORPUS_DIR} not found -- run data/download_kaggle.sh first "
              "for a BM/Manglish source, or the corpus will be BankBench-only (small).")

    corpus = "\n\n".join(chunks)
    if len(corpus) < 50_000:
        print(f"WARNING: corpus is only {len(corpus)} chars -- nanoGPT will overfit almost "
              "instantly at this size. Fine for a quick loop-sanity-check, not for a real "
              "sample-quality claim. Add more Kaggle text if you want a meaningful result.")

    args.out.write_text(corpus)
    print(f"Wrote {len(corpus)} chars to {args.out}")


if __name__ == "__main__":
    main()
