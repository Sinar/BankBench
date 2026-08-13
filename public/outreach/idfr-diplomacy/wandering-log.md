# Wandering Log — idfr-diplomacy RAG pipeline

> Build notes, decisions, and open threads. Sovereign Tier 3 (Cloudflare Workers + Vectorize).

## 2026-08-13 — Pipeline stood up (Tier 2 + Tier 3)

- **Tier 2 (local):** Drive PDFs → PyMuPDF extract → `.md` beside `toc.md`. Dyad app reads directly.
- **Tier 3 (sovereign):** Worker `ais-research-rag` @ `ais-research-rag.shalomshafa.workers.dev`
  — Drive → chunk → embed (`@cf/baai/bge-base-en-v1.5`, 768-dim) → Vectorize `idfr-diplomacy`.
  — Cron `*/30 * * * *` auto-syncs new/updated Drive PDFs.
  — `POST /query` for retrieval, `POST /sync` to ingest, `GET /health` + `/debug`.
- **Bugs fixed:** stale token (no refresh → added refresh flow); AI.run returns object-with-numeric-keys not array; `getByIds` probe for idempotent skip; `remaining` var scope.
- **Index MD:** `gdrive_pdf_index.md` — 157 PDFs, 4 subfolders, clickable URLs, last-sync line.

## Open threads (next upgrades)

### (a) Bump to paid Workers to fill faster
- Free-tier CPU limit (~30s/req) caps `/sync` at ~1 large PDF/invocation. Cron fills 135 remaining at 1/tick ≈ 3 days.
- **Fix:** upgrade Workers plan (paid = 5-min CPU) → raise `limit` in `handleSync` to 15–20/tick → full corpus in 1–2 cron cycles.
- Alt: add Cloudflare Queue (fan-out) — needs `Workers KV/Queues:Edit` scope (same gap that blocked KV earlier).

### (b) Improve PDF text quality
- Current `extractPdfText` is a byte-range heuristic → chunks carry xref/stream/object noise (e.g. `endobj`, `/Subtype/Link`, raw font glyphs). Retrieval works but signal is diluted.
- **Fix:** use a proper PDF text layer — either (i) `pdf.js`/`unpdf` in the Worker, or (ii) pre-extract clean text locally (PyMuPDF/marker) and upsert pre-cleaned chunks. Option (ii) keeps the Worker light and avoids Workers-bundle PDF-parser weight.
- Higher-quality chunks → cleaner `metadata.text` snippets + better embedding signal.

## Decisions
- Keep corpus + retrieval in Cloudflare account (not Google's model boundary) — Dynamic-Stabilism / no-backdoor principle.
- Incremental + idempotent sync (re-runs safe) over full re-embed each tick.
