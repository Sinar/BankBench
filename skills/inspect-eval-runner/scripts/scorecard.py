#!/usr/bin/env python3
"""AISL Scorecard of AI Evaluation Quality — generic engine.

Grades ANY evaluation in this repo against San Joaquin, Gipiskis & Chin
(Feb 2026): five dimensions scored 1 (best) to 4 (worst), then classified into
a category (A ideal .. E exploratory) using the paper's Table 7 minimum
components. The highest category whose minimums are all met wins.

This is the AISL half of the pipeline. It is deliberately SEPARATE from the
eval run: the grade is a property of the evaluation design, not of any model
you happened to run against it. Grade once; re-use across models.

    python3 scorecard.py <assessment.json>
    python3 scorecard.py --suite ../suites/fomca-consumer-eval
    python3 scorecard.py <assessment.json> --json

WHAT IS NOT COMPUTED, AND WHY
  The paper's §3.1 colour-downgrade rule (yellow=2 / orange=3 / red=4 on an
  unsatisfied highlighted item) needs the highlight colours, which are
  formatting that does not survive markdown extraction of the paper and have no
  structured copy in this repo. Guessing them would fabricate the grade, so
  dimension scores are taken directly from the assessment file and the colour
  pass is reported as an open item.

A scorecard written by the team that built the eval is a SELF-assessment. It is
not an independent third-party grade, and the paper says so too.
"""

import argparse
import json
import sys
from pathlib import Path

DIMENSIONS = [
    "construct_validity", "internal_validity", "external_validity",
    "reliability", "correctness",
]
DIM_LABELS = {
    "construct_validity": "Construct Validity",
    "internal_validity": "Internal Validity",
    "external_validity": "External Validity",
    "reliability": "Reliability",
    "correctness": "Correctness",
}

# Table 7 — the minimum component requirement per dimension per category.
# "E  4 Construct Validity + 3 Internal Validity + ..." reads as: the dimension
# score may be as bad as that number. 1 = best, 4 = worst.
CATEGORY_MIN = {
    "A": {"construct_validity": 1, "internal_validity": 1, "external_validity": 1, "reliability": 1, "correctness": 1},
    "B": {"construct_validity": 2, "internal_validity": 2, "external_validity": 1, "reliability": 1, "correctness": 1},
    "C": {"construct_validity": 2, "internal_validity": 2, "external_validity": 1, "reliability": 2, "correctness": 2},
    "D": {"construct_validity": 3, "internal_validity": 3, "external_validity": 3, "reliability": 3, "correctness": 3},
    "E": {"construct_validity": 4, "internal_validity": 3, "external_validity": 4, "reliability": 4, "correctness": 4},
}
CATEGORY_ORDER = ["A", "B", "C", "D", "E"]
CATEGORY_INDEX = {c: i + 1 for i, c in enumerate(CATEGORY_ORDER)}
CATEGORY_LABEL = {
    "A": "Ideal for major policy decisions",
    "B": "Minimum for major policy decisions",
    "C": "Final model checkpoint — not enough for external governance action",
    "D": "During model development / community-driven evaluation",
    "E": "Exploratory research — results not indicative of real abilities",
}
CATEGORY_CAUTION = {
    "A": "Usable as a policy aid for immediate-harm and complex-behaviour risks.",
    "B": "Usable for major policy decisions alongside other evaluation tools.",
    "C": "Trust at a superficial level only, and always with a disclaimer. NOT a basis for external governance action.",
    "D": "Indicators of research direction or product signal; corroborate before relying on it.",
    "E": "Rapid prototyping only. Treat results as noisy. Do NOT use for significant decisions, and do not quote externally as a model finding.",
}


def classify(scores: dict) -> str:
    """Highest category whose Table 7 minimum is met on every dimension."""
    for cat in CATEGORY_ORDER:
        req = CATEGORY_MIN[cat]
        if all(scores[d] <= req[d] for d in DIMENSIONS):
            return cat
    return "E"


def capping_dimensions(scores: dict, category: str) -> list:
    """The dimensions blocking the next-better category — the binding constraints."""
    i = CATEGORY_ORDER.index(category)
    if i == 0:
        return []
    better = CATEGORY_ORDER[i - 1]
    return [d for d in DIMENSIONS if scores[d] > CATEGORY_MIN[better][d]]


def find_assessment(suite_dir: Path) -> Path:
    hits = sorted(suite_dir.glob("**/*assessment*.json"))
    if not hits:
        sys.exit(f"No *assessment*.json found under {suite_dir}")
    return hits[0]


def load(path: Path):
    data = json.loads(path.read_text())
    evals = data.get("evals") or {}
    if not evals:
        sys.exit(f"{path} has no 'evals' entry")
    key = next(iter(evals))
    entry = evals[key]
    scores = {d: entry["assessment"][d]["score"] for d in DIMENSIONS}
    graded = {
        "suite": entry.get("display", key),
        "status": entry.get("status", ""),
        "scores": scores,
        "category": classify(scores),
        "capping": capping_dimensions(scores, classify(scores)),
        "assessed_by": data.get("assessed_by", "self-assessment (not third-party)"),
        "framework": data.get("paper", "Scorecard of AI Evaluation Quality (Feb 2026)"),
        "assessment_file": str(path),
    }
    graded["category_label"] = CATEGORY_LABEL[graded["category"]]
    graded["category_index"] = CATEGORY_INDEX[graded["category"]]
    graded["caution"] = CATEGORY_CAUTION[graded["category"]]
    return graded, entry


def render_text(g: dict) -> str:
    L = []
    L.append("=" * 74)
    L.append(f"AISL SCORECARD — {g['suite']}")
    L.append(f"Framework: {g['framework']}")
    L.append("=" * 74)
    L.append("")
    L.append(f"  GRADE: Category {g['category']}  (index {g['category_index']} of 5; 1 = best)")
    L.append(f"         {g['category_label']}")
    L.append("")
    if g["capping"]:
        L.append("  Held back by: " + ", ".join(
            f"{DIM_LABELS[d]} ({g['scores'][d]}/4)" for d in g["capping"]))
        L.append("")
    L.append("  Dimension                     Score   (1 = best .. 4 = worst)")
    for d in DIMENSIONS:
        s = g["scores"][d]
        L.append(f"    {DIM_LABELS[d]:<26}  {s}   [{'#' * s}{'.' * (4 - s)}]")
    L.append("")
    L.append("  Table 7 classification check:")
    for cat in CATEGORY_ORDER:
        req = CATEGORY_MIN[cat]
        ok = all(g["scores"][d] <= req[d] for d in DIMENSIONS)
        need = " ".join(f"{DIM_LABELS[d].split()[0][:4]}<={req[d]}" for d in DIMENSIONS)
        mark = "PASS" if ok else "fail"
        arrow = "   <-- assigned" if cat == g["category"] else ""
        L.append(f"    {cat}  {mark:<4} needs {need}{arrow}")
    L.append("")
    L.append(f"  How to use this result: {g['caution']}")
    L.append("")
    L.append(f"  Assessed by: {g['assessed_by']}")
    L.append("  Colour-downgrade rule (paper §3.1) NOT applied — highlight colours are")
    L.append("  not recoverable from the paper source. Treated as an open item.")
    L.append(f"  Assessment file: {g['assessment_file']}")
    return "\n".join(L)


def render_markdown(g: dict, entry: dict) -> str:
    L = [f"# AISL Scorecard — {g['suite']}\n",
         f"**Grade: Category {g['category']}** — {g['category_label']}  ",
         f"**Framework:** {g['framework']}  ",
         f"**Assessed by:** {g['assessed_by']}\n"]
    if g["capping"]:
        L.append("**Held back by:** " + ", ".join(
            f"{DIM_LABELS[d]} ({g['scores'][d]}/4)" for d in g["capping"]) + "\n")
    L.append("| Dimension | Score | Bar | Blocks? |\n|---|---|---|---|")
    for d in DIMENSIONS:
        s = g["scores"][d]
        L.append(f"| {DIM_LABELS[d]} | **{s}**/4 | `{'#'*s}{'.'*(4-s)}` | "
                 f"{'yes' if d in g['capping'] else '—'} |")
    L.append("\n## Table 7 check\n")
    L.append("| Category | Status | Minimum components |\n|---|---|---|")
    for cat in CATEGORY_ORDER:
        req = CATEGORY_MIN[cat]
        ok = all(g["scores"][d] <= req[d] for d in DIMENSIONS)
        need = " + ".join(f"{req[d]} {DIM_LABELS[d]}" for d in DIMENSIONS)
        mark = "**PASS**" if ok else "fail"
        if cat == g["category"]:
            mark += " ← assigned"
        L.append(f"| {cat} | {mark} | {need} |")
    L.append(f"\n> {g['caution']}\n")
    L.append("\n## Per-dimension detail\n")
    for d in DIMENSIONS:
        a = entry["assessment"][d]
        L.append(f"### {DIM_LABELS[d]} — {a['score']}/4\n")
        L.append("**Satisfied**")
        L += [f"- {x}" for x in a["satisfied"]]
        L.append("\n**Gaps**")
        L += [f"- {x}" for x in a["gaps"]]
        L.append(f"\n**Justification.** {a['justification']}\n")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("assessment", nargs="?", help="path to an *assessment*.json")
    ap.add_argument("--suite", help="suite dir; auto-discovers the assessment file")
    ap.add_argument("--json", action="store_true", help="machine-readable grade")
    ap.add_argument("--write", action="store_true", help="also write .md next to it")
    args = ap.parse_args()

    if args.suite:
        path = find_assessment(Path(args.suite))
    elif args.assessment:
        path = Path(args.assessment)
    else:
        ap.error("give an assessment file or --suite <dir>")

    g, entry = load(path)
    if args.json:
        print(json.dumps(g, indent=2))
    else:
        print(render_text(g))
    if args.write:
        out = path.parent / "scorecard_report.md"
        out.write_text(render_markdown(g, entry))
        print(f"\nwrote: {out}")
