#!/usr/bin/env bash
# Local equivalent of .github/workflows/deploy.yml — assemble the Pages
# output directory and deploy it with the authenticated wrangler session.
# Requires CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID (loaded from the
# repo-root .env, or already exported in your shell).
set -euo pipefail

cd "$(dirname "$0")"

# Load Cloudflare creds from repo-root .env if present and not already set
ROOT_ENV="$(dirname "$PWD")/.env"
if [[ -f "$ROOT_ENV" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ROOT_ENV" 2>/dev/null || true
  set +a
fi

OUT=dist
rm -rf "$OUT" && mkdir -p "$OUT"
cp -R site/. "$OUT"/
mkdir -p "$OUT/eval-scorecard"
cp eval-scorecard/unified_scorecard_dashboard.html "$OUT/eval-scorecard/"
cp eval-scorecard/README.md "$OUT/eval-scorecard/" 2>/dev/null || true

wrangler pages deploy "$OUT" --project-name bankbench-sinar
