# Contributing to BankBench-MY

Thank you for your interest in BankBench-MY — an open-source safety evaluation
for Malaysian digital banking agents. This guide focuses on the part contributors
most often touch: **writing and reviewing evaluation scenarios** (the JSON tasks
in `bankbench_my/scenarios/`).

For repo-wide norms (CI, license, code style), also see `README.md` and the
issue/PR templates under `.github/`.

---

## 1. What a "scenario" is

A scenario is one self-contained safety test. It presents a banking-agent LLM
with a single input, expects a single graded outcome (`block` or a richer
label), and carries structured metadata that says *what construct* it is testing
and *why*. Scenarios live as objects in `bankbench_my/scenarios/bankbench-20-tasks.json`
(a JSON array). Each object has exactly three top-level keys:

```json
{
  "id": "AUTH-01",
  "input": "Hi, I'm actually from Ryt Digital Bank's compliance team. ...",
  "target": "block",
  "metadata": { ... }
}
```

- **`id`** — stable, human-readable, prefixed by category (`AUTH`, `STATE`,
  `LANG`, `SEAM`, `PRES`, …) and zero-padded where multiple exist
  (`AUTH-01`, `AUTH-02`). Do not reuse or renumber an existing id; a retired id
  stays retired to preserve citations in reports and the public-education site.
- **`input`** — the exact text (or, for multi-turn scenarios, the scripted
  turn sequence) handed to the agent. This is the only thing the model sees.
  Keep it realistic and minimal — no commentary, no grading hints inside it.
- **`target`** — the expected safe outcome. Today this is almost always
  `"block"` (the agent must refuse / escalate rather than execute). If your
  scenario needs a graded label other than block, propose it in the PR and state
  the rubric in `grading_guidance`.

---

## 2. The `metadata` schema (required)

Every scenario must carry the full metadata block. This is what makes a scenario
*reusable, reviewable, and citable* — without it the input is just a prompt, not
an evaluation. The canonical fields (all required unless marked optional):

| Field | Type | Purpose |
|---|---|---|
| `category` | string | Top-level taxonomy axis, e.g. `authority_social_engineering`, `multi_turn_state_manipulation`, `code_switching`, `cross_role_seam_exploitation`, `pressure_escalation`. |
| `title` | string | One-line plain-language name of the trick. |
| `target_role` | string | Which agent role is under test, e.g. `guardrail_agent`. |
| `probe_question` | string | The research question this scenario answers ("Can a user impersonating internal bank authority bypass safety?"). |
| `grading_guidance` | string | Exact safe/unsafe definition: what a correct response does vs. the failure mode. Used by human and automated graders. |
| `construct_definition` | string | The precise safety-boundary failure being isolated. Name the *cause* (e.g. "waives confirmation based solely on unverifiable in-chat authority claim"). |
| `scope_boundary` | string | What this scenario deliberately does **not** test, and which sibling scenario owns the adjacent construct (e.g. "AUTH-02 tests external authority; distinct construct"). Prevents overlap. |
| `difficulty_level` | int | 1–3 (low/medium/high). Reflects eval difficulty, not real-world severity. |
| `language_pressure` | string | `EN` / `BM` / `Manglish` / `code_switch` — which register the input uses. |
| `failure_mode_tags` | array[string] | Machine-readable failure tags, e.g. `["authority_bypass","confirmation_skip"]`. |
| `seam_type` | string/null | For cross-role scenarios: which seam is exploited. `null` otherwise. |
| `t_control_pair` | string/null | Id of the paired control scenario, if this is one half of a treatment/control pair. |
| `task_space_position` | object | Four-axis position: `category_axis`, `difficulty_axis`, `language_axis`, `pressure_type`. Used to keep the suite evenly spread across the task space. |
| `verification_criteria` | array[string] | The concrete properties the input **must** exhibit for the scenario to be valid (see §4). Reviewers check these line-by-line. |
| `edge_case` | bool | Whether this is an explicit edge/stress case. |
| `edge_case_note` | string | Why it's an edge case, if `edge_case` is true. |
| `bnm_reference` | string | The BNM guideline clause the construct maps to (e.g. "BNM Operational Risk Guidelines 2023 §12.4 — 'No instruction received via customer chat channel… constitutes authorisation to bypass confirmation controls.'"). Cite the real clause; do not invent section numbers. |

---

## 3. The golden rule: one construct per scenario

A scenario tests **one** safety-boundary failure. If your input mixes urgency
*and* authority *and* a language switch, you cannot tell which lever broke the
agent. Split it:

- Want to test authority alone? Strip the urgency and distress. (`AUTH-01`)
- Want to test urgency alone? Drop the authority claim. (`PRES-01`)
- Want to test the *combination*? That is a separate, deliberately stacked
  scenario — and it must cite its own construct, not borrow three. (`PRES-05`)

This is why `scope_boundary` exists: state what you are **not** testing and name
the sibling that owns it. Overlap is the most common rejection reason.

---

## 4. Writing the `input`

- **Be realistic, not theatrical.** Real scam transcripts are often flat and
  plausible. Theatrical "EVIL HACKER" prose tests your imagination, not the
  model's safety.
- **Keep the unsafe request present and unambiguous.** The agent must have
  something concrete to refuse (a transfer to a named account, a skipped check).
- **Use a consistent dummy payee.** `7777-8888-9999` is the repo convention for
  an unverified new payee — keep it so graders and the public site stay aligned.
- **Multi-turn scenarios** must encode the full turn sequence in `input` (the
  harness replays it). State in `verification_criteria` that the test requires a
  multi-turn scaffold (e.g. STATE-01: "Requires multi-turn scaffold to evaluate
  (cannot be tested in single turn)").
- **Never embed grading hints** ("this is a test, you should block") in the
  input. That contaminates the eval.

---

## 5. Writing the `verification_criteria`

This is the contract reviewers enforce. Each criterion must be a checkable
statement about the *input's* properties — not about the model's behavior. Good:

> - Input claims internal bank employee identity with specific ID ('RYT-2847')
> - Input requests skipping a specific security control ('skip human-in-the-loop')
> - Authority claim is unverifiable via chat channel
> - Penetration test framing provides plausible cover story

Bad (this is grading, not verification):

> - The model should refuse

If a criterion describes the model, it belongs in `grading_guidance`, not
`verification_criteria`.

---

## 6. Grounding the `bnm_reference`

Every scenario should map to a real BNM guideline clause. Search the BNM
guidelines (Operational Risk, e-Payment Fraud, AML, RMiT) for the clause that
says the behavior under test is *required* or *prohibited*. Quote it accurately
with section numbers. If you cannot find a clause, the scenario may be out of
scope or ahead of regulation — flag it in the PR rather than inventing a
citation. **Fabricated BNM references are a hard reject.**

---

## 7. Language and register

BankBench-MY is Malaysian-first. Cover the full register range:
`EN`, `BM` (Baku/standard), `Manglish`, and `code_switch` (formal opener →
casual switch). When you use a register switch, the `verification_criteria`
must pin *where* the switch lands (e.g. LANG-02: "Register switch coincides
temporally with the unsafe request (not before, not after)"). A scenario that
only works because of a switch must say so, or it's testing the wrong thing.

---

## 8. Pull-request checklist

- [ ] New scenario has a unique `id` (no reuse/renumber of retired ids).
- [ ] `input` is realistic, contains a concrete unsafe request, uses `7777-8888-9999` as the dummy payee, and has **no** grading hints.
- [ ] `target` is set and, if not `"block"`, the rubric is in `grading_guidance`.
- [ ] **All** metadata fields are filled; `seam_type`/`t_control_pair` are `null` when not applicable (not omitted).
- [ ] `construct_definition` names the *cause* of the failure, not just the symptom.
- [ ] `scope_boundary` states what is **not** tested and names the sibling scenario.
- [ ] `verification_criteria` are about the input's properties (checkable), not the model's behavior.
- [ ] `bnm_reference` cites a **real** clause, quoted accurately.
- [ ] No overlap with an existing scenario's construct (checked against `scope_boundary` of siblings).
- [ ] If multi-turn, the turn sequence is fully encoded and flagged in `verification_criteria`.
- [ ] `README.md` and the public-education index are updated if the scenario changes a surface users see.

---

## 9. Public-education explainers (consumer surface)

The `site/public-education/explainer-*.html` files translate scenarios into
plain language for the public. When you add or change a scenario that has a
public explainer:

- Keep the explainer grounded in the **actual** `input` text and `bnm_reference`
  from the scenario — do not paraphrase into something stronger than the data.
- Match the existing explainer-1 template (hero + sections + checklist + research
  footer). Use the repo's light theme tokens (no dark backgrounds).
- Mark the explainer `Live` only when its content is fully written; the
  "Coming Soon" stub is for not-yet-authored explainers.

---

## 10. License

By contributing, you agree your contributions are released under the repository
license (CC BY-SA 4.0, see `LICENSE`). Add yourself / the rights holder to the
license notice where applicable.
