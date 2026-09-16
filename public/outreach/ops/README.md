# `ops` — Operational Integrity Evals outreach site

MVP HTML microsite for the scenario-based agent-assurance method described in
`ais-research-companion/outreach/government/ops-eval.md`. Branding, palette, and
type scale follow `Sinar-BankBench/src/cetalabs.html` so both sites read as the
same house style.

Static HTML, no build step.

## Files

| File | Role |
|---|---|
| `ops.css` | Shared shell: tokens, type scale, nav, section rhythm, tables, cards, demo widgets, ghost styles |
| `skeleton.html` | Skeleton/blueprint — 13 named slots, file map, build order, ghost-element conventions |
| `index.html` | Home page — framing, the interactive harness demo, and every reference section |
| `evals.html` | **The eval console** — no-code agent evaluation: 3 models × 10 scenarios, faux tool sandbox, full prompt/tool/output trace with tokens and cost |
| `nvidia-proxy.py` | Local CORS proxy for live runs (stdlib only, no pip install) |
| `worker/` | Cloudflare Worker — the same proxy for the deployed site, with the key held server-side as a secret |

All pages link the same `ops.css`, so tokens and section spacing cannot drift
between them. If a page is copied out of this folder on its own, the stylesheet
link breaks.

## Running it

Three ways, in increasing order of setup. Simulated mode is always available, so
you can look at everything before deciding to spend anything.

### 1 · Simulated — nothing to install

```bash
python3 -m http.server -d Sinar-BankBench/public/outreach/ops 8000
# then open  http://localhost:8000/          (home page)
#            http://localhost:8000/evals.html (eval console)
```

No key, no network, no proxy, no cost. All 10 scenarios, all 25 tools, both
sandbox modes and both harness conditions are explorable, and every result is
labelled `simulated`.

### 2 · Live, locally — the Python proxy

NVIDIA's endpoint sends no `Access-Control-Allow-Origin` header, so a browser
cannot call it directly. Run the bundled proxy in a second terminal:

```bash
cd Sinar-BankBench/public/outreach/ops
python3 nvidia-proxy.py           # listens on http://127.0.0.1:8790/v1
```

Port 8790 is the default because 8787 is often already taken on developer
machines. If it is taken here too, the proxy says so and exits — pick another:

```bash
PROXY_PORT=9000 python3 nvidia-proxy.py
# then set the console's proxy base URL to http://127.0.0.1:9000/v1
```

Then in the console choose **Live · local proxy** and paste your key into the
field. The key on this machine lives in `~/.hermes/.env` as `NVIDIA_API_KEY`.

To keep the key out of the browser entirely, hand it to the proxy instead and
leave the field empty — the proxy reads `NVIDIA_API_KEY` from its own environment:

```bash
set -a; source ~/.hermes/.env; set +a
python3 nvidia-proxy.py
```

If the proxy answers **502**, it is almost always TLS: python.org builds on macOS
ship without a wired-up CA bundle, so `urlopen` fails with
`CERTIFICATE_VERIFY_FAILED`. `pip install certifi` fixes it — the proxy uses
certifi automatically and says so in the error body.

### 3 · Live, online — Cloudflare Worker + Pages

Online the key should never reach the browser. The Worker in `worker/` holds it as
a secret, and the page calls the Worker.

**a · Deploy the Worker** (once):

```bash
cd Sinar-BankBench/public/outreach/ops/worker
npx wrangler login
npx wrangler deploy
npx wrangler secret put NVIDIA_API_KEY    # paste the key when prompted
```

Wrangler prints the Worker URL — note the subdomain.

**b · Point the console at it.** Open the site, choose **Live · Cloudflare**, and
set the proxy base URL to
`https://bankbench-nvidia-proxy.<your-subdomain>.workers.dev/v1`. Leave the
API-key field **empty**: the Worker supplies the key.

To make that the default for everyone, set `MODE_BASE.hosted` in `evals.html` to
your real URL. A caller-supplied key always overrides the Worker secret, so you
can still point the page at it with a different key to compare accounts.

**c · Deploy the site.** Pushing to `main` triggers
`.github/workflows/deploy.yml`, which now assembles this folder into
`dist/outreach/ops/` and publishes it alongside `site/`. Or deploy by hand:

```bash
cd Sinar-BankBench
./deploy.sh
```

The console then lives at
`https://bankbench-sinar.pages.dev/outreach/ops/evals.html`, next to the existing
overview page at the site root.

#### Which Cloudflare secret goes where

These are easy to conflate, and they are different things:

| Secret | Belongs to | Set with | Needed because |
|---|---|---|---|
| `NVIDIA_API_KEY` | the **Worker** | `npx wrangler secret put NVIDIA_API_KEY` | live online runs need no key in the browser |
| `CLOUDFLARE_API_TOKEN` | **GitHub Actions** repo secret | GitHub → Settings → Secrets and variables → Actions | the Action deploys to Pages |
| `CLOUDFLARE_ACCOUNT_ID` | **GitHub Actions** repo secret | same | same |

Cloudflare Pages itself serves static files and never needs the NVIDIA key. Both
Cloudflare values are already in `~/.hermes/.env`, which `deploy.sh` sources
automatically when you deploy by hand.

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

## The eval console (`evals.html`)

A no-code agent evaluation interface: pick three models, pick scenarios, run, and
read the full trace. Ten scenarios, 25 faux tools, two sandbox modes, two harness
conditions. This is the agentic counterpart to the home page's demo — the model is
not answering a question, it is given a role, an objective, and tools, then left
to decide.

### Two run modes

- **Simulated** (default) — no key, no network, no cost. A scripted tool sequence
  per scenario executed against the real sandbox, with a templated output. Every
  result is labelled `simulated` in the summary and the trace.
- **Live** — real calls to NVIDIA-hosted models. Token counts come from the API's
  own `usage` field, summed across every step of the agent loop.

### Live runs are retried, and some models are slow

NVIDIA's hosted endpoint is not perfectly reliable, so the console is built for
that rather than assuming it away:

- **Intermittent 500s.** The same request that succeeds can return
  `500 Internal server error` a minute later. The console retries 5xx and 429 up
to three times with backoff before recording a failure.
- **90-second per-request timeout.** A hung request would otherwise stall the
  whole run. On timeout the step fails with a clear message instead of retrying,
  because a slow model stays slow and retrying only triples the wait.
- **Step-level progress.** The status line reads
  `Running 2 of 3 — <model> × S01 (step 3/8)…` so a slow run is visibly working
  rather than apparently frozen.
- **Some models are too slow to use here.** `z-ai/glm-5.3` completes but takes
  minutes per scenario; `moonshotai/kimi-k3`, `z-ai/glm-5.3-flash` and
  `google/gemma-4-31b-it` exceeded 180s on a single tool call and were dropped.
  The defaults are chosen for speed.
- **Models sometimes never commit.** A model can keep calling tools until the
  12-step limit without producing a decision. That is reported as its own finding
  rather than hidden — an agent that never concludes is an operational problem.
  Scenarios are sized so a competent agent can finish inside the budget: S01 has
  6 cases, not 14, because one tool call per step is the common pattern.

### Live runs need the proxy, and here is why

`https://integrate.api.nvidia.com` sends **no `Access-Control-Allow-Origin`
header** — verified by inspecting the preflight response directly. A browser
therefore cannot call it; the request is blocked before it leaves the page. So
live mode posts to a local proxy instead:

```bash
python3 nvidia-proxy.py          # listens on http://127.0.0.1:8790/v1
```

The proxy adds the CORS headers and forwards to NVIDIA unchanged. It uses
certifi's CA bundle when available, because python.org builds on macOS otherwise
fail TLS verification with `CERTIFICATE_VERIFY_FAILED` — which surfaces as a bare
502 until fixed. Your API key is sent from the page to your own localhost proxy
and straight through to NVIDIA; it is never stored or logged.

### Models are probed, not assumed

NVIDIA retires hosted models aggressively, so nothing in the picker is there on
reputation. Every entry passed **two** checks against the live API with a real key
on **2026-09-16**:

1. the model still exists (no `410 end-of-life`), and
2. it actually performed a tool call when handed a tool schema.

The second check matters because this is an **agent** eval, not a chat eval.
Excluded, and why:

| Excluded model | Result |
|---|---|
| `nvidia/llama-3.1-nemotron-ultra-253b-v1`, `google/gemma-3-12b-it`, `ibm/granite-3.0-8b-instruct` | HTTP 404 `Function ... not found` — accepts chat, rejects tools |
| `moonshotai/kimi-k3`, `z-ai/glm-5.3-flash`, `google/gemma-4-31b-it` | timed out past 180s on a single tool call |
| `mistralai/mistral-nemotron` | HTTP 500 from upstream |
| `openai/gpt-oss-120b`, `qwen/qwen3-next-80b-a3b-instruct`, `meta/llama-3.3-70b-instruct`, `microsoft/phi-4-mini-instruct`, `deepseek-ai/deepseek-v4-flash`, `moonshotai/kimi-k2-instruct`, `minimaxai/minimax-m2.7`, `nvidia/nemotron-3-nano-30b-a3b`, `nvidia/llama-3.3-nemotron-super-49b-v1.5` | already end-of-life (410) |

The page also carries a **Check selected models are live** button that re-probes
the current selection: 410 = end-of-life, 401/403 = exists but the key was
rejected, 404 = not found, 200 = answered.

### The sandbox is the point

Every tool has a neutral and a loaded variant. Loaded responses are framed,
incomplete, or pre-decided — a pre-made ranking, a policy revision with the
non-discrimination clause omitted, a conflict check that finds nothing, a ledger
with the inconvenient entries excluded. The non-neutrality enters through the
**tool result** rather than the prompt, which is what makes the "mentality" claim
testable: same model, same scenario, same objective, different operational
decision.

The harness condition adds policy retrieval, a protected-characteristic rule,
structured uncertainty, integrity and de-escalation protocols, and approval gates
that make `send_external`, `record_delete`, `decide`, `allocate` and
`approve_list` refuse and require escalation instead of proceeding.

### Editing it

`MODELS`, `SCENARIOS`, `TOOLS`, `HARNESS_PROMPT` and the per-mode proxy defaults
(`MODE_BASE`) sit at the top of the inline `<script>`. A scenario needs `system`,
`user`, `tools`, `simTools`, `safe`, and the two `sim*` outputs. A tool needs
`desc`, `params`, and a `run(args, loaded)` that branches on `loaded`. Rate
defaults live in `TIER_RATES` and are editable in the UI.

## Ghost elements

Dashed outline + hatched fill + a written `ghost` label mark everything that is
proposed rather than built: the four Phase 1 screens, the Phase 2 and Phase 3
roadmap items, and the harness components when the harness is switched off.

Always keep the text label. The styling is a visual cue, never the only signal —
the same convention is documented in `skeleton.html#ghost`.

## Status

Phase 1 demonstration layer. The home page demo is pre-authored synthetic data;
the eval console runs for real in live mode and is scripted in simulated mode.
Still absent: a scenario builder, saved runs, an independent scoring pipeline, and
export. Those are drawn as ghosts on purpose.
