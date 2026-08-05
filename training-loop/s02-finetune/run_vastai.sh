#!/usr/bin/env bash
# Prints the rent/connect/upload steps for VastAI -- doesn't automate the rental
# itself (that's a manual "click RENT" step on cloud.vast.ai/create), just gets
# you from a rented box to a running training script fast.
set -euo pipefail

cat <<'EOF'
=== VastAI setup for S-02 fine-tune ===

1. Go to https://cloud.vast.ai/create/
   Filter: GPU = RTX 3090 or RTX 4090, Disk >= 30GB, Docker template = pytorch/pytorch (any recent CUDA tag)
   Budget check: 0.5B-1.5B model LoRA fine-tune on ~15-20 held-in examples should finish in
   well under an hour -- a $0.30-0.50/hr card keeps this stage under $2.

2. Click RENT. Wait for it to start, then Instances tab -> Connect -> copy the SSH command.
   ssh -p <PORT> root@<HOST>.vast.ai

3. From your Mac, upload this stage's code + data:
   scp -P <PORT> -r \
     s02-finetune \
     ../data/sft_train.jsonl ../data/sft_heldout.jsonl ../data/smoke_benign.jsonl \
     root@<HOST>.vast.ai:/workspace/

4. On the instance:
   cd /workspace/s02-finetune
   pip install -r requirements.txt
   python finetune_lora.py --model Qwen/Qwen2.5-0.5B-Instruct --epochs 3
   python reeval_bankbench.py --base-model Qwen/Qwen2.5-0.5B-Instruct --ft-model ./out/checkpoint-final

5. Download results BEFORE terminating:
   scp -P <PORT> -r root@<HOST>.vast.ai:/workspace/s02-finetune/out ./out
   scp -P <PORT> root@<HOST>.vast.ai:/workspace/s02-finetune/results.json ./results.json

6. TERMINATE THE INSTANCE. Instances tab -> the instance -> Destroy.
   Don't leave it running "just in case" -- that's how this stage blows the $10 cap.

EOF
