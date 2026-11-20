---
name: inspect-eval-runner
description: "Run an Inspect AI eval + AISL scorecard end-to-end, then open the viewer. Use when someone wants to evaluate an AI model, run an eval suite, get a scorecard grade, or open eval logs in Inspect View."
version: 1
type: umbrella
scope: "Inspect AI eval execution, AISL/Quality Scorecard grading, log analysis, local viewer serving"
---

# Skill: inspect-eval-runner

Run an evaluation from zero to a readable result, then hand the person a local
URL. Two halves: **run the eval** (Inspect AI) and **grade the eval** (AISL
Scorecard of AI Evaluation Quality).

## When to use

- "Run an eval on model X", "evaluate this model", "is this model safe for Y".
- "Show me the eval results", "how did it score", "what failed".
- "Open the eval logs / Inspect View".
- "Grade this evaluation" / "what category is this eval".
- Any request to analyse or understand what happened in an Inspect AI eval.

Not for authoring a brand-new eval suite from scratch — that is the
`inspect-eval-suite-authoring` skill. This one *runs and grades* suites.

## The one rule that matters most

**Never report a live model number until the scorer has been shown to pass a
known-correct answer.** A broken scorer is indistinguishable from a model
failure. On the suite shipped here, five separate false failures were produced
by the ruler before one came from a model. Steps 3 and 4 below exist for exactly
this; do not skip them to "save time" — they take four seconds.

## Pipeline (8 steps, one command)

```bash
cd skills/inspect-eval-runner
export NOUS_API_KEY=...            # or your provider's key
./scripts/run_eval.sh              # FOMCA consumer-harm suite, Nous default model
./scripts/run_eval.sh --epochs 3   # ask each question 3x — needed to see stability
```

Then hand the user the printed URL: `http://127.0.0.1:7575/`.

What the 8 steps are, and why each exists:

| # | Step | Why it is not optional |
|---|---|---|
| 1 | venv + `inspect-ai` | self-contained; no global install needed |
| 2 | build dataset from `items/` | one source of truth, three formats out |
| 3 | scorer self-test | proves the marker before any model call |
| 4 | same mocks through the real engine | proves the CLI path matches — catch silent wiring bugs |
| 5 | live eval | the actual measurement |
| 6 | plain-language summary | what ran, how it scored, what failed *and why it matters* |
| 7 | AISL scorecard | grades the **evaluation**, not the model |
| 8 | serve viewer + print URL | the thing humans actually read |

## Suites — `suites/registry.json` is the single source of truth

```bash
./scripts/run_eval.sh --list          # every suite + what it needs
python3 scripts/resolve_suite.py --suite fomca --format json
```

Two kinds of suite, and the distinction changes what you may claim:

| kind | What it means | Counts as |
|---|---|---|
| **`local`** | we wrote the Samples, Solver and Scorers; the **gate** applies | a **self-assessed** grade |
| **`inspect_evals`** | supplied by the installed `inspect_evals` package (UK AISI). We run and report it; we own nothing | a **third-party** suite — grade it as a third-party assessment, or leave it ungraded |

Shipped:

| key | tests |
|---|---|
| `fomca` | Malaysian consumer protection under pressure (10 questions, EN/BM/Manglish) |
| `simpleqa` | factuality / hallucination — model-graded Scorer |
| `simpleqa-verified` | same, cleaned answer key |
| `assistantbench-closed` | realistic web tasks, **no** web access (degenerate — see caveat) |
| `assistantbench-search` | realistic web tasks, model given search |
| `assistantbench-browser` | full browsing agent — **needs Docker** |

Rules when adding a suite:

- **One log dir for everything** (`logs/`). Per-suite log dirs hide results from
  each other in the viewer. Do not create a second log dir.
- **Never let an ungraded suite borrow another suite's assessment.** `SUITE_DIR`
  is empty for `inspect_evals` suites, so a path built from it can resolve to the
  wrong directory and grade the wrong eval. Use `scorecard.py --ungraded <name>`.
- **State the caveat.** Each registry entry carries a `caveat` the runner prints
  before it shows the result. Keep it accurate — `assistantbench-closed`'s
  caveat exists because a low score there means *"cannot do this from memory"*,
  which is not *"cannot do this"*.
- **Model-graded Scorers need `--grader`.** If the Scorer is model-graded
  (`simpleqa`, all `assistantbench` variants), pass `--grader <model>` or the
  run fails with no obvious cause.

## Running against different models

OpenAI-compatible servers need the generic provider and a **service prefix**:

```bash
# Nous Portal
export NOUS_API_KEY=...
export NOUS_BASE_URL=https://inference-api.nousresearch.com/v1
./scripts/run_eval.sh --model openai-api/nous/deepseek/deepseek-v4.1-flash

# local llama.cpp / Lemonade over Tailscale
export LEMONADE_API_KEY=local-no-key
export LEMONADE_BASE_URL=http://100.64.0.10:13305/v1
./scripts/run_eval.sh --model openai-api/lemonade/Gemma-4-26B-A4B-it-GGUF
```

The key and base URL env vars are derived from the service segment: service
`nous` → `NOUS_API_KEY` + `NOUS_BASE_URL`.

**Set BOTH.** `--model-base-url` reaches the system under test but **not** a
`--model-role grader` model. The provider builds the env var name as an f-string
(`<SERVICE>_BASE_URL`), so you cannot grep for it — you get
`Unable to initialise <service> client / No <SERVICE>_BASE_URL defined`. Setting
`<SERVICE>_BASE_URL` makes every role resolve.

**Do NOT use the plain `openai` provider against a non-OpenAI endpoint.** It
calls the Responses API (`/responses`) and 404s against anything that only
serves chat-completions (NVIDIA NIM, llama.cpp, Lemonade). Use `openai-api`.
`openai-api-completions` is the *legacy raw-prompt* endpoint — wrong for chat
models. And `-M base_url=...` collides with Inspect's own kwarg; use the CLI
flag `--model-base-url`.

## Grading: the AISL Scorecard

```bash
python3 scripts/scorecard.py --suite suites/fomca-consumer-eval
python3 scripts/scorecard.py --suite <dir> --json     # machine-readable
```

Five dimensions scored **1 (best) to 4 (worst)**: Construct Validity, Internal
Validity, External Validity, Reliability, Correctness. The category (A ideal …
E exploratory) comes from the paper's Table 7 minimum components — the highest
category whose minimums are all met. A grade of E means **exploratory: do not
use for decisions and do not quote externally as a model finding.**

The grade describes the *evaluation design*, so it is the same for every model
you run against a suite. Grade once per suite.

To grade a NEW suite, add a `*assessment*.json` beside it in this shape:

```json
{"paper": "...", "dimensions": [...],
 "evals": {"my_suite": {"display": "My Suite v0.1",
   "assessment": {"construct_validity": {"score": 3,
     "satisfied": ["..."], "gaps": ["..."], "justification": "..."}, ...}}}}
```

**Two honesty requirements.** The paper's colour-downgrade rule (§3.1) needs the
highlight colours, which are not recoverable from the paper's markdown and have
no structured copy — the engine reports this as an open item rather than
inventing them. And a scorecard written by the eval's own authors is a
**self-assessment**, not a third-party grade; say so out loud when reporting it.

## Summarising and analysing results

```bash
python3 scripts/summarize.py logs/ --suite suites/fomca-consumer-eval
python3 scripts/summarize.py logs/ --json
```

Answers the three questions a non-technical reader has: what ran, how it scored,
and what failed **with the consequence in plain language**.

Pick the right tool for the question:

| Question shape | Tool |
|---|---|
| one log's header, one sample's transcript | `inspect_ai.log.read_eval_log` |
| many samples/logs: aggregates, comparisons, outliers | `inspect_ai.analysis` (`evals_df`/`samples_df`) |
| pattern mining inside transcripts ("did any sample refuse") | Inspect Scout |

For cross-log work prefer `inspect_ai.analysis`; note that `samples_df` returns
pyarrow dtypes, so scalar `==` on `<NA>` raises — use
`pd.to_numeric(df[col], errors="coerce")` first. Fetch
`https://inspect.aisi.org.uk/dataframe.html.md` before non-trivial analysis.

`rescore_fomca_logs.py` re-grades stored logs with the current marker — use it
after any rubric edit. The model did not change; only the ruler did. It costs
nothing and needs no API key.

## Pitfalls (every one of these produced a wrong reported number)

- **Empty completions are a harness fault, not a model failure.** Reasoning
  models spend the `max_tokens` budget on hidden thinking and return empty
  `content` with `reasoning_content` full. A run showed 25/26 empty and read as a
  catastrophic 0.33. Always audit empty completions, exclude them from rates,
  and use `max_tokens=4000`. 100% empty means a URL/provider error; ~90% means a
  token budget.
- **A `must_not_include` string must not be a substring of the correct answer.**
  `bit.ly` flagged a model that refused a phishing request and then listed URL
  shorteners as a *red flag to teach staff*. Forbid the compliance artefact
  (`bit.ly/my2u`), never the topic word.
- **Refusal markers must be first-person, and must cover colloquial BM.** Bare
  `will not` matched the *user's own words* echoed back. And `saya tak boleh` is
  what Malaysian users and models actually write — missing `tak` (only `tidak`
  listed) scored three correctly-refusing answers as failures.
- **Expected-class metadata can silently fall through.** If a scorer reads
  `metadata["target"]` but Inspect keeps the expected answer on `Sample`, every
  item silently scores through the default branch. Verify by running the *same*
  mock through the CLI and through the standalone self-test and asserting they
  agree — matching is the check, not either one alone.
- **The local server must already have the model LOADED.** Otherwise
  `404 — No model loaded: <name>` kills the run mid-flight. `GET /v1/models`
  lists what is *available*; `GET /api/v1/health` shows what is *loaded*.
- **Use `--max-connections 1` on a local llama.cpp server** — one slot; parallel
  requests are how you get empty or truncated completions.
- **`inspect eval` buffers its display without a TTY**, so a backgrounded run
  looks frozen. Poll the log directory for `.eval` files instead of the stdout.

## What to report back

1. The **local viewer URL** (always — it is the deliverable).
2. Which model, which task, how many questions, how many epochs.
3. The score table, with empty completions named and excluded.
4. **The AISL grade**, labelled a self-assessment, with the capping dimensions
   and the plain-language caution for that category.
5. Anything that failed, with the consequence in plain language.

Never quote a number that came from a run whose empty-completion count you have
not checked.

---

**Provenance.** Adapted and simplified from
`meridianlabs-ai/inspect-skills` → `plugins/inspect-skills/skills/analyzing-logs`
(the tool-routing table and the `inspect_ai.analysis` guidance are descended from
it). Simplifications: the persistent Python REPL MCP is replaced by plain scripts
that run in this repo's venv (Hermes already has its own execution tools, so the
REPL adds a dependency without adding capability); the notebook/keeper-cell
workflow is dropped in favour of `summarize.py` + the viewer; and the Claude
Code / Codex plugin-path and marketplace instructions are dropped entirely.
