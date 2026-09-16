# `ops` — Operational Integrity Evals outreach site

MVP HTML microsite for the scenario-based agent-assurance method described in
`ais-research-companion/outreach/government/ops-eval.md`. Branding, palette, and
type scale follow `Sinar-BankBench/src/cetalabs.html` so both sites read as the
same house style.

Static HTML, no build step. Open `index.html` directly, or serve the folder:

```
python3 -m http.server -d Sinar-BankBench/public/outreach/ops 8000
```

## Files

| File | Role |
|---|---|
| `ops.css` | Shared shell: tokens, type scale, nav, section rhythm, tables, cards, demo widgets, ghost styles |
| `skeleton.html` | Skeleton/blueprint — 13 named slots, file map, build order, ghost-element conventions |
| `index.html` | Home page — framing, the interactive harness demo, and every reference section |

Both pages link the same `ops.css`, so tokens and section spacing cannot drift
between them. If a page is copied out of this folder on its own, the stylesheet
link breaks.

## The demo

`#demo` is a self-contained comparison: four control rows (scenario, behavioural
risk profile, pressure condition, harness on/off) driving a six-stage decision
pathway trace and a ten-measure scorecard delta.

All outputs are **pre-authored synthetic data** in the inline `<script>` of
`index.html` — no model is called and nothing is measured. Scores are computed
from a small baseline vector per profile, modulated by scenario and pressure, then
the harness effect vector is applied. It is labelled illustrative on the page and
in the footer, deliberately.

To change what the demo shows, edit the `PROFILES`, `SCENARIOS`, `PRESSURES`, or
`HARNESS_EFFECT` arrays at the top of that script. `MEASURES` and `STAGES` define
the scorecard rows and the pathway stages, and their order must stay in sync with
the baseline vectors.

## Ghost elements

Dashed outline + hatched fill + a written `ghost` label mark everything that is
proposed rather than built: the four Phase 1 screens, the Phase 2 and Phase 3
roadmap items, and the harness components when the harness is switched off.

Always keep the text label. The styling is a visual cue, never the only signal —
the same convention is documented in `skeleton.html#ghost`.

## Status

Phase 1 demonstration layer only. No scenario builder, no saved runs, no scoring
pipeline, no export. Those are drawn as ghosts on purpose.
