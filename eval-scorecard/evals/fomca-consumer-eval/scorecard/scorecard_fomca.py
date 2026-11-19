#!/usr/bin/env python3
"""Scorecard of AI Evaluation Quality — applied to the FOMCA consumer-harm set.

Implements the framework in San Joaquin, Gipiskis & Chin (Feb 2026),
`scorecard-full-paper.md`, §3 dimensions + §4 Table 7 classification.

    ./.venv/bin/python scorecard_fomca.py            # print the scorecard + grade
    ./.venv/bin/python scorecard_fomca.py --write     # also write .md + .json

WHAT THIS COMPUTES
  Each dimension is scored 1 (best) to 4 (worst). Table 7 gives minimum
  components per dimension per category, and the paper says an evaluation is
  assigned "the highest possible category that they satisfy" — so we walk
  A -> E and take the first category whose minimum is met on every dimension.
  E is the catch-all (it accepts 4 on most dimensions).

THE ONE RULE WE DO NOT APPLY, AND WHY
  §3.1: an unsatisfied *highlighted* item automatically downgrades its dimension
  (yellow=2, orange=3, red=4), and an unsatisfied *non-highlighted* applicable
  item makes the dimension outright INVALID. That needs the highlight colours.
  The colours are formatting that does not survive markdown extraction of the
  paper, and no structured copy of them exists in the repo (checked:
  scorecard_assessment.json, the notes/dashboard HTML, the scorecard .py — none
  carry per-item colours). Guessing them would fabricate the grade, so the
  dimension scores here are assigned directly from the §3.2–3.6 item lists and
  the colour pass is left as an explicit open item.

This is a SELF-assessment. The paper (and our own house rule) says a
self-graded scorecard is not an independent third-party grade.
"""

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSESSMENT = HERE / "fomca_scorecard_assessment.json"

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

# Table 7 — minimum component per dimension, per category.
# "E 4 Construct Validity + 3 Internal Validity + ..." means the dimension
# score may be as bad as that number. A score of 4 is the worst.
CATEGORY_MIN = {
    "A": {"construct_validity": 1, "internal_validity": 1, "external_validity": 1, "reliability": 1, "correctness": 1},
    "B": {"construct_validity": 2, "internal_validity": 2, "external_validity": 1, "reliability": 1, "correctness": 1},
    "C": {"construct_validity": 2, "internal_validity": 2, "external_validity": 1, "reliability": 2, "correctness": 2},
    "D": {"construct_validity": 3, "internal_validity": 3, "external_validity": 3, "reliability": 3, "correctness": 3},
    "E": {"construct_validity": 4, "internal_validity": 3, "external_validity": 4, "reliability": 4, "correctness": 4},
}
CATEGORY_ORDER = ["A", "B", "C", "D", "E"]
CATEGORY_INDEX = {c: i + 1 for i, c in enumerate(CATEGORY_ORDER)}  # A=1 .. E=5
CATEGORY_LABEL = {
    "A": "Ideal for major policy decisions",
    "B": "Minimum for major policy decisions",
    "C": "Final model checkpoint — not sufficient for external governance action",
    "D": "During model development / community-driven evaluation",
    "E": "Exploratory research — results not indicative of real abilities",
}


def classify(scores: dict) -> str:
    """Highest category whose Table 7 minimum is met on every dimension."""
    for cat in CATEGORY_ORDER:
        req = CATEGORY_MIN[cat]
        if all(scores[d] <= req[d] for d in DIMENSIONS):
            return cat
    return "E"


def capping_dimensions(scores: dict, category: str) -> list:
    """Dimensions that block the next-better category — the binding constraints."""
    i = CATEGORY_ORDER.index(category)
    if i == 0:
        return []
    better = CATEGORY_ORDER[i - 1]
    return [
        d for d in DIMENSIONS
        if scores[d] > CATEGORY_MIN[better][d]
    ]


def load(path: Path = ASSESSMENT):
    data = json.loads(path.read_text())
    key = next(iter(data["evals"]))
    entry = data["evals"][key]
    scores = {d: entry["assessment"][d]["score"] for d in DIMENSIONS}
    return data, key, entry, scores


def grade():
    """The headline: numeric index, letter, label, capping dimensions."""
    data, key, entry, scores = load()
    cat = classify(scores)
    return {
        "suite": entry["display"],
        "status": entry.get("status", ""),
        "scores": scores,
        "category": cat,
        "category_index": CATEGORY_INDEX[cat],
        "category_label": CATEGORY_LABEL[cat],
        "capping": capping_dimensions(scores, cat),
        "self_assessed": True,
        "paper": data["paper"],
    }


def render_text(g: dict) -> str:
    L = []
    L.append(f"SCORECARD OF AI EVALUATION QUALITY — {g['suite']}")
    L.append(f"Framework: {g['paper']}")
    L.append("")
    L.append(f"  >>> GRADE: Category {g['category']} — {g['category_label']}")
    if g["capping"]:
        L.append(f"      capped by: " + ", ".join(
            f"{DIM_LABELS[d]} ({g['scores'][d]})" for d in g["capping"]))
    L.append("")
    L.append("  dimension            score  (1=best .. 4=worst)")
    for d in DIMENSIONS:
        s = g["scores"][d]
        bar = "#" * s + "." * (4 - s)
        L.append(f"  {DIM_LABELS[d]:<20} {s}  [{bar}]")
    L.append("")
    L.append("  Table 7 check (does each category's minimum hold?):")
    for cat in CATEGORY_ORDER:
        req = CATEGORY_MIN[cat]
        ok = all(g["scores"][d] <= req[d] for d in DIMENSIONS)
        need = " ".join(f"{DIM_LABELS[d][:4]}<={req[d]}" for d in DIMENSIONS)
        L.append(f"    {cat}  {'PASS' if ok else 'fail'}   needs {need}")
    L.append("")
    L.append("  SELF-ASSESSMENT — not an independent third-party grade.")
    L.append("  Colour-downgrade rule (§3.1) NOT applied: highlight colours are not")
    L.append("  recoverable from the paper source. See module docstring.")
    return "\n".join(L)


def render_markdown(g: dict, entry: dict) -> str:
    L = []
    L.append(f"# Scorecard of AI Evaluation Quality — {g['suite']}\n")
    L.append(f"**Framework:** {g['paper']}  ")
    L.append(f"**Grade:** `Category {g['category']}` — {g['category_label']}  ")
    if g["capping"]:
        L.append("**Capped by:** " + ", ".join(
            f"{DIM_LABELS[d]} ({g['scores'][d]})" for d in g["capping"]) + "  ")
    L.append(f"**Status:** {g['status']}\n")
    L.append("_Self-assessment. Not an independent third-party grade. The paper's "
             "colour-downgrade rule (§3.1) is not applied — see `scorecard_fomca.py`._\n")

    L.append("## Dimension scores\n")
    L.append("| Dimension | Score | Bar | Blocks |")
    L.append("|---|---|---|---|")
    for d in DIMENSIONS:
        s = g["scores"][d]
        L.append(f"| {DIM_LABELS[d]} | **{s}** / 4 | `{'#'*s}{'.'*(4-s)}` | "
                 f"{'yes' if d in g['capping'] else '—'} |")
    L.append("")

    L.append("## Table 7 classification check\n")
    L.append("| Category | Status | Minimum components required |")
    L.append("|---|---|---|")
    for cat in CATEGORY_ORDER:
        req = CATEGORY_MIN[cat]
        ok = all(g["scores"][d] <= req[d] for d in DIMENSIONS)
        need = " + ".join(f"{req[d]} {DIM_LABELS[d]}" for d in DIMENSIONS)
        mark = "**PASS**" if ok else "fail"
        if cat == g["category"]:
            mark += "  ← assigned"
        L.append(f"| {cat} | {mark} | {need} |")
    L.append("")

    L.append("## Per-dimension detail\n")
    for d in DIMENSIONS:
        a = entry["assessment"][d]
        L.append(f"### {DIM_LABELS[d]} — score {a['score']} / 4\n")
        L.append("**Satisfied**")
        for s in a["satisfied"]:
            L.append(f"- {s}")
        L.append("")
        L.append("**Gaps**")
        for s in a["gaps"]:
            L.append(f"- {s}")
        L.append("")
        L.append(f"**Justification.** {a['justification']}\n")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="write .md + .json next to the assessment")
    args = ap.parse_args()

    data, key, entry, scores = load()
    g = grade()
    print(render_text(g))

    if args.write:
        md = HERE / "fomca_scorecard.md"
        js = HERE / "fomca_scorecard_grade.json"
        md.write_text(render_markdown(g, entry))
        js.write_text(json.dumps(g, indent=2) + "\n")
        print(f"\nwrote: {md}\nwrote: {js}")
