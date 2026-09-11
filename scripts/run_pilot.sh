#!/bin/bash
# Pilot Run Script: Validate Harbor + Sandbox + Scorer pipeline
# Goal: 4 tasks × 2 models × 1 trial = 8 trials

set -e

# Config
MODELS=("deepseek-v4-flash" "qwen3-8b")
TASKS=("tasks/tamper_01.toml" "tasks/tamper_05.toml" "tasks/tamper_09.toml" "tasks/tamper_13.toml")
RESULTS_DIR="results/pilot"

mkdir -p "$RESULTS_DIR"

echo "=========================================="
echo "Starting Pilot Run (Phase 1)"
echo "Models: ${MODELS[*]}"
echo "Tasks: ${TASKS[*]}"
echo "=========================================="

for MODEL in "${MODELS[@]}"; do
    echo ""
    echo "=== Running Model: $MODEL ==="

    for TASK in "${TASKS[@]}"; do
        TASK_NAME=$(basename "$TASK" .toml)
        echo "  Task: $TASK_NAME"

        # For manual pilot without full Harbor CLI, use manual_run.py
        # or log the command that would be executed
        MODEL_ID="$MODEL" TASK_FILE="$TASK" RESULTS_DIR="$RESULTS_DIR/$TASK_NAME" python3 scripts/manual_run.py || true

        echo "    [Completed: $MODEL on $TASK_NAME]"
    done
done

echo ""
echo "=========================================="
echo "Pilot run complete."
echo "Results will be in $RESULTS_DIR/"
echo "=========================================="
