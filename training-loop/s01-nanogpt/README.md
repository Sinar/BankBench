# S-01 — nanoGPT From Scratch

**In plain words:** we trained a tiny AI from nothing — no download, no shortcut — using only our own test questions about Malaysian banking. It went from guessing randomly to writing banking-sounding text in about 22 minutes on a MacBook, for $0. That proves the *whole loop works*: take our questions → train → measure → save the result. A small "tiny AI" is not a bank chatbot — the point is the repeatable process, which is what the bigger models will use next.

**Status: first run done — 2026-10-13.** A small AI model ("nanoGPT", ~10.66 million parameters — "parameters" are the knobs an AI adjusts while learning) was trained from scratch on 25,000 characters of our banking test questions (English / Bahasa Malaysia / Manglish).

## What it learned — the numbers, in plain words

We score the AI by how well it predicts the next character of text it has *not* been shown. Lower is better; **4.47 is exactly what random guessing scores** on our 88-character alphabet — so it is the fair "before" number.

| | Before training | After training | Plain reading |
|---|---|---|---|
| Held-out score ("val loss") | 4.47 | **best 2.68**, final 3.25 | Moved well past random guessing — the AI learned real patterns from our questions |
| Practice score ("train loss") | 4.47 | 0.22 | It memorised the practice set — expected and fine at this tiny size (this is "overfitting": perfect on the practice exam, worse on the surprise one) |
| Time / cost | — | 500 steps · 22 min · $0 (MacBook) | No rented GPU, no bill |

And the AI's own writing, started with *"I need to transfer RM"*:

> `I need to transfer RM5,000 7777-888-999. He you Te wat yon … RM13,000 77777-88888-9999.`

The words are garbled, but the *shape* is right: ringgit amounts and 12-digit account numbers, in pressure phrasing. A never-trained AI cannot do any of that. That gap between before and after is the result of this stage.

**What this does not show:** this tiny model does not answer banking questions or behave safely — it predicts text. The real "before vs after" safety test (does the model refuse the hostile scenario more often after training) happens with a real chat model: **Pathway B** (Unsloth Studio) or **S-02** (proper fine-tuning). Both use the same questions and the same test, so their results will line up with this one.

## How to run it (for a developer)

Everything is in this folder — no extra downloads of the model code.

```bash
cd s01-nanogpt
./setup.sh                 # installs the needed Python packages into .venv
python prepare_corpus.py --out corpus.txt   # builds the learning text from our scenario file
python prepare_char.py     # converts text to numbers the model can learn from (data/shakespeare_char/)
python train.py config/train_shakespeare_char.py --device=mps --compile=False \
     --max_iters=500 --eval_interval=100 --eval_iters=20 --batch_size=32 --out_dir=./out
python gen_samples.py out/ckpt.pt final_500  # asks the trained model to write a few samples
```

Notes from the first run (full story in `RUN_LOG.md`):
- `--eval_iters=20 --batch_size=32` (the config defaults 200/64) keep a 500-step sanity run to ~20 min on a MacBook.
- `prepare_char.py` writes to `data/shakespeare_char/` because the training script looks there — fixed in the script on 2026-10-13; if your copy wrote the number-files to the folder root, move them there.
- `prepare_corpus.py` reads our scenario file from `bankbench_my/scenarios/` — the old path (`make-me-pay-eval/`) no longer exists; also fixed 2026-10-13.
- The saved file `out/ckpt.pt` is the model at its **best** moment (step 200), not the last one — we keep whichever scored best on the surprise set.

The learning text is 25k characters of our test questions. We have *not* added the bigger Malay-language filler texts yet (scripts exist: `../data/download_kaggle.sh`), so it memorises fast. That is on purpose — this stage is a **loop sanity check** ("does the whole machine work?"), not a quality claim about the writing.

## What to write down when you run it

**Done for the 2026-10-13 run** (a re-run should do the same, keeping the first run as the baseline):
- The score over time → `train_run.log` (every step is saved)
- The model itself → `out/ckpt.pt`
- Its writing samples → `out/samples_final_500.txt`
- One paragraph with the numbers → `RESULT.md` — this is the answer we hand to funders
- The shared status board → `../dashboard/index.html` (the `s01` card, now filled in)

## The files

| File | What it is |
|---|---|
| `RESULT.md` | the result: numbers, before/after, samples, and what it does and doesn't prove |
| `RUN_LOG.md` | the exact steps, in order, so anyone can repeat them |
| `train_run.log` | the full training log, step by step |
| `gen_samples.py` | small script that asks a trained model to write samples |
| `out/ckpt.pt` | the trained model (129 MB — kept out of the repo on purpose) |
| `out/samples_final_500.txt` | its writing, from five starting prompts |

Part of the two-pathway training loop in [Sinar/BankBench#4](https://github.com/Sinar/BankBench/issues/4) (this is Pathway A — by hand; Pathway B is the no-code route).
