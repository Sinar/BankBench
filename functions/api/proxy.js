// Cloudflare Pages Function — serves /api/proxy on the Pages domain itself.
//
// Why: a Worker route cannot attach to *.pages.dev (pages.dev is Cloudflare's
// shared zone, not this account's), so workers/api-proxy.js never received
// /api/proxy/* traffic. A Pages Function is same-origin and needs no route.
//
// Request: POST /api/proxy?target=<full upstream chat/completions URL>
//          Authorization: Bearer <the caller's key>  (forwarded as-is)

const ALLOWED_HOSTS = ['integrate.api.nvidia.com', 'openrouter.ai'];

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, HTTP-Referer, X-Title',
};

function json(body, status) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });
}

export async function onRequest(context) {
  const { request } = context;

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS });
  }

  // searchParams.get() ALREADY percent-decodes. Do not decode a second time —
  // the old Worker called decodeURIComponent() on an already-decoded value.
  const rawTarget = new URL(request.url).searchParams.get('target');
  if (!rawTarget) return json({ error: 'Missing target parameter' }, 400);

  let target;
  try {
    target = new URL(rawTarget);
  } catch {
    return json({ error: 'Invalid target URL' }, 400);
  }

  const allowed = ALLOWED_HOSTS.some(
    (h) => target.hostname === h || target.hostname.endsWith('.' + h)
  );
  if (!allowed) return json({ error: 'Target host not allowed' }, 403);

  // Forward ONLY the headers we mean to. The old Worker spread every inbound
  // header, which leaked Host/Origin/Cookie upstream.
  const headers = new Headers();
  for (const h of ['Content-Type', 'Authorization', 'HTTP-Referer', 'X-Title']) {
    const v = request.headers.get(h);
    if (v) headers.set(h, v);
  }

  const hasBody = request.method !== 'GET' && request.method !== 'HEAD';

  // NOTE: target already contains the full upstream path. The old Worker did
  // `decodedTarget + request.url.pathname`, which appended "/api/proxy" to the
  // upstream URL — that was the actual cause of the failed Seed calls.
  let upstream;
  try {
    upstream = await fetch(target.toString(), {
      method: request.method,
      headers,
      body: hasBody ? request.body : undefined,
    });
  } catch (err) {
    return json({ error: 'Proxy failed', detail: String(err) }, 502);
  }

  const out = new Headers(upstream.headers);
  for (const [k, v] of Object.entries(CORS)) out.set(k, v);
  return new Response(upstream.body, {
    status: upstream.status,
    statusText: upstream.statusText,
    headers: out,
  });
}
