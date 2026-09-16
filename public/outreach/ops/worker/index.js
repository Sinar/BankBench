/**
 * Cloudflare Worker — NVIDIA NIM CORS proxy for the Operational Integrity Evals console.
 *
 * Why this exists
 * ---------------
 * `https://integrate.api.nvidia.com` sends no `Access-Control-Allow-Origin`
 * header, so a browser cannot call it directly. The Python proxy in the parent
 * folder solves that locally. This Worker solves it for the deployed site, and
 * better: the key lives here as a secret, so nothing sensitive is sent from the
 * browser at all.
 *
 * Deploy
 * ------
 *   cd public/outreach/ops/worker
 *   npx wrangler deploy
 *   npx wrangler secret put NVIDIA_API_KEY      # paste the key when prompted
 *
 * Then set the console's proxy base URL to
 *   https://<worker-name>.<your-subdomain>.workers.dev/v1
 * and leave the API-key field empty.
 *
 * A caller-supplied Authorization header always wins over the secret, so you can
 * still point the page at this Worker with a different key to compare accounts.
 */

const UPSTREAM = 'https://integrate.api.nvidia.com';
const ALLOWED = ['/v1/chat/completions', '/v1/models'];

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Authorization, Content-Type, Accept',
  'Access-Control-Max-Age': '86400',
};

function json(body, status) {
  return new Response(JSON.stringify(body), {
    status: status || 200,
    headers: Object.assign({}, CORS, { 'Content-Type': 'application/json' }),
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS });
    }

    const url = new URL(request.url);
    if (ALLOWED.indexOf(url.pathname) === -1) {
      return json({ error: { message: 'Only ' + ALLOWED.join(', ') + ' are proxied.' } }, 404);
    }

    // A caller-supplied key wins; otherwise fall back to the Worker secret.
    const supplied = request.headers.get('Authorization');
    const bearer =
      supplied && supplied.indexOf('Bearer ') === 0 && supplied.length > 20
        ? supplied
        : env.NVIDIA_API_KEY
          ? 'Bearer ' + env.NVIDIA_API_KEY
          : null;

    if (!bearer) {
      return json(
        {
          error: {
            message:
              'No API key. Set the NVIDIA_API_KEY secret on this Worker, or send an Authorization header.',
          },
        },
        401,
      );
    }

    if (request.method === 'GET') {
      const upstream = await fetch(UPSTREAM + url.pathname, {
        headers: { Authorization: bearer, Accept: 'application/json' },
      });
      return new Response(upstream.body, {
        status: upstream.status,
        headers: Object.assign({}, CORS, { 'Content-Type': 'application/json' }),
      });
    }

    if (request.method !== 'POST') {
      return json({ error: { message: 'Method not allowed.' } }, 405);
    }

    const body = await request.text();
    const upstream = await fetch(UPSTREAM + url.pathname, {
      method: 'POST',
      headers: { Authorization: bearer, 'Content-Type': 'application/json' },
      body: body,
    });

    return new Response(upstream.body, {
      status: upstream.status,
      headers: Object.assign({}, CORS, { 'Content-Type': 'application/json' }),
    });
  },
};
