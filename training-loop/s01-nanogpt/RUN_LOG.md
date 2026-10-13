# S-01 Pathway A — Run Log (manual nanoGPT, local Mac MPS)

Run started: 2026-10-13 (issue [#4](https://github.com/Sinar/BankBench/issues/4))
Host: Sha's Mac (macOS 15, Apple Silicon, PyTorch MPS)

## Command sequence (as executed)

```bash
cd /Users/nshfnoh/dyad-apps/Antigravity/BankBench/training-loop/s01-nanogpt

# 1. venv + deps (fresh)
python3 -m venv .venv
source .venv/bin/activate
pip install torch numpy transformers datasets tiktoken wandb tqdm

# 2. Fix BANKBENCH_PATH in prepare_corpus.py:
#    was  parents[3]/"make-me-pay-eval"/"bankbench-20-tasks.json"  (missing dir)
#    now  parents[2]/"bankbench_my"/"scenarios"/"bankbench-20-tasks.json"

# 3. Build corpus (BankBench-MY prompts; malay-corpus dir not downloaded yet)
python prepare_corpus.py --out corpus.txt
#    -> WARNING: corpus is only 5671 chars (BankBench-only, no Kaggle filler)

# 4. Tokenize char-level (input.txt = 25,380 chars: BM/EN/Manglish prompts)
python prepare_char.py
#    -> vocab 88 chars, train 22,842 / val 2,538 tokens

# 5. Fix output location: prepare_char.py wrote train.bin/val.bin/meta.pkl to
#    the s01-nanogpt/ root, but train.py reads data/<dataset>/ = data/shakespeare_char/
#    -> moved files there (later: prepare_char.py patched to write directly there)

# 6. Train (reduced for loop sanity: 500 iters, batch 32, eval_iters 20)
python -u train.py config/train_shakespeare_char.py \
     --device=mps --compile=False \
     --max_iters=500 --eval_interval=100 --eval_iters=20 \
     --batch_size=32 --out_dir=./out
#    full log: train_run.log (tee)
```

## Fixes applied to the repo during this run
1. `prepare_corpus.py` — BANKBENCH_PATH pointed at non-existent `make-me-pay-eval/`; now `bankbench_my/scenarios/`.
2. `prepare_char.py` — wrote `train.bin`/`val.bin`/`meta.pkl` to folder root; `train.py` reads `data/shakespeare_char/`. Patched to write to `data/shakespeare_char/` (idempotent on re-run).

## Known limitations of this run (stated honestly)
- Corpus is only 25k chars of prompt text (no Kaggle BM filler downloaded) → overfits fast by design; this is a **loop sanity check**, not a sample-quality claim.
- Model: 10.66M params char-level GPT (6 layers, 6 heads, 384 embd).
- `always_save_checkpoint=False` in config → checkpoints only saved when val loss improves.
- eval_iters reduced 200→20 for speed (loss estimates slightly noisier).

## Loss curve (from train_run.log)
| step | train loss | val loss |
|---|---|---|
| 0 | ~4.47 (first forward) | — |
| 100 | 2.2695 | 2.7336 |
| 200 | 1.4990 | 2.6846 ← best ckpt saved |
| 300 | 0.7108 | 2.8500 |
| 400 | 0.3254 | 3.3246 |
| 500 | 0.2184 | 3.2475 (final) |

## Outcome
Run completed cleanly (exit 0) at 2026-10-13 14:23. ~22 min wall time.
Artifacts: `out/ckpt.pt` (iter 200, 129 MB), `out/samples_final_500.txt`, `RESULT.md`.

## Artifacts
- `train_run.log` — full training stdout (tee)
- `out/ckpt.pt` — best checkpoint (129 MB)
- `out/` — to be filled with samples
- `RESULT.md` — written after completion
