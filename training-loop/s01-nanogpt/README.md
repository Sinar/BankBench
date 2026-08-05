# S-01 — nanoGPT From Scratch

Proves: you can run a full pretraining loop with your own hands. Cheapest, fastest stage — do this locally, no VastAI spend.

## Run

```bash
cd s01-nanogpt
./setup.sh                 # clones nanoGPT, installs deps
python prepare_corpus.py   # builds a tiny BM/Manglish + BankBench-MY text corpus
python ../../../../nanoGPT/train.py config_train.py --device=mps --compile=False
```

(`setup.sh` clones `nanoGPT` as a sibling `nanoGPT/` folder next to this one — not vendored into git, it's upstream code you drive, not code you own.)

## Deliverable to capture

Once training finishes, fill in `RESULT.md` with:
- Loss curve screenshot (`nanoGPT` writes to `out/`)
- 3 sample generations at different checkpoint steps
- One paragraph: params, steps, loss X→Y — this paragraph is your literal securefast.ai answer

Then copy the final numbers into `../dashboard/index.html (edit the DATA block)` under `"s01"`.
