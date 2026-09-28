export default {
  async fetch(request, env, ctx) {
    // Handle preflight OPTIONS requests for CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    // Parse the target URL from query parameters
    const url = new URL(request.url);
    const targetUrl = url.searchParams.get('target');

    if (!targetUrl) {
      return new Response(
        JSON.stringify({ error: 'Missing target parameter' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Decode the target URL
    const decodedTarget = decodeURIComponent(targetUrl);

    // Only allow specific API providers
    const allowedHosts = [
      'integrate.api.nvidia.com',
      'openrouter.ai',
    ];

    try {
      const parsedUrl = new URL(decodedTarget);

      // Check if the target host is allowed
      const isAllowed = allowedHosts.some(host =>
        parsedUrl.hostname === host || parsedUrl.hostname.endsWith('.' + host)
      );

      if (!isAllowed) {
        return new Response(
          JSON.stringify({ error: 'Target host not allowed' }),
          { status: 403, headers: { 'Content-Type': 'application/json' } }
        );
      }

      // Extract the path from the original request
      const path = new URL(decodedTarget).pathname;

      // Create the forward request
      const forwardRequest = new Request(
        decodedTarget + request.url.pathname,
        {
          method: request.method,
          headers: {
            'Content-Type': 'application/json',
            ...Object.fromEntries(request.headers.entries()),
          },
          body: request.method !== 'GET' ? request.body : undefined,
        }
      );

      // Forward the request
      const response = await fetch(forwardRequest);

      // Add CORS headers to the response
      const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      };

      // Build the response with CORS headers
      const newResponse = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: {
          ...Object.fromEntries(response.headers.entries()),
          ...corsHeaders,
        },
      });

      return newResponse;

    } catch (error) {
      console.error('Proxy error:', error);
      return new Response(
        JSON.stringify({ error: 'Proxy failed' }),
        { status: 500, headers: { 'Content-Type': 'application/json' } }
      );
    }
  }
};