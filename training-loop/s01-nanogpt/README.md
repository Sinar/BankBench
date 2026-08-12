# S-01 — nanoGPT From Scratch

Proves: you can run a full pretraining loop with your own hands. Cheapest, fastest stage — do this locally, no VastAI spend.

## Run

nanoGPT is flattened directly into this folder (`train.py`, `model.py`, `config/`,
`data/` at the top level) — no sibling clone. Run everything from inside `s01-nanogpt/`.

```bash
cd s01-nanogpt
./setup.sh                 # installs deps into .venv (nanoGPT already present)
python prepare_corpus.py --bankbench-path ../../bankbench_my/scenarios/bankbench-20-tasks.json
python prepare_char.py     # tokenizes input.txt -> data/shakespeare_char/*.bin
python train.py config/train_shakespeare_char.py --device=mps --compile=False \
     --max_iters=500 --eval_interval=100 --out_dir=./out
```

The corpus (`input.txt`) is BankBench-MY prompt text + Sinar civic text
(`../data/raw/sinar-civic/pool.txt`, see `../data/ECOSYSTEMS_DATA_SOURCES.md`),
so this is a from-scratch run on our own Malaysian civic + adversarial corpus,
not Shakespeare. It is small (~25k chars) so it will overfit fast — that's a
loop sanity check, not a sample-quality claim; add a Kaggle BM corpus for more.

## Deliverable to capture

Once training finishes, fill in `RESULT.md` with:
- Loss curve + final `out/` checkpoint (nanoGPT writes to `out/`)
- 3 sample generations at different checkpoint steps
- One paragraph: params, steps, loss X→Y — this paragraph is your literal securefast.ai answer

Then copy the final numbers into `../dashboard/index.html (edit the DATA block)` under `"s01"`.
