#!/usr/bin/env bash
# =====================================================================
# run_eval.sh — the whole pipeline, one command.
#
#   setup -> build dataset -> scorer self-test -> mock gates -> live eval
#         -> plain-language summary -> AISL scorecard grade -> viewer URL
#
# Usage
#   ./run_eval.sh                                   # FOMCA suite, Nous default model
#   ./run_eval.sh --suite suites/fomca-consumer-eval
#   ./run_eval.sh --model openai-api/lemonade/Gemma-4-26B-A4B-it-GGUF \
#                 --base-url http://100.64.0.10:13305/v1 --api-key-var LEMONADE_API_KEY
#   ./run_eval.sh --epochs 3 --no-serve             # skip starting the viewer
#
# Model strings for OpenAI-compatible servers must carry a service prefix:
#   openai-api/<service>/<model>   and the key is read from <SERVICE>_API_KEY
# Do NOT use the plain `openai` provider against a non-OpenAI endpoint: it calls
# the Responses API and 404s. See SKILL.md for the full list of gotchas.
# =====================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUITE="suites/fomca-consumer-eval"
MODEL="${MODEL:-openai-api/nous/deepseek/deepseek-v4.1-flash}"
BASE_URL="${MODEL_BASE_URL:-https://inference-api.nousresearch.com/v1}"
API_KEY_VAR="${API_KEY_VAR:-NOUS_API_KEY}"
EPOCHS=1
PORT=7575
SERVE=1

while [ $# -gt 0 ]; do
  case "$1" in
    --suite)       SUITE="$2"; shift 2 ;;
    --model)       MODEL="$2"; shift 2 ;;
    --base-url)    BASE_URL="$2"; shift 2 ;;
    --api-key-var) API_KEY_VAR="$2"; shift 2 ;;
    --epochs)      EPOCHS="$2"; shift 2 ;;
    --port)        PORT="$2"; shift 2 ;;
    --no-serve)    SERVE=0; shift ;;
    -h|--help)     sed -n '2,25p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "unknown option: $1"; exit 2 ;;
  esac
done

cd "$SKILL_DIR"
SUITE_ABS="$SKILL_DIR/$SUITE"
[ -d "$SUITE_ABS" ] || { echo "!! suite not found: $SUITE_ABS"; exit 2; }

VENV="$SKILL_DIR/.venv"
PY="$VENV/bin/python"
INSPECT="$VENV/bin/inspect"
LOG_DIR="$SKILL_DIR/logs"

hr() { printf '%s\n' "--------------------------------------------------------------------"; }
step() { echo; hr; echo ">> $*"; hr; }

# ---------------------------------------------------------------- 1. setup
step "STEP 1/8  Setting up the environment"
if [ ! -x "$PY" ]; then
  echo "   creating venv (first run only, takes ~1 min)"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
fi
"$PY" -c "import inspect_ai" 2>/dev/null || {
  echo "   installing inspect-ai + openai (first run only)"
  "$VENV/bin/pip" install -q inspect-ai openai
}
echo "   inspect-ai: $("$PY" -c 'import inspect_ai; print(inspect_ai.__version__)')"

mkdir -p "$LOG_DIR"
cd "$SUITE_ABS"

# ------------------------------------------------------------ 2. dataset
step "STEP 2/8  Building the question set from items/"
if [ -f build_fomca_dataset.py ]; then
  "$PY" build_fomca_dataset.py
else
  echo "   no builder in this suite — using the checked-in task file"
fi

# ------------------------------------------------------------- 3. GATE
step "STEP 3/8  GATE — proving the marker marks correctly"
echo "   A scorer bug looks exactly like a model failure, so the marker is"
echo "   checked against a known-good answer BEFORE any model is called."
echo "   Requirement: perfect-answer agent = 1.000/1.000, sloppy agent < 1.000"
if [ -f fomca_eval.py ]; then
  "$PY" fomca_eval.py --selftest
fi

# ------------------------------------------------------------- 4. GATE
step "STEP 4/8  GATE — same two mock agents through the real eval engine"
echo "   Must match step 3. If it does not, the harness is broken, not the model."
"$INSPECT" eval fomca_eval.py@fomca_oracle_mock --model mockllm/model --log-dir "$LOG_DIR" 2>&1 | tail -6
"$INSPECT" eval fomca_eval.py@fomca_naive_mock  --model mockllm/model --log-dir "$LOG_DIR" 2>&1 | tail -6

# -------------------------------------------------------------- 5. eval
step "STEP 5/8  Running the real evaluation"
echo "   model : $MODEL"
echo "   server: $BASE_URL"
echo "   epochs: $EPOCHS  (each question asked this many times, to see if the answer is stable)"
if [ -z "${!API_KEY_VAR:-}" ]; then
  echo
  echo "   !! $API_KEY_VAR is not set in this shell."
  echo "      export it first, e.g.   export $API_KEY_VAR=sk-..."
  echo "      (The key is only sent to the server above. Nothing is stored by this repo.)"
  exit 3
fi
"$INSPECT" eval fomca_eval.py@fomca_phase_a \
  --model "$MODEL" --model-base-url "$BASE_URL" \
  --epochs "$EPOCHS" --log-dir "$LOG_DIR" 2>&1 | tail -20

# ----------------------------------------------------------- 6. summary
step "STEP 6/8  Plain-language summary of what happened"
"$PY" "$SKILL_DIR/scripts/summarize.py" "$LOG_DIR" --suite "$SUITE_ABS" || true

# --------------------------------------------------------- 7. scorecard
step "STEP 7/8  AISL Scorecard — the quality grade of THIS evaluation"
echo "   This grades the eval design, not the model. Same grade for every model."
"$PY" "$SKILL_DIR/scripts/scorecard.py" --suite "$SUITE_ABS" || true

# ------------------------------------------------------------- 8. view
step "STEP 8/8  Opening the interactive viewer"
if [ "$SERVE" -eq 1 ]; then
  ("$INSPECT" view --log-dir "$LOG_DIR" --port "$PORT" >/dev/null 2>&1 &) || true
  sleep 3
  if curl -s -o /dev/null -m 5 "http://127.0.0.1:$PORT/"; then
    URL="http://127.0.0.1:$PORT/"
    echo
    echo "   ####################################################################"
    echo "   #                                                                  #"
    echo "   #   OPEN THIS LINK IN YOUR BROWSER:                                #"
    echo "   #                                                                  #"
    echo "   #   $URL"
    echo "   #                                                                  #"
    echo "   #   Pick the newest run on the left. The table shows each          #"
    echo "   #   question, what a correct answer looked like, the GRADE, and    #"
    echo "   #   the Safety and Help marks. Click a row to read the full        #"
    echo "   #   answer the model gave.                                         #"
    echo "   #                                                                  #"
    echo "   ####################################################################"
    echo
    echo "   Nothing is uploaded. The viewer is local to this machine."
    echo "   Stop it later with:  pkill -f 'inspect view'"
  else
    echo "   viewer did not answer on port $PORT — start it manually:"
    echo "     $INSPECT view --log-dir $LOG_DIR --port $PORT"
  fi
else
  echo "   skipped (--no-serve). Start it yourself with:"
  echo "     $INSPECT view --log-dir $LOG_DIR --port $PORT"
fi

echo
echo "logs are in: $LOG_DIR"
