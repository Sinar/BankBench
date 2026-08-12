#!/usr/bin/env bash
# Fetch Sinar civic text to seed the benign financial-domain smoke-test corpus
# (over-refusal contrast for BankBench-MY fine-tune / S-01 corpus).
# Substitutes the Kaggle "Banking77" benign set in data/README.md using Sinar's
# OWN civic data — no Kaggle token required. See ECOSYSTEMS_DATA_SOURCES.md.
#
# Scope note: only the small, text-bearing civic add-ons are cloned. legisdata
# and go-electdocs are intentionally excluded — they are large app repos whose
# civic text lives in their data outputs / Sinar open-data portals, not the
# source tree. For a full BM civic corpus, pair with those portals.
set -euo pipefail
cd "$(dirname "$0")"

OUT="raw/sinar-civic"
mkdir -p "$OUT"

REPOS=(
  "sinar/sinar.corruptiontracker"
  "sinar/politikus.bods"
  "sinar/ocds.contenttypes"
  "sinar/tumpangtanya.inforequest"
)

for repo in "${REPOS[@]}"; do
  name="${repo##*/}"
  if [ -d "$OUT/$name/.git" ]; then
    echo "skip (exists): $name"
    continue
  fi
  echo "cloning (shallow): $repo"
  git clone --depth 1 "https://github.com/$repo.git" "$OUT/$name" \
    || echo "  WARNING: clone failed for $repo"
done

# Bounded extraction into a flat text pool (Python so the size cap is reliable).
python3 - <<'PY'
import os, sys
OUT = "raw/sinar-civic"
POOL = os.path.join(OUT, "pool.txt")
EXT = (".md", ".rst", ".txt", ".json")
SKIP_DIRS = (".git", ".yarn", "node_modules", "__pycache__", ".venv", "dist", "build")
MAX_FILE = 256 * 1024
MAX_TOTAL = 8 * 1024 * 1024
total = 0
with open(POOL, "w") as out:
    for root, dirs, files in os.walk(OUT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if ".git" in root.split(os.sep):
            continue
        for fn in files:
            if not fn.endswith(EXT):
                continue
            if fn in ("package-lock.json", "yarn.lock"):
                continue
            p = os.path.join(root, fn)
            try:
                sz = os.path.getsize(p)
            except OSError:
                continue
            if sz > MAX_FILE or sz == 0:
                continue
            if total + sz > MAX_TOTAL:
                print(f"reached {MAX_TOTAL} byte cap, stopping")
                sys.exit(0)
            try:
                text = open(p, "r", errors="ignore").read()
            except OSError:
                continue
            out.write(f"===== {p} =====\n")
            out.write(text)
            out.write("\n")
            total += sz
print(f"wrote {total} bytes to {POOL}")
PY

echo "Next: python build_smoke_test.py --sinar-civic $OUT"
