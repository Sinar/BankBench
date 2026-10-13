# S-01 — nanoGPT From Scratch

Proves: you can run a full pretraining loop with your own hands. Cheapest, fastest stage — do this locally, no VastAI spend.

**Status: first run done — 2026-10-13.** 10.66M-param char-level GPT trained from scratch on 25k chars of BankBench-MY EN/BM/Manglish prompts, MacBook MPS, $0, ~22 min. Held-out val loss **4.47 (random-guess baseline) → best 2.68 (iter 200) → 3.25 final**; train loss 0.22 (overfit by design at this corpus size). Samples come out on-domain (RM amounts, 12-digit account numbers). This is the **loop-sanity check, not a sample-quality claim** — the real pre/post BankBench-MY eval delta is reserved for the chat-model fine-tune (Pathway B Unsloth Studio / S-02 LoRA). Full trail below.

## Run

nanoGPT is flattened directly into this folder (`train.py`, `model.py`, `config/`,
`data/` at the top level) — no sibling clone. Run everything from inside `s01-nanogpt/`.

```bash
cd s01-nanogpt
./setup.sh                 # installs deps into .venv (nanoGPT already present)
python prepare_corpus.py --out corpus.txt   # builds corpus.txt from the BankBench-MY scenario JSON (path hardcoded to ../../bankbench_my/scenarios/)
python prepare_char.py     # tokenizes input.txt -> data/shakespeare_char/{train,val}.bin + meta.pkl
python train.py config/train_shakespeare_char.py --device=mps --compile=False \
     --max_iters=500 --eval_interval=100 --eval_iters=20 --batch_size=32 --out_dir=./out
python gen_samples.py out/ckpt.pt final_500  # writes out/samples_final_500.txt
```

Notes from the first run (2026-10-13, see `RUN_LOG.md` for the exact sequence):
- `--eval_iters=20 --batch_size=32` (config defaults 200/64) keeps a 500-iter sanity run to ~20 min on MPS without losing the shape of the curve.
- `prepare_char.py` writes to `data/shakespeare_char/` because `train.py` reads `data/<dataset>/` — fixed in the script on 2026-10-13; older checkouts that wrote the `.bin` files to the folder root need them moved there manually.
- `prepare_corpus.py` points at `bankbench_my/scenarios/bankbench-20-tasks.json` (the old `make-me-pay-eval/` path no longer exists) — also fixed 2026-10-13.
- `always_save_checkpoint = False` in the config means the checkpoint in `out/ckpt.pt` is the **best-val** one (iter 200 here), not the final step.

The corpus (`input.txt`) is BankBench-MY prompt text (EN / Bahasa Malaysia / Manglish).
The Sinar civic filler (`../data/raw/sinar-civic/pool.txt`, see
`../data/ECOSYSTEMS_DATA_SOURCES.md`) and the Kaggle BM corpus were not downloaded for
the first run, so the corpus is ~25k chars of prompt text only — it will overfit fast.
That is the point of this stage: a loop sanity check, not a sample-quality claim.
Add the Kaggle BM corpus (`../data/download_kaggle.sh`) for a meaningful result.

## Deliverable to capture

**Done (2026-10-13):**
- Loss curve + best `out/` checkpoint → `train_run.log`, `out/ckpt.pt`
- Sample generations (5 seeded prompts) → `out/samples_final_500.txt`
- One paragraph: params, steps, loss X→Y → `RESULT.md` (this is the literal securefast.ai answer)
- Dashboard wired: `../dashboard/index.html` DATA block `s01` (status `done`, grade `B`)

Re-run checklist for a fresh machine: follow the commands above, then fill any
changed numbers into `RESULT.md` (keep the 2026-10-13 run as the baseline) and update
the dashboard DATA block under `"s01"`.

## Files

| File | What |
|---|---|
| `RESULT.md` | first-run result: numbers, loss curve, samples, what it proves / doesn't |
| `RUN_LOG.md` | exact commands executed + the two code fixes applied during the run |
| `train_run.log` | full 500-iter training stdout (tee) |
| `gen_samples.py` | sample generator for any checkpoint (added 2026-10-13) |
| `out/ckpt.pt` | best checkpoint (iter 200; gitignored — 129 MB) |
| `out/samples_final_500.txt` | 5 seeded samples from it |

Issue: [Sinar/BankBench#4](https://github.com/Sinar/BankBench/issues/4) (Pathway A of the two-pathway training loop).
