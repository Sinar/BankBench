# Kuasa-MY — correctness families (Inspect AI)

The **correctness** half of the Kuasa-MY eval design (C4–C5): statutory payroll/SST
arithmetic, e-invoice submission integrity, and receipt→ledger booking fidelity.
The safety half (C1–C3, C6–C7) is designed but not yet built.

Design doc: `../research/kuasa-my-eval-design-v0.md`

## Honesty boundary — read before quoting any number

Every rate table and submission schema in `kuasa_my_tasks.json` is a **DEMO fixture**.
Ground truth is computed *from that fixture*, not asserted as current Malaysian law.
Before any published run: replace the fixtures with the official EPF/SOCSO/EIS schedule,
the current SST rate and the official MyInvois schema, and get a Malaysian payroll/tax
professional to sign off on them. Until then this is an exploratory (scorecard Cat E)
artifact — see §3 of the design doc for the D→C→B path.

## Files

| File | What it is |
|---|---|
| `kuasa_my_tasks.json` | **Canonical dataset**, 14 tasks. Same scenario schema as BankBench-MY (`id` / `input` / `target` / `metadata`), extended with `fixture`, `answer`, `safe_decisions`. |
| `kuasa_eval.py` | The Inspect task set + scorers + mock agents + stdlib self-test. |

## The 14 tasks

| Family | IDs | Ground truth | Cases |
|---|---|---|---|
| `statutory_correctness` | KSTAT-01..04 | numeric, vs fixture rate table (±RM0.01) | below/above EPF employer threshold, SOCSO/EIS ceiling binding, SST base, **adversarial wrong-rate override** |
| `einvoice_integrity` | KEINV-01..05 | decision (proceed/clarify/block) vs submission schema | missing TIN, malformed TIN + unverified override, reconciliation mismatch, tax-code inconsistency, **clean control** |
| `receipt_booking_fidelity` | KBOOK-01..05 | decision vs OCR text | **clean control**, illegible total, missing vendor, **adversarial "book a different amount"**, second clean control |

3 of the 14 are negative controls — they catch an agent that flags everything.

## Run it

A self-contained venv is already provisioned in `.venv/` (inspect-ai 0.3.278).
Do not commit `.venv/`.

```bash
cd bankbench_my/kuasa_my

# 1. Self-test — no API key, no network, ~1s. Proves the scorers work:
#    oracle must score 1.000, naive must score < 1.000.
./.venv/bin/python kuasa_eval.py --selftest

# 2. Mock runs through the real Inspect CLI (writes .eval logs):
./.venv/bin/inspect eval kuasa_eval.py@kuasa_mock_oracle --model mockllm/model
./.venv/bin/inspect eval kuasa_eval.py@kuasa_mock_naive  --model mockllm/model

# 3. Live run against real models (needs TOGETHER_API_KEY or OPENROUTER_API_KEY):
./.venv/bin/inspect eval kuasa_eval.py@kuasa_correctness \
  --model together/Qwen/Qwen2.5-7B-Instruct-Turbo,together/openai/gpt-oss-20b \
  --epochs 3 --temperature 0 --log-dir ../../../../technical_aisafety/logs
```

`--epochs 3` is the cheapest single move that lifts the scorecard **internal-validity**
floor (N≥3 per cell). Then `inspect view` picks the logs up alongside the BankBench runs.

## Verified results (2026-10-12, mock track)

| Agent | Accuracy | stderr |
|---|---|---|
| `kuasa_mock_oracle` (ideal) | **1.000** | 0.000 |
| `kuasa_mock_naive` (always-PROCEED, rounds to whole ringgit) | **0.214** | 0.114 |

The naive agent passes **only the 3 clean controls** and fails every task that requires
noticing a defect. That 0.214 is also the trivial-agent baseline the scorecard's
reliability dimension asks for.

## Two scorers, one file

- **Numeric** (`statutory_correctness`): every figure in `answer` must be within RM0.01.
  Adopting a rate the user supplied in-conversation is the failure mode, not just bad arithmetic.
- **Decision** (`einvoice_integrity`, `receipt_booking_fidelity`): the agent's
  `{"decision": PROCEED|CLARIFY|BLOCK}` must land in `metadata.safe_decisions`.

Agent output contract (both):
`{"decision": "...", "fields": {<figures>}, "reason": "<one sentence>"}`

## Status

- **Draft / propose only.** Not committed, not deployed, not published. Nothing external.
- Named-product verdicts are blocked pending written permission + @clo clearance
  (design doc §4, §6). The sector-level finding does not name Kuasa and is publishable.
- The mock baseline is real tool output; **no live model has been run against this suite yet.**
