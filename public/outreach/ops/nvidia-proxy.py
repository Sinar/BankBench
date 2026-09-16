#!/usr/bin/env python3
"""
Local CORS proxy for the Operational Integrity Evals demo (evals.html).

Why this exists
---------------
NVIDIA's hosted NIM endpoint (https://integrate.api.nvidia.com) does not send
`Access-Control-Allow-Origin`, so a browser page cannot call it directly — the
preflight fails and the request is blocked. This proxy sits on localhost, adds
the CORS headers, and forwards to NVIDIA unchanged.

Your API key is never stored here. The browser sends it in the Authorization
header on each request and this process passes it straight through.

Usage
-----
    export NVIDIA_API_KEY=nvapi-...        # optional; the browser can send its own
    python3 nvidia-proxy.py                # listens on http://127.0.0.1:8790

Then in evals.html choose "Live · local proxy" and set the proxy base URL to
http://127.0.0.1:8790/v1

Port 8790 is the default because 8787 is commonly already taken on developer
machines. Override it with PROXY_PORT if you need to:

    PROXY_PORT=9000 python3 nvidia-proxy.py

Standard library only — no pip install. Uses certifi's CA bundle when
available, because python.org builds on macOS otherwise fail TLS verification.
"""

import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "https://integrate.api.nvidia.com"
PORT = int(os.environ.get("PROXY_PORT", "8790"))
ALLOWED_PATHS = ("/v1/chat/completions", "/v1/models")


def _ssl_context():
    """Prefer certifi's CA bundle.

    python.org builds on macOS ship without a wired-up CA store, so a plain
    urlopen fails with CERTIFICATE_VERIFY_FAILED. certifi is present in most
    environments and fixes it; if it is missing we fall back to the default
    context and surface a clear hint instead of a bare 502.
    """
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


SSL_CTX = _ssl_context()


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Authorization, Content-Type, Accept",
        )
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if self.path not in ALLOWED_PATHS:
            self._fail(404, "Only %s are proxied." % ", ".join(ALLOWED_PATHS))
            return
        self._forward("GET", None)

    def do_POST(self):
        if self.path not in ALLOWED_PATHS:
            self._fail(404, "Only %s are proxied." % ", ".join(ALLOWED_PATHS))
            return
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        self._forward("POST", body)

    def _forward(self, method, body):
        headers = {"Accept": "application/json"}
        auth = self.headers.get("Authorization")
        if auth:
            headers["Authorization"] = auth
        elif os.environ.get("NVIDIA_API_KEY"):
            headers["Authorization"] = "Bearer " + os.environ["NVIDIA_API_KEY"]
        if body is not None:
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(
            UPSTREAM + self.path, data=body, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(req, timeout=180, context=SSL_CTX) as resp:
                payload = resp.read()
                status = resp.status
        except urllib.error.HTTPError as exc:
            payload = exc.read()
            status = exc.code
        except urllib.error.URLError as exc:
            reason = getattr(exc, "reason", exc)
            if isinstance(reason, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(reason):
                self._fail(502, "TLS certificate verification failed. Run "
                                "`pip install certifi` (or on macOS: "
                                "'/Applications/Python 3.11/Install Certificates.command'), "
                                "then restart this proxy.")
            else:
                self._fail(502, "Upstream request failed: %s" % reason)
            return
        except Exception as exc:  # network / DNS / timeout
            self._fail(502, "Upstream request failed: %s" % exc)
            return

        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _fail(self, status, message):
        payload = json.dumps({"error": {"message": message}}).encode()
        self.send_response(status)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt, *args):
        sys.stderr.write("[proxy] %s\n" % (fmt % args))


if __name__ == "__main__":
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), ProxyHandler)
    except OSError as exc:
        if getattr(exc, "errno", None) in (48, 98):  # EADDRINUSE on macOS / Linux
            print("Port %d is already in use." % PORT)
            print("Pick another one, e.g.  PROXY_PORT=9000 python3 nvidia-proxy.py")
            print("then set the console's proxy base URL to http://127.0.0.1:9000/v1")
            raise SystemExit(1)
        raise
    print("CORS proxy for NVIDIA NIM listening on http://127.0.0.1:%d" % PORT)
    print("Set the proxy base URL in evals.html to http://127.0.0.1:%d/v1" % PORT)
    print("Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
