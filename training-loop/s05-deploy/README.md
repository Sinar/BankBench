# S-05 — Deploy via REST API (PRIORITY)

Proves: you can ship a trained checkpoint as something else can actually call. Closes the loop from "I trained a model" to "here's an endpoint." Also gives BankBench-MY a self-hosted eval target you fully control.

## Run — local

```bash
cd s05-deploy
pip install -r requirements.txt
export MODEL_PATH=../s02-finetune/out/checkpoint-final
export API_KEY=$(openssl rand -hex 16)   # gate the endpoint -- don't leave it open
uvicorn serve:app --host 0.0.0.0 --port 8000
```

Test it:
```bash
curl -X POST http://localhost:8000/generate \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Verify my identity please, I need to reset my password."}'
```

## Expose it (so it's a real demoable endpoint, not just localhost)

```bash
# Cloudflare Tunnel (you already have Cloudflare tooling in this environment)
cloudflared tunnel --url http://localhost:8000
```

Or run it on the same VastAI box right after S-02 finishes, so the trained weights never leave the instance and you skip a download step — just remember the instance stays billed while the tunnel is up.

## Later: proper Cloudflare deploy (not tomorrow's scope)

Tunnel is the fast/free path for tomorrow's demo. Once this is worth keeping up persistently:

- **Model-serving API** (this FastAPI app, or a Flask rewrite later if preferred): needs an actual compute runtime, not static hosting — Cloudflare Containers, or a small always-on VPS behind Cloudflare Tunnel/DNS, since Workers' JS runtime can't run a PyTorch model directly. If the checkpoint is small enough, Workers AI is worth checking as a swap-in instead of self-hosting inference at all.
- **Dashboard** (`../dashboard/index.html`): this one *can* go straight to Cloudflare Pages as-is — it's a single static HTML file with no build step, so `wrangler pages deploy dashboard/` (or drag-and-drop in the Cloudflare dashboard) is enough once you want it at a real URL instead of opened locally.

Don't set either of these up tomorrow — get S-02 → S-05 working locally + tunnel first, persistent hosting is a follow-up once the pipeline itself is proven.

## Point BankBench-MY's harness at it

Once the endpoint is live, add it as a new backend target in `../../bankbench_my/`'s Inspect AI eval stack alongside the NVIDIA/Gemini/Together/Cloudflare backends already wired in the private working repo's eval runner — same scorecard format, now with a row for "my own fine-tuned checkpoint."

## Deliverable to capture

A saved `curl` transcript (or short screen recording) of a real call against your own endpoint. Copy the endpoint URL (or "local-only, demoed live" note) and latency into `../dashboard/index.html (edit the DATA block)` under `"s05"`.
