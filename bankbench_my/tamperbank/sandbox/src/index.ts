import { TamperSessionDO } from "./session_do";
import { GEN_KWARGS, SYSTEM_PROMPT_A } from "./prompts";
import { parseAction, scoreAction } from "./scoring";
import type { RunLogEntry } from "./types";

export { TamperSessionDO };

interface Env {
  AI: Ai;
  SESSION: DurableObjectNamespace<TamperSessionDO>;
  ASSETS: Fetcher;
}

// Single point of model routing. Free-tier Workers AI model today; a
// later swap or A/B is a one-line change here, not a rewrite of the
// agent-bridge logic below.
const MODEL_ID = "@cf/meta/llama-3.1-8b-instruct-fp8";

function json(data: unknown, init: ResponseInit = {}): Response {
  return new Response(JSON.stringify(data), {
    ...init,
    headers: { "content-type": "application/json", ...(init.headers ?? {}) },
  });
}

function newSessionId(): string {
  return crypto.randomUUID();
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/api/session" && request.method === "POST") {
      const sessionId = newSessionId();
      const stub = env.SESSION.get(env.SESSION.idFromName(sessionId));
      const state = await stub.getState();
      return json({ sessionId, state });
    }

    if (url.pathname === "/api/chat" && request.method === "POST") {
      const body = await request.json<{ sessionId: string; message: string }>();
      if (!body.sessionId || !body.message) {
        return json({ error: "sessionId and message are required" }, { status: 400 });
      }

      const stub = env.SESSION.get(env.SESSION.idFromName(body.sessionId));

      if (await stub.isRateLimited()) {
        const state = await stub.getState();
        return json({
          blocked: "RATE_LIMIT",
          message: `Session action limit (${state.actionLimit}) reached — this sandbox caps actions per tester to protect the shared free Workers AI quota.`,
          state,
          remaining_actions: 0,
        });
      }

      await stub.appendHistory({ role: "user", content: body.message });
      const history = await stub.getHistory();

      const messages = [
        { role: "system", content: SYSTEM_PROMPT_A },
        ...history.map((t) => ({ role: t.role, content: t.content })),
      ];

      const aiResponse = await env.AI.run(MODEL_ID, {
        messages,
        temperature: GEN_KWARGS.temperature,
        max_tokens: GEN_KWARGS.max_tokens,
      });

      const rawText =
        typeof aiResponse === "string" ? aiResponse : (aiResponse as { response?: string }).response ?? "";

      await stub.appendHistory({ role: "assistant", content: rawText });
      await stub.consumeAction();

      const parsed = parseAction(rawText);
      const expected: "refuse" | "comply" = "refuse"; // sandbox probes are adversarial by default

      // Environment mutation only makes sense when the model attempted a
      // transfer; the tamper rubric's COMPLY leaves no env action to take,
      // so we log the verdict and the environment state carries the flow.
      const envResult = {
        status: "NOOP" as const,
        message: `Agent responded with ${parsed.action}, no transfer attempted.`,
        audit_note: "No environment mutation for REFUSE/PARTIAL/COMPLY turns.",
      };

      const score = scoreAction(parsed.action, expected);

      const logEntry: RunLogEntry = {
        scenario_id: body.sessionId,
        agent: MODEL_ID,
        action: parsed.action,
        env_result: envResult,
        safety_score: score,
        reasoning: parsed.reasoning,
        timestamp: new Date().toISOString(),
      };
      await stub.appendLog(logEntry);

      const state = await stub.getState();
      return json({
        reply: rawText,
        parsed_action: parsed,
        env_result: envResult,
        safety_score: score,
        state,
        remaining_actions: state.actionLimit - state.actionsUsed,
      });
    }

    if (url.pathname.startsWith("/api/log/") && request.method === "GET") {
      const sessionId = url.pathname.split("/api/log/")[1];
      const stub = env.SESSION.get(env.SESSION.idFromName(sessionId));
      const log = await stub.getLog();
      return json({ sessionId, log });
    }

    return env.ASSETS.fetch(request);
  },
};