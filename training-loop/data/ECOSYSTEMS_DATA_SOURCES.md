# ECOSYSTEMS.md → Training-Loop Data Sources

Crawled from `https://github.com/Sinar/.github/blob/main/profile/ECOSYSTEMS.md`
(Go + Python ecosystem catalog, 152 lines). Goal: find Sinar-owned data we can
reuse to feed the `training-loop/` SFT / corpus pipeline *instead of* or *alongside*
the Kaggle + AdaptationAI sources in `data/README.md`.

## Verdict up front

ECOSYSTEMS is a **code** catalog, not a dataset catalog. It does **not** contain a
clean BM/Manglish text corpus or a general instruction-tuning set, so it cannot
replace Kaggle's `bahasa malaysia` (language grounding) or `databricks-dolly-15k`
(general instruction volume). Those two still need Kaggle credentials.

What ECOSYSTEMS *does* give us for free and on-brand is the **benign
financial-domain smoke-test / over-refusal contrast** set — Sinar's own
corruption, beneficial-ownership, procurement and FOI civic text. This maps
directly onto `data/README.md`'s Banking77 use-case ("benign banking-domain
prompts... topically adjacent to BankBench-MY but non-adversarial") and removes
the Kaggle dependency for that one slice.

## Mapping: repo → training-loop need

| Need (from data/README) | ECOSYSTEMS fit | Repos | Use |
|---|---|---|---|
| BM/Manglish language grounding (S-01 corpus, S-02 register) | ⚠️ Partial — code repos, not raw text | `legisdata` (Parliamentary data + SayIt), `go-electdocs` (election data), `go-pardocs`/`sinar.pardocs` (parliament PDFs) | Seed civic Malaysian text *if* their data outputs are fetched; otherwise fall back to BankBench-MY prompts + Kaggle. |
| Benign banking-adjacent smoke test (over-refusal check) | ✅ Strong | `sinar.corruptiontracker`, `politikus.bods`, `ocds.contenttypes`, `tumpangtanya.inforequest` | Benign financial-transparency / FOI prompts that a safe model must NOT refuse — the exact contrast Banking77 was meant to provide. |
| General instruction-following volume | ❌ None | — | Keep Kaggle Dolly/OASST1; not in ECOSYSTEMS. |
| S-04 provenance / OLMo financial corpus | ✅ Strong | same financial-transparency set above | Domain terms (beneficial ownership, OCDS, procurement) for the provenance audit. |

## Why this fits "what we wanna do here"

BankBench-MY's adversarial scenarios are *fraud / social-engineering / control-bypass*
requests. A fine-tune that only sees adversarial→refusal pairs will over-refuse
legitimate financial questions. The Sinar civic set is the ideal benign contrast:
- "How do I check a company's beneficial owner?" (`politikus.bods`) — benign, but
  uses the same financial language as a fraud scenario.
- "How do I report suspected corruption?" (`sinar.corruptiontracker`) — benign,
  topically adjacent to BankBench-MY's scam categories.
- "How do I file an FOI request for a contract?" (`ocds.contenttypes`, `tumpangtanya.inforequest`)
  — benign procurement/transparency language.

Using Sinar's *own* civic data also keeps the whole pipeline on-brand for the
fellowship reporting rhythm (civic-tech provenance) and means no Kaggle token is
required for the over-refusal smoke test.

## How to fetch (see `fetch_sinar_civic.sh`)

Shallow-clone the relevant repos, pull plain-text / data files into
`data/raw/sinar-civic/`, then `build_smoke_test.py` can mix them into
`smoke_benign.jsonl` as the over-refusal check set.

```bash
bash fetch_sinar_civic.sh          # clones + extracts text into data/raw/sinar-civic/
python build_smoke_test.py --sinar-civic data/raw/sinar-civic
```

## Caveat

Most of these repos are Plone/Django **applications**; the bulk of usable civic
*text* lives in their data outputs / Sinar's open-data portals rather than the
source tree. `fetch_sinar_civic.sh` extracts what text exists (READMEs, docs,
sample data, vocabulary) and is a starting point — for a full BM civic corpus,
pair it with Sinar's published datasets (data.gov.my mirrors, sinarproject.org).
