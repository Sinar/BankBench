// Standalone Cloudflare Worker — OpenAI-compatible proxy.
//
// IMPORTANT: this Worker is NOT what serves /api/proxy on the Pages site.
// A Worker route cannot be attached to *.pages.dev, so that traffic is handled
// by functions/api/proxy.js instead. This Worker exists for callers that hit
// it directly on its workers.dev URL or a custom domain.
//
// Fixes applied vs. the previous version:
//   1. no longer appends request.url.pathname to the upstream URL
//   2. no longer double-decodes the (already decoded) ?target= param
//   3. forwards only Content-Type/Authorization/HTTP-Referer/X-Title

const ALLOWED_HOSTS = ['integrate.api.nvidia.com', 'openrouter.ai'];

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, HTTP-Referer, X-Title',
};

const json = (body, status) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS },
  });

export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

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

    const headers = new Headers();
    for (const h of ['Content-Type', 'Authorization', 'HTTP-Referer', 'X-Title']) {
      const v = request.headers.get(h);
      if (v) headers.set(h, v);
    }

    const hasBody = request.method !== 'GET' && request.method !== 'HEAD';

    try {
      const upstream = await fetch(target.toString(), {
        method: request.method,
        headers,
        body: hasBody ? request.body : undefined,
      });
      const out = new Headers(upstream.headers);
      for (const [k, v] of Object.entries(CORS)) out.set(k, v);
      return new Response(upstream.body, {
        status: upstream.status,
        statusText: upstream.statusText,
        headers: out,
      });
    } catch (err) {
      return json({ error: 'Proxy failed', detail: String(err) }, 502);
    }
  },
};
