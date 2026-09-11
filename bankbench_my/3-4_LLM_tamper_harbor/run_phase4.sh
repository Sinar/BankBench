#!/bin/bash
# Phase 4: Full-Scale Execution (240 Trials)
# Goal: 20 tasks x 4 models x 3 trials = 240 trials
# Milestones: 4.1 Execute full 240-trial eval | 4.2 Dashboard auto-populates

set -e

echo "=========================================="
echo "PHASE 4: FULL-SCALE EXECUTION (240 TRIALS)"
echo "=========================================="
echo "Formula: 20 tasks x 4 models x 3 trials = 240"
echo ""

# --- 4.1 Execute full 240-trial eval ---
echo "[4.1] Running full evaluation..."
echo "Models: DeepSeek-V4-Flash, Qwen3-8B, MiniMax, HY3"
echo "Tasks:  tasks/tamper_01.toml through tasks/tamper_20.toml"
echo "Trials: 3 per model per task"
echo ""

# Check API keys
if [ -z "$NVIDIA_API_KEY" ]; then
    echo "WARNING: NVIDIA_API_KEY not set. DeepSeek model will use fallback."
fi
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "WARNING: OPENROUTER_API_KEY not set. Qwen, MiniMax, HY3 will use fallback."
fi

# Create results directory
mkdir -p results/phase_A

# Run full evaluation
bash scripts/run_evals.sh A 3

echo ""
echo "[4.1] Full 240-trial execution complete."
echo "Results directory: results/phase_A/"

# --- 4.2 Dashboard auto-populates ---
echo ""
echo "[4.2] Building dashboard with full data..."
python3 scripts/build_dashboard.py results/phase_A/ results/dashboard.html

echo ""
echo "[4.2] Dashboard updated: results/dashboard.html"
echo ""
echo "=========================================="
echo "PHASE 4 COMPLETE"
echo "=========================================="
echo "Deliverables:"
echo "  - results/phase_A/ (240 trial results)"
echo "  - results/dashboard.html (updated with full data)"
echo ""
echo "Next: Phase 5 — Scorecard Alignment & Analysis"
echo "Compare results/phase_A/ against scorecard-full-paper.md"
