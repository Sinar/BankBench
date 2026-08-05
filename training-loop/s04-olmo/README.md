# S-04 — OLMo Provenance-First Comparison (stretch, do last)

Proves: you understand training-data provenance end-to-end, not just script-in/weights-out. This is the SinarProject civic-tech / standards hook — open data lineage as a transparency property, not just a performance one.

## Prereqs
- S-02 finished (this stage reuses the same SFT data + eval)
- Pick the smallest available OLMo-2 checkpoint that's actually feasible on a rented GPU — check current OLMo-2 model card sizes before committing an instance size

## Run

```bash
cd s04-olmo
python provenance_audit.py          # what's in Dolma relevant to banking/BM-Manglish domain
python continue_pretrain_olmo.py --data ../data/sft_train.jsonl   # small SFT/continued-pretrain step
python contamination_check.py       # does BankBench-MY-style content already appear in Dolma?
```

## Deliverable to capture

`provenance_audit.py` + `contamination_check.py` output a short audit note: what's auditable here that isn't for Qwen/Gemma (closed pretraining mixtures), and whether any BankBench-MY-adjacent content already exists in the base model's training data (which would undermine a "held-out" claim on this specific base model). Copy the summary into `../dashboard/index.html (edit the DATA block)` under `"s04"`.

This is the paragraph that goes into a SinarProject / Wawasanex-style policy note: open training-data provenance is what makes independent safety evaluation falsifiable.
