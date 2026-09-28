#!/usr/bin/env bash
# Local equivalent of .github/workflows/deploy.yml — assemble the Pages
# output directory and deploy it with the authenticated wrangler session.
# Requires CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID (loaded from the
# repo-root .env, or already exported in your shell).
set -euo pipefail

cd "$(dirname "$0")"

# Load Cloudflare creds from the repo-root .env if present and not already set.
# FIX: this used to be `$(dirname "$PWD")/.env`, which resolved to the PARENT of
# the repo (Antigravity/.env) — so the token in BankBench/.env was never loaded.
ROOT_ENV="$PWD/.env"
if [[ -f "$ROOT_ENV" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ROOT_ENV" 2>/dev/null || true
  set +a
fi

# Keep the site/ mirror in sync with the source pages BEFORE assembling dist.
# Edits to bankbench_my/*.html used to require a manual copy into site/, which
# silently went stale and shipped old, non-proxied pages.
mkdir -p site/bankbench_my
for f in factory.html platform.html models.js; do
  if [[ -f "bankbench_my/$f" ]]; then
    cp "bankbench_my/$f" "site/bankbench_my/$f"
    echo "synced site/bankbench_my/$f"
  fi
done

OUT=dist
rm -rf "$OUT" && mkdir -p "$OUT"
cp -R site/. "$OUT"/
mkdir -p "$OUT/eval-scorecard"
cp eval-scorecard/unified_scorecard_dashboard.html "$OUT/eval-scorecard/"
cp eval-scorecard/README.md "$OUT/eval-scorecard/" 2>/dev/null || true

# Public outreach microsite (Operational Integrity Evals) — static files only.
# The worker/ folder is deployed separately with `wrangler deploy` from
# public/outreach/ops/worker, so it is deliberately not copied into Pages.
mkdir -p "$OUT/outreach"
cp -R public/outreach/ops "$OUT/outreach/ops"
rm -rf "$OUT/outreach/ops/worker"

# Public outreach microsite — Uni eval pages (static files only).
mkdir -p "$OUT/outreach/uni"
cp -R public/outreach/uni "$OUT/outreach/uni"

# `functions/` is picked up automatically by `wrangler pages deploy` from the
# current working directory — that is what serves /api/proxy on the Pages domain.
echo "deploying Pages project bankbench-sinar (with functions/api/proxy.js)…"
wrangler pages deploy "$OUT" --project-name bankbench-sinar
