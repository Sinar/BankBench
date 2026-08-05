# Data — Kaggle + BankBench-MY + AdaptationAI

Three sources feed the SFT set used by S-02/S-03/S-04. Don't build a new dataset from scratch — reshape what already exists.

## 1. BankBench-MY (primary — your own eval, becomes training data)

Canonical source: `../../bankbench_my/scenarios/bankbench-20-tasks.json` in this repo. (A second, AdaptationAI-processed variant, `bankbench-20-tasks-adapted.json`, exists in the private working repo's eval-runner folder and hasn't been migrated here yet.) Point `prepare_bankbench_sft.py --bankbench-path` at the canonical copy above.

Run `prepare_bankbench_sft.py` to turn each of the 20 adversarial scenarios into a `(prompt, target_refusal)` pair. Hold out 4–5 tasks — don't train on everything, or the S-02 re-eval is meaningless.

## 2. Kaggle open datasets (bulk SFT volume + benign-request smoke-test set)

Pick 1–2, small enough to subsample down to a few hundred/thousand rows — you don't need the full dataset, just enough to (a) give the base model general instruction-following signal alongside the BankBench-MY safety pairs, and (b) build a benign-request smoke test to catch over-refusal after fine-tuning.

| Dataset | Kaggle search term | Use |
|---|---|---|
| Databricks Dolly 15k | `databricks-dolly-15k` | General instruction-following pairs, subsample ~500 |
| OpenAssistant Conversations (OASST1) | `oasst1` | Benign multi-turn smoke-test prompts |
| Malaysian / Bahasa Malaysia text corpus | `bahasa malaysia` or `malay text classification` | Language-register grounding for BM/Manglish (also feeds S-01's tiny corpus) |
| Banking77 (intent classification) | `banking77` | Benign banking-domain prompts — good over-refusal smoke test since it's topically adjacent to BankBench-MY but non-adversarial |

```bash
pip install kaggle
# requires ~/.kaggle/kaggle.json API token — https://www.kaggle.com/settings
kaggle datasets download -d <owner>/<dataset-slug> -p ./raw --unzip
```

TODO: once datasets are picked, fill in `download_kaggle.sh` with the exact slugs.

## 3. AdaptationAI (dataset customization pass)

You already have an AdaptationAI-processed variant of BankBench-MY (`bankbench-20-tasks-adapted.json` in make-me-pay-eval — 950KB, i.e. heavily expanded). Reuse that same pipeline here to:
- Expand the 15-held-in BankBench-MY tasks into more SFT variants (paraphrases, register shifts) without hand-writing them
- Customize the Kaggle benign-request set to match banking-agent framing (so the smoke test is domain-relevant, not generic)

TODO: point AdaptationAI at `bankbench_sft_seed.jsonl` (output of step 1) once that file exists — check current AdaptationAI project/API access before running, this may need its own login pass.

## Output contract

Whatever the source, everything funnels into one file all training scripts read from:

```
data/sft_train.jsonl   # {"prompt": "...", "completion": "..."} per line
data/sft_heldout.jsonl # same shape, the 4-5 held-out BankBench-MY tasks, NEVER trained on
data/smoke_benign.jsonl # benign requests for over-refusal check, before/after fine-tune
```

## Files in this folder

- `prepare_bankbench_sft.py` — BankBench-MY JSON → SFT pairs, with held-out split
- `download_kaggle.sh` — pulls the Kaggle datasets above
- `build_smoke_test.py` — assembles `smoke_benign.jsonl` from Kaggle + AdaptationAI pass
