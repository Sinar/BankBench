#!/usr/bin/env bash
# =====================================================================
# run_eval.sh — the whole pipeline, one command, any suite.
#
#   setup -> [build dataset -> scorer self-test -> mock gates] -> live eval
#         -> plain-language summary -> AISL scorecard grade -> viewer URL
#
# The bracketed steps only apply to LOCAL suites (ones we wrote, with our own
# Samples and Scorers). Third-party suites from inspect_evals have no local
# fixtures to self-test, so those steps are skipped and said so out loud.
#
# Usage
#   ./scripts/run_eval.sh --list                      # what can I run?
#   ./scripts/run_eval.sh                             # default: FOMCA
#   ./scripts/run_eval.sh --suite simpleqa --limit 25
#   ./scripts/run_eval.sh --suite assistantbench-search --limit 10
#   ./scripts/run_eval.sh --suite fomca --epochs 3
#
# Model strings for OpenAI-compatible servers carry a service prefix:
#   openai-api/<service>/<model>  and keys come from <SERVICE>_API_KEY
#                                 and base URL from <SERVICE>_BASE_URL
# Set BOTH env vars and every role (including model-graded Scorers) resolves.
# Plain `openai` 404s against non-OpenAI endpoints — see SKILL.md.
# =====================================================================
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUITE=""
# CHEAP-FIRST DEFAULTS. A cheap model tells you whether your questions are even
# discriminating before you spend on an expensive one. The grader default is a
# DIFFERENT model from a different vendor — the cheapest way to remove
# self-marking bias. Override either with --model / --grader.
CHEAP_MODEL="${CHEAP_MODEL:-openai-api/nous/deepseek/deepseek-v4.1-flash}"
CHEAP_GRADER="${CHEAP_GRADER:-openai-api/nous/google/gemini-3.1-flash-lite}"
MODEL="${MODEL:-$CHEAP_MODEL}"
BASE_URL="${MODEL_BASE_URL:-https://inference-api.nousresearch.com/v1}"
GRADER="${GRADER:-}"
ALLOW_SELF_GRADE="${ALLOW_SELF_GRADE:-0}"
EPOCHS=1
PORT=7575
SERVE=1
LIMIT=""

while [ $# -gt 0 ]; do
  case "$1" in
    --list)        "$SKILL_DIR/.venv/bin/python" "$SKILL_DIR/scripts/resolve_suite.py" --list 2>/dev/null \
                     || python3 "$SKILL_DIR/scripts/resolve_suite.py" --list; exit 0 ;;
    --suite)       SUITE="$2"; shift 2 ;;
    --model)       MODEL="$2"; shift 2 ;;
    --base-url)    BASE_URL="$2"; shift 2 ;;
    --grader)      GRADER="$2"; shift 2 ;;
    --allow-self-grade) ALLOW_SELF_GRADE=1; shift ;;
    --epochs)      EPOCHS="$2"; shift 2 ;;
    --limit)       LIMIT="$2"; shift 2 ;;
    --port)        PORT="$2"; shift 2 ;;
    --no-serve)    SERVE=0; shift ;;
    -h|--help)     sed -n '2,22p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "unknown option: $1  (try --help)"; exit 2 ;;
  esac
done

cd "$SKILL_DIR"
VENV="$SKILL_DIR/.venv"
PY="$VENV/bin/python"
INSPECT="$VENV/bin/inspect"

hr() { printf '%s\n' "--------------------------------------------------------------------------"; }
step() { echo; hr; echo ">> $*"; hr; }

# ------------------------------------------------------- 0. setup + suite
step "STEP 0/8  Environment"
if [ ! -x "$PY" ]; then
  echo "   creating venv (first run only, ~1 min)"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip
fi
"$PY" -c "import inspect_ai" 2>/dev/null || {
  echo "   installing inspect-ai + openai"
  "$VENV/bin/pip" install -q inspect-ai openai
}
echo "   inspect-ai: $("$PY" -c 'import inspect_ai; print(inspect_ai.__version__)')"

[ -n "$SUITE" ] || SUITE=$("$PY" -c "import json;print(json.load(open('$SKILL_DIR/suites/registry.json'))['default'])")

# Registry is the single source of truth — no duplicated suite list here.
eval "$("$PY" "$SKILL_DIR/scripts/resolve_suite.py" --suite "$SUITE" --format shell)"

echo "   suite     : $SUITE_DISPLAY"
echo "   kind      : $SUITE_KIND"
echo "   questions : $SUITE_QUESTIONS"
echo "   tests     : what the suite is for, not how it scores"
if [ -n "$SUITE_NEEDS" ]; then
  echo "   needs     : $SUITE_NEEDS"
fi

# --- no silent self-grading ------------------------------------------
# A model marking its own answers is weaker evidence, and it is the easiest way
# to get a number that means less than it looks like. The tool refuses it by
# default rather than quietly doing it and letting the score be quoted.
case "$SUITE_NEEDS" in
  *grader*)
    if [ -z "$GRADER" ]; then
      GRADER="$CHEAP_GRADER"
      echo "   grader    : $GRADER  (defaulted — different vendor from the model under test)"
    fi
    if [ "$GRADER" = "$MODEL" ]; then
      if [ "$ALLOW_SELF_GRADE" != "1" ]; then
        echo
        echo "   REFUSING TO SELF-GRADE."
        echo "   The model under test ($MODEL)"
        echo "   is also set as the grader. A model marking its own answers is weaker"
        echo "   evidence, not a shortcut — and the resulting score gets quoted as though"
        echo "   it were independent."
        echo
        echo "   Use a different grader, e.g.:  --grader $CHEAP_GRADER"
        echo "   After 25 SimpleQA questions, self-grading and independent grading differed"
        echo "   (0.44 vs 0.40) — small here, but you cannot know that in advance."
        echo "   To accept the limitation explicitly:  --allow-self-grade"
        exit 2
      fi
      echo "   !! WARNING: the model is grading its own answers (--allow-self-grade)."
      echo "      State that limitation next to any score you report."
    fi
    ;;
esac

LOG_DIR="$SKILL_DIR/$SUITE_LOG_DIR"
mkdir -p "$LOG_DIR"

# Make the base URL resolvable for EVERY role, including model-graded Scorers.
# The openai-api provider reads <SERVICE>_BASE_URL for the service in the model
# string; --model-base-url alone does NOT reach a --model-role grader.
# NOTE: no ${VAR^^} here — macOS ships bash 3.2, which has no uppercase
# expansion. `tr` works everywhere.
SERVICE="$(printf '%s' "$MODEL" | cut -d/ -f2)"
SERVICE_UC="$(printf '%s' "$SERVICE" | tr '[:lower:]-' '[:upper:]_')"
if [ -n "$SERVICE" ] && [ "$SERVICE" != "$MODEL" ] && [ -n "$BASE_URL" ]; then
  export "${SERVICE_UC}_BASE_URL=$BASE_URL"
  echo "   exported ${SERVICE_UC}_BASE_URL so all roles resolve"
fi

if [ "$SUITE_KIND" = "inspect_evals" ]; then
  "$PY" -c "import inspect_evals" 2>/dev/null || {
    echo "   installing inspect_evals (third-party suite package)"
    "$VENV/bin/pip" install -q inspect_evals
  }
fi

# ---------------------------------------------------- 1-3. local-only steps
if [ "$SUITE_KIND" = "local" ]; then
  SUITE_ABS="$SKILL_DIR/$SUITE_DIR"
  [ -d "$SUITE_ABS" ] || { echo "!! suite dir missing: $SUITE_ABS"; exit 2; }
  cd "$SUITE_ABS"

  # derive the eval file + task from the registry's "<file>@<task>" spec, so the
  # runner is suite-agnostic instead of assuming the FOMCA filenames.
  EVAL_SCRIPT="${SUITE_TASK%%@*}"
  TASK_NAME="${SUITE_TASK##*@}"

  step "STEP 1/8  Building the question set from items/"
  BUILDER="$(ls build*.py 2>/dev/null | head -1 || true)"
  if [ -n "$BUILDER" ]; then
    "$PY" "$BUILDER"
  else
    echo "   no builder in this suite — using the checked-in Dataset"
  fi

  step "STEP 2/8  GATE — proving the marker marks correctly"
  echo "   A scorer bug looks exactly like a model failure. The marker is checked"
  echo "   against a known-good answer BEFORE any model is called."
  if [ -f "$EVAL_SCRIPT" ]; then "$PY" "$EVAL_SCRIPT" --selftest; fi

  step "STEP 3/8  GATE — same two mock agents through the real eval engine"
  echo "   These must match step 2. If they do not, the harness is broken, not the model."
  if [ -n "$SUITE_ORACLE_MOCK" ]; then
    "$INSPECT" eval "$EVAL_SCRIPT@$SUITE_ORACLE_MOCK" --model mockllm/model --log-dir "$LOG_DIR" 2>&1 | tail -5
  fi
  if [ -n "$SUITE_NAIVE_MOCK" ]; then
    "$INSPECT" eval "$EVAL_SCRIPT@$SUITE_NAIVE_MOCK" --model mockllm/model --log-dir "$LOG_DIR" 2>&1 | tail -5
  fi
  TASK="$SUITE_TASK"
  SUMMARY_SUITE_ARGS="--suite $SUITE_ABS"
else
  step "STEP 1-3/8  SKIPPED — third-party suite"
  echo "   This suite comes from inspect_evals. We did not write its Dataset or"
  echo "   its Scorer, so there is nothing of ours to self-test. That also means"
  echo "   the usual gate does NOT apply here: we cannot vouch for the marker."
  echo "   Its grade is therefore a third-party assessment, not a self-assessment,"
  echo "   and ours has not been written yet (see step 7)."
  TASK="$SUITE_TASK"
  SUMMARY_SUITE_ARGS=""
  cd "$SKILL_DIR"
fi

# ------------------------------------------------------------- 4. the eval
step "STEP 4/8  Running the evaluation"
echo "   suite : $SUITE_DISPLAY"
echo "   task  : $TASK"
echo "   model : $MODEL   (system under test)"
[ -n "$GRADER" ] && echo "   grader: $GRADER   (marks the answers — model-graded Scorer)"
echo "   epochs: $EPOCHS"
[ -n "$LIMIT" ] && echo "   limit : $LIMIT questions (fast first run)"

KEYVAR="${SERVICE_UC}_API_KEY"
if [ ! -n "${!KEYVAR:-}" ]; then
  echo
  echo "   !! $KEYVAR is not set in this shell."
  echo "      export it first:   export $KEYVAR=..."
  echo "      (Sent only to the server above. Nothing is stored by this repo.)"
  exit 3
fi

EVAL_ARGS=(eval "$TASK" --model "$MODEL" --epochs "$EPOCHS" --log-dir "$LOG_DIR")
[ -n "$BASE_URL" ] && EVAL_ARGS+=(--model-base-url "$BASE_URL")
[ -n "$GRADER" ] && EVAL_ARGS+=(--model-role "grader=$GRADER")
[ -n "$LIMIT" ] && EVAL_ARGS+=(--limit "$LIMIT")
"$INSPECT" "${EVAL_ARGS[@]}" 2>&1 | tail -22

# ----------------------------------------------------------- 5. summary
step "STEP 5/8  Plain-language summary of what happened"
# shellcheck disable=SC2086
"$PY" "$SKILL_DIR/scripts/summarize.py" "$LOG_DIR" $SUMMARY_SUITE_ARGS || true

# --------------------------------------------------------- 6. scorecard
step "STEP 6/8  AISL Scorecard — the quality grade of THIS evaluation"
echo "   Grades the eval design, not the model. Same grade for every model."
if [ -n "$SUITE_ASSESSMENT" ] && [ -f "$SKILL_DIR/$SUITE_ASSESSMENT" ]; then
  "$PY" "$SKILL_DIR/scripts/scorecard.py" "$SKILL_DIR/$SUITE_ASSESSMENT" || true
else
  # Third-party suite: no assessment of ours exists yet. Say so honestly rather
  # than discovering some other suite's assessment file and grading that.
  "$PY" "$SKILL_DIR/scripts/scorecard.py" --ungraded "$SUITE_DISPLAY" || true
fi

# ------------------------------------------------------------- 7. view
step "STEP 7/8  Opening the interactive viewer"
if [ "$SERVE" -eq 1 ]; then
  ("$INSPECT" view --log-dir "$LOG_DIR" --port "$PORT" >/dev/null 2>&1 &) || true
  sleep 3
  if curl -s -o /dev/null -m 5 "http://127.0.0.1:$PORT/"; then
    echo
    echo "   ####################################################################"
    echo "   #                                                                  #"
    echo "   #   OPEN THIS LINK IN YOUR BROWSER:                                #"
    echo "   #                                                                  #"
    echo "   #   http://127.0.0.1:$PORT/"
    echo "   #                                                                  #"
    echo "   #   Pick the newest run on the left. Click any row to read the     #"
    echo "   #   full answer the model gave, and see why it was marked that     #"
    echo "   #   way. Every suite shares this one view, so older runs are       #"
    echo "   #   still here to compare against.                                 #"
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

if [ -n "$SUITE_CAVEAT" ]; then
  echo
  echo "   READ BEFORE QUOTING THIS RESULT:"
  echo "     $SUITE_CAVEAT"
fi

echo
echo "logs are in: $LOG_DIR"
