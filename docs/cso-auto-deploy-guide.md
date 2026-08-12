# Auto-deploying a static site with a GitHub Action — a CSO how-to

**Surface:** `+ Public Education` (Sinar/BankBench)
**Audience:** other civil-society organisations (CSOs), civic-tech groups, and small research labs who want their public reports/dashboards to update themselves whenever the source changes — without a server, a DevOps hire, or a manual upload step.

> **Relationship to the rest of this repo.** BankBench-MY is a *safety evaluation* for banking-agent LLMs — the science is in `bankbench_my/`, `eval-scorecard/`, and `training-loop/`. This document is **not** about that science. It is about the *plumbing* we use to publish the transparency artifacts those surfaces produce (the overview page, the eval-scorecard dashboard) so the public can always see the current version. Think of it as the "how we make our findings legible" note. It lives under the **+ Public Education** surface because, for a civic-tech org like Sinar, *how you publish* is itself a public-interest question: verifiable, self-hostable, no-vendor-lock-in infra is part of the message, not a side effect.

---

## TL;DR

We turned "push to `main`" into "site is live, updated" using one free GitHub Action that assembles a folder and deploys it to Cloudflare Pages. No server, no manual `wrangler` command, no remembering to re-upload. Any CSO with a public GitHub repo can do the same in ~15 minutes.

---

## What we actually did

The live site (`bankbench-sinar.pages.dev`) is a **static site** — just HTML/CSS, no backend. The source lives in this repo under `site/`. We added:

1. **A workflow file** — `.github/workflows/deploy.yml`.
2. **Two repository secrets** — `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` (set once, in the GitHub repo settings; never committed to the code).
3. **A small "assemble" step** that copies `site/` plus the generated dashboard (`eval-scorecard/unified_scorecard_dashboard.html`) into a `dist/` folder, then deploys that folder.

The workflow (verbatim):

```yaml
name: Deploy to Cloudflare Pages

on:
  push:
    branches: [main]
    paths:
      - "site/**"
      - "eval-scorecard/unified_scorecard_dashboard.html"
      - "eval-scorecard/README.md"
      - ".github/workflows/deploy.yml"
  workflow_dispatch:

permissions: {}

concurrency:
  group: pages-deploy
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Assemble site output
        run: |
          OUT=dist
          rm -rf "$OUT" && mkdir -p "$OUT"
          cp -R site/. "$OUT"/
          mkdir -p "$OUT/eval-scorecard"
          cp eval-scorecard/unified_scorecard_dashboard.html "$OUT/eval-scorecard/"
          cp eval-scorecard/README.md "$OUT/eval-scorecard/" 2>/dev/null || true

      - name: Deploy to Cloudflare Pages
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          command: pages deploy dist --project-name bankbench-sinar
```

The `paths:` filter means the Action only burns a run (and a deploy) when something *visible on the site* changes — editing eval code that doesn't affect the published HTML does not trigger a redeploy.

---

## How another CSO can apply this

**Prerequisites**
- A public (or private) GitHub repo.
- A Cloudflare account (free tier is enough) with a **Pages** project created (you can create it empty; the first `wrangler pages deploy` will populate it).
- The thing you want to publish is **static** — HTML, CSS, JS, images. (If you have a build step — Jekyll, Hugo, a Python script that emits HTML — add it before the `cp` step. That's what we'd do if `eval-scorecard/` ever needed generation; today its dashboard is already static.)

**Steps**
1. In Cloudflare, create an **API Token** scoped to "Account → Cloudflare Pages → Edit". Copy it.
2. In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret**. Add `CLOUDFLARE_API_TOKEN` (the token) and `CLOUDFLARE_ACCOUNT_ID` (from the Cloudflare dashboard URL/account home).
3. Drop the workflow above into `.github/workflows/deploy.yml`, changing `--project-name bankbench-sinar` to your Pages project name, and adjusting the `paths:` and the `cp` lines to match your folder layout.
4. Commit and push. Watch the **Actions** tab: the job should go green, and your `*.pages.dev` URL updates within a minute.
5. (Optional) Point a custom domain at the Pages project in the Cloudflare dashboard.

**Local equivalent.** We also keep `deploy.sh` at the repo root — same assembly + `wrangler pages deploy` — for when someone wants to publish from their laptop without a push. The Action is just this script, run by GitHub instead of you.

---

## When you need this

- **More than one person edits the site.** Auto-deploy means the last merge is always what's live; nobody ships a stale manual upload.
- **The site is generated from data that changes.** Dashboards, scorecards, leaderboards, election trackers — anything where the HTML is rebuilt from source files. If the source moves and the page doesn't, the page lies.
- **You care about an audit trail / verifiability.** Every published version is tied to a git commit and a logged CI run. For a civic-tech org making public-interest claims, "here is the exact commit that produced this page" is a feature, not bureaucracy.
- **You want zero standing infrastructure.** No VM to patch, no FTP creds to lose, no "who has the deploy key" question.
- **You want it free.** GitHub Actions (free minutes for public repos) + Cloudflare Pages (free static hosting) covers typical CSO traffic.

## When you do **not** need this

- **You are the only author and you publish rarely.** A one-off `wrangler pages deploy` (or `netlify deploy`, or dragging a folder into GitHub Pages) is simpler. Don't add a workflow you'll never read.
- **Your host already deploys on git push with zero config.** GitHub Pages, Netlify, and Vercel all do "push → live" out of the box. Add a custom Action only when you need *assembly* (multiple source folders, generated files) that their default publish doesn't handle — which is exactly our case (overview + generated dashboard in different folders).
- **The artifact is a document you attach, not a site.** If the deliverable is a PDF in a release, or an email to a regulator, a deploy pipeline adds nothing.
- **The content is private or sensitive.** Pages is public by default; for anything access-controlled, use a different mechanism (and don't put secrets in the repo — use the encrypted secrets store, as above).
- **You don't control the Cloudflare/GitHub accounts.** If the deployment account belongs to a fiscal sponsor or partner, coordinate first; an Action tied to credentials you don't own is a bus-factor risk.

---

## Why this belongs in a BankBench repo at all

It mostly doesn't — and that's the point to flag. BankBench-MY's contribution is the *evaluation*; the deploy pipeline is generic infra any project could use. We keep it here, in the **+ Public Education** surface, for two reasons:

1. **It's a worked example of verifiable publishing.** Sinar's broader argument — about open training-data provenance, about standards being checkable by an outside party rather than taken on a vendor's word — applies to *how we ship our own results* too. A scorecard you have to email someone to see is less accountable than one anyone can load at a URL that's reproducible from a public commit.
2. **It lowers the barrier for other CSOs.** The pattern above is copy-pasteable. A consumer-rights group or election watchdog can fork the workflow and publish their own transparency dashboards the same way, without learning Cloudflare's console.

So: read the eval surfaces for the substance; read this file for the *distribution method*. They are deliberately separate so neither obscures the other.

---

## Security notes (short)

- Scope the Cloudflare API token to **Pages:Edit only** — not account-wide.
- `permissions: {}` in the workflow means the Action gets no elevated GitHub permissions; the deploy uses *only* the two secrets.
- Never paste tokens into the code or commit them. They live in repo Settings → Secrets.
- `concurrency: cancel-in-progress` stops overlapping deploys from racing if you push fast.
