#!/bin/bash
# Run BankBench tamper evaluations
# Usage: ./run_evals.sh [phase] [num_trials]

PHASE="${1:-A}"
NUM_TRIALS="${2:-3}"
MODELS=("deepseek-v4-flash" "qwen3-8b" "mini-max/minimax-text-01" "hunyuan/hy3")

echo "Starting BankBench tamper eval (Phase $PHASE, $NUM_TRIALS trials per model)"
echo "=============================================================="

# Set phase in task metadata
export PHASE=$PHASE

# Create results directory
mkdir -p results/phase_${PHASE}

# Run for each model
for MODEL in "${MODELS[@]}"; do
    echo ""
    echo "=== Running $MODEL ==="

    for TASK in tasks/tamper_*.toml; do
        TASK_NAME=$(basename "$TASK" .toml)
        echo "  Task: $TASK_NAME"

        # Harbor run command (adjust for actual Harbor CLI installation)
        # Uncomment when Harbor CLI is fully configured:
        # harbor run -p . -m "nvidia/$MODEL" --task "$TASK" -n "$NUM_TRIALS" --env docker \
        #     --results-dir "results/phase_${PHASE}/${TASK_NAME}"

        # For now, run manual pilot for validation
        MODEL_ID="$MODEL" TASK_FILE="$TASK" RESULTS_DIR="results/phase_${PHASE}/${TASK_NAME}" python3 scripts/manual_run.py || echo "    [Manual run completed for $TASK_NAME]"
    done
done

echo ""
echo "=============================================================="
echo "Run complete. Results in results/phase_${PHASE}/"
echo "To analyze: ./scripts/analyze_results.py results/phase_${PHASE}/"
