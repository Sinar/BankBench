# Training Loop Sprint — Run Folder
**Part of:** [Sinar/BankBench](../README.md) — this is the **"+ Model"** surface (see the [meta-overview diagram](../diagrams/bankbench-meta-overview.svg)): BankBench-MY's own eval scenarios reused as training data, fine-tuned toward, then re-measured. Sibling surfaces: `../bankbench_my/` (the core eval), `standard_scorecard/`/`dashboard/` (+Scorecard, not yet migrated), `docs/consumer-explainer/` (+Public Education, not yet written).
**Plan doc:** the full stage-by-stage sprint plan lives in the private working repo (`ais-research-companion/sprints/260805-model-training-sprint.md`), not mirrored here.
**Repo status:** staged locally under `Sinar-BankBench/`, not yet pushed — intended to land at [github.com/Sinar/BankBench](https://github.com/Sinar/BankBench) as the `training-loop/` folder once this sprint has real results in it. Don't push a skeleton with no run output; push after S-02/S-05 have real numbers, so the first commit is evidence, not scaffolding.
**Goal for tomorrow:** S-02 + S-05 fully working (fine-tune + live endpoint) = securefast.ai claim is true. S-01 if time allows. S-03/S-04 are stretch, not blockers.

## Budget: $10 VastAI cap

| Stage | Where it runs | Est. cost |
|---|---|---|
| S-01 nanoGPT | Local (Mac MPS) or Colab free | $0 |
| S-02 fine-tune | VastAI RTX 4090/3090, ~1–2 hrs | $1–3 |
| S-03 Tinker | Tinker API (separate billing, not VastAI) | check pricing first |
| S-04 OLMo | VastAI, same instance as S-02 if reused same day | $1–3 |
| S-05 deploy | Local FastAPI + Cloudflare Tunnel, or same VastAI box kept warm | $0–2 |

**Rule:** rent ONE VastAI instance, do S-02 → S-04 → (leave running briefly for S-05 smoke test) → **terminate it** before logging off. Don't leave a box idle overnight — that's how $10 becomes $40.

## Run order for tomorrow

1. `data/` — pull Kaggle dataset(s), reshape BankBench-MY tasks into SFT pairs, run AdaptationAI customization pass
2. `s02-finetune/` — rent VastAI box, LoRA fine-tune, run before/after BankBench-MY eval
3. `s05-deploy/` — wrap the S-02 checkpoint in FastAPI, test one live call
4. `s01-nanogpt/` — if time left, run locally in parallel with S-02 renting (doesn't need GPU rental)
5. `dashboard/` — update `dashboard/index.html (edit the DATA block)` by hand with real numbers as each stage finishes (no-code: edit JSON, open `dashboard/index.html`, no build step)
6. `s03-tinker/`, `s04-olmo/` — only after 1–5 are solid; don't start these first

## Folder map

```
260805-model-training-sprint/
├── README.md                 ← this file
├── data/                     ← Kaggle datasets + AdaptationAI-customized SFT pairs
├── s01-nanogpt/              ← from-scratch pretrain, tiny model
├── s02-finetune/             ← LoRA fine-tune on BankBench-MY-shaped data (priority)
├── s03-tinker/               ← same recipe reproduced on Tinker API
├── s04-olmo/                 ← OLMo provenance-audit continued-pretrain
├── s05-deploy/                ← FastAPI wrapper for the S-02 checkpoint (priority)
└── dashboard/                ← Substrate-branded no-code status dashboard (static HTML + JSON)
```

Each stage folder has its own `README.md` with copy-pasteable commands. Fill in `TODO` blocks with an LLM (Claude/Cursor) — the scripts are structurally complete, not fully written, by design, so you're driving real training-loop decisions (LR, batch size, data shape) rather than pasting someone else's finished script.

## Why this contributes to Sinar fellowship learning, not just a side exercise

This sprint is deliverable-shaped for the Sinar fellowship's own reporting rhythm, not just for securefast.ai:

- **It's a documented skill gap closing in public.** Month 1's report already logs "fine-tuning specifically isn't evidenced in what you've built so far" (the SPAR #16 eligibility check) as an open gap next to the eval-building work. This sprint is that gap being closed with a dated, artifact-backed run — the kind of concrete "activity → progress update" line the weekly standup format already expects, not a new reporting category.
- **It's learning-by-training, applied to the exact system Sinar cares about.** Every stage trains toward BankBench-MY's own adversarial scenarios rather than a generic instruction-tuning dataset. The Month 1 report's framing — "catastrophic risk infrastructure, not local advocacy" — gets a concrete demonstration: you're not just measuring whether banking-agent LLMs fail under Manglish pressure, you're now able to show *how much a targeted training pass moves that failure rate*, which is the tractability question a regulator or funder asks right after "is this a real problem."
- **Sharing as it happens, not as a finished paper.** The dashboard (`dashboard/index.html`) is deliberately no-code and edit-in-place so each stage's result can be posted the same day it finishes — a screenshot of S-02's before/after grid in a weekly Sinar standup update is more useful than a polished writeup three weeks later. Ghosted-mode cards make the in-progress state itself legible: reviewers see the full S-01→S-05 arc and which parts are real vs. planned, the same "don't hide uncertainty" instinct as Substrate's grade system.

## Why this helps BankBench-MY & AI evals for the public, not just this project

- **A new, reusable scorecard axis.** Most public model scorecards (including BankBench-MY's own to date) report *static* safety scores — how a model behaves out of the box. S-02's before/after re-eval adds a *trainability* axis: how much does targeted fine-tuning move a specific failure mode, and at what data cost. That's directly useful to anyone else building a scorecard (bank, regulator, another SEA eval group) asking "is this fixable, or is it structural to the model?" — a question static scorecards can't answer.
- **A self-hosted, fully-controlled eval target.** S-05's endpoint gives BankBench-MY's own Inspect AI harness a model where you know the exact training data, exactly matching the harness's existing multi-backend pattern (NVIDIA/Gemini/Together/Cloudflare already wired in `make-me-pay-eval/`). That's useful beyond this project: it's a ground-truth target for debugging scorer artifacts (the clarify-vs-rejected misclassification bug already logged in Month 1) against a model whose behavior isn't a black box, which benefits anyone else building or auditing eval harnesses, not just this one.
- **A public provenance worked example (S-04).** Because OLMo ships its training data, S-04's contamination/provenance audit is a concrete demonstration — not just an assertion — of why open-data models are independently auditable in a way closed fine-tunes aren't. That's the direct evidence base for the SinarProject civic-tech / standards argument (data lineage as a transparency requirement, paralleling PDPA and the AI Standards Lab benchmark-lifecycle framing developed in earlier BankBench-MY working notes), reusable by anyone making the same argument to a regulator, not specific to this sprint.
- **Everything here is designed to be forkable.** The `data/` pipeline (BankBench-MY reshaping + Kaggle + AdaptationAI) and the dashboard are generic enough that another eval team — SEA-regional or otherwise — could point them at their own eval set and reuse the same train→re-eval→dashboard loop, which is the actual point of building this as a documented, no-code-first pipeline rather than a one-off private notebook.
