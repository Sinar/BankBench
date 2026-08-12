# =====================================================================
# Unified Eval-Scorecard — dashboard builder (dashboard + scorecard step)
# =====================================================================
# Reads bankbench_results.json, hle_results.json, cybench_results.json
# (from run_eval.py) plus scorecard_assessment.json, normalizes every
# eval onto a common 0-100 "higher-is-better" scale, and renders ONE
# dashboard that compares the evals against each other AND against the
# AI Evaluation Quality scorecard (5 dimensions, Category A-E).
#
# Output: unified_scorecard_dashboard.html
# =====================================================================

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

EVAL_ORDER = ["bankbench", "hle", "cybench"]
EVAL_FILE = {e: os.path.join(HERE, f"{e}_results.json") for e in EVAL_ORDER}
SCORECARD_FILE = os.path.join(HERE, "scorecard_assessment.json")
OUT_HTML = os.path.join(HERE, "unified_scorecard_dashboard.html")

results = {}
for e in EVAL_ORDER:
    p = EVAL_FILE[e]
    results[e] = json.load(open(p)) if os.path.exists(p) else None

scorecard = json.load(open(SCORECARD_FILE))


# ---------------------------------------------------------------------
# Per-model unified scores (higher = better everywhere)
#   bankbench -> Phase A (clean baseline) safety pass rate  (NOT the
#                averaged Phase A/B number, so it reflects clean safety)
#   hle       -> accuracy
#   cybench   -> solve rate
# ---------------------------------------------------------------------
def bankbench_clean_per_model(res):
    rows = [r for r in res["results"] if r["phase"].startswith("Phase A")]
    out = {}
    for l in [m["label"] for m in res["models"]]:
        s = [r["score"] for r in rows if r["model"] == l]
        out[l] = round(100 * sum(s) / len(s), 1) if s else None
    return out


def per_model_unified(e, res):
    if e == "bankbench":
        return bankbench_clean_per_model(res)
    return {l: res["per_model_score_pct"].get(l) for l in [m["label"] for m in res["models"]]}


UNIFIED = {e: per_model_unified(e, results[e]) for e in EVAL_ORDER if results[e]}
MODEL_LABELS = [m["label"] for m in results["bankbench"]["models"]]

# classification from weakest dimension (1 best .. 4 worst)
def classify(scores):
    worst = max(scores.values())
    return {1: "A", 2: "B", 3: "C", 4: "D"}.get(worst, "E")


# ---------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------
sns_ok = True
try:
    import seaborn as sns
    sns.set_style("whitegrid")
except Exception:
    sns_ok = False

DIM_LABELS = {
    "construct_validity": "Construct Validity",
    "internal_validity": "Internal Validity",
    "external_validity": "External Validity",
    "reliability": "Reliability",
    "correctness": "Correctness",
}

# Chart 1: grouped bar — models x evals
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(MODEL_LABELS))
width = 0.26
colors = {"bankbench": "#4E7A51", "hle": "#2563eb", "cybench": "#7c3aed"}
for i, e in enumerate(EVAL_ORDER):
    if e not in UNIFIED:
        continue
    vals = [UNIFIED[e].get(l) for l in MODEL_LABELS]
    ax.bar(x + (i - 1) * width, vals, width, label=results[e]["display_name"], color=colors[e])
ax.set_xticks(x)
ax.set_xticklabels(MODEL_LABELS, rotation=15, ha="right")
ax.set_ylabel("Unified score (%, higher = better)")
ax.set_ylim(0, 100)
ax.set_title("Unified eval-scorecard — per-model score across evals")
ax.legend(fontsize=9)
plt.tight_layout()
buf1 = __import__("io").BytesIO()
fig.savefig(buf1, format="png", dpi=140, bbox_inches="tight")
chart1 = __import__("base64").b64encode(buf1.getvalue()).decode()
plt.close(fig)

# Chart 2: BankBench Phase A vs B (Delta ADVOCACY)
chart2 = ""
if results["bankbench"] and "delta_advocacy" in results["bankbench"]:
    da = results["bankbench"]["delta_advocacy"]
    fig, ax = plt.subplots(figsize=(10, 4))
    a_vals = [bankbench_clean_per_model(results["bankbench"]).get(l) for l in MODEL_LABELS]
    # Phase B per model
    rows_b = [r for r in results["bankbench"]["results"] if r["phase"].startswith("Phase B")]
    b_vals = []
    for l in MODEL_LABELS:
        s = [r["score"] for r in rows_b if r["model"] == l]
        b_vals.append(round(100 * sum(s) / len(s), 1) if s else 0)
    ax.bar(x - width/2, a_vals, width, label="Phase A (clean)", color="#4E7A51")
    ax.bar(x + width/2, b_vals, width, label="Phase B (compliance-forcing)", color="#dc2626")
    ax.set_xticks(x); ax.set_xticklabels(MODEL_LABELS, rotation=15, ha="right")
    ax.set_ylabel("Safety pass rate (%)"); ax.set_ylim(0, 100)
    ax.set_title(f"BankBench Delta ADVOCACY = {da['overall_pp']:+.1f}pp (Phase B - Phase A)")
    ax.legend(fontsize=9)
    plt.tight_layout()
    buf2 = __import__("io").BytesIO()
    fig.savefig(buf2, format="png", dpi=140, bbox_inches="tight")
    chart2 = __import__("base64").b64encode(buf2.getvalue()).decode()
    plt.close(fig)

# Chart 3: scorecard heatmap (dims x evals), 1=green .. 4=red
fig, ax = plt.subplots(figsize=(8, 4))
grid = np.array([[scorecard["evals"][e]["assessment"][d]["score"] for e in EVAL_ORDER]
                 for d in scorecard["dimensions"]])
im = ax.imshow(grid, cmap="RdYlGn_r", vmin=1, vmax=4, aspect="auto")
ax.set_xticks(range(len(EVAL_ORDER)))
ax.set_xticklabels([scorecard["evals"][e]["display"] for e in EVAL_ORDER], fontsize=9)
ax.set_yticks(range(len(scorecard["dimensions"])))
ax.set_yticklabels([DIM_LABELS[d] for d in scorecard["dimensions"]], fontsize=9)
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        ax.text(j, i, grid[i, j], ha="center", va="center", fontsize=11, fontweight="bold",
                color="black")
ax.set_title("AI Evaluation Quality scorecard — dimension score (1 best .. 4 worst)")
plt.tight_layout()
buf3 = __import__("io").BytesIO()
fig.savefig(buf3, format="png", dpi=140, bbox_inches="tight")
chart3 = __import__("base64").b64encode(buf3.getvalue()).decode()
plt.close(fig)


# ---------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------
def pill(v, good_hi=True, lo=60, hi=30):
    if v is None:
        return '<span class="pill pill-na">n/a</span>'
    if good_hi:
        cls = "pill-good" if v >= lo else ("pill-mid" if v >= hi else "pill-bad")
    else:
        cls = "pill-good" if v <= lo else ("pill-mid" if v <= hi else "pill-bad")
    return f'<span class="pill {cls}">{v:.1f}%</span>'


def dim_pill(s):
    cls = {1: "pill-good", 2: "pill-mid", 3: "pill-worse", 4: "pill-bad"}.get(s, "pill-na")
    return f'<span class="pill {cls}">{s}</span>'


def cat_pill(c):
    cls = {"A": "pill-good", "B": "pill-good", "C": "pill-mid", "D": "pill-worse", "E": "pill-bad"}.get(c, "pill-na")
    return f'<span class="pill {cls}">Cat {c}</span>'


# ---------------------------------------------------------------------
# Build sections
# ---------------------------------------------------------------------
# Section 1: unified matrix
matrix_rows = ""
for l in MODEL_LABELS:
    cells = ""
    for e in EVAL_ORDER:
        v = UNIFIED[e].get(l) if e in UNIFIED else None
        cells += f"<td>{pill(v)}</td>"
    matrix_rows += f"<tr><td class='model-name'>{l}</td>{cells}</tr>"

# BankBench is the safety anchor: capability(ev) vs safety(bankbench) gap callout
gap_note = ""
if "bankbench" in UNIFIED and "hle" in UNIFIED:
    safest = max(UNIFIED["bankbench"], key=lambda k: UNIFIED["bankbench"][k])
    cap = max(UNIFIED["hle"], key=lambda k: UNIFIED["hle"][k])
    gap_note = (f"On this trial sample, the strongest capability model ({cap}, "
                f"{UNIFIED['hle'][cap]:.0f}% HLE) is not necessarily the safest "
                f"({safest}, {UNIFIED['bankbench'][safest]:.0f}% BankBench clean). "
                f"Capability benchmarks and the safety benchmark measure different things — "
                f"a model can top HLE/Cybench and still fail adversarial banking scenarios.")

# Section 2: per-eval detail
detail_sections = ""
for e in EVAL_ORDER:
    res = results[e]
    if not res:
        continue
    disp = res["display_name"]
    per_model = UNIFIED[e]
    per_cat = res["per_category_score_pct"]
    model_rows = "".join(
        f"<tr><td class='model-name'>{l}</td><td>{pill(per_model.get(l))}</td></tr>"
        for l in MODEL_LABELS)
    cat_rows = "".join(
        f"<tr><td class='model-name'>{c}</td><td>{pill(v)}</td></tr>"
        for c, v in sorted(per_cat.items(), key=lambda kv: -(kv[1] or 0)))
    da_block = ""
    if e == "bankbench" and "delta_advocacy" in res:
        da = res["delta_advocacy"]
        da_rows = "".join(
            f"<tr><td class='model-name'>{l}</td><td>{da['by_model_pp'].get(l):+0.1f}pp</td></tr>"
            for l in MODEL_LABELS)
        da_block = f"""
        <h3>Delta ADVOCACY (Phase B - Phase A)</h3>
        <p class='sub'>Headline safety number: how much the compliance-forcing overlay degrades the clean baseline.</p>
        <table><tr><th>Model</th><th>Delta (pp)</th></tr>{da_rows}</table>
        <div class='stat-row'>
          <div class='stat'><div class='label'>Overall Delta ADVOCACY</div><div class='value'>{da['overall_pp']:+.1f}pp</div></div>
        </div>
        """
    detail_sections += f"""
    <section>
      <h2>{disp}</h2>
      <p class='sub'>{res['scoring']['note']} Mode: {res['mode']}. Overall: {pill(res['overall_score_pct'])}.</p>
      <table><tr><th>Model</th><th>{res['scoring']['metric']}</th></tr>{model_rows}</table>
      <table style='margin-top:14px'><tr><th>Category</th><th>Score</th></tr>{cat_rows}</table>
      {da_block}
    </section>
    """

# Section 3: scorecard
sc_rows = ""
for d in scorecard["dimensions"]:
    dl = DIM_LABELS[d]
    cells = ""
    for e in EVAL_ORDER:
        s = scorecard["evals"][e]["assessment"][d]["score"]
        cells += f"<td>{dim_pill(s)}</td>"
    sc_rows += f"<tr><td class='model-name'>{dl}</td>{cells}</tr>"

sc_cards = ""
for e in EVAL_ORDER:
    ev = scorecard["evals"][e]
    scores = {d: ev["assessment"][d]["score"] for d in scorecard["dimensions"]}
    cat = classify(scores)
    dim_items = ""
    for d in scorecard["dimensions"]:
        a = ev["assessment"][d]
        dim_items += f"""
        <div class='sc-dim'>
          <div class='sc-dim-h'><span>{DIM_LABELS[d]}</span> {dim_pill(a['score'])}</div>
          <div class='sc-j'>{a['justification']}</div>
          <div class='sc-gaps'><b>Gaps:</b> {', '.join(a['gaps']) if a['gaps'] else 'none'}</div>
        </div>"""
    sc_cards += f"""
    <div class='sc-card'>
      <div class='sc-card-h'>{ev['display']} &nbsp; {cat_pill(cat)}</div>
      {dim_items}
    </div>"""

CSS = """
:root{--bg:#F5F5F3;--surface:#E8E8E5;--surface-2:#fff;--border:#C8C8C4;--ink:#1A1A18;--ink-2:#3A3A38;--ink-3:#6A6A68;--ink-4:#9A9A98;--accent:#2A5298;--teal:#0F6E56;--teal-soft:#E1F5EE;--coral:#993C1D;--coral-soft:#FAECE7;--amber:#7A4A0A;--amber-soft:#FEF3E2;--green:#4E7A51;--green-soft:#E3EEE4;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Inter',-apple-system,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.6;}
.wrap{max-width:1100px;margin:0 auto;padding:40px 24px 80px;}
h1{font-size:26px;font-weight:600;margin-bottom:8px;}
.sub{color:var(--ink-3);font-size:13.5px;margin-bottom:18px;max-width:820px;}
.meta{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--ink-4);display:flex;gap:20px;flex-wrap:wrap;margin-bottom:28px;padding-bottom:16px;border-bottom:1px solid var(--border);}
.meta b{color:var(--ink-3);}
.callout{border-left:3px solid var(--green);background:var(--green-soft);border-radius:0 4px 4px 0;padding:14px 18px;margin-bottom:28px;font-size:13.5px;color:var(--ink-2);}
.callout b{color:var(--ink);}
section{margin-bottom:40px;}
h2{font-size:18px;font-weight:600;margin-bottom:12px;padding-bottom:8px;border-bottom:1.5px solid var(--border);}
h3{font-size:14px;font-weight:600;margin:18px 0 8px;}
table{width:100%;border-collapse:collapse;margin-bottom:8px;font-size:13px;background:var(--surface-2);border:1px solid var(--border);border-radius:6px;overflow:hidden;}
th{text-align:left;padding:10px 14px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-4);background:var(--surface);border-bottom:1.5px solid var(--border);}
td{padding:10px 14px;border-bottom:1px solid #eee;vertical-align:top;}
tr:last-child td{border-bottom:none;}
.model-name{font-weight:600;white-space:nowrap;}
.pill{display:inline-block;padding:2px 9px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:500;white-space:nowrap;}
.pill-good{background:var(--teal-soft);color:var(--teal);}
.pill-mid{background:var(--amber-soft);color:var(--amber);}
.pill-bad{background:var(--coral-soft);color:var(--coral);}
.pill-na{background:var(--surface);color:var(--ink-4);}
.pill-flat{background:var(--surface);color:var(--ink-3);}
.pill-worse{background:var(--coral-soft);color:var(--coral);}
.stat-row{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:16px 0;}
.stat{border:1px solid var(--border);border-radius:6px;padding:16px 18px;background:var(--surface-2);}
.stat .label{font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;color:var(--ink-4);margin-bottom:6px;}
.stat .value{font-size:24px;font-weight:600;}
img.chart{width:100%;border:1px solid var(--border);border-radius:6px;margin-top:12px;}
.sc-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;}
.sc-card{border:2px solid var(--green);border-radius:10px;padding:16px;background:#fff;box-shadow:4px 4px 0 var(--green);}
.sc-card-h{font-family:'Space Grotesk','Inter',sans-serif;font-weight:700;font-size:15px;color:var(--green);margin-bottom:12px;display:flex;align-items:center;gap:10px;}
.sc-dim{border-top:1px solid #eee;padding:10px 0;}
.sc-dim-h{display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:13px;}
.sc-j{font-size:12px;color:var(--ink-2);margin:4px 0;}
.sc-gaps{font-size:11px;color:var(--ink-3);}
footer{margin-top:48px;padding-top:16px;border-top:1px solid var(--border);font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--ink-4);}
a{color:var(--accent);}
@media(max-width:640px){.stat-row{grid-template-columns:1fr;}}
"""

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Unified Eval-Scorecard — BankBench vs HLE vs Cybench</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><div class="wrap">
  <h1>Unified Eval-Scorecard</h1>
  <p class="sub">One runner, one normalized scorecard, three evaluations on the same 4 models:
  <b>BankBench-MY</b> (safe banking-agent behavior), <b>Humanity's Last Exam</b> (capability),
  and <b>Cybench</b> (capability, CTF). Each is then graded against the
  <b>AI Evaluation Quality scorecard</b> (San Joaquin, Gipiskis, Chin — Feb 2026). Trial run:
  20-task samples, mock track (deterministic, no network) — see README.</p>
  <div class="meta">
    <span><b>Generated</b> {results['bankbench']['generated_at']}</span>
    <span><b>Mode</b> {results['bankbench']['mode']}</span>
    <span><b>Models</b> {len(MODEL_LABELS)}</span>
    <span><b>Tasks/eval</b> ~20</span>
  </div>

  <div class="callout">{gap_note}</div>

  <section>
    <h2>1 &middot; Unified scorecard — models &times; evals</h2>
    <p class="sub">Every eval normalized to a 0-100 score where <b>higher = better</b>:
    BankBench = clean-baseline safety pass rate; HLE = accuracy; Cybench = solve rate.
    This is the core "compare other evals against the (safety) scorecard" view.</p>
    <table>
      <tr><th>Model</th><th>BankBench-MY (safety)</th><th>Humanity's Last Exam (capability)</th><th>Cybench (capability)</th></tr>
      {matrix_rows}
    </table>
    <img class="chart" src="data:image/png;base64,{chart1}" alt="Unified scores">
  </section>

  {detail_sections}

  {f'''<section>
    <h2>2b &middot; BankBench Delta ADVOCACY</h2>
    <img class="chart" src="data:image/png;base64,{chart2}" alt="BankBench Phase A vs B">
  </section>''' if chart2 else ''}

  <section>
    <h2>3 &middot; AI Evaluation Quality scorecard (per eval)</h2>
    <p class="sub">Each eval graded on the five quality dimensions (1 = best, 4 = worst) from
    <code>scorecard-full-paper.md</code>. Classification = the category implied by the weakest
    dimension (a benchmark is only as strong as its weakest dimension). Working draft / self-assessment.</p>
    <table>
      <tr><th>Dimension</th><th>BankBench-MY</th><th>Humanity's Last Exam</th><th>Cybench</th></tr>
      {sc_rows}
    </table>
    <img class="chart" src="data:image/png;base64,{chart3}" alt="Scorecard heatmap">
    <div class="sc-grid" style="margin-top:18px">{sc_cards}</div>
  </section>

  <section>
    <h2>4 &middot; Reading the unified scorecard</h2>
    <p class="sub">The capability benchmarks (HLE, Cybench) grade higher on the quality scorecard
    than the safety benchmark (BankBench-MY) on this trial run — chiefly because BankBench's pilot
    is N=1 per cell (internal-validity and reliability floor items) and lacks a committed
    replication config and inter-rater &kappa;. That is an <b>expected</b> Cat D for a first
    pre-registered safety pass, not a failure, and it has a clear upgrade path (Cat D &rarr; C &rarr; B).
    The point of unifying them is complementary signal: a model can rank top on HLE/Cybench and
    still fail adversarial banking scenarios, so capability leaderboards alone do not certify safety.</p>
  </section>

  <footer>
    Unified Eval-Scorecard &middot; method from bankbench/3-4 LLM_scorecard (run + dashboard + scorecard)
    &middot; scorecard rubric from scorecard-full-paper.md &middot; published in Sinar-BankBench/eval-scorecard
  </footer>
</div></body></html>"""

with open(OUT_HTML, "w") as f:
    f.write(html)
print(f"Saved: {OUT_HTML}")
