#!/usr/bin/env python3
"""Audit OLMo-2's public Dolma training-data mixture for content relevant to the
banking / Bahasa Malaysia / Manglish domain BankBench-MY tests.

This is the step Qwen/Gemma/Tinker fine-tunes CANNOT do -- their pretraining
data mixtures aren't public, so contamination can't be ruled in or out.

TODO: point --dolma-index at the actual Dolma dataset index/manifest once
downloaded (https://github.com/allenai/dolma) -- this skeleton assumes a
local manifest file, fill in the real path/format before running.

Run:
  python provenance_audit.py --dolma-index /path/to/dolma-manifest.json
"""
import argparse
import json
from pathlib import Path

KEYWORDS = ["bahasa malaysia", "manglish", "maybank", "cimb", "bank negara", "rmit", "kyc", "otp"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dolma-index", type=Path, required=False)
    ap.add_argument("--out", type=Path, default=Path("provenance_audit.json"))
    args = ap.parse_args()

    if not args.dolma_index or not args.dolma_index.exists():
        print("No local Dolma manifest provided -- documenting the audit PLAN instead of running it.")
        audit = {
            "stage": "s04",
            "status": "plan-only",
            "sources_to_check": [
                "Dolma source list (web, code, papers, books, Reddit, Wikipedia, etc.) by license/provenance",
                f"Keyword sweep for domain terms: {KEYWORDS}",
                "Any Malaysian-government or banking-sector domains in the web crawl subset",
            ],
            "note": "TODO: download Dolma manifest/index and rerun with --dolma-index set",
        }
    else:
        manifest = json.loads(args.dolma_index.read_text())
        # TODO: real matching logic once manifest schema is known
        audit = {"stage": "s04", "status": "TODO-implement-real-scan", "manifest_sources": len(manifest)}

    args.out.write_text(json.dumps(audit, indent=2))
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
