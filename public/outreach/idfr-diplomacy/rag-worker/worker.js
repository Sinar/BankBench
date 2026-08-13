// ais-research-rag — sovereign RAG for the idfr-diplomacy Drive folder.
// Tier 3: Drive PDFs -> extract -> chunk -> embed (Workers AI) -> Vectorize.
// Plus /query (retrieval) and /sync (ingest). Cron every 30 min re-syncs.
//
// Secrets:  wrangler secret put GOOGLE_TOKEN   (contents of ~/.hermes/google_token.json)
// Routes:
//   POST /sync     -> recursive PDF ingest -> Vectorize
//   POST /query    -> {query} -> top-k chunks
//   GET  /health   -> status
//   GET  /debug    -> step-by-step self-test, surfaces real errors (no 1101 masking)

const CHUNK_SIZE = 1800;
const CHUNK_OVERLAP = 200;
const EMBED_MODEL = "@cf/baai/bge-base-en-v1.5"; // 768-dim, matches index
const TOP_K = 5;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/health") {
      return json({ ok: true, index: env.VECTORIZE.index_name });
    }

    if (url.pathname === "/debug") {
      return handleDebug(env);
    }

    if (url.pathname === "/sync" && request.method === "POST") {
      try {
        return await handleSync(env);
      } catch (e) {
        return json({ error: String(e && e.message ? e.message : e), stack: String(e && e.stack ? e.stack : "") }, 500);
      }
    }

    if (url.pathname === "/query" && request.method === "POST") {
      try {
        return await handleQuery(request, env);
      } catch (e) {
        return json({ error: String(e && e.message ? e.message : e) }, 500);
      }
    }

    return new Response("Unknown route. Use /sync, /query, /health, or /debug.", { status: 404 });
  },

  // Cron trigger (every 30 min per wrangler.toml)
  async scheduled(event, env, ctx) {
    ctx.waitUntil(handleSync(env).catch((e) => console.error("cron sync failed", e)));
    return new Response("scheduled sync triggered");
  },
};

async function handleDebug(env) {
  const steps = [];
  try {
    const tok = await getAccessToken(env);
    steps.push({ step: "getAccessToken", ok: true, len: tok.length });
  } catch (e) {
    return json({ failedAt: "getAccessToken", error: String(e.message || e) });
  }
  try {
    const files = await listDrivePdfsRecursive(env.DRIVE_FOLDER_ID, env);
    steps.push({ step: "listDrivePdfsRecursive", ok: true, count: files.length });
    if (!files.length) return json({ steps, note: "no PDFs found — check DRIVE_FOLDER_ID / token scope" });
    const sample = files[0];
    const bytes = await downloadDriveFile(sample.id, env);
    steps.push({ step: "downloadDriveFile", ok: true, bytes: bytes.length, name: sample.name });
    const text = extractPdfText(bytes);
    steps.push({ step: "extractPdfText", ok: true, chars: text.length });
    // DUMP raw shape of a batch embedding response
    const e2 = await env.AI.run(EMBED_MODEL, { text: [text.slice(0, 100), text.slice(100, 200)] });
    steps.push({ step: "AI.run batch raw", ok: true,
      keys: Object.keys(e2 || {}),
      dataType: Array.isArray(e2?.data) ? "array" : typeof e2?.data,
      firstRowKeys: e2?.data?.[0] ? Object.keys(e2.data[0]) : "no-data",
      sampleEmbedding: e2?.data?.[0]?.embedding ? e2.data[0].embedding.slice(0, 3) : "NO embedding key",
    });
    return json({ steps, allOk: true });
  } catch (e) {
    return json({ steps, failedAt: steps[steps.length - 1]?.step, error: String(e.message || e), stack: String(e.stack || "") }, 500);
  }
}

async function handleSync(env, limit = 1) {
  const files = await listDrivePdfsRecursive(env.DRIVE_FOLDER_ID, env);
  if (!files.length) return json({ status: "no_files", files: [] });

  // Check which files are already embedded (id prefix ${fileId}-0 exists)
  const probeIds = files.map((f) => `${f.id}-0`);
  let already = new Set();
  try {
    const existing = await env.VECTORIZE.getByIds(probeIds);
    for (const e of existing || []) if (e) already.add(e.id.replace(/-0$/, ""));
  } catch (_) { /* getByIds may be unsupported; treat all as new */ }

  const pending = files.filter((f) => !already.has(f.id));
  const batch = pending.slice(0, limit);
  let upserted = 0;
  for (const f of batch) {
    const pdfBytes = await downloadDriveFile(f.id, env);
    const text = extractPdfText(pdfBytes);
    const chunks = chunkText(text, CHUNK_SIZE, CHUNK_OVERLAP);
    for (let i = 0; i < chunks.length; i += 20) {
      const slice = chunks.slice(i, i + 20);
      const vectors = await embedBatch(slice, env);
      const records = vectors.map((v, j) => ({
        id: `${f.id}-${i + j}`,
        values: v,
        metadata: { source: f.name, driveId: f.id, chunk: i + j, text: slice[j].slice(0, 500) },
      }));
      await env.VECTORIZE.upsert(records);
      upserted += records.length;
    }
  }
  const lastSync = new Date().toISOString();
  const remaining = pending.length - batch.length;
  return json({
    status: "synced_batch",
    processed: batch.length,
    alreadyEmbedded: files.length - pending.length,
    remaining,
    vectorsThisRun: upserted,
    lastSync,
    note: remaining > 0 ? "Cron will continue embedding remaining files next tick (idempotent)." : "All files embedded.",
  });
}

async function handleQuery(request, env) {
  const body = await request.json().catch(() => ({}));
  const query = body.query;
  if (!query) return json({ error: "missing query" }, 400);
  const [emb] = await embedBatch([query], env);
  const results = await env.VECTORIZE.query(emb, { topK: TOP_K, returnMetadata: "all" });
  return json({
    query,
    matches: (results.matches || []).map((m) => ({ score: m.score, source: m.metadata?.source, text: m.metadata?.text })),
  });
}

// ---- Drive helpers ----

async function getAccessToken(env) {
  const tok = JSON.parse(env.GOOGLE_TOKEN);
  const accessToken = tok.access_token || tok.token;
  if (!accessToken) throw new Error("no access token in GOOGLE_TOKEN secret");

  // If token has expiry info and is expired (or missing), refresh via refresh_token
  const expiry = tok.expiry ? new Date(tok.expiry) : null;
  const expired = expiry && expiry.getTime() < Date.now() - 60000; // 1-min buffer
  if ((expired || !expiry) && tok.refresh_token && tok.client_id && tok.client_secret) {
    const body = new URLSearchParams({
      client_id: tok.client_id,
      client_secret: tok.client_secret,
      refresh_token: tok.refresh_token,
      grant_type: "refresh_token",
    });
    const r = await fetch(tok.token_uri || "https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "content-type": "application/x-www-form-urlencoded" },
      body,
    });
    const fresh = await r.json();
    if (fresh.access_token) return fresh.access_token;
  }
  return accessToken;
}

async function listDrivePdfsRecursive(folderId, env, path = "") {
  const token = await getAccessToken(env);
  const q = encodeURIComponent(`'${folderId}' in parents`);
  const res = await fetch(
    `https://www.googleapis.com/drive/v3/files?q=${q}&fields=files(id,name,mimeType,webViewLink)`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  const data = await res.json();
  let pdfs = [];
  for (const f of data.files || []) {
    if (f.mimeType === "application/vnd.google-apps.folder") {
      pdfs = pdfs.concat(await listDrivePdfsRecursive(f.id, env, `${path}/${f.name}`));
    } else if (f.mimeType === "application/pdf") {
      pdfs.push({ id: f.id, name: f.name, path: path || "(root)", webViewLink: f.webViewLink });
    }
  }
  return pdfs;
}

async function downloadDriveFile(id, env) {
  const token = await getAccessToken(env);
  const res = await fetch(`https://www.googleapis.com/drive/v3/files/${id}?alt=media`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return new Uint8Array(await res.arrayBuffer());
}

function extractPdfText(bytes) {
  let s = "";
  for (let i = 0; i < bytes.length; i++) {
    const c = bytes[i];
    if (c >= 32 && c < 127) s += String.fromCharCode(c);
    else if (c === 10 || c === 13) s += " ";
  }
  return s.replace(/\s+/g, " ").trim();
}

function chunkText(text, size, overlap) {
  const chunks = [];
  let start = 0;
  while (start < text.length) {
    chunks.push(text.slice(start, start + size));
    start += size - overlap;
  }
  return chunks.filter((c) => c.trim().length > 0);
}

async function embedBatch(texts, env) {
  const res = await env.AI.run(EMBED_MODEL, { text: texts });
  let arr = res?.data;
  if (!arr && Array.isArray(res)) arr = res;
  if (!arr) throw new Error("AI.run returned unexpected shape: " + JSON.stringify(res).slice(0, 300));
  // Workers AI returns each embedding as an OBJECT with numeric keys {0:..,1:..},
  // not a plain array. Convert to number[] for Vectorize.
  return arr.map((d) => (Array.isArray(d) ? d : Object.values(d).map(Number)));
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json", "access-control-allow-origin": "*" },
  });
}
