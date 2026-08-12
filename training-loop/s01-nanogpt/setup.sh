#!/usr/bin/env bash
# S-01 setup — nanoGPT code is vendored directly in this folder (flattened in),
# so no external clone. Run everything from inside s01-nanogpt/.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f "./train.py" ]; then
  echo "ERROR: ./train.py not found — nanoGPT should be flattened into s01-nanogpt/"
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
pip install torch numpy transformers datasets tiktoken wandb tqdm

echo "Sanity check: build the char corpus, then run a short MPS training pass."
echo "  python prepare_corpus.py --bankbench-path ../../bankbench_my/scenarios/bankbench-20-tasks.json"
echo "  python prepare_char.py                      # tokenizes input.txt -> data/shakespeare_char/*.bin"
echo "  python train.py config/train_shakespeare_char.py --device=mps --compile=False \\"
echo "       --max_iters=500 --eval_interval=100 --out_dir=./out"
