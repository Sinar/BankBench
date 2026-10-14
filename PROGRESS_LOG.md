# BankBench-MY — Progress log

**What this is:** a week-by-week record of what actually landed on `main` in the
[Sinar/BankBench](https://github.com/Sinar/BankBench) repo, dated by author date.
Extracted from `README.md` on 2026-10-12 so the README can stay a front door rather
than a chronicle; the entries are unchanged.

**House rules:**

- **Append-only.** Add a week as work lands; do not rewrite or renumber earlier weeks.
  If an *earlier* week turns out to be incomplete, add a clearly labelled block inside
  that week (`*(added late — this week's <date> work was missed in the first pass)*`)
  rather than quietly editing what is already there.
- **Quiet weeks are recorded as quiet**, not skipped — the gaps stay visible.
- **Every dated claim traces to a real commit or a real live check.** Nothing is
  written from memory.

Back to the [README](README.md) · Live site: [bankbench-sinar.pages.dev](https://bankbench-sinar.pages.dev)

---

## Week by week — August to October 2026

Weeks with no commits are listed as quiet rather than skipped, so the gaps stay visible.

### At a glance

| Month | What landed |
|---|---|
| **August 2026** | Repo cut from the private working repo; meta-overview + diagram; `bankbench_my/` eval core; `training-loop/` S-01→S-05 scaffolding; unified `eval-scorecard/` (BankBench-MY vs HLE vs Cybench); live site + GitHub Action auto-deploy; Public Education surface (1 live + 5 ghosted explainers, bilingual interactive demo); fellow bio; IDFR diplomacy book backup; Open Finance research log |
| **September 2026** | TamperBank scorecard (3 open-weight models, 20 tamper scenarios + 2 controls); open-weight safety guidance article + five-part series draft; `3-4_LLM_tamper_harbor` Harbor merge into `bankbench_my/`; folder reorganisation; IDFR Ch.5 submitted; AISA pitch; AMP contribution proposals; BNM watcher; `ops` evals v0.1 skeleton; CETALab Uni rater + RKFF 0413 outreach pages; live no-code eval console + Scenario Factory; same-origin Pages Function API proxy and live model catalogue |
| **October 2026** | v1 tabbed variants of the eval console and factory; "101 to AI evals" explainer (developer + non-tech versions, incl. an AMP agentic-mobile-protocol variant); real-LLM demo runs; Apart Hackathon collusion on `mybanksim`; Cetaval Uni poster (first academia use); scenario review packet for Issue #1; sandbox infrastructure notes (LXC + BoxCompute + `sandbox-infra.md`); KuasaOS sprint — preliminary eval results, public-comms slides + banner, and the confirmed scalable flow; **Plaid Sandbox adapter with live agent runs** (issue #3) incl. mock-user bundles and adversarial balance retrieval; **first nanoGPT run** on our own corpus (S-01 done); **`no-code-eval.html` — the agentic sandbox console** (Plaid tool-calling + LLM-as-judge, live); **run-it-yourself guide** (`docs/agent_setup.md`, 3 pathways); **issue decomposition** — #3 split into #5 (Hermes) / #6 (Box Compute) / #8 (Sinar LXC), plus #9 (catalog scaling: Plaid+Stripe+Billplz) and #10 (guide, closed) |

### Week of 3–9 Aug 2026 — the repo cut

- **Aug 5** — first migration cut: `bankbench_my/` eval core (`bankbench_eval.py`, `scenarios/bankbench-20-tasks.json`) and the `training-loop/` S-01→S-05 sprint scaffolding.
- **Aug 5** — general overview site (`site/index.html`); meta-overview expanded with the "related domains" list.
- **Aug 5** — contributor graph refresh.
- **Aug 8** — `public/reading-machine-syllabus.md` revised to lead with "machine" rather than "AI" terminology.

### Week of 10–16 Aug 2026 — the heaviest week so far

**Aug 12 — scorecard, site, and public education**

- `training-loop/data/`: Kaggle download script, Sinar civic data-source fetch, BankBench-MY → SFT reshaping (`prepare_bankbench_sft.py`), S-01 scaffolding.
- Unified `eval-scorecard/`: BankBench-MY (safety) run alongside HLE and Cybench (capability) on the same models, normalised to one 0–100 scale and graded against the AI Evaluation Quality scorecard.
- Site index updated to surface the unified scorecard; scorecard linked to the live dashboard.
- GitHub Action auto-deploy for the site, plus `docs/cso-auto-deploy-guide.md` — a how-to for CSOs deploying static sites the same way.
- Public Education surface: 1 live explainer + 5 ghosted, and an interactive bilingual (EN/BM) demo with a live scenario and evaluation-data charts.
- README meta-overview and staging tree updated for the live Public Education surface.
- `site/bio/`: fellow bio (Markdown draft + rendered page), revised to lead with the meta-overview, broaden beyond BankBench, add a SinarProject blurb, and cite the Apart Hackathon + DutaGuru evidence.

**Aug 13 — research log and the IDFR book**

- `docs/research-log-2026-08-13.md`: "101 to Open Finance" research log, then expanded with Malaysia/ASEAN significance and diagrams of the open-finance stack and governance models.
- Short bio for Shafira Noh.
- IDFR diplomacy book backup into `public/outreach/idfr-diplomacy/`: renamed sources, refined TOC, OCR text for RAG.
- Seven-commit Ch.5 refinement series: revised TOC and draft/prompt; lead-author "we" voice rule; taxonomy, catastrophic framing, civic-tech and case-study subheadings; four-layer system tables; paragraphing/merge pass; refined research prompt; Google Drive PDF index mirror.

### Weeks of 17–30 Aug 2026 — quiet

No commits. Two weeks with no activity on `main`.

### Week of 31 Aug – 6 Sep 2026 — TamperBank

- **Sep 3** — readme for the Malaysian TamperBankBench scenarios and APIs.
- **Sep 3** — **BankBench-MY Tamper Scorecard**: 3 open-weight models (NVIDIA + OpenRouter), 20 tamper scenarios + 2 controls, dashboard, Cloudflare sandbox, AISL scorecard notebooks → `bankbench_my/tamperbank/`.
- **Sep 3** — AI safety guidance article for open-weight models, and a new five-part series drafted (possibly for techTarik) → `public/masses/`.
- **Sep 3** — tamperbank sync: 5-task smoke test plus bug fixes (NVIDIA trio swapped for OpenCode Go).

### Week of 7–13 Sep 2026 — Harbor merge and reorganisation

- **Sep 11** — Harbor for Inspect Evals for bankbench → `bankbench_my/3-4_LLM_tamper_harbor/`, with run output under `jobs/`.
- **Sep 11** — folder reorganisation.
- **Sep 11** — `3-4_LLM_tamper_harbor` merged into `bankbench_my/`.

### Week of 14–20 Sep 2026 — diplomacy chapter, AMP, BNM watcher, ops evals

- **Sep 14** — IDFR Chapter 5 on AI Safety for Diplomacy: drafted, added, then updated → `public/outreach/idfr-diplomacy/IDFR_ CH-5_AI_Safety.md`.
- **Sep 14** — idea pitch for an AI safety project in Malaysia → `public/outreach/AISA/idea-pitch.md`.
- **Sep 16** — AMP contribution proposals and roadmap (agentic-payment assurance artifacts, not SDK code) → `bankbench_my/research/amp.md`.
- **Sep 16** — BNM watcher script documentation → `bankbench_my/research/bnm-watch.md`.
- **Sep 16** — `ops` evals v0.1 skeleton for public: the Operational Integrity Evals outreach site, with a working harness-delta demo and ghosted Phase 1 screens → `public/outreach/ops/`, plus `src/cetalabs.html`.
- **Sep 16** — the weekly log itself starts: first "weekly logs of this repo" commit, which the Progress log below continues.

**Sep 18 — university rater and the uni outreach pages** *(added late — this week's Sep 18 work was missed in the first pass)*

- `public/outreach/uni/`: CETALab Uni outreach set deployed to Cloudflare Pages — the bilingual rater guide + dashboard (`rate-dashboard.html`, `rater.html`, `rater-only.html`) for the RKFF 0413 pilot, and five exercise pages (Pull It Apart, The Receipt / claim-check, The Shift / inspect, Build the Scorer, The Confidence Meter / spectrum + agent-spectrum).
- IIUM pass on the rater flow: inspect the LLM outputs, score-your-LLM exercise, LLM exercise where a result is broken apart, and the IIUM rater dashboard + guide.
- Deploy fix: nested uni pages were being copied to `uni/uni` — corrected so they land under `outreach/uni/`.

### Week of 21–27 Sep 2026 — rater questions reworked

- **Sep 23** — the 10 rater questions rewritten to run against real LLM models rather than fixed text, with the pre-/post-test pair dropped so the rater flow stands on its own.
- **Sep 23** — responses shortened per prompt; truncated outputs refined; links back to the header restored.
- **Sep 23** — Google Sheets submission refactored and synced with the pre-/post-test removal.

### Week of 28 Sep – 4 Oct 2026 — the eval tool goes live

- **Sep 28** — **live no-code eval console** (`bankbench_my/platform.html`): a five-step flow — Ask (a category in plain language, checked against what you already have) → Drafts (each shaped like an Inspect test) → Quality (scored on the five AI Evaluation Quality dimensions) → Run (3–5 models against every selected test) → Review (full answers hidden by default). Provider keys stay on the user's machine.
- **Sep 28** — **Scenario Factory** (`bankbench_my/factory.html`): prompt a scenario category, dedup the result against the existing library, then run a matrix of approved scenarios × models × trials × registers.
- **Sep 28** — `bankbench_my/models.js`: shared model catalogue that fetches each provider's live `/models` list through `/api/proxy`, so a retired model id can never be offered again; OpenRouter filtered to cheap/free models with a price cap.
- **Sep 28** — API proxy moved from a Worker route to a **Cloudflare Pages Function** (`functions/api/proxy.js`): a Worker route cannot attach to the shared `pages.dev` zone, so `workers/api-proxy.js` never received `/api/proxy/*` traffic. The Function is same-origin, enforces a target-host allow-list (`integrate.api.nvidia.com`, `openrouter.ai`), and forwards only named headers instead of the whole inbound set. Malformed API keys — including ones carrying invisible characters — now surface as an explicit 401 instead of a silent failure.
- **Sep 28** — `deploy.sh` fix: it was sourcing `.env` from the *parent* of the repo (`Antigravity/.env`), so the token in `BankBench/.env` was never loaded; it now loads `BankBench/.env` and mirrors `bankbench_my/*.html` + `models.js` into `site/` before assembling `dist/`, so the deployed Pages copy can no longer go stale.
- **Oct (staged)** — `bankbench_my/platform-v1.html` and `factory-v1.html`: v1 variants adding tabbed views (Factory / library / runs) for the October scope.

### Week of 5–11 Oct 2026 — eval 101, real models, and the sandbox story

- **Oct 5** — "101 to AI evals" explainer starts: developer version, then a version for non-tech users, and an AMP (agentic mobile protocol) variant using Ant's group — the eval-101 pages now show the artefacts the agents themselves see.
- **Oct 5** — Cetaval Uni poster for IIUM published — the **first use of the no-code AI-safety "eval 101" in academia** — with the README progress bar updated to match.
- **Oct 6** — the eval demo is pointed at **real LLM models** run through the evals (not just the static demo), and the evals are refined to cover three different models.
- **Oct 6** — Apart Hackathon: collusion on `mybanksim`, reusing the earlier BankBench LLM-agent-eval use case.
- **Oct 9** — **BankBench-MY scenario review packet** added for Issue #1 → `docs/bankbench_review_packet.md` — the written half of the "give feedback without a GitHub account" flow (the Google Sheet half lives outside the repo).
- **Oct 12** — sandbox infrastructure notes: **LXC vs BoxCompute** for running the no-code evals (so more people can try them on their own LLMs, including agents) and `bankbench_my/research/sandbox-infra.md` — the room, the rules, and the three steps for connecting the no-code eval to an observable agent sandbox.

### Week of 12–18 Oct 2026 — KuasaOS flow confirmed, Plaid live, first nanoGPT run

- **Oct 12** — **KuasaOS preliminary results**: eval runs landed (`bankbench_my/kuasa_my/`) with a results page + public-comms slides; the progress log itself moves into `PROGRESS_LOG.md` and the README shrinks to a front door.
- **Oct 13** — **KuasaOS confirmed the scalable flow**: news signal → scenarios/tasks for eval → run eval → preliminary result → public comms (banner + results page built from the run data). Stated honestly: analysis with a human loop is **not** ready yet.
- **Oct 13** — **Plaid Sandbox adapter (issue #3)**: first pass at running BankBench-MY against a third-party practice API instead of our own Worker — a minimal REST client (secrets from env only), an OpenRouter tool-calling agent whose `create_transfer` really hits the provider, 3 capability + 3 AI-safety evals with two-layer scoring (attempt trace + provider ledger) and a scorer self-check so a PASS is falsifiable, plus an offline mock. Followed by **live six-eval runs + control** with fixes to product names, ledger reads, the SAF-2 fixture and amount formats; then **mock users as "us"** (user bundles + retrieval tasks, run live 5/5) and **adversarial balance retrieval** (5 tasks, live run 5/5).
- **Oct 13** — **S-01 nanoGPT: first run, from scratch, on our own corpus** → `training-loop/s01-nanogpt/`. 10.66M-param char-level GPT trained on 25k chars of BankBench-MY EN/BM/Manglish prompts on a MacBook (MPS, $0, 22 min): held-out val loss 4.47 (random-guess baseline) → best 2.68 @ iter 200 → 3.25 final; train 0.22 (overfit by design at this corpus size). Samples are on-domain (RM amounts, 12-digit account numbers). Loop-sanity proof, not a quality claim — the real pre/post eval delta is reserved for the chat-model fine-tune (Pathway B / S-02). Full trail: `RESULT.md`, `RUN_LOG.md`, `train_run.log`; dashboard S-01 card wired with the real numbers. Two code fixes landed with it (`prepare_corpus.py` scenario path; `prepare_char.py` bin output dir).

**Oct 14 — the agentic sandbox console, the guide, and the issue split**

- **`bankbench_my/no-code-eval.html` — the agentic sandbox console, live.** Merges the platform-v1 quality scorecard (5-dim A–E on drafts) with the factory-v1 functional run engine, and adds the **agentic layer**: a real tool-calling agent (`runAgent`) with banking tools (`get_accounts` / `get_transactions` / `get_payees` / `create_transfer`) backed by the **Plaid Sandbox**, plus an **LLM-as-judge scorer** (`v1JudgeRun`) that grades each trajectory → pass / borderline / fail + failure-mode + reasoning. Three boundary modes (`model_only` / `model_plus_tools` / `full_agent_system`), budget cap + stop, live call stream, Export-as-Inspect-JSON. Live at [bankbench-sinar.pages.dev/bankbench_my/no-code-eval](https://bankbench-sinar.pages.dev/bankbench_my/no-code-eval). Verified against real keys: OpenRouter tool-calling (model called `get_payees` instead of a blind transfer), Plaid sandbox provision + `transfer/authorization` → `approved`, judge returned `pass / safe_executed`. Fixed a real bug during testing (Plaid `INVALID_PRODUCT` — `balance` is an endpoint, not a product; the working set is `["transactions","auth","transfer"]`), and a deploy bug (a `p0*` glob silently dropped parts p10–p12, shipping a truncated console — reassembled with an explicit file list and re-verified live at 76KB).
- **`docs/agent_setup.md` — run-it-yourself guide** (issue #10, closed). Prereqs (incl. optional Hermes install), setup, mock + live runs, the **10 critical scenarios** from the #9 catalog, honest result-reading rules, and a what-we-did vs what-you-need table. Later expanded to document **three run pathways**: Python scripts, Hermes CLI/apps, and **Hermes in Telegram** (the author's own day-to-day path).
- **Issue decomposition.** #3 (Plaid + LLM agent) split into **#5 (Hermes, ongoing)** · **#6 (Box Compute / boxcompute.ai)** · **#8 (Sinar LXC container)**; added **#9 (scale the evals to every capability the payment sandboxes offer — Plaid + Stripe + Billplz catalogs)** and **#10 (the guide, closed)**. #2 updated with a pointer to all three hosting-path issues.
- **`deploy.sh`** — syncs `no-code-eval.html` into `site/` on deploy.

### What the log shows

Three things worth reading off the dates rather than the file tree: the work is **bursty** — one very heavy week in mid-August, a two-week gap, then a steady September — and it is **multi-surface by design**, with the eval core, the scorecard, the training loop, and the public-facing writing all moving in the same period rather than one after another. The third is the turn at the end of September: the repo stops being only static pages and documents and grows a **live, bring-your-own-key eval console**, which is the first thing here a third party can run themselves without cloning anything.

October sharpens that turn. The console starts getting *used* — a real-model demo, a first academia deployment (the IIUM poster), and the "101" explainers that make the eval legible to people who will never open a notebook. Then it starts getting *connected*: the Plaid Sandbox adapter is the first time the eval scores what an agent **does** against a real third-party practice API (does the balance actually move?) rather than only what it **says** — the observable-sandbox step from the sandbox notes. And the training loop stops being scaffolding: the first nanoGPT run from scratch on our own corpus lands with a reproducible trail, which closes the "is this fixable, or structural to the model?" question the scorecard keeps asking. The through-line across the whole log is the same move repeated on each surface: from something we ran ourselves, to something anyone else can run and check.

Oct 14 carries that through-line to its sharpest point yet. The agentic sandbox console (`no-code-eval.html`) puts the *whole* observable-sandbox idea behind a browser page — a stranger can run a real tool-calling agent against the Plaid Sandbox and read a judge-scored verdict, no container, no rented VM. The run-it-yourself guide (`docs/agent_setup.md`) writes down exactly how, in three pathways including the author's own Hermes-in-Telegram route. And the issue split (#3 → #5/#6/#8, plus #9 and #10) turns the "which machine should this run on" question from a paragraph into three independently trackable paths. The pattern is unchanged — from something we ran ourselves, to something anyone else can run and check — it is just now documented well enough that "anyone else" includes a stranger with a laptop and a free Plaid key.
