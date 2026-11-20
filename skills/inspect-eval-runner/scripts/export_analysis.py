#!/usr/bin/env python3
"""Export every Inspect eval log in a directory to HTML + Markdown + slide deck,
with FULL per-task detail: input (customer message), output (agent reply),
every scorer value, the 5-dimension nuance breakdown, and critical-failure flags.

This is the automation that turns whatever lands in `logs/` (and therefore in
`http://127.0.0.1:7575/`) into readable, shareable artefacts. It is the
companion to `summarize.py`: that one answers "what ran / how did it score" in
plain text; this one renders the whole thing — every transcript, every score —
as a static page, a markdown report, and a slide deck.

Usage:
    python3 export_analysis.py logs/                       # all logs -> analysis/
    python3 export_analysis.py logs/ --out analysis/       # explicit dir
    python3 export_analysis.py logs/ --watch              # poll for new logs forever
    python3 export_analysis.py logs/ --suite ../suites/sme-whatsapp   # load item text

No external dependencies beyond inspect_ai. The slide deck is a standalone HTML
file (CSS scroll-snap, keyboard nav) — no CDN, works offline.
"""
import argparse
import glob
import html
import json
import os
import sys
import time
from pathlib import Path

from inspect_ai.log import read_eval_log

NUANCE_DIMS = ["contextual_accuracy", "tone_empathy", "policy_adherence",
               "escalation_judgment", "language_fit"]
SCORE_ORDER = ["sme_safety", "sme_helpfulness", "sme_customer_support", "sme_nuance"]


def esc(x):
    return html.escape(str(x if x is not None else ""))


def short_model(m):
    return (m or "").replace("openai-api/nous/", "").replace("openai-api/", "")


def load_item_meta(suite_dir):
    meta = {}
    if not suite_dir:
        return meta
    sd = Path(suite_dir)
    for pat in ("*tasks.json", "items.json", "**/*tasks.json"):
        for b in sd.glob(pat):
            try:
                data = json.loads(b.read_text())
                items = data.get("items", data if isinstance(data, list) else [])
                for t in items:
                    md = dict(t.get("metadata", {}))
                    md["target"] = t.get("target")
                    md.setdefault("input", t.get("input", ""))
                    meta[t["id"]] = md
            except Exception:
                pass
    return meta


def extract_run(path, item_meta):
    lg = read_eval_log(path)
    model = lg.eval.model if hasattr(lg, "eval") else None
    task = lg.eval.task if hasattr(lg, "eval") else None
    created = str(getattr(lg.eval, "created", ""))[:19] if hasattr(lg, "eval") else ""
    samples = []
    for s in lg.samples:
        out = s.output.completion if s.output else ""
        blank = not (out or "").strip()
        scores = {}
        for name, sc in (s.scores or {}).items():
            scores[name] = {
                "value": getattr(sc, "value", None),
                "explanation": getattr(sc, "explanation", ""),
                "metadata": getattr(sc, "metadata", None) or {},
            }
        md = item_meta.get(s.id, {})
        samples.append({
            "id": s.id,
            "input": s.input if isinstance(s.input, str) else (getattr(s.input, "text", "") or ""),
            "output": out,
            "blank": blank,
            "target": md.get("target"),
            "category": md.get("category"),
            "scores": scores,
            "crit": any(
                (sc.get("metadata") or {}).get("critical_failure")
                for sc in scores.values()
            ),
        })
    return {
        "file": Path(path).name,
        "model": model,
        "model_short": short_model(model),
        "task": task,
        "created": created,
        "n": len(samples),
        "n_blank": sum(1 for s in samples if s["blank"]),
        "samples": samples,
    }


def score_means(run):
    means = {}
    for name in SCORE_ORDER:
        vals = [float(s["scores"].get(name, {}).get("value") or 0)
                for s in run["samples"]
                if not s["blank"] and s["scores"].get(name, {}).get("value") is not None]
        if vals:
            means[name] = sum(vals) / len(vals)
    return means


# ----------------------------------------------------------------- HTML
def render_html(runs, out_dir, item_meta):
    idx = out_dir / "index.html"
    cards = []
    for r in runs:
        means = score_means(r)
        bars = "".join(
            f'<div class="brow"><span class="bl">{esc(n.replace("sme_",""))}</span>'
            f'<div class="bt"><div class="bf" style="width:{means[n]*100:.0f}%"></div></div>'
            f'<span class="bv">{means[n]:.2f}</span></div>'
            for n in SCORE_ORDER if n in means
        )
        rows = []
        for s in r["samples"]:
            nu = s["scores"].get("sme_nuance", {}).get("metadata", {})
            nu_cells = "".join(
                f'<td class="{"cf" if nu.get(d) is not None and float(nu.get(d,0))<0.6 else ""}">{nu.get(d) if nu.get(d) is not None else "—"}</td>'
                for d in NUANCE_DIMS
            )
            rows.append(
                f'<tr class="{"blank" if s["blank"] else ""} {"crit" if s["crit"] else ""}">'
                f'<td class="tid">{esc(s["id"])}</td>'
                f'<td class="in">{esc(s["input"])}</td>'
                f'<td class="out">{esc(s["output"][:600]) or "<i>empty — harness fault</i>"}</td>'
                f'<td>{s["scores"].get("sme_safety",{}).get("value") or "—"}</td>'
                f'<td>{s["scores"].get("sme_helpfulness",{}).get("value") or "—"}</td>'
                f'<td>{s["scores"].get("sme_customer_support",{}).get("value") or "—"}</td>'
                f'<td>{s["scores"].get("sme_nuance",{}).get("value") or "—"}</td>'
                f'{nu_cells}</tr>'
            )
        nu_head = "".join(f"<th>{d.replace('_',' ')}</th>" for d in NUANCE_DIMS)
        cards.append(f"""
        <section class="run">
          <h2>{esc(r['model_short'])} <span class="sub">· {esc(r['task'])} · {esc(r['created'])}</span></h2>
          <p class="meta">{r['n']} tasks · {r['n_blank']} empty (harness fault, excluded)</p>
          <div class="bars">{bars}</div>
          <details><summary>Show all {r['n']} tasks (inputs, outputs, scores)</summary>
          <table class="grid">
            <thead><tr><th>ID</th><th>Customer message</th><th>Agent reply</th>
            <th>Safety</th><th>Help</th><th>Cust.Sup</th><th>Nuance</th>{nu_head}</tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table></details>
        </section>""")
    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Eval Analysis — {len(runs)} runs</title>
<style>
*{{box-sizing:border-box}} body{{font-family:Inter,system-ui,sans-serif;margin:0;background:#FAFAF8;color:#23271f;line-height:1.5}}
.wrap{{max-width:1100px;margin:0 auto;padding:24px 20px 80px}}
h1{{font-family:'DM Serif Display',serif;font-weight:400;font-size:26px;margin:0 0 4px}}
.sub{{color:#6b7260;font-size:12px;font-weight:400}}
.run{{background:#fff;border:1px solid #e7e7e1;border-radius:14px;padding:16px 18px;margin:16px 0}}
.brow{{display:flex;align-items:center;gap:10px;margin:5px 0}}
.bl{{width:120px;font-size:12px;font-weight:600;text-transform:capitalize}}
.bt{{flex:1;height:14px;background:#eee;border-radius:7px;overflow:hidden}}
.bf{{height:100%;background:#266533}}
.bv{{width:42px;text-align:right;font-variant-numeric:tabular-nums}}
.meta{{color:#6b7260;font-size:12px;margin:8px 0}}
table.grid{{width:100%;border-collapse:collapse;font-size:12px;margin-top:8px}}
.grid th{{text-align:left;color:#6b7260;font-size:10px;text-transform:uppercase;padding:6px 7px;border-bottom:1px solid #e7e7e1}}
.grid td{{border-bottom:1px solid #f0f0ea;padding:6px 7px;vertical-align:top}}
.grid td.tid{{font-weight:700}}.grid td.in{{max-width:220px;color:#4d5a4f}}
.grid td.out{{max-width:340px;white-space:pre-wrap}}.grid tr.blank{{opacity:.5}}
.grid tr.crit{{background:#fdecea}}.grid td.cf{{background:#fff3cd}}
</style></head><body><div class="wrap">
<h1>Eval Analysis</h1><div class="sub">{len(runs)} runs · generated from logs/ · full per-task detail</div>
{''.join(cards)}
</div></body></html>"""
    idx.write_text(doc)


# ----------------------------------------------------------------- MD
def render_md(runs, out_dir):
    parts = [f"# Eval Analysis\n\n_{len(runs)} runs generated from `logs/`_\n"]
    for r in runs:
        means = score_means(r)
        parts.append(f"## {r['model_short']}\n\n"
                     f"- Task: `{r['task']}`  ·  {r['created']}\n"
                     f"- {r['n']} tasks, {r['n_blank']} empty (excluded)\n")
        if means:
            parts.append("**Scores (0–1):** " +
                         ", ".join(f"{n.replace('sme_','')}={means[n]:.2f}" for n in SCORE_ORDER if n in means) + "\n")
        parts.append("\n| ID | Customer | Agent reply | Safety | Help | Cust.Sup | Nuance |")
        parts.append("|---|---|---|---|---|---|---|")
        for s in r["samples"]:
            reply = (s["output"][:200].replace("\n", " ") or "_(empty)_")
            parts.append(
                f"| {s['id']} | {s['input'][:60].replace('|','/')} | {reply} | "
                f"{s['scores'].get('sme_safety',{}).get('value') or '—'} | "
                f"{s['scores'].get('sme_helpfulness',{}).get('value') or '—'} | "
                f"{s['scores'].get('sme_customer_support',{}).get('value') or '—'} | "
                f"{s['scores'].get('sme_nuance',{}).get('value') or '—'} |"
            )
        parts.append("")
    (out_dir / "analysis.md").write_text("\n".join(parts))


# ----------------------------------------------------------------- SLIDE
def render_slides(runs, out_dir):
    slides = [f"""<section class="slide title"><h1>Eval Analysis</h1>
<p>{len(runs)} runs · {runs[0]['task'] if runs else ''}</p></section>"""]
    # comparison slide
    head = "".join(f"<th>{r['model_short']}</th>" for r in runs)
    if runs:
        rows = ""
        for n in SCORE_ORDER:
            cells = ""
            for r in runs:
                m = score_means(r).get(n)
                cells += f"<td>{m:.2f}</td>" if m is not None else "<td>—</td>"
            rows += f"<tr><td>{n.replace('sme_','')}</td>{cells}</tr>"
        slides.append(f"""<section class="slide"><h2>Score comparison</h2>
<table class="cmp"><thead><tr><th>score</th>{head}</tr></thead><tbody>{rows}</tbody></table></section>""")
    # per-run task slides (summary: lowest-scoring tasks)
    for r in runs:
        low = sorted([s for s in r["samples"] if not s["blank"]],
                     key=lambda s: float(s["scores"].get("sme_safety", {}).get("value") or 1))[:3]
        items = "".join(
            f"<li><b>{esc(s['id'])}</b> safety={s['scores'].get('sme_safety',{}).get('value')}"
            f"<br><span class='q'>{esc(s['input'][:120])}</span>"
            f"<br><span class='a'>{esc(s['output'][:200])}</span></li>"
            for s in low
        )
        slides.append(f"""<section class="slide"><h2>{esc(r['model_short'])} — weakest replies</h2>
<ul class="tasks">{items}</ul></section>""")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><title>Eval Slides</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,system-ui,sans-serif;background:#1d2b20;color:#f3f1e6}}
.slide{{height:100vh;width:100vw;scroll-snap-align:start;display:flex;flex-direction:column;justify-content:center;padding:6vw;overflow:auto}}
h1{{font-family:'DM Serif Display',serif;font-size:7vw;margin:0}} h2{{font-size:4vw;margin:0 0 2vh;color:#E1DC53}}
p{{font-size:2vw;color:#BEE0C7}} table.cmp{{border-collapse:collapse;font-size:2vw;margin-top:2vh}}
.cmp th,.cmp td{{border:1px solid #3a4d3f;padding:1vh 2vw;text-align:center}} .cmp th{{color:#E1DC53}}
.tasks li{{font-size:1.6vw;margin-bottom:2vh;list-style:none}} .q{{color:#9fb8a6}} .a{{color:#f3f1e6}}
</style></head><body style="scroll-snap-type:y mandatory">
{''.join(slides)}
<script>addEventListener('keydown',e=>{{const d=document.documentElement;if(e.key==='ArrowDown'||e.key===' ')d.scrollBy(0,innerHeight);if(e.key==='ArrowUp')d.scrollBy(0,-innerHeight);}});</script>
</body></html>"""
    (out_dir / "slides.html").write_text(doc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("logs", nargs="?", default="logs")
    ap.add_argument("--out", default=None)
    ap.add_argument("--suite", help="suite dir for item text")
    ap.add_argument("--watch", action="store_true", help="poll logs/ for new files forever")
    a = ap.parse_args()

    out_dir = Path(a.out) if a.out else (Path(a.logs).resolve().parent / "analysis")
    out_dir.mkdir(parents=True, exist_ok=True)
    item_meta = load_item_meta(a.suite)

    def run_once():
        paths = sorted(glob.glob(str(Path(a.logs) / "*.eval")))
        runs = []
        for p in paths:
            try:
                runs.append(extract_run(p, item_meta))
            except Exception as e:
                print(f"  ! {Path(p).name}: {e}", file=sys.stderr)
        if not runs:
            return 0
        render_html(runs, out_dir, item_meta)
        render_md(runs, out_dir)
        render_slides(runs, out_dir)
        print(f"  wrote {len(runs)} runs -> {out_dir}/ (index.html, analysis.md, slides.html)")
        return len(runs)

    n = run_once()
    if not a.watch:
        return
    seen = set(glob.glob(str(Path(a.logs) / "*.eval")))
    print(f"  watching {a.logs} for new logs (Ctrl-C to stop)...")
    while True:
        time.sleep(15)
        cur = set(glob.glob(str(Path(a.logs) / "*.eval")))
        if cur - seen:
            run_once()
            seen = cur


if __name__ == "__main__":
    main()
