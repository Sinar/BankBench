// Shapes mirror bankbench-tamper-live.py's action schema and export_phase()
// result shape, so sandbox run logs are drop-in compatible with the eval
// exports (same discipline as the reference sandbox vs bankbench_eval.py).

export type ActionType = "REFUSE" | "PARTIAL" | "COMPLY" | "PARSE_ERROR";

export interface ParsedAction {
  action: ActionType;
  response?: string | null;
  reasoning: string;
}

export interface EnvResult {
  status: "SUCCESS" | "BLOCKED_PENDING_OTP" | "BLOCKED_UNKNOWN_PAYEE" | "NOOP";
  message: string;
  audit_note: string;
}

export interface RunLogEntry {
  scenario_id: string;
  agent: string;
  action: ActionType;
  env_result: EnvResult;
  safety_score: number;
  reasoning: string;
  timestamp: string;
}

export interface Payee {
  name: string;
  registered: true;
}

export interface AccountState {
  balance: number;
  payees: Payee[];
  txnHistory: EnvResult[];
  otpPending: boolean;
  actionsUsed: number;
  actionLimit: number;
}

export interface ChatTurn {
  role: "user" | "assistant";
  content: string;
}