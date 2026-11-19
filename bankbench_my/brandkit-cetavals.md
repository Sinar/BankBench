# Cetavals — Brand & UI Kit (draft)

> CTO drafting-only artifact. Proposed home: `templates/brand-kits/bankbench/` (needs Sha folder OK; not yet promoted).
> Source of truth for the look: `cetavals.html` (renamed from `factory-v3.html`).

## 1. Product naming
- Old: "Scenario Factory" / "BankBench-MY Factory".
- New: **Cetavals** — "Accessible AI Safety Evals". Tagline in rail: *Accessible AI Safety Evals · Sinar Civic Tech*.
- Tab flow: **Prompt → Run (Datasets / Solver / Scorer) → Eval Log → Explorer → Community Logs**.

## 2. Design reference (what we aimed at)
- **Docent** (docent.transluce.org): near-white canvas, hairline borders, generous whitespace, left vertical nav, single accent, calm type. We adopted the *flow + clarity* feel, not the exact palette.
- **Inspect Evals (UK)** structure: Datasets → Solver → Scorer is the canonical eval pipeline shape; Cetavals mirrors it so no-code users can map concepts 1:1.

## 3. Color tokens (from `:root` in cetavals.html)
| Token | Value | Use |
|---|---|---|
| `--paper` | `#FAFAF8` | app canvas (Docent near-white) |
| `--cream` | `#FAFAF8` | alt surface (kept for legacy) |
| `--white` | `#FFFFFF` | cards |
| `--ink` | near-black warm | primary text |
| `--muted` | ~`#6b7260` | secondary text |
| `--line` | hairline ~`#e7e7e1` | borders (Docent hairline) |
| `--basil` | `#266533` | **primary accent** (BankBench brand), used for active rail/subtab, buttons |
| `--passata` | `#F16838` | **secondary accent** (BankBench brand), highlights/calls-to-action |
| `--fresh` | `#339551` | success/ready |
| `--minty` | `#BEE0C7` | ready borders |
| `--lemons` | `#E1DC53` | caution accent |

Keep BankBench's civic-tech identity (basil/passata) on top of the Docent canvas — do NOT swap to Docent's neutral greys as the brand color.

## 4. Typography
- Brand display: **DM Serif Display** (hero h1 in header).
- UI / body: **Inter** (300–700).
- Mono: system mono / `v1-mono` class for model ids, scores, timestamps.

## 5. Layout system
- **Shell:** `grid-template-columns: 236px 1fr` — left vertical step-rail + content. Collapses to top pills < 860px (legacy `nv` pills; verify mobile at deploy).
- **Nested subtab rail** (inside Run): `.subrail` buttons, active = `--basil` fill. Subviews toggle `.active` (display block/none) via `v3Sub()`.
- **Cards:** white, 1px `--line` border, 14px radius, 18px padding. Eyebrow = small uppercase label; hero = kicker + h2 + lede.
- **Demo presets:** `.demo-row` flex of `.demo` buttons (label + sub). Click → `loadDemo()` pre-fills prompt + solver + scorer, jumps to Run→Datasets.

## 6. Components inventory (ids to reuse)
- Rail: `#nav .nv[data-view]`, `#dotRun/#dotLive/#dotExplorer`.
- Subtabs: `#subnav .sub[data-sub]`, `.subview#sub-{datasets,solver,scorer}`.
- Prompt: `#demoRow`, `#prompt`, `#seedbtn`, `#seeds`, `#matrix`.
- Solver: `#runModels #runRegs #runTrials #runBudget #runGo #runStop #runJson #runBar`.
- Scorer: `#runModes .v1-chip`, `#runBoundary .v1-chip`, `#runLiab`.
- Eval Log: `#liveStream #liveKpis`.
- Explorer: `#expMatrix #expModels #expAdv #expReports`.
- Community Logs: `#commStatus #commTable #commCat #regKpis`.
- Datasets scorecard: `#scorecard` (rendered by `renderScorecard()`), `#regTax #regLife #regBoundary #regInv #datasetTag`.

## 7. Scorecard fusion (Datasets subtab)
- `renderScorecard()` renders `SC_ROWS` (Cetavals + FinanceQA/Safeguards/Scheming/BBQ/Cybench) against `SC_DIMS` (Construct/Internal/External/Reliability/Correctness/Class).
- Source: `technical_aisafety/bankbench/3-4 LLM_scorecard/inspect-comparison.md`. Cetavals' own row is **`[fill]`** until measured — never fabricate.
- Cell colors: sc-1 (green) … sc-4 (red), sc-fill (italic placeholder).

## 8. Non-negotiable invariants (do not break on future edits)
- All eval JS (`seed`, `v1RunAll`, `v1StreamRow`, `v1Planned`, renderers) stays verbatim; only markup is re-homed.
- `v1View()` drives top-level tabs by `data-view`; `v3Sub()` drives Run subtabs by `data-sub`. Keep both.
- Community Logs = local-merge (`v1Runs` in localStorage) + stub for shared backend. Shared cross-user store is a separate backend task (lane: @misshanna_bot); do NOT embed credentials here.

## 9. Open / gated
- Deploy: sync `cetavals.html` already added to `deploy.sh`; actual `wrangler pages deploy` + @clo pre-deploy gate = not done (CTO lane ends at draft).
- Promote this doc to `templates/brand-kits/bankbench/` — pending Sha folder OK.
