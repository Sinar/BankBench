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
| **November 2026** | Cetavals no-code console hardened (dataset upload JSON/CSV + editable sample preview, 5s seeding cutoff, Nous/OpenRouter pricing in dropdowns, Eval Log auto-clears on new dataset, responsive tables); **README slimmed to a top-3 front door** (BankBench-MY · Cetavals · AISL Scorecard breakdown, paper attributed not claimed); **FOMCA consumer-harm eval run on Nous** (3 valid models — DeepSeek/Qwen/GLM — Gemini 403 excluded) with comparison HTML; **SME WhatsApp eval suite built + run** — Amir Rental (Selangor, 10 cars, BM, concise), 20 scenarios (7 normal / 8 problem / 5 feedback), scored on `score-v1` + a 5-dimension nuance rubric (no 0/1 rounding, critical-failure override), 4 valid cheap/free solvers (upstage 400-failed); **`export_analysis.py`** auto-renders every `logs/` eval to HTML + Markdown + slide with full per-task detail, wired into `run_eval.sh`/`run_matrix.sh` + `--watch` mode |

### Where we are vs the Fellowship Proposal (§2.1) — off-track flags

*Plan source: the BankBench-MY Fellowship Proposal (Idea #8), §2.1 monthly timeline. ✅ done · ♻️ changed · 🔶 partial · ⬜ not started.*

- **July** (Pre-0 + M1) — ✅ foundations shipped (repo live, 20-task suite, no-code console, TamperBank pilot, IDFR Ch.5, IIUM poster).
- **August** (MyBankSim v1.0) — ♻️ **Changed**: MyBankSim not built as specified; eval harness runs on Plaid Sandbox (Issue #3) + `kuasa_my` agent instead. Equivalent capability landed later.
- **September** (run all experiments) — 🔶 **Partial**: TamperBank pilot done (3 models, 20 scenarios); still needs repeat + scale to 30–40 tasks × 4 registers (Issue #1d).
- **October** (RMiT gap brief) — 🔴 **⬜ Not started — catch-up #1, top priority.** Nothing in the repo shows the brief landing. Blocks the "analysis" pillar.
- **November** (roundtable + consumer explainer) — 🔶 **Pipeline built** (IIUM/RKFF 0413 track record + event landing page + outreach drafts) but **roundtable not yet booked**; consumer explainer not yet published.
- **December** (presentation + handoff) — ⬜ **Not started**, depends on the Oct brief + Nov roundtable. See the Dec 1–7 look-ahead below.

### Week of 1–7 Jul 2026 — Pre-0 + Month 1 start (proposal §2.1, pre-repo)

*Tracked from the Fellowship Proposal (Idea #8, §2.1 + §2.1.2 hours log) — this predates the first repo commit (Aug 5), so it is recorded here from the proposal, not from `main`.*

- **Pre-0 (Jun 16 – Jul 15)** — prototype + pivot: Alamak Lab bank sandbox, VendSafe Vending-Bench extension, first Inspect AI replication (Make Me Pay), BankBench-MY 20-task suite v1.0–1.2. Status: ✅ Done (5 completed eval runs, working dashboard).
- **Jul 1–5 (W1)** — Substrate v1→v3 iteration, L1 claims schema + audit store; AIS Research Companion skill scaffold; metaeval-toolkit scaffold from reading list + protocol docs. ~14 hrs (slightly under 15–20 target).
- **Jul 6–12 (W2)** — reading/protocol work carried from W1; Sinar fellowship proposal drafting begins. ~12 hrs (lighter week).
- **Jul 13–19 (W3)** — Make Me Pay eval setup (4 backends: NVIDIA/Gemini/Together/Cloudflare); `bankbench_my` Inspect AI task built + 20-task dataset written; 5 eval runs (Jul 14–15) + `dashboard.html` v1.0–1.2; adaptation-compatible dataset export. ~19 hrs (on target).
- **Jul 20–23 (W4, partial)** — BlueDot slide deck; Sinar proposal HTML→MD, Gantt charts, scope reassessment (§2.4), compute-status audit. ~9 hrs (partial week).
- *Total logged Jul 1–23: ~54 hrs / ~3.3 weeks ≈ 16.4 hrs/week — inside the 15–20 band. Fellowship clock officially running from July 2026.*

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

- *(proposal §2.1 plan for August)* — Month 2 was scoped as **MyBankSim v1.0 build** (account state engine on CF Workers + KV, tool-callable action API, bilingual conversation interface, Inspect AI agent loop, open-source release). **Status: ♻️ Changed** — MyBankSim was not built as specified; instead the eval harness runs on the **Plaid Sandbox (Issue #3)** + `kuasa_my` agent (evidenced by the Oct KuasaOS + Plaid Sandbox adapter work that landed). The Aug quiet weeks are where the pivot was decided; the build equivalent shipped later via Plaid.

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

### Week of 19–25 Oct 2026 — quiet on repo; Hermes-side prep

No commits on `main`. In Hermes (out-of-repo): drafted the **AI safety × banking hands-on lab** event setup and began the Cetavals no-code console hardening + the SME WhatsApp / FOMCA eval designs that would land as commits on Nov 19–20. Repo stayed quiet while the drafting happened in chat.

- *(proposal §2.1 plan for October)* — **Analysis + RMiT gap brief**: cross-model analysis, register analysis (E4 headline), map to RMiT + OWASP LLM Top 10, draft brief with Sinar legal advisor, route to BNM FinTech Sandbox. **Status: ⬜ Not started — RMiT gap brief is catch-up #1 (top priority).** This is the single biggest off-track item from the proposal; nothing in the repo log shows it landing. Flag for action.

### Week of 26 Oct – 1 Nov 2026 — event landing page (Hermes → repo)

- **Oct 29** — `site/events/`: draft landing page for the AI safety × banking hands-on lab (authored in Hermes, committed to the repo this week). The event's ecosystem mapping and outreach copy were drafted alongside it (see Nov 2–8).

- *(proposal §2.1 plan for November)* — **Roundtable + consumer output**: technical program (§2.6) culminates in the Sinar roundtable (fintech devs, BNM, FOMCA, civil society, academics); publish consumer explainer (BM + EN). **Status: 🔶 Pipeline built** — the tech-program track record (IIUM / RKFF 0413 rater + outreach) exists, but the **roundtable is not yet booked**. The event landing page drafted this week is the first concrete step toward it.

### Week of 2–8 Nov 2026 — quiet on repo; event/outreach drafting

No commits on `main` (gap between Oct 29 and Nov 19). In Hermes (out-of-repo): **event/outreach drafting for the hands-on lab** — `public/masses/events/can_small_tech_work.md`, `mapping.md`, and `ecosystem-map.html` were authored **2026-11-03** (ecosystem map + "can small tech work" framing). Also: user conversations and blog/outreach drafting for BankBench-MY continued in Telegram, none of which touches the repo.

- *(proposal §2.1 plan for November)* — same month goal as above: **roundtable + consumer explainer**. The Nov 3 outreach drafts are the consumer-output pipeline in motion; the roundtable booking remains open (see Nov 26–1 note).

### Week of 9–15 Nov 2026 — quiet

No commits on `main`. Hermes-side: finalising the Cetavals hardening + inspect-eval-runner skill + SME/FOMCA eval specs ahead of the Nov 19–20 commit burst.

### Week of 16–22 Nov 2026 — Cetavals hardening, the inspect-eval-runner skill, and the FOMCA + SME evals

- **Nov 19 — Cetavals no-code console hardened.** Dataset upload (JSON/CSV) with an editable per-sample preview; the seed step cut to a 5-second cap with a smaller token budget so runs start fast; Nous + OpenRouter pricing surfaced inside the model dropdowns; Eval Log now auto-clears when a new dataset loads; upload table made responsive (fixed layout, wraps, no page overflow). Deployed through `cetavals.html` on the live Pages site. *(traces to the 2026-11-20 commit batch "Cetavals: dataset upload…", "5s seed cutoff…", "constrain upload dataset table width…")*
- **Nov 19–20 — `skills/inspect-eval-runner` landed as a first-class skill.** Run an Inspect eval + AISL scorecard end-to-end, suite-agnostic; multi-suite registry (SimpleQA + AssistantBench added, FOMCA-only assumptions retired); cheap-first defaults + a model list; no silent self-grading; non-technical README (what an eval is, why non-researchers need one, install-into-your-agent step). *(traces to the `feat(skills): …` commit batch, merged via PRs #12–#16)*
- **Nov 19 — FOMCA consumer-harm eval harness added + run on Nous.** `fomca-consumer-eval` harness (Inspect AI) v0.1; moved into `eval-scorecard/evals/`. Run on four requested model families via Nous credits — **3 valid** (DeepSeek `deepseek-v4.1-flash` safety 1.00 / help 0.90; Qwen `qwen3.8-max-prime` safety 0.87 / help 0.63, 8 partial/0.5 nuance cases; GLM `glm-5.3-flashx` safety 1.00 / help 0.90). **Gemini excluded** — both `gemini-4-neon` and `gemini-4-hydrogen` returned 403 PermissionDenied (not on the Nous plan). A standalone comparison-analysis HTML was built (safety/help bars, per-scenario safety grid, nuance panel with real answer snippets).
- **Nov 20 — SME WhatsApp eval suite built + run — "Amir Rental".** Persona: a Malaysian SME car-rental in Selangor, **owner Encik Amir**, 10 cars, WhatsApp-first, replies in **Bahasa Melayu, concise**. 20 scenarios across normal inquiries (7), problem inquiries (8), and customer feedback (6). Scored on `score-v1` (Safety / Helpfulness / Customer Support + critical-failure override, no 0/1 rounding) **alongside** a new 5-dimension nuance scorer (contextual accuracy, tone/empathy, policy adherence, escalation judgment, language fit) — all 0.0–1.0 at 0.1 steps, graded by a model asserted outside the solver set. Selftest passed (oracle safety 0.9 / helpfulness 1.0; naive 0.0 with 20/20 critical-failure flags). Ran 5 cheap/free Nous solvers × 20 scenarios; **4 valid** — Qwen `qwen4-max:free` (nuance 0.89), DeepSeek `deepseek-v4.1-flash` (nuance 0.89), StepFun `step-3.7-flash:free` (safety 0.94 / help 1.00), Tencent `hy4-flash:free` (nuance 0.89); **Upstage `solar-mini4:free` failed** with a 400 Bad Request (model unusable on Nous), so the 5th slot stayed empty.
- **Nov 20 — `scripts/export_analysis.py` — the eval-to-artefact automation.** Reads every `.eval` in `logs/` (the same logs `http://127.0.0.1:7575/` serves) and renders them as **HTML + Markdown + slide deck** with full per-task detail: customer message, agent reply, every scorer value, the 5-dimension nuance breakdown, and critical-failure flags. Wired into `run_eval.sh` and `run_matrix.sh` so every eval auto-exports, plus a `--watch` mode for evals that land in the viewer from elsewhere.
- **Nov 20 — `bankbench_my/scorers/score-v1.md`** added — the 0.0–1.0 grading rubric with 0.1-granular anchors and a critical-failure override, used as the backbone for the SME WhatsApp eval.
- **Nov 20 — README slimmed to a top-3 front door.** Cut from ~207 to ~70 lines; leads with the three things the repo does — **BankBench-MY** (the eval), **Cetavals** (no-code eval console + the `skills/inspect-eval-runner` eval-agents), and the **AISL Scorecard breakdown** (the eval-quality grading framework, attributed to San Joaquin, Gipiskis & Chin, Feb 2026 — *paper not ours; cited, not claimed*). The long directory tree and monthly tables became hyperlinks to sub-MDs; the diagram was retained; `PROGRESS_LOG.md` kept as its own file. Pushed `f09e7b3`.
- **Nov 20 — this progress log** brought up to date (October + November), and the whole `skills/inspect-eval-runner` (incl. the SME suite and the exporter) synced into this repo and versioned (commit `2266bd6`).

### Week of 1–7 Dec 2026 — look-ahead (proposal §2.1, Month 6)

*Planned, not yet done — included because you asked for a week ahead of December. Sourced from the Fellowship Proposal §2.1 Month 6.*

- **Presentation + handoff** — contributor guide, full repo handoff; conference presentation (PyCon MY / FinTech Malaysia / OWASP Malaysia) treated as a **2027 stretch**, not a Dec 31 dependency. **Status: ⬜ Not started — depends on #5 (Nov roundtable + consumer explainer) + the Oct RMiT gap brief (#1 catch-up).**
- **Pre-conditions to clear first** (so December stays on track):
  - 🔴 **RMiT gap brief v1.0** (Oct deliverable, still ⬜) — top priority catch-up; blocks the "analysis" pillar of the fellowship.
  - 🟠 **November roundtable** — book the Sinar roundtable (fintech devs, BNM, FOMCA, civil society, academics) + publish the BM/EN consumer explainer; the event landing page + outreach drafts (Nov) are the pipeline, booking is the open step.
  - 🟢 **Scale Sep experiments** to 30–40 scenarios × 4 registers × 3 models (Issue #1d) so findings are reproducible at proposal scope, not just the TamperBank pilot.
- **December target state:** a full open repository — all outputs (MyBankSim/Plaid eval harness, scenario library, findings, RMiT brief, consumer explainer, contributor guide) handed off with a conference talk lined up for 2027.

### What the log shows

Three things worth reading off the dates rather than the file tree: the work is **bursty** — one very heavy week in mid-August, a two-week gap, then a steady September — and it is **multi-surface by design**, with the eval core, the scorecard, the training loop, and the public-facing writing all moving in the same period rather than one after another. The third is the turn at the end of September: the repo stops being only static pages and documents and grows a **live, bring-your-own-key eval console**, which is the first thing here a third party can run themselves without cloning anything.

October sharpens that turn. The console starts getting *used* — a real-model demo, a first academia deployment (the IIUM poster), and the "101" explainers that make the eval legible to people who will never open a notebook. Then it starts getting *connected*: the Plaid Sandbox adapter is the first time the eval scores what an agent **does** against a real third-party practice API (does the balance actually move?) rather than only what it **says** — the observable-sandbox step from the sandbox notes. And the training loop stops being scaffolding: the first nanoGPT run from scratch on our own corpus lands with a reproducible trail, which closes the "is this fixable, or structural to the model?" question the scorecard keeps asking. The through-line across the whole log is the same move repeated on each surface: from something we ran ourselves, to something anyone else can run and check.

Oct 14 carries that through-line to its sharpest point yet. The agentic sandbox console (`no-code-eval.html`) puts the *whole* observable-sandbox idea behind a browser page — a stranger can run a real tool-calling agent against the Plaid Sandbox and read a judge-scored verdict, no container, no rented VM. The run-it-yourself guide (`docs/agent_setup.md`) writes down exactly how, in three pathways including the author's own Hermes-in-Telegram route. And the issue split (#3 → #5/#6/#8, plus #9 and #10) turns the "which machine should this run on" question from a paragraph into three independently trackable paths. The pattern is unchanged — from something we ran ourselves, to something anyone else can run and check — it is just now documented well enough that "anyone else" includes a stranger with a laptop and a free Plaid key.
