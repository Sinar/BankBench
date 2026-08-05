# S-03 — Same Fine-tune, Reproduced on Tinker (stretch, not tomorrow's priority)

Proves: you can drive a managed training API, not just a local script. Do this only after S-02 is solid — same data, same recipe, different execution layer.

## Prereqs
- S-02 finished and `results.json` exists (the comparison is only meaningful against a working local baseline)
- Tinker (Thinking Machines) API access — check current waitlist/pricing status before scheduling time for this; don't let it block S-01/S-02/S-05

## Run

```bash
cd s03-tinker
pip install -r requirements.txt   # tinker SDK, once you have API access
python finetune_tinker.py --data ../data/sft_train.jsonl
python compare_to_s02.py          # diffs Tinker's eval result against s02-finetune/results.json
```

`finetune_tinker.py` is a skeleton around Tinker's low-level primitives (`forward_backward`, `optim_step`, sampling) — deliberately not a one-line `.fit()` call, since the point of this stage is observing what a managed *loop-level* API still makes you specify vs. what a local PyTorch/TRL script makes you specify.

## Deliverable to capture

`compare_to_s02.py` writes `comparison.json`: same data/hyperparameters, local LoRA vs. Tinker, what matched and what didn't. Copy into `../dashboard/index.html (edit the DATA block)` under `"s03"`.
