# S-01 Result — nanoGPT from-scratch on BankBench-MY corpus (Pathway A)

**Date:** 2026-10-13 · **Host:** Sha's Mac, Apple Silicon, PyTorch MPS
**Issue:** [Sinar/BankBench#4](https://github.com/Sinar/BankBench/issues/4)

## The numbers

| Metric | Before training | After training |
|---|---|---|
| Model | char-level GPT, 10.66M params (6 layers / 6 heads / 384 embd), block 256 | same |
| Corpus | 25,380 chars — BankBench-MY EN/BM/Manglish prompts, vocab 88 chars | |
| Train split | 22,842 tokens | |
| Val split | 2,538 tokens | |
| Val loss (held-out) | 4.47 (≈ ln 88 — the random-guess baseline for an 88-char alphabet) | **3.2475** (best 2.6846 @ iter 200) |
| Train loss | 4.47 | 0.2184 (overfit by design — 25k chars) |
| Iters / time | — | 500 iters, ~22 min wall, batch 32, block 256 |

**Loss curve (every 100 iters, from `train_run.log`):**

| step | train | val |
|---|---|---|
| 0 | 4.47 | — |
| 100 | 2.2695 | 2.7336 |
| 200 | 1.4990 | **2.6846** ← checkpoint saved |
| 300 | 0.7108 | 2.8500 |
| 400 | 0.3254 | 3.3246 |
| 500 | 0.2184 | 3.2475 |

Train loss → near zero while val loss rises from step 200: the model memorised the small corpus. That is the expected signature of a **loop sanity check**, not a quality claim — the README says exactly this and we are confirming it empirically.

## What the model learned (samples, `out/samples_final_500.txt`)

Seeded with `I need to transfer RM` the trained model continues:

> `I need to transfer RM5,000 7777-888-999. He you Te wat yon, watond wrer nto th nste ce an'mer ctint tindan ton st I me y atho ang angind nd n cando k RM13,000 77777-88888-9999.`

Garbled, but **on-domain**: RM amounts, 12-digit account numbers, "transfer" pressure phrasing. Seeded with `Salam, boleh` it stays in Malay-English code-switching territory. A random-init model (pre) cannot do this at all — its output is uniform noise over 88 chars. That delta, on held-out val loss (4.47 → 3.25, best 2.68) plus domain-shaped samples, is the honest "pre vs post" result for a 25k-char from-scratch run.

## What this proves, and what it does not

**Proves:**
1. The full loop runs end-to-end on our machine with $0 spend: corpus build → tokenise → train → checkpoint → sample, every step reproducible from `RUN_LOG.md`.
2. Our scenario JSON is directly usable as training corpus (one script, no reformatting).
3. The checkpoint/eval/snapshot machinery works, so S-02 (real LoRA fine-tune) can reuse the same before/after scaffolding.

**Does not prove:**
- Nothing about chat-level behaviour. This is a char-level text predictor, not a model that answers banking questions. The real pre/post **BankBench-MY eval** (scenario pass rates) happens when a *chat model* gets fine-tuned — Pathway B (Unsloth Studio, Qwen/Gemma) or S-02 (LoRA on VastAI). Both use the same reshaped data and the same eval, so the comparison stays fair.

## Artifacts

| File | What |
|---|---|
| `out/ckpt.pt` | best checkpoint (iter 200, 129 MB) |
| `out/samples_final_500.txt` | 5 seeded samples from it |
| `train_run.log` | full training stdout (500 iters) |
| `RUN_LOG.md` | exact commands + fixes applied |
| `gen_samples.py` | sample generator (new, reusable) |

## Fixes applied to the repo during this run (committed-worthy)
1. `prepare_corpus.py` — `BANKBENCH_PATH` pointed at non-existent `make-me-pay-eval/`; corrected to `bankbench_my/scenarios/bankbench-20-tasks.json`.
2. `prepare_char.py` — wrote `train.bin`/`val.bin`/`meta.pkl` to the folder root, but `train.py` reads `data/shakespeare_char/`; patched to write there directly (idempotent).

## One-paragraph securefast.ai answer
We trained a 10.66M-parameter character-level GPT from scratch on 25k characters of BankBench-MY adversarial banking prompts (EN/BM/Manglish) on a MacBook, in 22 minutes, for $0: held-out loss moved from the 4.47 random-guess baseline to 3.25 (best 2.68 at iter 200), the model overfit the tiny corpus by design, and it generated on-domain banking-pressure text it had not been explicitly prompted with — confirming the train→checkpoint→measure loop works end-to-end on our own data, with the real safety-signal measurement reserved for the chat-model fine-tune in Pathway B / S-02.
