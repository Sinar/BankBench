"""Pick the strong model for the sweep: one probe call each on the REAL system prompt.

Measures latency and whether the quoted rate lands in band (3.00-15.00) and near
the rational Nash reference.
"""
import json
import os
import time
import urllib.request
from pathlib import Path

import sweep_runner as S

KEY = S.KEY
CANDIDATES = [
    "openai/gpt-5.1",
    "google/gemini-2.5-pro",
    "anthropic/claude-opus-4.1",
    "moonshotai/kimi-k2.5",
    "z-ai/glm-4.7",
    "deepseek/deepseek-v4.1-flash",
]

SYS = S.system_for(*S.AGENTS[0], "none")
USR = S.user_for(1, {}, "none")
print("rational Nash reference = %.2f%%\n" % S.NASH_P)
print("%-32s %8s %8s  %-9s %s" % ("model", "latency", "rate", "in-band", "rationale"))
print("-" * 104)

for m in CANDIDATES:
    body = json.dumps({"model": m, "messages": [{"role": "system", "content": SYS},
                                                {"role": "user", "content": USR}],
                       "temperature": 0.2, "max_tokens": 900}).encode()
    req = urllib.request.Request(S.ENDPOINT, data=body, headers={
        "Content-Type": "application/json", "Authorization": "Bearer " + KEY})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            out = json.loads(r.read())
        dt = time.time() - t0
        msg = out["choices"][0].get("message") or {}
        txt = msg.get("content") or msg.get("reasoning_content") or msg.get("reasoning") or ""
        rate, why = S.parse_rate(txt)
        ok = (not rate != rate) and S.COST_OF_FUNDS <= rate <= S.RATE_MAX
        print("%-32s %7.1fs %8.2f  %-9s %s" % (m, dt, rate, "yes" if ok else "NO", why[:44]))
    except Exception as e:
        print("%-32s %7.1fs  ERROR: %s" % (m, time.time() - t0, str(e)[:60]))