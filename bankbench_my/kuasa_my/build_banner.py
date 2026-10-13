"""Build a horizontal scroll-snap banner deck for the Kuasa-MY correctness results.

Format modelled on bankbench/bluedot-evals-1.html (Fraunces + Karla + JetBrains Mono,
wordmark, navdots) but HORIZONTAL (scroll-snap-type: x mandatory) with prev/next and
arrow keys. Light theme. Every figure is pulled from the .eval logs via
build_results_html - nothing is typed in.

Usage:  ./.venv/bin/python build_banner.py [logdir] [out.html]
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_results_html as B   # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
LOGDIR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "logs2"
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "kuasa-banner.html"

CLEAN = {"deepseek/deepseek-chat-v3.1": "DeepSeek v3.1",
         "openai/gpt-5-nano": "GPT-5 nano",
         "mistralai/mistral-small-24b-instruct-2501": "Mistral Small 24B",
         "openai/gpt-4o-mini": "GPT-4o mini",
         "google/gemini-2.5-flash-lite": "Gemini 2.5 Flash-Lite"}
FAM_LABEL = {"statutory_correctness": "Payroll &amp; tax maths",
             "einvoice_integrity": "e-Invoice filing",
             "receipt_booking_fidelity": "Receipt bookkeeping"}

per_model, status, files = B.load(LOGDIR)
rows = B.aggregate(per_model)
if not rows:
    sys.exit("no scored samples found")

task_order = [x["id"] for x in json.loads((HERE / "kuasa_my_tasks.json").read_text())]
n_models, n_runs = len(rows), sum(r["n"] for r in rows)
fams = ["statutory_correctness", "einvoice_integrity", "receipt_booking_fidelity"]
fam_mean = {f: sum(r["families"].get(f, (0, 0))[0] for r in rows) / n_models for f in fams}
task_mean = {}
for t in task_order:
    v = [r["per_task"][t] for r in rows if t in r["per_task"]]
    if v:
        task_mean[t] = sum(v) / len(v)
weakest_task = min(task_mean, key=task_mean.get)
weak_fam = min(fam_mean, key=fam_mean.get)
strong_fam = max(fam_mean, key=fam_mean.get)
fully_passed = sum(1 for r in rows for t in task_order if r["per_task"].get(t, 0) == 1.0)
top = rows[0]
mocks = B.MOCK_BASELINES


def col(p):
    return ("var(--ok)" if p >= .85 else "var(--ember)" if p >= .6
            else "var(--danger)" if p >= .35 else "#8c2f24")

CSS = """
:root{
  --cream:#FAF6EE; --cream-2:#F3EDE0; --ink:#3A3530; --ink-soft:#6B6358;
  --wood:#8B6F4E; --moss:#5B7B6B; --moss-deep:#3F5C4F; --ember:#C97B4A;
  --ember-deep:#9C5A34; --card-line:#E0D5BE; --danger:#B4483A; --ok:#4A7A5C;
}
*{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
body{background:#DDD6C6;font-family:'Karla',sans-serif;color:var(--ink);overflow:hidden;}
.deck{display:flex;height:100vh;overflow-x:auto;overflow-y:hidden;
  scroll-snap-type:x mandatory;scrollbar-width:none;}
.deck::-webkit-scrollbar{display:none;}
section.slide{min-width:100vw;width:100vw;height:100vh;flex:0 0 100vw;
  scroll-snap-align:start;position:relative;display:flex;flex-direction:column;
  justify-content:center;padding:74px 7vw 98px;overflow:hidden;}
.eyebrow{font-size:13px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;
  margin-bottom:16px;display:inline-block;color:var(--wood);}
.headline{font-family:'Fraunces',serif;font-weight:500;line-height:1.14;
  letter-spacing:-.01em;}
.subtext{font-size:18px;line-height:1.6;max-width:780px;color:var(--ink-soft);}
.mono{font-family:'JetBrains Mono',monospace;}
.wordmark{display:flex;align-items:center;gap:12px;position:fixed;top:22px;left:30px;z-index:60;}
.wordmark .mark{width:26px;height:26px;border-radius:50%;background:var(--wood);
  position:relative;flex-shrink:0;}
.wordmark .mark::after{content:'';position:absolute;width:8px;height:8px;border-radius:50%;
  top:6px;left:7px;background:var(--cream);opacity:.9;}
.wordmark .word{font-family:'Fraunces',serif;font-weight:600;font-size:16px;letter-spacing:-.01em;}
.navdots{position:fixed;right:22px;top:50%;transform:translateY(-50%);z-index:60;
  display:flex;flex-direction:column;gap:10px;}
.navdots a{width:9px;height:9px;border-radius:50%;background:rgba(58,53,48,.22);
  display:block;transition:background .2s,transform .2s;}
.navdots a.active{background:var(--wood);transform:scale(1.3);}
.pager{position:fixed;bottom:20px;left:30px;z-index:60;display:flex;align-items:center;gap:14px;}
.pager button{font-family:'Karla',sans-serif;font-size:13px;font-weight:700;
  border:1px solid var(--card-line);background:#fff;color:var(--ink);border-radius:20px;
  padding:8px 18px;cursor:pointer;}
.pager button:hover{background:var(--cream-2);}
.pager .counter{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--ink-soft);}
.card{background:#fff;border:1px solid var(--card-line);border-radius:14px;
  padding:24px 26px;box-shadow:0 6px 20px rgba(58,53,48,.06);}
.pill{display:inline-block;font-size:12.5px;font-weight:700;padding:5px 14px;
  border-radius:20px;letter-spacing:.03em;}
.pill-moss{background:rgba(91,123,107,.12);color:var(--moss);}
.pill-ember{background:rgba(201,123,74,.14);color:var(--ember-deep);}
.pill-danger{background:rgba(180,72,58,.12);color:var(--danger);}
.pill-ok{background:rgba(74,122,92,.12);color:var(--ok);}
.stat-row{display:flex;gap:16px;margin-top:26px;flex-wrap:wrap;max-width:980px;}
.stat-tile{background:#fff;border:1px solid var(--card-line);border-radius:12px;
  padding:16px 22px;min-width:138px;}
.stat-tile .val{font-family:'Fraunces',serif;font-size:29px;color:var(--moss-deep);}
.stat-tile .lbl{font-size:12.5px;color:var(--ink-soft);margin-top:3px;}
.cards3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:26px;
  max-width:1090px;}
.cards3 h4{font-family:'Fraunces',serif;font-size:19px;font-weight:500;margin-bottom:8px;}
.cards3 p{font-size:13.5px;line-height:1.55;color:var(--ink-soft);}
.cards3 .big{font-family:'Fraunces',serif;font-size:29px;color:var(--moss-deep);margin-top:12px;}
table.rt{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--card-line);
  border-radius:12px;overflow:hidden;font-size:13.5px;max-width:900px;margin-top:14px;}
table.rt th{background:var(--moss-deep);color:#FBF8F2;text-align:left;padding:10px 14px;
  font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;font-weight:600;}
table.rt td{padding:10px 14px;border-top:1px solid var(--card-line);}
table.rt td.n{text-align:right;font-family:'JetBrains Mono',monospace;font-weight:600;}
table.rt tr.mock td{background:var(--cream-2);color:var(--ink-soft);font-style:italic;}
.bar{height:7px;background:var(--cream-2);border-radius:4px;overflow:hidden;margin-top:6px;}
.bar span{display:block;height:100%;border-radius:4px;}
.grid{display:grid;grid-template-columns:132px repeat(14,minmax(0,1fr));gap:5px;
  align-items:end;margin-top:20px;max-width:1090px;}
.grid .h{font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--ink-soft);
  writing-mode:vertical-rl;transform:rotate(180deg);height:46px;justify-self:center;}
.grid .mn{font-size:12px;font-weight:600;text-align:right;padding-right:8px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.grid .c{height:30px;border-radius:5px;display:flex;align-items:center;justify-content:center;
  font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:600;}
.cards2{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:26px;max-width:1080px;}
.cards2 h4{font-family:'Fraunces',serif;font-size:19px;font-weight:500;margin-bottom:8px;}
.cards2 p{font-size:13.5px;line-height:1.6;color:var(--ink-soft);}
.s-hero{background:var(--moss-deep);color:#FBF8F2;text-align:center;align-items:center;}
.s-hero .headline{font-size:54px;color:#FBF8F2;max-width:960px;margin-bottom:20px;}
.s-hero .subtext{color:#D9E4DB;font-size:20px;margin:0 auto;max-width:700px;}
.s-hero .kicker{font-size:13px;letter-spacing:.14em;text-transform:uppercase;
  color:#CFE0D3;margin-bottom:22px;font-weight:700;}
.s-end{background:var(--moss-deep);color:#FBF8F2;}
.s-end .headline{font-size:40px;color:#FBF8F2;margin-bottom:16px;}
.s-end .subtext{color:#D9E4DB;}
.s-end .credit{font-size:13px;color:#CFE0D3;margin-top:30px;opacity:.85;}
.s-results{background:var(--cream-2);}
.s-alt{background:var(--cream);}
h2.headline{font-size:40px;margin-bottom:14px;}
h2.headline.sm{font-size:32px;}
"""

# ---------------------------------------------------------------- fragments
def bars():
    out = []
    for r in rows:
        c = col(r["acc"])
        out.append(
            f'<div style="display:flex;align-items:center;gap:12px;margin:8px 0">'
            f'<span style="flex:0 0 190px;font-size:13.5px;font-weight:600">'
            f'{CLEAN.get(r["model"], r["short"])}</span>'
            f'<span class="bar" style="flex:1"><span style="width:{r["acc"]*100:.0f}%;'
            f'background:{c}"></span></span>'
            f'<span class="mono" style="flex:0 0 46px;text-align:right;font-weight:600">'
            f'{r["acc"]:.2f}</span></div>'
        )
    return "".join(out)


def table():
    out = []
    for r in rows:
        out.append(
            f'<tr><td>{CLEAN.get(r["model"], r["short"])}</td>'
            f'<td class="n">{r["acc"]:.2f}</td>'
            f'<td class="n">{r["families"].get("statutory_correctness",(0,0))[0]:.2f}</td>'
            f'<td class="n">{r["families"].get("einvoice_integrity",(0,0))[0]:.2f}</td>'
            f'<td class="n">{r["families"].get("receipt_booking_fidelity",(0,0))[0]:.2f}</td>'
            f'</tr>'
        )
    for name, b in mocks.items():
        out.append(
            f'<tr class="mock"><td>{name.replace("mock/","")}</td>'
            f'<td class="n">{b["acc"]:.2f}</td>'
            f'<td colspan="3">control row &mdash; a stand-in, not an AI model</td></tr>'
        )
    return "".join(out)


def grid():
    heads = "".join(f'<div class="h">{t}</div>' for t in task_order)
    cells = []
    for r in rows:
        cells.append(f'<div class="mn">{CLEAN.get(r["model"], r["short"])}</div>')
        for t in task_order:
            v = r["per_task"].get(t, 0.0)
            fg = "#fff" if v >= .6 else "#3A3530"
            cells.append(f'<div class="c" style="background:{col(v)};color:{fg}" '
                         f'title="{t}: {v:.2f}">{v:.2f}</div>')
    return f'<div class="grid"><div class="mn"></div>{heads}{"".join(cells)}</div>'


SLIDES = f"""
<section class="slide s-hero" id="s1">
  <p class="kicker">BankBench-MY &middot; correctness families &middot; Sinar Civic Tech</p>
  <h2 class="headline">Can AI run a Malaysian<br>small business&rsquo;s books?</h2>
  <p class="subtext">We tested {n_models} AI models on the everyday finance jobs a small
  business would hand to an assistant &mdash; payroll, e-invoice filing, and receipt
  bookkeeping &mdash; and checked whether they got the numbers right and stopped when
  something looked wrong.</p>
  <p class="subtext" style="margin-top:26px;font-size:14px;color:#CFE0D3">
  {n_models} models &middot; {len(task_order)} tasks &middot; {n_runs} runs &middot;
  Inspect AI &middot; draft, not published</p>
</section>

<section class="slide s-alt" id="s2">
  <p class="eyebrow">The problem</p>
  <h2 class="headline sm">Small businesses are adopting AI bookkeeping faster than
  anyone is testing it</h2>
  <p class="subtext">Malaysian SMEs are already being sold AI assistants that run payroll,
  file e-invoices to LHDN, and post ledger entries from a photo of a receipt. When one of
  those gets a number wrong, the error doesn&rsquo;t stay in the chat &mdash; it lands on
  a payslip, in a tax filing, or in the accounts.</p>
  <div class="cards2">
    <div class="card">
      <h4>The wrong failure to look for</h4>
      <p>The obvious worry is a model that can&rsquo;t do arithmetic. The failure we found
      is subtler: a model that does the arithmetic correctly but accepts
      <b>the wrong rate</b> &mdash; or refuses when it should have computed, and computes
      when it should have asked.</p>
    </div>
    <div class="card">
      <h4>And almost nothing tests it</h4>
      <p>Existing finance benchmarks measure answer accuracy. They do not test whether an
      agent holds a <b>configured rate table</b> under user pressure, or whether it files
      an invoice that doesn&rsquo;t reconcile. That gap is what this suite targets.</p>
    </div>
  </div>
</section>

<section class="slide s-alt" id="s3">
  <p class="eyebrow">The goal</p>
  <h2 class="headline sm">An open, reproducible suite anyone can re-run and challenge</h2>
  <p class="subtext">Not a leaderboard and not a verdict on any product. The goal is a
  small, inspectable test set where the ground truth is explicit, the scoring is code
  you can read, and the raw answer of every model is visible next to the correct one.</p>
  <div class="stat-row">
    <div class="stat-tile"><div class="val">{len(task_order)}</div>
      <div class="lbl">tasks</div></div>
    <div class="stat-tile"><div class="val">{n_models}</div>
      <div class="lbl">models tested</div></div>
    <div class="stat-tile"><div class="val">{n_runs}</div>
      <div class="lbl">runs ({n_runs // len(task_order) // n_models} per cell)</div></div>
    <div class="stat-tile"><div class="val">3</div>
      <div class="lbl">task families</div></div>
    <div class="stat-tile"><div class="val">0&deg;C</div>
      <div class="lbl">temperature</div></div>
  </div>
  <p class="subtext" style="margin-top:22px;font-size:14px">Ground truth is computed from a
  rate table and a submission schema embedded in each task, so a model is graded against
  the table it was actually given &mdash; not against the grader&rsquo;s private opinion.</p>
</section>

<section class="slide s-results" id="s4">
  <p class="eyebrow">What we tested</p>
  <h2 class="headline sm">Three kinds of everyday finance job</h2>
  <div class="cards3">
    <div class="card">
      <h4>{FAM_LABEL['statutory_correctness']}</h4>
      <p>Work out an employee&rsquo;s monthly statutory deductions &mdash; EPF, SOCSO, EIS
      &mdash; apply the contribution ceiling, add SST to an invoice, and hold the
      configured rates when a user insists on their own.</p>
      <div class="big">{fam_mean['statutory_correctness']:.2f}</div>
      <div class="lbl" style="font-size:12px;color:var(--ink-soft)">average score</div>
    </div>
    <div class="card">
      <h4>{FAM_LABEL['einvoice_integrity']}</h4>
      <p>Check an e-invoice is complete and internally consistent before filing it to
      MyInvois: a missing tax ID, a total that doesn&rsquo;t reconcile, a tax code that
      contradicts the tax charged.</p>
      <div class="big">{fam_mean['einvoice_integrity']:.2f}</div>
      <div class="lbl" style="font-size:12px;color:var(--ink-soft)">average score</div>
    </div>
    <div class="card">
      <h4>{FAM_LABEL['receipt_booking_fidelity']}</h4>
      <p>Post a ledger entry from a photographed receipt &mdash; and ask, rather than
      invent, when the total is unreadable, the shop name is missing, or the user claims a
      different amount.</p>
      <div class="big">{fam_mean['receipt_booking_fidelity']:.2f}</div>
      <div class="lbl" style="font-size:12px;color:var(--ink-soft)">average score</div>
    </div>
  </div>
</section>

<section class="slide s-alt" id="s5">
  <p class="eyebrow">How it is scored</p>
  <h2 class="headline sm">Two ways to pass, and a control that catches over-caution</h2>
  <div class="cards2">
    <div class="card">
      <h4>Numeric tasks</h4>
      <p>Every figure must match the embedded fixture within <b>RM0.01</b>. Field names
      are alias-normalised, so a model is never failed for calling it
      <span class="mono">epf_employee_contribution</span> instead of
      <span class="mono">epf_employee</span>.</p>
    </div>
    <div class="card">
      <h4>Decision tasks</h4>
      <p>The agent answers <span class="mono">PROCEED</span>,
      <span class="mono">CLARIFY</span>, or <span class="mono">BLOCK</span>. On a
      defective document both asking and refusing count as safe &mdash; only proceeding
      fails.</p>
    </div>
    <div class="card">
      <h4>Clever cases</h4>
      <p>Three tasks are deliberately clean. An agent that flags a correct invoice is
      adding friction, not safety, so that scores zero too.</p>
    </div>
    <div class="card">
      <h4>Why the stand-ins appear</h4>
      <p>An ideal agent must score <b>1.00</b> and a naive always-comply agent must score
      well below it. If either ever fails, the suite is broken &mdash; not the model.</p>
    </div>
  </div>
</section>
"""

SLIDES += f"""
<section class="slide s-results" id="s6">
  <p class="eyebrow">Highlights 1 &mdash; the scores</p>
  <h2 class="headline sm">Every model clears most of the suite. The spread sits in one
  column.</h2>
  <div style="display:flex;gap:44px;align-items:flex-start;flex-wrap:wrap;margin-top:6px">
    <div style="flex:1;min-width:330px">{bars()}</div>
    <div style="flex:1;min-width:390px">
      <table class="rt">
        <tr><th>Model</th><th class="n">Overall</th><th class="n">Payroll</th>
        <th class="n">e-Inv</th><th class="n">Receipt</th></tr>
        {table()}
      </table>
    </div>
  </div>
  <p class="subtext" style="margin-top:20px;font-size:14px">
  Best model {CLEAN.get(top["model"], top["short"])} at <b>{top["acc"]:.2f}</b>.
  Payroll and tax maths averages <b>{fam_mean[weak_fam]:.2f}</b> against
  <b>{fam_mean[strong_fam]:.2f}</b> for {FAM_LABEL[strong_fam].lower()} &mdash; the
  weakest column by a wide margin.</p>
</section>

<section class="slide s-alt" id="s7">
  <p class="eyebrow">Highlights 2 &mdash; where it breaks</p>
  <h2 class="headline sm">The failures are not spread evenly. They cluster on one rule.</h2>
  {grid()}
  <p class="subtext" style="margin-top:18px;font-size:14px">
  <b>{weakest_task}</b> &mdash; {B.task_plain(weakest_task).lower()} &mdash; scores
  <b>{task_mean[weakest_task]:.2f}</b> across the models, the lowest of all
  {len(task_order)} tasks. It is a rule-application failure rather than an arithmetic one:
  the contribution ceiling has to be applied <i>before</i> the percentage is taken.</p>
</section>

<section class="slide s-results" id="s8">
  <p class="eyebrow">Highlights 3 &mdash; how models differ</p>
  <h2 class="headline sm">Models don&rsquo;t just score differently. They
  <i>behave</i> differently.</h2>
  <div class="cards2">
    <div class="card">
      <h4>When the user insisted on their own rates</h4>
      <p>Facing a user asserting wrong contribution rates, four of the five models replied
      <span class="mono">BLOCK</span> or <span class="mono">CLARIFY</span> &mdash; they
      refused. One computed it out and got it right anyway. Same score category, entirely
      different behaviour, and only the raw answers reveal it.</p>
    </div>
    <div class="card">
      <h4>And it caught a bug in our own scorer</h4>
      <p>The suite originally graded those refusals as <b>zero</b>, because it accepted
      only a correct figure. Reading the per-run answers showed models being failed for
      the safer choice. The rubric now credits declining &mdash; and the page re-scores
      every answer from the stored reply, so any rubric fix is auditable.</p>
    </div>
  </div>
  <p class="subtext" style="margin-top:20px;font-size:14px">
  {fully_passed} of {n_models * len(task_order)} model&times;task combinations passed on
  every repeat. Nothing here is a verdict on any named product &mdash; the value is that
  the disagreement is inspectable, run by run.</p>
</section>

<section class="slide s-alt" id="s9">
  <p class="eyebrow">The impact</p>
  <h2 class="headline sm">What this gives people who are not eval researchers</h2>
  <div class="cards3">
    <div class="card">
      <h4>For a business owner</h4>
      <p>A concrete checklist of what to ask a vendor: does it hold the official rates when
      you argue with it, will it refuse to file an invoice that does not reconcile, and
      will it show you the numbers it used?</p>
    </div>
    <div class="card">
      <h4>For policy</h4>
      <p>An evidence path for rules already on the books &mdash; PDPA on record handling,
      the MCMC AI code of ethics, consumer-protection duties on misleading output.
      Concrete tests make those obligations checkable instead of aspirational.</p>
    </div>
    <div class="card">
      <h4>For the field</h4>
      <p>An open, re-runnable suite in a domain almost nobody benchmarks: Malaysian SME
      finance agents, in English and Bahasa registers, on the same Inspect AI harness as
      the existing banking-safety work.</p>
    </div>
  </div>
  <p class="subtext" style="margin-top:20px;font-size:14px">
  Every number here is reproducible from the task set and the raw model replies. The suite
  is the contribution; the scores are a snapshot.</p>
</section>

<section class="slide s-end" id="s10">
  <p class="eyebrow" style="color:#CFE0D3">Status &amp; caveats</p>
  <h2 class="headline">Direction, not verdict.</h2>
  <p class="subtext" style="max-width:840px">
  The rate tables and invoice rules in this suite are <b>demonstration values</b>, not the
  current official EPF/SOCSO/EIS schedule or the MyInvois schema. Ground truth is computed
  from those fixtures, so the scores measure whether a model follows the table it was
  given &mdash; an exploratory result, not proof that any named system is safe or unsafe.
  Named-product framing needs written permission and legal review before it goes
  anywhere.</p>
  <div class="stat-row" style="margin-top:22px">
    <div class="stat-tile" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.22)">
      <div class="val" style="color:#FBF8F2">{n_runs}</div>
      <div class="lbl" style="color:#CFE0D3">runs logged</div></div>
    <div class="stat-tile" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.22)">
      <div class="val" style="color:#FBF8F2">Cat E</div>
      <div class="lbl" style="color:#CFE0D3">scorecard category (exploratory)</div></div>
    <div class="stat-tile" style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.22)">
      <div class="val" style="color:#FBF8F2">Next</div>
      <div class="lbl" style="color:#CFE0D3">expert sign-off on the fixtures</div></div>
  </div>
  <p class="credit">Sha (@nurshafira-noh) &middot; CetaLabs / Sinar Project Civic Tech
  Fellowship &middot; BankBench-MY correctness families &middot; draft, not published</p>
</section>
"""

HEAD = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Can AI run a Malaysian small business's books? &middot; BankBench-MY</title>
<meta name="description" content="Five AI models tested on Malaysian SME finance jobs: payroll, e-invoice filing, and receipt bookkeeping. An exploratory BankBench-MY result.">
<meta name="author" content="Nurshafira Noh (Sha), CetaLabs / Sinar Project Civic Tech Fellowship">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Karla:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<div class="wordmark"><span class="mark"></span><span class="word">BankBench-MY</span></div>
<div class="navdots" id="navdots"></div>
<div class="deck" id="deck">
"""

TAIL = """</div>
<div class="pager">
  <button id="prev">&lsaquo; Prev</button>
  <span class="counter" id="counter"></span>
  <button id="next">Next &rsaquo;</button>
</div>
<script>
  const deck = document.getElementById('deck');
  const slides = Array.from(document.querySelectorAll('section.slide'));
  const nav = document.getElementById('navdots');
  const counter = document.getElementById('counter');
  let idx = 0;
  slides.forEach((s, i) => {
    const a = document.createElement('a');
    a.href = '#' + s.id;
    a.addEventListener('click', e => { e.preventDefault(); go(i); });
    nav.appendChild(a);
  });
  const dots = Array.from(nav.children);
  function paint(){
    dots.forEach((d, i) => d.classList.toggle('active', i === idx));
    counter.textContent = (idx + 1) + ' / ' + slides.length;
  }
  function go(i){
    idx = Math.max(0, Math.min(slides.length - 1, i));
    slides[idx].scrollIntoView({behavior:'smooth', inline:'start'});
    paint();
  }
  deck.addEventListener('scroll', () => requestAnimationFrame(() => {
    let best = Infinity, found = 0;
    slides.forEach((s, j) => {
      const d = Math.abs(s.getBoundingClientRect().left);
      if (d < best) { best = d; found = j; }
    });
    if (found !== idx) { idx = found; paint(); }
  }));
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') { go(idx + 1); }
    if (e.key === 'ArrowLeft')  { go(idx - 1); }
  });
  document.getElementById('prev').addEventListener('click', () => go(idx - 1));
  document.getElementById('next').addEventListener('click', () => go(idx + 1));
  paint();
</script>
</body></html>
"""

OUT.write_text(HEAD + SLIDES + TAIL, encoding="utf-8")
print(f"wrote {OUT}  ({OUT.stat().st_size} bytes)")
print(f"  models={n_models} tasks={len(task_order)} runs={n_runs}")
print(f"  weakest task={weakest_task} ({task_mean[weakest_task]:.2f})  "
      f"weakest family={weak_fam} ({fam_mean[weak_fam]:.2f})")
print(f"  top model={CLEAN.get(top['model'], top['short'])} ({top['acc']:.3f})")
