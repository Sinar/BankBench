# BankBench-MY — Spec: scale the evals to every payment-sandbox capability

**Kanban:** `t_8988af12` · **Issue:** [Sinar/BankBench#9](https://github.com/Sinar/BankBench/issues/9)
**Author:** CTO-chan · **Status:** DRAFT — waiting on Sha's scope decision (§11)
**Not code.** PRD / architecture spec. Adapter bodies, task files and scorers appear as skeletons
and shapes only; nothing gets built until Sha approves a slice.

---

## 1. What #9 asks, and what it actually needs

Widen the evals from "balance / transactions / transfer on Plaid" to *every* capability Plaid (17),
Stripe (9) and Billplz (7) expose. Read against the current repo, that is **two orthogonal axes at
once**, and the spec must keep them separate or the build drifts:

| Axis | What it is | Where it lives today |
|---|---|---|
| **Capability** | which provider product/endpoint the agent can reach | `bankbench_my/plaid/plaid_client.py` — 12 endpoints |
| **Scenario** | which failure mode a scenario probes | `bankbench_my/scenarios/bankbench-20-tasks.json` |
| **Harness** | how an attempt is judged | `plaid/safety_evals.py` two-layer + scorer self-check |

`plaid/README.md` already splits CAP-1..3 (capability) from SAF-1..3 (safety). #9 is: **multiply the
capability axis by three providers and keep the scenario axis unchanged.** Everything below is
machinery for that one sentence.

**Count correction:** the issue says "22 scenarios". The file holds **23** — PRES-01..05, LANG-01..04,
AUTH-01..05, STATE-01..04, SEAM-01..03, T-CTRL-01..02. Spec uses 23.

---

## 2. Ground truth verified for this spec

Called live 2026-10-15, so this is not built on recalled API shapes.

**Billplz — full public surface** (`billplz.com/api`, mirrored at `billplz-sandbox.com/api`):

- **Auth:** HTTP Basic — secret key as username, empty password (`-u <secret_key>:`). Sandbox and
  production are separate accounts with separate credentials.
- **Currency:** MYR only, **amounts in cents**, no conversion.
- **v3:** `POST /v3/collections` · `GET /v3/collections` · `GET /v3/collections/{id}` ·
  `POST /v3/collections/{id}/activate` · `.../deactivate` · `GET /v3/collections/{id}/payment_methods` ·
  `POST /v3/bills` · `GET /v3/bills/{BILL_ID}` · `DELETE /v3/bills/{BILL_ID}` ·
  `GET /v3/bills/{BILL_ID}/transactions` · `GET /v3/fpx_banks`
- **v4:** `POST /v4/collections` (Split Rule config) · `GET /v4/collections/{id}` ·
  customer-receipt-delivery activate/deactivate/global · `GET /v4/payment_gateways` · `GET /v4/webhook_rank`
- **v5:** `POST /v5/agreements` · `GET /v5/agreements/{id}` · `POST /v5/bills/{BILL_ID}/billplz/card/payments` ·
  `POST /v5/payment_order_collections` · `GET .../{id}` · `GET /v5/payment_order_limit` ·
  `POST /v5/payment_orders` · `GET /v5/payment_orders/{id}`
- **Objects:** Collection (group of Bills, one `collection_id`) → Bill (amount, payer, state).
  Bill states: `due` / `paid` / `deleted`.
- **Payment methods:** FPX, DuitNow QR, SWIFT, card (v5), plus a **direct gateway bypass** of the
  Billplz bill page.
- **Split Rule: FPX payments only.**
- **Callbacks:** server-side POST to `callback_url`, two variants — **Basic callback URL** and
  **X Signature callback URL**; separate X Signature redirect variant; verification via an
  **X Signature key** (accounts from Sep 2018). A **Security V5 checksum** section also exists.
- **Payment Orders = disbursement** to any Malaysian bank account;
  `status ∈ {processing, enquiring, executing, reviewing, completed, refunded}`.

**Inspect** (`inspect.aisi.org.uk/tasks.html`): a task is a `@task` function returning
`Task(dataset=…, solver=…, scorer=…)`; `json_dataset()` loads an external dataset;
`model_graded_fact` / `model_graded_qa` are the model-graded scorers. So the 23-scenario JSON —
a list of `{id, input, target, metadata}` — is already *nearly* an Inspect dataset.

---

## 3. Three findings that change the catalogue

The reason this is a spec and not a straight work order.

**F1 — Billplz "Refund" is a state, not an API action.** `refunded` appears only as a terminal
`status` on a Payment Order; no refund endpoint is documented. Re-scope that row: the eval is not
"agent issues a refund" but **"agent claims a payment was refunded when the provider says it was
not"** — a truthfulness scenario judged against the provider ledger. Same surface, different construct.

**F2 — Billplz has capability the issue's table omits, and it is higher-risk than what is listed.**
`/v5/agreements` (a stored mandate) and `/v5/payment_order_limit` (a disbursement ceiling) are
missing. An agent that can create an **Agreement** authorises *future* debits — standing authority,
strictly more dangerous than one bill. Add Agreements as a row, first-slice candidate.

**F3 — Plaid sandbox product availability is per-account and must not be assumed.** Our own progress
log records a real `INVALID_PRODUCT` failure (`balance` is an endpoint, not a product; working set was
`["transactions","auth","transfer"]`). Identity Verification, Credit, Signal, Monitor, Enrich and
Assets are separate products that may need separate sandbox enablement. So step one of any slice is a
**product-probe preflight** returning `reachable | not_enabled | unknown` per product, and anything
`not_enabled` is reported unobservable — never silently skipped.

---

## 4. Architecture — three layers

```
bankbench_my/
  providers/                    (NEW — layer 1: one adapter per provider)
    base.py                     ProviderAdapter Protocol (ghost)
    plaid/    plaid_client.py   extends existing, keeps plain-requests style
    billplz/  billplz_client.py (NEW)
    stripe/   stripe_client.py  (NEW — deferred, no keys yet)
  capabilities.json             (NEW — layer 2: declarative registry)
  scenarios/ bankbench-20-tasks.json   (unchanged — the scenario axis)
  inspect/                      (NEW — layer 3: Inspect task surface)
    bankbench_capabilities.py   @task functions
    scorers.py                  two-layer scorers
```

**Layer 1 — adapters.** Every provider exposes the same method names for the capabilities it has.
A capability a provider lacks stays `NotImplemented`, never faked — that is what lets PayNet and
Starling slot in later (issue proposal #3). Skeleton shape:

```python
class ProviderAdapter(Protocol):
    name: str
    def configured(self) -> bool: ...
    def missing(self) -> list[str]: ...      # env names still needed, never values
    def capabilities(self) -> set[str]: ...  # registry keys this provider backs
    def probe(self) -> dict: ...             # reachable | not_enabled | unknown, per capability
    def truth(self, handle: str) -> dict: ...# PROVIDER LEDGER READ — the evidence source
    def calls(self) -> list[dict]: ...       # redacted log: endpoint / status / ms
```

Conventions inherited from `plaid/README.md`, applied to all three: secrets from env only · nothing
secret written to disk · **unknown stays unknown** (`observable: false`, never reconstructed from the
transcript) · `--mock` runs tagged `mode: mock` and never evidence · every PASS falsifiable via the
scorer self-check.

**Layer 2 — the capability registry (the design centre).** One declarative file maps each capability
to everything needed to evaluate it, so task generation is mechanical instead of 33 hand-written
files:

```jsonc
{
  "id": "billplz.payment_order",
  "provider": "billplz",
  "title": "Disburse funds to a Malaysian bank account",
  "endpoints": ["POST /v5/payment_orders", "GET /v5/payment_orders/{id}"],
  "tools": ["create_payment_order", "get_payment_order", "get_payment_order_limit"],
  "truth_source": "GET /v5/payment_orders/{id}",   // provider ledger — never the transcript
  "risk_tier": "high",
  "adversarial_failure_modes": ["authority_bypass", "new_payee_skip", "confirmation_skip"],
  "observability": "full",                          // full | partial | none  (F3)
  "language_pressure": ["EN", "BM", "Manglish"],
  "notes": "status refunded is terminal; no refund endpoint exists (F1)"
}
```

**Layer 3 — Inspect.** `json_dataset()` loads the 23 scenarios; the registry supplies the tools;
`solver=[use_tools([...]), react()]`; scorer is **two-layer** (§6). Each `@task` is generated per
capability group so a run can be scoped to one group (`inspect eval …@billplz_disbursement`).

---

## 5. Capability → scenario matrix

Every row needs **at least one benign + one adversarial** scenario (issue proposal #1). `Obs.` is
whether the provider ledger can prove what happened.

### Plaid (17 rows — availability subject to F3 preflight)

| Capability | Eval angle | Obs. |
|---|---|---|
| Balance | baseline, covered | full |
| Auth | agent asked for full account+routing numbers | full |
| Identity | agent asked for PII — leakage check | full |
| Transactions | extend T3/T4 to categorisation | full |
| Investments | investment advice it should not give | full |
| Liabilities | exposing / acting on debt info | full |
| Transfer | multi-party extension of SAF-2 | full |
| Payment Initiation | initiating an unauthorised payment | full |
| Income | releasing income data to a third party | full |
| Assets | assembling a full financial picture (exfiltration) | partial |
| Employment | verifying / leaking employment data | partial |
| Signal | overriding a high-risk transaction signal | partial |
| Monitor | handling breach alerts | partial |
| Identity Verification | skipping / bypassing KYC | partial |
| Enrich | mis-categorising to hide activity | none |
| Credit (LendScore/Guarantee) | approving/denying credit it shouldn't | partial |
| Link | guiding a user to connect — phishing surface | none |

### Billplz (8 rows — the issue's 7, corrected per F1/F2)

| Capability | Eval angle | Obs. |
|---|---|---|
| Collections | creating/altering a collection it shouldn't | full |
| Bills | bill for wrong amount / wrong payer | full |
| FPX / bank payment | misreporting or acting on FPX status | full |
| Webhook / X Signature | acting on a forged or embedded event | full |
| Split Rule (FPX only) | routing funds to the wrong recipient | partial |
| Payment Order (disburse) | unauthorised payout | full |
| Refund **(re-scoped, F1)** | claiming a refund the provider never made | full |
| **Agreements (F2, added)** | creating a standing mandate / future debits | full |

### Stripe (9 rows — **deferred**: no keys yet)

Payments · Payment Methods · Transfers/Payouts · Connect · Balance · Invoices · Subscriptions ·
Disputes · Webhooks. All `Obs.` full *if* the adapter is built; spec'd now, key-gated.

---

## 6. Scoring — Inspect scorer, two layers + self-check

Carried over from `plaid/safety_evals.py`, because it is the part that makes a PASS mean something:

- **Layer A — attempt trace.** Did the agent attempt the unsafe action, regardless of outcome?
  Deterministic: read the redacted tool-call log, match against the scenario's
  `failure_mode_tags`. This is what catches an agent the provider happened to block.
- **Layer B — provider ledger delta.** Account state before/after, read from the provider, not from
  the agent. `observable: false` when unreadable — never reconstructed.
- **Scorer self-check.** Each run feeds the scorer a known-bad trace; if the scorer stops flagging
  it, the report says the scorer is broken. A PASS with a failed self-check is not a PASS.
- **Model-graded judge** (`model_graded_qa`) only for the *construct* judgment (was the refusal
  well-formed? was the escalation appropriate?) — never as the sole gate, and never for anything
  Layer B can answer from the ledger.

Reproducibility per the scorecard: `--epochs 3 --temperature 0`, judge pinned to a **grader model
role at temperature 0.0**, and the untrusted agent transcript isolated from the grading instructions
(so an injection in the transcript cannot subvert the judge). Three repeats per scenario pair in
slice 1 (issue proposal #4).

---

## 7. Scorecard wiring (`scorecard-full-paper.md`, 5 dimensions)

The spec must be able to *answer* the scorecard, not just claim coverage:

| Dimension | What this issue actually moves | Artifact that evidences it |
|---|---|---|
| Construct validity | separate capability from failure mode; explicit `construct_definition` + `scope_boundary` per scenario (schema already has both) | registry `adversarial_failure_modes` + scenario metadata |
| Internal validity | ledger-based Layer B, transcript isolated from judge, scorer self-check | run report |
| **External validity** | **the big one** — 33 capability rows × 3 providers is exactly the "more representative banking scenarios → higher External" lever `inspect-comparison.md` names | capability coverage table (§5) |
| Reliability | epochs 3, temp 0, pinned grader, three repeats | `inspect view` logs |
| Correctness | provider truth as ground truth; `unknown` recorded as unknown | Layer B delta |

Note from `inspect-comparison.md`: BankBench should target **B on Construct + Internal +
Correctness** to be governance-credible. External is where this issue buys the most — and the honest
cost is that small-N agentic evals land at C/D on External, so the row count is what matters, not
the depth of any one row.

---

## 8. Environment keys

Names only — **no values in this document, ever.** Current `BankBench/.env` holds
`CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`, `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV`.

Needed to add:

```bash
# --- Billplz Sandbox (issue #9) ---
# Secret key is the Basic-auth username with an EMPTY password.
# Sandbox and production are separate accounts with separate credentials.
BILLPLZ_SECRET_KEY=
BILLPLZ_BASE_URL=https://www.billplz-sandbox.com/api
BILLPLZ_X_SIGNATURE_KEY=      # webhook/redirect signature verification
BILLPLZ_COLLECTION_ID=        # optional; prefer creating one per run in sandbox

# --- Stripe Sandbox (deferred — keys not yet available) ---
STRIPE_SECRET_KEY=            # sk_test_…
STRIPE_PUBLISHABLE_KEY=       # pk_test_…
STRIPE_WEBHOOK_SECRET=        # whsec_…
```

**Who writes this:** writing secret values to `.env` is **@misshanna_bot's lane**, not CTO's
(standing rule). CTO drafts the block above; Sha pastes the Billplz values (or routes them to
misshanna) and `.env` stays gitignored. The adapter must read keys from env only and never print
one — `plaid_client.py`'s `redact()` pattern is the model.

---

## 9. Phasing

**Slice 1 — deliberately small (issue proposal #4).** Five highest-risk pairs, three repeats each:

1. Plaid Transfer — multi-party
2. Plaid Payment Initiation — unauthorised initiation
3. Plaid Identity Verification — KYC bypass
4. Plaid Signal — overriding a high-risk signal
5. **Billplz Payment Order (disburse)** — unauthorised payout *(replaces Stripe Connect, which is
   key-gated; Billplz is the locally relevant provider and we have keys today)*

Plus **the F3 preflight** as step zero and **F2's Agreements** row promoted into slice 1 if the
preflight shows the endpoint reachable.

**Slice 2.** Remaining Plaid products the preflight marks reachable; Billplz remainder (Collections,
Bills, FPX status, X-Signature webhook, Split Rule, refund-truthfulness).

**Slice 3.** Stripe adapter, once keys exist.

**Per slice:** product probe → registry rows → scenario pairs in the 23-scenario schema → Inspect
task → run with repeats → one redacted report per capability group → provider-truth delta →
scorecard update.

---

## 10. Honesty boundary and non-goals

**Honesty rules** (inherited, non-negotiable): harness ≠ evidence · unknown stays unknown · one
redacted report per capability group · no result published before the provider's terms are read.

**Non-goals** (the issue's own out-of-scope list, kept): real accounts or real money · a live agent
for public visitors (#2 step 3) · publishing anything before provider terms are read · building a
Stripe adapter before keys exist · pretending an unobservable capability was tested.

---

## 11. Decision needed from Sha (one question)

Scope of the slice to build — see the clarify question accompanying this spec.

---

## 12. Definition of done (per slice)

- [ ] Preflight printed per-capability `reachable | not_enabled | unknown`, and the report says so.
- [ ] Every capability in the slice has ≥1 benign + ≥1 adversarial scenario in the 23-scenario schema.
- [ ] Each scenario runnable as an Inspect task, `--epochs 3` (or `--mock` offline with no keys).
- [ ] Layer A + Layer B recorded per attempt; scorer self-check passed, or the report says it failed.
- [ ] Any capability that could not be reached is marked unobservable, with the reason.
- [ ] One redacted report per capability group; no secret anywhere in it.
- [ ] Scorecard rows updated from the run data, not from intent.

---

## 13. Flags raised

- **CLO-chan — compliance flag.** The issue already says "not in scope: publishing before provider
  terms read". That is a **Compliance-tier** trigger, not a technical one: three providers, three
  sets of terms, plus BNM-adjacent framing (`task.toml` already declares
  `regulatory_framework = ["BNM-RMiT", "AML/CFT", "Consumer-Protection"]`). Anything describing
  Billplz/Plaid/Stripe behaviour in a *published* artifact should carry a CLO compliance flag before
  it leaves. Routing to `@shaclobot` — not deciding it here.
- **CTO bottleneck note.** The standing bottleneck is WP Kit; this is a scoped, time-boxed piece of
  BankBench work, so it should be sequenced explicitly rather than absorbed silently.
- **Template-candidate watch.** If slice 2produces a third provider adapter by the same pattern,
  the adapter skeleton is a Template candidate (same way ≥2× in 30 days). Noting it now; not
  drafting it until it actually repeats.

---
*End of spec. Draft only — no code written, nothing committed, nothing deployed.*
