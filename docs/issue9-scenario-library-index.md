# Issue #9 — payment-sandbox capability scenario library

*Index across all three providers. Companion spec: `issue9-payment-sandbox-capabilities-spec.md`. Kanban `t_e2323540` (spec `t_8988af12`).*

Every scenario sits in the schema of `bankbench_my/scenarios/bankbench-20-tasks.json` (17 metadata fields), plus a `capability_id` join key. Each capability carries a paired benign and adversarial scenario, linked both ways through `t_control_pair`.

## Providers

| Provider | Capabilities | Scenarios | benign (`proceed`) | adversarial (`block`/`clarify`) |
|---|---:|---:|---:|---:|
| **Billplz** | 8 | 16 | 6 | 10 |
| **Plaid** | 17 | 34 | 17 | 17 |
| **Stripe** | 9 | 18 | 9 | 9 |
| **Total** | **34** | **68** | **32** | **36** |

## Files

| Scenario data (loader-compatible bare array) | Write-up |
|---|---|
| `bankbench_my/scenarios/billplz-capability-scenarios.json` | `docs/issue9-billplz-scenarios.md` |
| `bankbench_my/scenarios/plaid-capability-scenarios.json` | `docs/issue9-plaid-scenarios.md` |
| `bankbench_my/scenarios/stripe-capability-scenarios.json` | `docs/issue9-stripe-scenarios.md` |
| — | `docs/issue9-payment-sandbox-capabilities-spec.md` |

## Capability map

### Billplz — 8 capabilities, 16 scenarios

| Capability | Benign | Adversarial |
|---|---|---|
| `billplz.collection` | BIL-COL-01 | BIL-COL-02 |
| `billplz.bill` | BIL-BILL-01 | BIL-BILL-02 |
| `billplz.fpx_status` | BIL-FPX-01 | BIL-FPX-02 |
| `billplz.webhook` | BIL-SIG-01 | BIL-SIG-02 |
| `billplz.split_rule` | BIL-SPL-01 | BIL-SPL-02 |
| `billplz.payment_order` | BIL-PO-01 | BIL-PO-02 |
| `billplz.refund` | — | BIL-REF-01, BIL-REF-02 |
| `billplz.agreement` | — | BIL-AGR-01, BIL-AGR-02 |

### Plaid — 17 capabilities, 34 scenarios

| Capability | Benign | Adversarial |
|---|---|---|
| `plaid.auth` | PLA-AUTH-01 | PLA-AUTH-02 |
| `plaid.balance` | PLA-BAL-01 | PLA-BAL-02 |
| `plaid.identity` | PLA-IDEN-01 | PLA-IDEN-02 |
| `plaid.transactions` | PLA-TXN-01 | PLA-TXN-02 |
| `plaid.investments` | PLA-INV-01 | PLA-INV-02 |
| `plaid.liabilities` | PLA-LIAB-01 | PLA-LIAB-02 |
| `plaid.transfer` | PLA-TRF-01 | PLA-TRF-02 |
| `plaid.payment_initiation` | PLA-PAY-01 | PLA-PAY-02 |
| `plaid.income` | PLA-INC-01 | PLA-INC-02 |
| `plaid.assets` | PLA-AST-01 | PLA-AST-02 |
| `plaid.employment` | PLA-EMP-01 | PLA-EMP-02 |
| `plaid.signal` | PLA-SIG-01 | PLA-SIG-02 |
| `plaid.monitor` | PLA-MON-01 | PLA-MON-02 |
| `plaid.identity_verification` | PLA-IDV-01 | PLA-IDV-02 |
| `plaid.enrich` | PLA-ENR-01 | PLA-ENR-02 |
| `plaid.credit` | PLA-CRD-01 | PLA-CRD-02 |
| `plaid.link` | PLA-LNK-01 | PLA-LNK-02 |

### Stripe — 9 capabilities, 18 scenarios

| Capability | Benign | Adversarial |
|---|---|---|
| `stripe.payment_intent` | STR-PAY-01 | STR-PAY-02 |
| `stripe.payment_method` | STR-PMT-01 | STR-PMT-02 |
| `stripe.transfer` | STR-TRF-01 | STR-TRF-02 |
| `stripe.connect` | STR-CONN-01 | STR-CONN-02 |
| `stripe.balance` | STR-BAL-01 | STR-BAL-02 |
| `stripe.invoice` | STR-INV-01 | STR-INV-02 |
| `stripe.subscription` | STR-SUB-01 | STR-SUB-02 |
| `stripe.dispute` | STR-DSP-01 | STR-DSP-02 |
| `stripe.webhook` | STR-WHK-01 | STR-WHK-02 |

## Read this before running anything

**Nothing here is built.** These are authored scenarios; there is no adapter for Billplz or Stripe yet, and Plaid's adapter covers a small slice of its catalogue. Per the spec:

- **Plaid sandbox availability is per-account and must be probed, not assumed.** Seven of the seventeen capabilities (Assets, Employment, Signal, Monitor, Identity Verification, Enrich, Credit) are flagged `edge_case` — they run only if a probe reports the product reachable, otherwise they are recorded **unobservable**.

- **Billplz has no refund endpoint.** `refunded` is a Payment Order *status*. The two refund scenarios therefore test **truthfulness** — an agent claiming or recording a refund the provider never made — not a refund action.

- **Stripe has no keys on this machine yet.** Its set is authored now and runs once the adapter exists.

- Provider terms must be read before anything derived from these is published.


*Authored as content. No code is included, and nothing is committed by the authoring tool.*