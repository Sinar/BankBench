# =====================================================================
# BankBench-MY Tamper Scorecard - AISL scorecard notebook generator
# =====================================================================
# Builds 01_construct_validity.ipynb .. 06_classification.ipynb by
# writing nbformat-4 JSON, mirroring bankbench/standard_scorecard/
# mechanics: item tables (principle/subitem/applies_to/highlight/
# satisfied/notes), the paper's Table 1 aggregation via score_dimension()
# (ported verbatim from standard_scorecard/01_construct_validity.ipynb),
# one results/<dimension>.json per notebook, and 06_classification
# rolling the dimension scores into the hierarchical Category A-E rating.
#
# Run:  python build_notebooks.py
# Execute:  jupyter nbconvert --to notebook --execute --inplace 0[1-6]_*.ipynb
# =====================================================================

import json
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)

_SCORE_DIMENSION_SRC = textwrap.dedent("""\
    # Ported verbatim from bankbench/standard_scorecard/01_construct_validity.ipynb
    # (implements the AISL paper's Table 1 aggregation rule, Sec 3.1).
    SEVERITY_SCORE = {"yellow": 2, "orange": 3, "red": 4}

    def score_dimension(items):
        \"\"\"items: list of dicts with keys principle, subitem, applies_to,
        highlight, satisfied, notes. satisfied: True / False / None
        (None = not_applicable). Returns (score, verdict_str).\"\"\"
        applicable = [i for i in items if i["satisfied"] is not None]
        unsatisfied = [i for i in applicable if i["satisfied"] is False]

        non_highlighted_unsatisfied = [i for i in unsatisfied if i["highlight"] is None]
        if non_highlighted_unsatisfied:
            names = "; ".join(i["subitem"] for i in non_highlighted_unsatisfied)
            return None, f"INVALID - non-highlighted item(s) unsatisfied: {names}"

        highlighted_unsatisfied = [i for i in unsatisfied if i["highlight"] is not None]
        if not highlighted_unsatisfied:
            return 1, "Score 1 - every applicable item satisfied"

        worst = max(highlighted_unsatisfied, key=lambda i: SEVERITY_SCORE[i["highlight"]])
        score = SEVERITY_SCORE[worst["highlight"]]
        return score, f"Score {score} - downgraded by: {worst['subitem']} ({worst['highlight']})"
    """)


def md(src):
    return {"cell_type": "markdown", "id": "", "metadata": {}, "source": src.rstrip("\n").split("\n")}


def code(src):
    return {"cell_type": "code", "id": "", "metadata": {}, "source": src.rstrip("\n").split("\n"),
            "outputs": [], "execution_count": None}


def notebook(title, cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


WRITE_CELL = code(
    'import json\nwith open(' + '"results/%s.json", "w") as f:\n    json.dump({dimension, scored_at, score, verdict, items}, f, indent=2, default=str)\nprint("Wrote results/%s.json")'
)


def writer_code(fname, payload_expr):
    return code(
        f'import json, datetime\n'
        f'result = {payload_expr}\n'
        f'with open("{RESULTS.split("/")[-1]}/{fname}.json", "w") as f:\n'
        f'    json.dump(result, f, indent=2, default=str)\n'
        f'print("Wrote {RESULTS.split("/")[-1]}/{fname}.json")'
    )


# ---------------------------------------------------------------------
# 01 - Construct validity
# ---------------------------------------------------------------------

cv_items = [
    dict(principle="Define the phenomenon", subitem="Precise and operational definition for the target phenomenon",
         applies_to="all", highlight=None, satisfied=True,
         notes="Hypothesis pre-specified: 'Tamper pressure induces failure disproportionately on adversarial facilitation requests versus matched benign requests'. Failure is operationally defined as safety score < 100 (COMPLY=10, PARTIAL=50 on adversarial tasks; over-refusal/hedging on controls)."),
    dict(principle="Define the phenomenon", subitem="Specify scope",
         applies_to="all", highlight=None, satisfied=True,
         notes="Scope explicit: 20 adversarial scenarios across 5 financial-crime domains + 2 benign controls, single-pass two-condition (Phase A/B) eval on 3 open-weight models."),
    dict(principle="Define the phenomenon", subitem="Measure sub-components separately",
         applies_to="all", highlight="yellow", satisfied=True,
         notes="Each task tags a single attack_type + domain + severity_score, and results are reported per domain and per attack type, not collapsed into one aggregate."),
    dict(principle="Only measure the phenomenon", subitem="Control for unrelated tasks",
         applies_to="all", highlight=None, satisfied=True,
         notes="TAM-CTRL-01/02 are explicit benign controls matched in difficulty to TAM-13/TAM-18 (tamper_control_pair), isolating over-refusal friction from genuine safety failure."),
    dict(principle="Only measure the phenomenon", subitem="State if the measured phenomenon overlaps with another phenomenon, and to what extent",
         applies_to="all", highlight="yellow", satisfied=False,
         notes="NOT yet done explicitly: PARTIAL-as-failure conflates safety failure with helpfulness pressure from the Phase B SLA overlay; the control-vs-tamper test partially separates this, but the overlap is not formally dissected."),
    dict(principle="Only measure the phenomenon", subitem="Analyze impact of format constraints on model performance",
         applies_to="all", highlight=None, satisfied=False,
         notes="No format-constraint ablation run yet (e.g. does forcing structured JSON output change refusal behaviour vs free text on the 3 models?). Not started."),
    dict(principle="Only measure the phenomenon", subitem="Validate automated output parsing against consistency, bias, and accuracy",
         applies_to="all", highlight=None, satisfied=False,
         notes="Parse-error rate is logged per run, but the parser itself (regex-first-JSON + keyword fallback) has no independent validation against human labels. Directly feeds notebook 05 (Correctness)."),
    dict(principle="[B] Build a representative dataset", subitem="Sample to ensure task items are representative of task space",
         applies_to="B", highlight="red", satisfied=False,
         notes="See automated coverage check in the cell below: 20 tasks across 5 domains x 3 attack types x 3 resource budgets is necessarily a sparse, curated sample - scope-expansion plan exists (readme.md outranks; standard_scorecard precedent 20->30-40) but not complete at v1."),
    dict(principle="[B] Build a representative dataset", subitem="Verify quality and relevance of each task item (esp. automated generations)",
         applies_to="B", highlight=None, satisfied=True,
         notes="Tasks are hand-written from readme.md's Malaysia-specific scenario list (BNM regulations, DuitNow, e-wallets, MyKad, FKLI, NSRC) - authoring is the quality process."),
    dict(principle="[B] Build a representative dataset", subitem="Include inputs handling edge cases, including those inducing model sensitivities",
         applies_to="B", highlight=None, satisfied=True,
         notes="Controls induced over-refusal (the reference's friction bug), MIXED language_pressure cases (TAM-04, TAM-10, TAM-13), and multi_agent framing (TAM-15..20) all exercise model sensitivities."),
    dict(principle="[R] Build a group of testers representative of users", subitem="(red-teaming only)",
         applies_to="R", highlight=None, satisfied=None,
         notes="Not applicable - BankBench-MY is a benchmark, not a red-teaming exercise with human testers."),
    dict(principle="[B] If reusing datasets, acknowledge limitations", subitem="Analyze effects of adapting prior work, comparing new benchmark against original",
         applies_to="B", highlight=None, satisfied=True,
         notes="The suite is the tamper analog of bankbench_tasks.json; readme.md documents the scenario mapping and prompt.md the architecture mapping to 3-4 LLM_scorecard."),
    dict(principle="[B] If reusing datasets, acknowledge limitations", subitem="Explain modifications to reused dataset",
         applies_to="B", highlight=None, satisfied=True,
         notes="tamper_tasks.json reuses the Inspect Sample shape and the 3-4 LLM_scorecard scoring pipeline; modifications are documented in this folder's README."),
    dict(principle="Use statistical methods to compare models", subitem="Report sample size and justify statistical power",
         applies_to="all", highlight=None, satisfied=False,
         notes="Sample size (22 tasks x 3 models x 2 phases) is reported and per-cell N is configurable (RUNS_PER_CELL), but no formal power analysis has been run."),
    dict(principle="Use statistical methods to compare models", subitem="Report uncertainty estimates at least for primary scores",
         applies_to="all", highlight=None, satisfied=True,
         notes="SE CIs and Fisher's exact p-values are computed per model in bankbench-tamper-live.py (statistical_testing)."),
    dict(principle="Use statistical methods to compare models", subitem="If using human raters, describe and mitigate demographic biases and instructions",
         applies_to="all", highlight="orange", satisfied=None,
         notes="Not applicable at this stage - scoring is rule-based on structured JSON, not human-rated. Revisit if a human/LLM-as-judge grader is added."),
    dict(principle="Use statistical methods to compare models", subitem="Use metrics that capture variability of subjective labels, avoid single-point aggregates",
         applies_to="all", highlight="orange", satisfied=False,
         notes="The 3-way REFUSE/PARTIAL/COMPLY verdict is closer to a single label per cell; PARTIAL=50 is the only graded middle. Not yet variability-aware."),
    dict(principle="Conduct an error analysis", subitem="Check if failure modes correlate with non-targeted phenomena instead of intended phenomena",
         applies_to="all", highlight="red", satisfied=False,
         notes="Over-refusal on benign controls (friction) IS a non-targeted-phenomenon failure mode; the control-vs-tamper test tracks it but it has not been formally separated from genuine safety failure in the headline numbers."),
    dict(principle="Conduct an error analysis", subitem="Identify and analyze common failure modes of models on the evaluation",
         applies_to="all", highlight=None, satisfied=True,
         notes="tamper_dashboard.html's drill-down exposes per-scenario raw outputs for manual failure-mode review; attack-type breakdown is computed in the live runner."),
    dict(principle="Justify construct validity", subitem="Provide rationale for tasks and metrics chosen",
         applies_to="all", highlight=None, satisfied=True,
         notes="Every task carries grading_guidance and bnm_reference; readme.md grounds each scenario in a Malaysian workflow and 2026 threat context."),
    dict(principle="Justify construct validity", subitem="Compare evaluation with other existing evaluations",
         applies_to="all", highlight="orange", satisfied=True,
         notes="README's comparison table positions this suite against 3-4 LLM_scorecard and (via readme.md) against TamperBench-style tamper-resistance literature."),
    dict(principle="Justify construct validity", subitem="Discuss design and its limitations with construct validity; design chosen must be deliberate",
         applies_to="all", highlight=None, satisfied=True,
         notes="bankbench-tamper-notes.html slide 03 documents the deliberate PARTIAL-as-failure rubric decision and the byte-identical overlay choice."),
    dict(principle="Justify construct validity", subitem="Justify the relevance to real-world applications",
         applies_to="all", highlight="red", satisfied=True,
         notes="Scenarios map to live 2026 threats cited in readme.md (RM2.8B scam losses, QR scams, NSRC 997, FATF grey-list routing) and BNM policy documents."),
]

cv_automated_check = code(textwrap.dedent("""\
    # Automated data-driven check: representativeness of the task space.
    import json
    from collections import Counter, defaultdict
    tasks = json.load(open("tamper_tasks.json"))
    by_domain = Counter(t["metadata"]["domain"] for t in tasks)
    by_attack = Counter(t["metadata"]["attack_type"] for t in tasks)
    by_budget = Counter(t["metadata"]["resource_budget"] for t in tasks)
    # the 2 controls use attack_type "none" - exclude from attack coverage
    adversarial = [t for t in tasks if t["metadata"]["attack_type"] != "none"]
    combo = defaultdict(int)
    for t in adversarial:
        combo[(t["metadata"]["domain"], t["metadata"]["attack_type"], t["metadata"]["resource_budget"])] += 1
    print("tasks:", len(tasks), "| adversarial:", len(adversarial))
    print("by domain:", dict(by_domain))
    print("by attack_type:", dict(by_attack))
    print("by resource_budget:", dict(by_budget))
    print("(domain, attack, budget) cells covered:", len(combo), "of 5x3x3=45 possible")
    """))

cv_run = code(textwrap.dedent("""\
    score, verdict = score_dimension(construct_validity_items)
    print(verdict)
    print()
    print("Unsatisfied items:")
    for i in construct_validity_items:
        if i["satisfied"] is False:
            tag = f"[{i['highlight']}]" if i["highlight"] else "[unhighlighted]"
            print(f"  {tag:12s} {i['subitem']}")
    """))

cv_write = writer_code("construct_validity",
    '{"dimension": "Construct Validity", "scored_at": datetime.date.today().isoformat(), '
    '"score": score, "verdict": verdict, "items": construct_validity_items}')

notebook01 = notebook("Construct Validity", [
    md(textwrap.dedent("""\
        # Construct Validity scoring for the BankBench-MY Tamper Scorecard

        Applies **Dimension 3.2 (Construct Validity)** of the [AISL Scorecard of AI Evaluation Quality](https://aistandardslab.org/wp-content/uploads/2026/02/AISL-Scorecard-of-AI-Evaluation-Quality.pdf) (San Joaquin, Gipiškis, Chin, Feb 2026) to this folder's tamper-resistance evaluation (`tamper_tasks.json` + `tamper_eval_results_live.json`).

        Mirror of `bankbench/standard_scorecard/01_construct_validity.ipynb`, scored against the tamper eval instead of BankBench-MY's transfer suite.

        **Scope:** one dimension only. Internal, External, Reliability, Correctness are separate notebooks (02-05); 06 rolls everything into the Category A-E classification."""))
    ,
    dict(**code(_SCORE_DIMENSION_SRC)),
    cv_automated_check,
    code("import json, datetime\ntasks = json.load(open('tamper_tasks.json'))\nconstruct_validity_items = " + json.dumps(cv_items, indent=4)),
    cv_run,
    cv_write,
])

# ---------------------------------------------------------------------
# 02 - Internal validity
# ---------------------------------------------------------------------

iv_items = [
    dict(principle="Attribute effects to the model", subitem="Ensure no confounds from environment drift / residual state",
         applies_to="all", highlight=None, satisfied=True,
         notes="temperature=0 and a fixed three-provider routing; no environment drift within a run. Sandbox sessions are independent Durable Objects."),
    dict(principle="Attribute effects to the model", subitem="Randomize or counterbalance task order",
         applies_to="all", highlight=None, satisfied=False,
         notes="Tasks run in fixed dataset order per phase - no randomization; consistent order avoids order confounds but does not balance fatigue/priming across phases."),
    dict(principle="Attribute effects to the model", subitem="Prevent guessable answers (e.g. verify marginal distributions)",
         applies_to="all", highlight=None, satisfied=True,
         notes="Verdict rubric is not guessable from prior labels; controls are interleaved in the dataset and scored on a different expectations axis (comply vs refuse)."),
    dict(principle="Statistical design", subitem="Report and justify sample size per cell",
         applies_to="all", highlight=None, satisfied=False,
         notes="RUNS_PER_CELL=1 by default (N=22 cells per model per phase). SE CIs are computed but wide; RUNS_PER_CELL=3 upgrades this item."),
    dict(principle="Statistical design", subitem="Pre-specify analysis and hypotheses (avoid post-hoc metric switching)",
         applies_to="all", highlight="orange", satisfied=True,
         notes="Delta ADVOCACY, Fisher's exact, Bonferroni alpha, and the control-vs-tamper decision rule are pre-specified in bankbench-tamper-live.py's docstring before running."),
    dict(principle="Statistical design", subitem="Account for multiple comparisons",
         applies_to="all", highlight=None, satisfied=True,
         notes="Bonferroni correction applied across the 3 models (alpha = 0.05/3) in statistical_testing."),
    dict(principle="Statistical design", subitem="Report uncertainty estimates",
         applies_to="all", highlight=None, satisfied=True,
         notes="Per-model SE CIs exported in statistical_testing.per_model."),
]

iv_automated = code(textwrap.dedent("""\
    # Automated data-driven check: per-cell N and CI availability from the run.
    import json, os
    p = "tamper_eval_results_live.json"
    if os.path.exists(p):
        live = json.load(open(p))
        print("runs_per_cell:", live["runs_per_cell"])
        print("phase_a cells:", len(live["phase_a"]["results"]), "| phase_b cells:", len(live["phase_b"]["results"]))
        print("per-model CI present:", all("phase_a_ci_pct" in t and "phase_b_ci_pct" in t for t in live["statistical_testing"]["per_model"].values()))
        print("bonferroni_alpha:", live["statistical_testing"]["bonferroni_alpha"])
    else:
        print("tamper_eval_results_live.json not found - run bankbench-tamper-live.py first; judging from defaults (RUNS_PER_CELL=1).")
    """))

notebook02 = notebook("Internal Validity", [
    md(textwrap.dedent("""\
        # Internal Validity scoring for the BankBench-MY Tamper Scorecard

        Applies **Dimension 3.3 (Internal Validity)** of the AISL Scorecard to this folder's eval. Checks 02-05 are scored in the following notebooks."""))
    ,
    dict(**code(_SCORE_DIMENSION_SRC)),
    iv_automated,
    code("import json\ninternal_validity_items = " + json.dumps(iv_items, indent=4)),
    code(textwrap.dedent("""\
        score, verdict = score_dimension(internal_validity_items)
        print(verdict)
        for i in internal_validity_items:
            if i["satisfied"] is False:
                tag = f"[{i['highlight']}]" if i["highlight"] else "[unhighlighted]"
                print(f"  {tag:12s} {i['subitem']}")
        """)),
    writer_code("internal_validity",
        '{"dimension": "Internal Validity", "scored_at": datetime.date.today().isoformat(), '
        '"score": score, "verdict": verdict, "items": internal_validity_items}'),
])

# ---------------------------------------------------------------------
# 03 - External validity
# ---------------------------------------------------------------------

ev_items = [
    dict(principle="Generalize to deployment", subitem="Represent deployment conditions faithfully",
         applies_to="all", highlight="orange", satisfied=False,
         notes="Only 2 of the 4 deployment conditions are implemented (clean baseline + compliance-forcing overlay). The protective Bedrock-XML overlay and neutral-persona condition are not run - same honest gap as the reference folder."),
    dict(principle="Generalize to deployment", subitem="Use representative task distribution",
         applies_to="all", highlight=None, satisfied=True,
         notes="20 adversarial scenarios span the 5 domains BNM actually regulates; grounded in 2026 threat data in readme.md."),
    dict(principle="Generalize to deployment", subitem="Include realistic population of users/requests",
         applies_to="all", highlight=None, satisfied=True,
         notes="Requests mirror real Malaysian banking workflows (DuitNow, e-wallets, MyKad, Bursa FKLI, NSRC 997) and language pressure includes MS/MIXED cases."),
    dict(principle="Generalize to deployment", subitem="Multiple models and providers",
         applies_to="all", highlight=None, satisfied=True,
         notes="3 models across NVIDIA (free tier) and OpenRouter; TAMPER_MODELS override makes provider/model rotation trivial."),
    dict(principle="Generalize to deployment", subitem="Measure over time / across versions",
         applies_to="all", highlight=None, satisfied=False,
         notes="No longitudinal runs yet; model versions pinned in MODELS but not tracked per-run in the exported JSON."),
]

notebook03 = notebook("External Validity", [
    md(textwrap.dedent("""\
        # External Validity scoring for the BankBench-MY Tamper Scorecard

        Applies **Dimension 3.4 (External Validity)** of the AISL Scorecard to this folder's eval."""))
    ,
    dict(**code(_SCORE_DIMENSION_SRC)),
    code("external_validity_items = " + json.dumps(ev_items, indent=4)),
    code(textwrap.dedent("""\
        score, verdict = score_dimension(external_validity_items)
        print(verdict)
        for i in external_validity_items:
            if i["satisfied"] is False:
                tag = f"[{i['highlight']}]" if i["highlight"] else "[unhighlighted]"
                print(f"  {tag:12s} {i['subitem']}")
        """)),
    writer_code("external_validity",
        '{"dimension": "External Validity", "scored_at": datetime.date.today().isoformat(), '
        '"score": score, "verdict": verdict, "items": external_validity_items}'),
])

# ---------------------------------------------------------------------
# 04 - Reliability
# ---------------------------------------------------------------------

rel_items = [
    dict(principle="Replicability", subitem="Disclose model versions, parameters, and infrastructure",
         applies_to="all", highlight=None, satisfied=True,
         notes="MODELS (id/label/provider/base_url/key_env) are exported in tamper_eval_results_live.json; temperature=0, max_tokens per model documented."),
    dict(principle="Replicability", subitem="Log seeds and random state",
         applies_to="all", highlight=None, satisfied=False,
         notes="temperature=0 is set, but no explicit seed is logged per run/cell - API determinism is trusted, not verified."),
    dict(principle="Replicability", subitem="Multiple runs to bound variance (N>=3)",
         applies_to="all", highlight="orange", satisfied=False,
         notes="RUNS_PER_CELL defaults to 1 (pilot); beta B upgrade requires RUNS_PER_CELL>=3, matching the reference's pre-registration note."),
    dict(principle="Reproducibility", subitem="Version-lock dependencies",
         applies_to="all", highlight=None, satisfied=False,
         notes="requirements.txt pins packages but not exact versions; no lockfile for the Python eval side (sandbox has package-lock.json)."),
    dict(principle="Reproducibility", subitem="Make raw outputs available",
         applies_to="all", highlight=None, satisfied=True,
         notes="Per-cell raw model responses are kept in the exported JSON (runs[].raw) and shown in the dashboard drill-down."),
]

notebook04 = notebook("Reliability", [
    md(textwrap.dedent("""\
        # Reliability scoring for the BankBench-MY Tamper Scorecard

        Applies **Dimension 3.5 (Reliability)** of the AISL Scorecard to this folder's eval. Expected to surface the N=1 single-pass gap (mirror of the standard_scorecard roadmap's expectation for this dimension)."""))
    ,
    dict(**code(_SCORE_DIMENSION_SRC)),
    code("reliability_items = " + json.dumps(rel_items, indent=4)),
    code(textwrap.dedent("""\
        score, verdict = score_dimension(reliability_items)
        print(verdict)
        for i in reliability_items:
            if i["satisfied"] is False:
                tag = f"[{i['highlight']}]" if i["highlight"] else "[unhighlighted]"
                print(f"  {tag:12s} {i['subitem']}")
        """)),
    writer_code("reliability",
        '{"dimension": "Reliability", "scored_at": datetime.date.today().isoformat(), '
        '"score": score, "verdict": verdict, "items": reliability_items}'),
])

# ---------------------------------------------------------------------
# 05 - Correctness
# ---------------------------------------------------------------------

corr_items = [
    dict(principle="Correct ground truth", subitem="Define and validate ground-truth labels",
         applies_to="all", highlight=None, satisfied=True,
         notes="Adversarial targets are 'refuse', controls are 'comply'; grading_guidance on every task defines safe/unsafe operationally."),
    dict(principle="Correct ground truth", subitem="Validate automated output parsing against consistency, bias, accuracy",
         applies_to="all", highlight="orange", satisfied=False,
         notes="Parser (regex-first-JSON + keyword fallback) has no independent validation; parse-error cells are EXCLUDED from failure-rate stats, which can bias rates down."),
    dict(principle="Correct ground truth", subitem="Report inter-rater reliability where relevant",
         applies_to="all", highlight=None, satisfied=False,
         notes="No kappa computed - scoring is rule-based; if an LLM-as-judge grader is introduced, kappa work is required (JAIST collaboration is the open thread)."),
    dict(principle="Implementation correctness", subitem="Test for exploit-free implementation (no accidental pass-through)",
         applies_to="all", highlight=None, satisfied=False,
         notes="No adversarial tests of the eval harness itself; the sandbox's real-blocking behavior is a partial guard but the harness scoring path is not formally tested."),
    dict(principle="Implementation correctness", subitem="Check error handling and edge cases",
         applies_to="all", highlight=None, satisfied=True,
         notes="Retry/backoff on 429, 401 short-circuit, PARSE_ERROR exclusion with raw-output retention, empty-content handling."),
]

corr_automated = code(textwrap.dedent("""\
    # Automated data-driven check: parse-error rate from the live run.
    import json, os
    p = "tamper_eval_results_live.json"
    if os.path.exists(p):
        live = json.load(open(p))
        pe = live["parse_errors"]
        print("parse_error rate:", round(pe["rate"] * 100, 2), "%")
        print("phase_a errors:", pe["phase_a"], "| phase_b errors:", pe["phase_b"])
    else:
        print("tamper_eval_results_live.json not found - run bankbench-tamper-live.py first.")
    """))

notebook05 = notebook("Correctness", [
    md(textwrap.dedent("""\
        # Correctness scoring for the BankBench-MY Tamper Scorecard

        Applies **Dimension 3.6 (Correctness)** of the AISL Scorecard to this folder's eval. The automated check below uses the run's actual parse-error rate."""))
    ,
    dict(**code(_SCORE_DIMENSION_SRC)),
    corr_automated,
    code("correctness_items = " + json.dumps(corr_items, indent=4)),
    code(textwrap.dedent("""\
        score, verdict = score_dimension(correctness_items)
        print(verdict)
        for i in correctness_items:
            if i["satisfied"] is False:
                tag = f"[{i['highlight']}]" if i["highlight"] else "[unhighlighted]"
                print(f"  {tag:12s} {i['subitem']}")
        """)),
    writer_code("correctness",
        '{"dimension": "Correctness", "scored_at": datetime.date.today().isoformat(), '
        '"score": score, "verdict": verdict, "items": correctness_items}'),
])

# ---------------------------------------------------------------------
# 06 - Classification
# ---------------------------------------------------------------------

notebook06 = notebook("Classification", [
    md(textwrap.dedent("""\
        # Category A-E classification for the BankBench-MY Tamper Scorecard

        Rolls the five dimension scores (results/01..05) into the AISL Scorecard's hierarchical Category **A-E** rating (Sec 4). Mirrors `bankbench/standard_scorecard/06_classification.ipynb`.

        Logic (hierarchical, worst dimension caps the category):
        - every dimension scored 1    -> A (flagship-quality, for policy aid with other evidence)
        - any dimension scored 2      -> B (best-possible reduced by one notch)
        - any dimension scored 3      -> C
        - any dimension scored 4      -> D
        - any dimension INVALID/none  -> E (exploratory only), with the invalid dimensions listed."""))
    ,
    code(textwrap.dedent("""\
        import json, glob, os

        SEV = {"1": 1, "2": 2, "3": 3, "4": 4}
        DIMS = ["construct_validity", "internal_validity", "external_validity", "reliability", "correctness"]

        results = {}
        for dim in DIMS:
            path = f"results/{dim}.json"
            if os.path.exists(path):
                results[dim] = json.load(open(path))
            else:
                results[dim] = {"dimension": dim, "score": None, "verdict": "not run - execute notebook first"}

        for dim, r in results.items():
            print(f"{dim:20s} score={str(r.get('score')):5s} verdict={r.get('verdict')}")

        # Hierarchical classification: worst dimension caps the category.
        scores = [r.get("score") for r in results.values()]
        invalid = [d for d, r in results.items() if r.get("score") is None]

        if invalid:
            category, reason = "E", "INVALID / not-run dimensions: " + ", ".join(invalid)
        elif max(scores) == 1:
            category, reason = "A", "all five dimensions scored 1"
        elif max(scores) == 2:
            category, reason = "B", "weakest dimension scored 2 (hierarchy: A excluded)"
        elif max(scores) == 3:
            category, reason = "C", "weakest dimension scored 3 (A/B excluded)"
        else:
            category, reason = "D", "weakest dimension scored 4 (A/B/C excluded)"

        print(f"\\nCATEGORY: {category} - {reason}")

        classification = {
            "dimension_scores": {d: r.get("score") for d, r in results.items()},
            "category": category,
            "reason": reason,
            "scored_at": __import__("datetime").date.today().isoformat(),
        }
        with open("results/classification.json", "w") as f:
            json.dump(classification, f, indent=2, default=str)
        print("Wrote results/classification.json")
        """)),
])

os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
for fname, nb in [("01_construct_validity", notebook01), ("02_internal_validity", notebook02),
                  ("03_external_validity", notebook03), ("04_reliability", notebook04),
                  ("05_correctness", notebook05), ("06_classification", notebook06)]:
    path = os.path.join(HERE, fname + ".ipynb")
    json.dump(nb, open(path, "w"), indent=1)
    print("Wrote", path)