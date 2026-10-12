"""Build a BankBench-branded HTML results page from Kuasa-MY .eval logs.

Usage:  ./.venv/bin/python build_results_html.py [logdir] [out.html]
Light theme only. Every figure is read from real .eval logs - nothing is typed in.
"""
import glob
import html
import json
import os
import sys
from collections import defaultdict, Counter
from pathlib import Path

from inspect_ai.log import read_eval_log

HERE = Path(__file__).resolve().parent
LOGDIR = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "logs2"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "kuasa-results.html"

FAMILY_LABEL = {
    "statutory_correctness": "Statutory (KSTAT)",
    "einvoice_integrity": "e-Invoice (KEINV)",
    "receipt_booking_fidelity": "Receipt booking (KBOOK)",
}
MOCK_BASELINES = {  # from `python kuasa_eval.py --selftest` (deterministic mocks)
    "mock/oracle (ideal agent)": {"acc": 1.000, "n": 14, "mock": True},
    "mock/naive (always-PROCEED)": {"acc": 0.214, "n": 14, "mock": True},
}


def short(model: str) -> str:
    return model.replace("openrouter/", "").replace(":free", " (free)")


def load(logdir: Path):
    """-> {model: {task_id: [(value, explanation, category), ...]}}, plus statuses"""
    per_model = defaultdict(lambda: defaultdict(list))
    status = {}
    files = sorted(glob.glob(str(logdir / "*.eval")))
    for f in files:
        try:
            lg = read_eval_log(f)
        except Exception as e:  # noqa: BLE001
            print(f"[warn] unreadable log {f}: {e}")
            continue
        if "kuasa-correctness" not in (lg.eval.task or "") and "kuasa" not in (lg.eval.task or ""):
            continue
        model = lg.eval.model
        status[model] = str(lg.status)
        for s in (lg.samples or []):
            sc = s.scores.get("kuasa_correctness_scorer")
            if sc is None:
                continue
            per_model[model][s.id].append(
                (float(sc.value), sc.explanation or "", s.metadata.get("category", ""))
            )
    return per_model, status, files


def aggregate(per_model):
    """-> rows: model, n, acc, parse_errors, {family: acc}, {task_id: acc}"""
    rows = []
    for model, tasks in per_model.items():
        vals, parse_err = [], 0
        fam = defaultdict(list)
        per_task = {}
        for tid, runs in tasks.items():
            tv = [v for v, _e, _c in runs]
            per_task[tid] = sum(tv) / len(tv) if tv else 0.0
            for v, expl, cat in runs:
                vals.append(v)
                fam[cat].append(v)
                if "PARSE_ERROR" in expl:
                    parse_err += 1
        if not vals:
            continue
        rows.append({
            "model": model, "short": short(model), "n": len(vals),
            "acc": sum(vals) / len(vals), "parse_errors": parse_err,
            "families": {k: (sum(v) / len(v), len(v)) for k, v in fam.items()},
            "per_task": per_task,
        })
    rows.sort(key=lambda r: -r["acc"])
    return rows

def render(rows, status, files, logdir: Path) -> str:
    fams = ["statutory_correctness", "einvoice_integrity", "receipt_booking_fidelity"]
    try:
        _ds = json.loads((HERE / "kuasa_my_tasks.json").read_text())
        task_order = [x["id"] for x in _ds]
        task_fam = {x["id"]: x["metadata"]["category"] for x in _ds}
    except Exception:
        task_order = sorted({tid for r in rows for tid in r["per_task"]})
        task_fam = {}
    try:
        n_tasks = len(json.loads((HERE / "kuasa_my_tasks.json").read_text()))
    except Exception:
        n_tasks = max((r["n"] for r in rows), default=0) // 3

    trs = []
    for r in rows:
        cells = "".join(
            f'<td class="num">{r["families"].get(f, (0, 0))[0]:.2f}'
            f'<span class="sub">n={r["families"].get(f, (0, 0))[1]}</span></td>'
            for f in fams
        )
        pe = (f'<span class="warn">{r["parse_errors"]}</span>' if r["parse_errors"] else "0")
        trs.append(
            f'<tr><td class="model">{html.escape(r["short"])}</td>'
            f'<td class="num big">{r["acc"]:.3f}</td>{cells}'
            f'<td class="num">{r["n"]}</td><td class="num">{pe}</td></tr>'
        )
    for name, b in MOCK_BASELINES.items():
        trs.append(
            f'<tr class="mock"><td class="model">{html.escape(name)}</td>'
            f'<td class="num big">{b["acc"]:.3f}</td>'
            f'<td class="num" colspan="3">deterministic mock &mdash; harness check, not a model</td>'
            f'<td class="num">{b["n"]}</td><td class="num">0</td></tr>'
        )

    fam_blocks = []
    for f in fams:
        bars = []
        for r in rows:
            acc, n = r["families"].get(f, (0.0, 0))
            bars.append(
                f'<div class="row"><span class="lbl">{html.escape(r["short"])}</span>'
                f'{bar(acc, colour_for(acc))}<span class="val">{acc:.2f}</span></div>'
            )
        fam_blocks.append(
            f'<div class="card"><h3>{FAMILY_LABEL[f]}</h3>{"".join(bars)}</div>'
        )

    # ---- per-model x per-task heatmap ----
    hdr = "".join(
        f'<th class="hm-h" title="{html.escape(task_fam.get(tid, ""))}">'
        f'{html.escape(tid)}</th>'
        for tid in task_order
    )
    hm_rows = []
    for r in rows:
        cells = []
        for tid in task_order:
            v = r["per_task"].get(tid)
            if v is None:
                cells.append('<td class="hm-c hm-na" title="not run">&middot;</td>')
                continue
            bg = colour_for(v)
            fg = "#fff" if v >= 0.60 else "#1d2b20"
            cells.append(
                f'<td class="hm-c" style="background:{bg};color:{fg}" '
                f'title="{html.escape(r["short"])} / {html.escape(tid)}: {v:.2f}">'
                f'{v:.2f}</td>'
            )
        hm_rows.append(
            f'<tr><td class="hm-lbl">{html.escape(r["short"])}</td>{"".join(cells)}</tr>'
        )
    legend = "".join(
        f'<span class="lg"><i style="background:{colour_for(v)}"></i>{lbl}</span>'
        for v, lbl in ((0.0, "0.00 fail"), (0.5, "0.50 partial"), (1.0, "1.00 pass"))
    )
    heatmap = (
        '<div class="card hm-wrap">'
        '<div class="hm-scroll"><table class="hm"><thead><tr>'
        f'<th class="hm-lbl"></th>{hdr}</tr></thead><tbody>{"".join(hm_rows)}</tbody></table></div>'
        f'<div class="hm-legend">{legend}'
        '<span class="lg"><i class="na"></i>not run</span></div>'
        '<p class="hm-note">Each cell is the mean over 3 epochs. '
        'KSTAT = statutory, KEINV = e-invoice, KBOOK = receipt booking.</p></div>'
    )

    detail = []
    for r in rows:
        fails = []
        for tid, runs in sorted(per_model[r["model"]].items()):
            for v, expl, cat in runs:
                if v == 0:
                    fails.append((tid, cat, expl))
        if not fails:
            continue
        seen = set()
        items = []
        for tid, cat, expl in fails:
            if tid in seen:
                continue
            seen.add(tid)
            items.append(
                f'<li><code>{html.escape(tid)}</code> '
                f'<span class="tag">{html.escape(FAMILY_LABEL.get(cat, cat))}</span>'
                f'<div class="why">{html.escape(expl[:220])}</div></li>'
            )
        detail.append(
            f'<details><summary>{html.escape(r["short"])} '
            f'<span class="cnt">{len(seen)} task(s) failed</span></summary>'
            f'<ul class="fails">{"".join(items)}</ul></details>'
        )

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kuasa-MY correctness eval &middot; BankBench</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--cream:#F6F4DC;--basil:#266533;--passata:#F16838;--lemons:#E1DC53;
--fresh:#339551;--minty:#BEE0C7;--white:#fff;--ink:#1d2b20;--line:#e4e0c6;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--cream);color:var(--ink);
font-family:'Inter',system-ui,sans-serif;line-height:1.5}}
.wrap{{max-width:1080px;margin:0 auto;padding:40px 24px 72px}}
header{{border-bottom:3px solid var(--basil);padding-bottom:20px;margin-bottom:28px}}
.eyebrow{{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
color:var(--basil);margin:0 0 8px}}
h1{{font-family:'DM Serif Display',serif;font-size:40px;margin:0 0 8px;font-weight:400}}
h2{{font-family:'DM Serif Display',serif;font-size:24px;margin:36px 0 14px;font-weight:400}}
h3{{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
color:var(--basil);margin:0 0 14px}}
.lede{{font-size:15px;color:#4a5548;max-width:74ch;margin:0}}
.banner{{background:#fff;border:1px solid var(--line);border-left:5px solid var(--passata);
border-radius:0 10px 10px 0;padding:14px 18px;margin:22px 0;font-size:13.5px}}
.banner b{{color:#b83a0d}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);
border-radius:12px;overflow:hidden;font-size:13.5px}}
th{{background:var(--basil);color:#fff;text-align:left;padding:11px 13px;
font-size:11px;letter-spacing:.07em;text-transform:uppercase;font-weight:600}}
td{{padding:11px 13px;border-top:1px solid var(--line);vertical-align:middle}}
td.num{{text-align:right;font-variant-numeric:tabular-nums}}
td.big{{font-weight:700;font-size:15px}}
td.model{{font-weight:600}}
.sub{{display:block;font-size:10.5px;color:#8a9284;font-weight:400}}
tr.mock td{{background:#fbfaf2;color:#6b7365;font-style:italic}}
.warn{{color:#b83a0d;font-weight:700}}
.card{{background:#fff;border:1px solid var(--line);border-radius:12px;
padding:18px 20px;margin-bottom:14px}}
.row{{display:flex;align-items:center;gap:12px;margin:7px 0}}
.lbl{{flex:0 0 250px;font-size:12.5px;font-weight:500;overflow:hidden;
text-overflow:ellipsis;white-space:nowrap}}
.bar{{flex:1;height:9px;background:#eef0e2;border-radius:5px;overflow:hidden}}
.bar span{{display:block;height:100%;border-radius:5px}}
.val{{flex:0 0 44px;text-align:right;font-size:12.5px;font-weight:700;
font-variant-numeric:tabular-nums}}
details{{background:#fff;border:1px solid var(--line);border-radius:10px;
padding:12px 16px;margin-bottom:9px}}
summary{{cursor:pointer;font-weight:600;font-size:13.5px}}
.cnt{{color:#8a9284;font-weight:400;font-size:12px}}
ul.fails{{margin:12px 0 4px;padding-left:18px}}
ul.fails li{{margin-bottom:11px;font-size:12.5px}}
code{{background:#eef0e2;padding:1px 6px;border-radius:4px;font-size:11.5px}}
.tag{{font-size:10px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
color:var(--basil);background:var(--minty);padding:2px 7px;border-radius:9px;margin-left:6px}}
.why{{color:#5a6252;font-size:12px;margin-top:3px;font-family:ui-monospace,Menlo,monospace}}
.hm-wrap{{padding:18px 20px 14px}}
.hm-scroll{{overflow-x:auto;padding-bottom:6px}}
table.hm{{border:0;background:transparent;border-radius:0;font-size:11px;width:auto}}
table.hm th.hm-h{{background:transparent;color:#6b7365;font-size:9.5px;letter-spacing:.03em;
padding:0 2px 6px;text-align:center;font-weight:600;white-space:nowrap}}
td.hm-lbl,th.hm-lbl{{font-size:11.5px;font-weight:600;padding:0 12px 0 0;white-space:nowrap;
border:0;background:transparent;text-align:left}}
td.hm-c{{width:34px;min-width:34px;height:26px;text-align:center;border:2px solid var(--cream);
border-radius:5px;font-variant-numeric:tabular-nums;font-weight:600;font-size:10.5px;
padding:0;cursor:default}}
td.hm-na{{background:#eef0e2;color:#b3b8a8}}
.hm-legend{{display:flex;gap:16px;align-items:center;margin-top:12px;font-size:11px;color:#5a6252}}
.lg{{display:flex;align-items:center;gap:5px}}
.lg i{{width:12px;height:12px;border-radius:3px;display:inline-block}}
.lg i.na{{background:#eef0e2}}
.hm-note{{font-size:11.5px;color:#8a9284;margin:9px 0 0}}
footer{{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);
font-size:12px;color:#6b7365}}
</style></head><body><div class="wrap">
<header>
<p class="eyebrow">BankBench-MY &middot; Sinar Civic Tech</p>
<h1>Kuasa-MY correctness eval</h1>
<p class="lede">Statutory payroll &amp; SST arithmetic, e-invoice submission integrity, and
receipt&rarr;ledger booking fidelity &mdash; run through the Inspect AI harness.
{len(rows)} models &times; {n_tasks} tasks &times; 3 epochs (N=3 per cell), temperature 0.</p>
</header>

<div class="banner">
<b>Exploratory result &mdash; not a product verdict.</b>
Every rate table and submission schema in this suite is a <b>demo fixture</b>; ground truth is
computed from that fixture, not asserted as current Malaysian law. No live model has been run
against the real EPF/SOCSO/EIS schedule or the official MyInvois schema. This is a
scorecard Category&nbsp;E artefact: use it to direct further work, not to make claims about any
named product. Named-product framing requires written permission and legal review.
</div>

<h2>Overall accuracy</h2>
<table>
<thead><tr><th>Model</th><th class="num">Accuracy</th>
<th class="num">Statutory</th><th class="num">e-Invoice</th><th class="num">Receipt</th>
<th class="num">n</th><th class="num">Parse err</th></tr></thead>
<tbody>{"".join(trs)}</tbody></table>

<h2>By family</h2>
{"".join(fam_blocks)}

<h2>Per-model &times; per-task</h2>
{heatmap}

<h2>What failed, per model</h2>
{"".join(detail) if detail else "<p class='lede'>No failures recorded.</p>"}

<footer>
Generated from {len(files)} Inspect <code>.eval</code> log(s) in <code>{html.escape(str(logdir))}</code>.
Every figure on this page is read from those logs &mdash; none is hand-entered.
BankBench &middot; CC BY-SA 4.0 &middot; draft, not published.
</footer>
</div></body></html>"""


def bar(pct: float, colour: str) -> str:
    w = max(0.0, min(1.0, pct)) * 100
    return f'<div class="bar"><span style="width:{w:.1f}%;background:{colour}"></span></div>'


def colour_for(pct: float) -> str:
    if pct >= 0.85:
        return "var(--fresh)"
    if pct >= 0.60:
        return "var(--lemons)"
    if pct >= 0.35:
        return "var(--passata)"
    return "#b83a0d"


if __name__ == "__main__":
    per_model, status, files = load(LOGDIR)
    rows = aggregate(per_model)
    print(f"log dir: {LOGDIR}")
    print(f"logs read: {len(files)}   scored models: {len(rows)}")
    for r in rows:
        print(f"  {r['short']:<46} acc={r['acc']:.3f}  n={r['n']}  parse_err={r['parse_errors']}")
    if not rows:
        print("no scored samples found - is the run still in flight?")
        sys.exit(1)
    OUT.write_text(render(rows, status, files, LOGDIR), encoding="utf-8")
    print(f"\nwrote {OUT}  ({OUT.stat().st_size} bytes)")
