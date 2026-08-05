#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d "../../../../nanoGPT" ]; then
  echo "TODO: pick a clone location -- defaulting to a sibling of technical_aisafety/"
  git clone https://github.com/karpathy/nanoGPT ../../../../nanoGPT
fi

python3 -m venv .venv
source .venv/bin/activate
pip install torch numpy transformers datasets tiktoken wandb tqdm

echo "Sanity check: run the tiny Shakespeare demo first to confirm the loop runs at all."
echo "  cd ../../../../nanoGPT && python data/shakespeare_char/prepare.py && python train.py config/train_shakespeare_char.py --device=mps --compile=False"
