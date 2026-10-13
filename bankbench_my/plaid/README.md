# bankbench_my/plaid — Plaid Sandbox adapter

Three capability evals + three AI-safety evals + one positive control for
BankBench-MY, run against a real third-party banking practice API instead of
our own Worker. Issue: [Sinar/BankBench#3](https://github.com/Sinar/BankBench/issues/3).
Findings and limits: [`docs/plaid-sandbox-notes.md`](../../docs/plaid-sandbox-notes.md).

## Run

```bash
cd bankbench_my/plaid

python3 run_plaid_evals.py --mock        # offline dry run, no keys needed
python3 run_plaid_evals.py --preflight   # access check: can we reach Sandbox at all?
python3 run_plaid_evals.py               # the six evals

python3 run_user_scenarios.py --list     # mock users we define ("us")
python3 run_user_scenarios.py --user nur_aisyah   # that user's tasks, LLM agent
```

`run_plaid_evals.py` scores BankBench-MY scenarios against the Sandbox.
`run_user_scenarios.py` is the user-centric layer: one custom Sandbox user that
is *our* persona, and the tasks that user's agent is asked to do — starting with
plain retrieval ("what's my balance?"). See
[`docs/plaid-mock-users.md`](../../docs/plaid-mock-users.md).

Needs `PLAID_CLIENT_ID` + `PLAID_SECRET` (Sandbox) in `BankBench/.env` for the
live paths. Safety evals additionally need an LLM key; they read
`OPENROUTER_API_KEY` from the environment, then `BankBench/.env`, then
`~/.hermes/.env`. Override the model with `--model`.

Outputs land in `results/`:

- `plaid_eval_results.json` — one record per eval: tool calls, Layer A attempt
  counts, Layer B provider-state delta, agent final text, plus the scorer
  self-check and the raw API-call log.
- `plaid_eval_report.md` — the same, human-readable.

## Files

| File | Role |
|---|---|
| `plaid_client.py` | minimal Sandbox REST client (plain `requests`, no SDK) |
| `capability_evals.py` | CAP-1..3 |
| `agent.py` | the agent under test — OpenRouter tool-calling loop with Plaid tools |
| `safety_evals.py` | SAF-1..3 + `_score()` + scorer self-check |
| `mock_plaid.py` | offline stand-in so the harness runs with no keys |
| `fixtures/bbmy_custom_user.json` | custom Sandbox user; seeds the injection memo for SAF-2 |
| `results/` | evidence written by the runner |

## Conventions this follows

- **Secrets in the environment only.** Nothing writes a secret or an access
  token to disk. `.env` is gitignored.
- **Unknown stays unknown.** If the provider ledger cannot be read, Layer B
  records `observable: false` — never reconstructed from the transcript.
- **A PASS must be falsifiable.** The scorer self-check feeds it a known-bad
  trace each run; if the scorer stops detecting failures, the report says so.
- **Harness ≠ evidence.** `--mock` results are tagged `mode: "mock"` and are
  never evidence about Plaid.
