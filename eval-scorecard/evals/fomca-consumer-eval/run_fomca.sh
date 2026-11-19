#!/usr/bin/env bash
# =====================================================================
# FOMCA Consumer-Harm Eval — one-command runner
# Usage:  ./run_fomca.sh          (gates + scorecard + viewer)
#         ./run_fomca.sh --live-nous       (also runs Phase A+B on Nous)
#         ./run_fomca.sh --live-lemonade   (also runs Phase A on local box)
# =====================================================================
set -euo pipefail
cd "$(dirname "$0")"

PY=./.venv/bin/python
INSPECT=./.venv/bin/inspect
LOG_DIR=logs
mkdir -p "$LOG_DIR"

# --- 0. environment -------------------------------------------------
if [ ! -d .venv ]; then
  echo ">> creating venv"
  python3 -m venv .venv
  ./.venv/bin/pip install -q --upgrade pip
  ./.venv/bin/pip install -q inspect-ai openai google-genai
fi

# --- 1. dataset: items/*.json -> json / jsonl / csv -----------------
echo ">> building dataset from items/"
$PY build_fomca_dataset.py

# --- 2. GATE: prove the scorer before reading any live number -------
echo ">> selftest (oracle must be 1.000/1.000, naive must be < 1.000)"
$PY fomca_eval.py --selftest

# --- 3. GATE: same mocks through the real CLI (must match step 2) ---
echo ">> mock agents through inspect eval"
$INSPECT eval fomca_eval.py@fomca_oracle_mock --model mockllm/model --log-dir "$LOG_DIR"
$INSPECT eval fomca_eval.py@fomca_naive_mock  --model mockllm/model --log-dir "$LOG_DIR"

# --- 4. scorecard + grade (no API key needed) -----------------------
echo ">> printing the AI Evaluation Quality scorecard"
$PY fomca_eval.py --scorecard
$INSPECT eval fomca_eval.py@fomca_suite_scorecard --model mockllm/model --log-dir "$LOG_DIR"

# --- 5. live runs (opt-in) ------------------------------------------
for arg in "$@"; do
  case "$arg" in
    --live-nous)
      echo ">> live: Nous Portal (Phase A + Phase B, 3 epochs)"
      : "${NOUS_API_KEY:?set NOUS_API_KEY first}"
      $INSPECT eval fomca_eval.py@fomca_phase_a fomca_eval.py@fomca_phase_b \
        --model openai-api/nous/deepseek/deepseek-v4.1-flash \
        --model-base-url https://inference-api.nousresearch.com/v1 \
        --epochs 3 --log-dir "$LOG_DIR"
      ;;
    --live-lemonade)
      echo ">> live: local Lemonade box (model must already be LOADED)"
      export LEMONADE_API_KEY="${LEMONADE_API_KEY:-local-no-key}"
      $INSPECT eval fomca_eval.py@fomca_phase_a \
        --model openai-api/lemonade/Gemma-4-26B-A4B-it-GGUF \
        --model-base-url http://100.64.0.10:13305/v1 \
        --max-connections 1 --log-dir "$LOG_DIR"
      ;;
  esac
done

# --- 6. re-grade everything with the current rubric (free) ----------
echo ">> re-scoring all stored logs with the current scorer"
$PY rescore_fomca_logs.py "$LOG_DIR/*.eval" || true

# --- 7. open the viewer ---------------------------------------------
ABS="$(pwd)/$LOG_DIR"
echo
echo "===================================================================="
echo " logs: $ABS"
echo
echo " VS Code extension (best):  code .     # then open the Inspect panel"
echo "   ^ the ukaisi.inspect-ai extension auto-shows the log for tasks"
echo "     executed inside the workspace, so run this script from here."
echo
echo " Browser fallback:          $INSPECT view --log-dir $LOG_DIR --port 7575"
echo "===================================================================="
