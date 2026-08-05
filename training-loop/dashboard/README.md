# Dashboard — no-code, edit-and-refresh

`index.html` is a single static file, no build step, no server required. It reads its data from a `DATA` object embedded directly in the `<script>` block near the top of the file (not a separate fetch — that avoids CORS issues when opening the file directly via `file://`, which matters since this needs to work tomorrow without setting up a local server).

## How to update it (no-code)

1. Open `index.html` in a text editor
2. Find the `const DATA = { ... }` block near the top
3. Edit the fields for whichever stage just finished (status, grade, numbers, note)
4. Save, then refresh `index.html` in your browser (double-click to open, or drag into a tab)

That's it — no npm install, no rebuild. The "coding later" part is wiring this up to auto-read `results.json` files from each stage folder instead of hand-edited JSON; that's a follow-up task once the sprint itself is done, not a blocker for tomorrow.

## Ghosted mode

Stages you haven't started yet render **ghosted**: visible (so the full S-01→S-05 arc is always in view), greyed out, with a 🔒 lock badge, and not clickable. This is deliberate — it shows the roadmap without pretending unfinished stages are done, and it's the same "don't hide uncertainty" instinct as Substrate's grade system (see brand kit). Set `"status": "ghosted"` on any stage in `DATA` to get this treatment; the dashboard does the rest.

## Brand

Styled from `/Users/nshfnoh/.hermes/projects/BrandKits/Substrate/brand-kit.md` — greyscale base, signal green (`--sig`) as the only chromatic accent, A/B/C/D grade coloring reused directly (green=A/B, amber=C, red=D), Space Grotesk / Inter / JetBrains Mono three-font system.
