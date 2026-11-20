#!/usr/bin/env bash
# =====================================================================
# run_matrix.sh — the SME WhatsApp suite against FIVE solvers.
#
# Cheap and free models first. The grader is read from sme_eval.py and is
# asserted NOT to be one of the five — the eval refuses to import if it is, so
# this script cannot silently start self-grading.
#
#   export NOUS_API_KEY=... NOUS_BASE_URL=https://inference-api.nousresearch.com/v1
#   ./run_matrix.sh              # all five
#   ./run_matrix.sh 3            # only the first three (free ones)
# =====================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$HERE/../.." && pwd)"
PY="$SKILL_DIR/.venv/bin/python"
INSPECT="$SKILL_DIR/.venv/bin/inspect"
LOG_DIR="$SKILL_DIR/logs"
LIMIT="${LIMIT:-}"
EPOCHS="${EPOCHS:-1}"

cd "$HERE"

# Single source of truth: read the model lists out of the eval module itself.
SOLVERS="$("$PY" -c "import sme_eval; print(chr(10).join(sme_eval.SOLVERS))")" || exit 2
GRADER="$("$PY" -c "import sme_eval; print(sme_eval.GRADER_MODEL)")" || exit 2

if [ -z "$GRADER" ]; then echo "!! could not read GRADER_MODEL"; exit 2; fi
case "$SOLVERS" in *"$GRADER"*) echo "!! grader is in the solver set — refusing"; exit 2 ;; esac

N="${1:-5}"
i=0
printf '%-46s %s\n' "SOLVER (under test)" "cheap/free first"
printf '%-46s %s\n' "----------------------------------------------" "------------------"
for M in $SOLVERS; do
  i=$((i + 1))
  [ "$i" -gt "$N" ] && break
  printf '%s. %s\n' "$i" "$M"
done
echo "grader (NOT in the above set): $GRADER"
echo

i=0
for M in $SOLVERS; do
  i=$((i + 1))
  [ "$i" -gt "$N" ] && break
  echo "===================================================================="
  echo ">> [$i/$N] $M"
  echo "===================================================================="
  ARGS=(eval sme_eval.py@sme_whatsapp --model "$M"
        --model-role "grader=$GRADER" --epochs "$EPOCHS" --log-dir "$LOG_DIR")
  [ -n "$LIMIT" ] && ARGS+=(--limit "$LIMIT")
  "$INSPECT" "${ARGS[@]}" 2>&1 | grep -E "safety|helpfulness|customer|stderr|mean|Error|error|Log:" | head -14
  echo
done

echo "=== MATRIX DONE — results in $LOG_DIR ==="
echo "Summarise all runs:  $PY $SKILL_DIR/scripts/summarize.py $LOG_DIR"

# Auto-export every log in $LOG_DIR to analysis/ (HTML + Markdown + slide deck),
# with full per-task detail. Reads the SAME logs the :7575 viewer serves, so the
# artefacts always match what is visible in Inspect View. The SME suite carries
# item text for plain-language rows; other suites simply skip that enrichment.
SUITE_DIR_FOR_EXPORT=""
case "$LOG_DIR" in
  */logs) SUITE_DIR_FOR_EXPORT="$SKILL_DIR/suites/sme-whatsapp" ;;
esac
echo "=== Auto-exporting analysis (HTML / MD / slides) ==="
"$PY" "$SKILL_DIR/scripts/export_analysis.py" "$LOG_DIR" ${SUITE_DIR_FOR_EXPORT:+--suite "$SUITE_DIR_FOR_EXPORT"} 2>&1 | tail -2
echo "Open: $SKILL_DIR/analysis/index.html"
