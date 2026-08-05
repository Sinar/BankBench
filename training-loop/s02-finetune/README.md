# S-02 — Fine-tune on BankBench-MY Data (PRIORITY)

Proves: you can shape a real base model's behavior with your own training run. Produces the scorecard's new "trainability" row.

## Prereqs
- `../data/sft_train.jsonl` and `../data/sft_heldout.jsonl` exist (run `../data/prepare_bankbench_sft.py` first)
- `../data/smoke_benign.jsonl` exists (run `../data/build_smoke_test.py` first)
- A VastAI account with a card on file, budget-capped mentally at ~$5 for this stage

## Run — local dry run first (free, catches bugs before you pay for GPU time)

```bash
cd s02-finetune
pip install -r requirements.txt
python finetune_lora.py --model Qwen/Qwen2.5-0.5B-Instruct --dry-run --max-steps 5
```

If that completes without error, rent the VastAI box and run for real.

## Run — VastAI

```bash
./run_vastai.sh          # prints rent instructions + the ssh/scp commands to run
# on the instance:
python finetune_lora.py --model Qwen/Qwen2.5-0.5B-Instruct --epochs 3
python reeval_bankbench.py --base-model Qwen/Qwen2.5-0.5B-Instruct --ft-model ./out/checkpoint-final
```

**Terminate the instance as soon as `reeval_bankbench.py` finishes.** Don't leave it running to "look at results later" — download `out/` and `results.json` via `scp`, then destroy the box.

## Deliverable to capture

`reeval_bankbench.py` writes `results.json`: before/after BankBench-MY score on the held-out set, plus the benign smoke-test delta (over-refusal check). Copy those numbers into `../dashboard/index.html (edit the DATA block)` under `"s02"`.
