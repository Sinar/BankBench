# BankBench Tamper Resistance Evaluation — Methodology

## Dataset Alignment

| Standard | Status | Notes |
|---|---|---|
| AgentBench | Methodology Align | Trajectory + outcome verification. Domain: Banking (not general). |
| Inspect Eval | Methodology Align | Follows Inspect `test.sh` → `reward.json` grading pattern. |
| BankBench | Domain-Specific | 20 scenarios derived from BNM RMiT, AML/CFT, Consumer Protection. |

## Task Format
- Schema: `task.toml` (Harbor v1.4)
- 20 scenarios across 5 categories:
  1. Direct Prompt Injection (1-4)
  2. Tool Tampering (5-8)
  3. Parameter Manipulation (9-12)
  4. Data Tampering & Exfiltration (13-16)
  5. Multi-Agent Collusion (17-20)
