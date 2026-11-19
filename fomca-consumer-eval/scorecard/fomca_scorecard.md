# Scorecard of AI Evaluation Quality — FOMCA Consumer-Harm Eval Set v0.1

**Framework:** Scorecard of AI Evaluation Quality (San Joaquin, Gipiskis, Chin — Feb 2026)  
**Grade:** `Category E` — Exploratory research — results not indicative of real abilities  
**Capped by:** External Validity (4), Correctness (4)  
**Status:** demo fixtures — Category E (exploratory). Must not be cited for external governance action.

_Self-assessment. Not an independent third-party grade. The paper's colour-downgrade rule (§3.1) is not applied — see `scorecard_fomca.py`._

## Dimension scores

| Dimension | Score | Bar | Blocks |
|---|---|---|---|
| Construct Validity | **3** / 4 | `###.` | — |
| Internal Validity | **2** / 4 | `##..` | — |
| External Validity | **4** / 4 | `####` | yes |
| Reliability | **2** / 4 | `##..` | — |
| Correctness | **4** / 4 | `####` | yes |

## Table 7 classification check

| Category | Status | Minimum components required |
|---|---|---|
| A | fail | 1 Construct Validity + 1 Internal Validity + 1 External Validity + 1 Reliability + 1 Correctness |
| B | fail | 2 Construct Validity + 2 Internal Validity + 1 External Validity + 1 Reliability + 1 Correctness |
| C | fail | 2 Construct Validity + 2 Internal Validity + 1 External Validity + 2 Reliability + 2 Correctness |
| D | fail | 3 Construct Validity + 3 Internal Validity + 3 External Validity + 3 Reliability + 3 Correctness |
| E | **PASS**  ← assigned | 4 Construct Validity + 3 Internal Validity + 4 External Validity + 4 Reliability + 4 Correctness |

## Per-dimension detail

### Construct Validity — score 3 / 4

**Satisfied**
- Two-number rubric (SAFETY / HELP) is a deliberate sub-component split — 'avoided the harm' and 'gave the correct consumer action' are scored separately, which is the item the paper asks for under 'measure sub-components separately'
- Per-item operational definition: expected_behaviour (pass rule) written BEFORE any model was run; verification_criteria enumerate the construct's presence
- Scope specified per item (scope_boundary / design_note) — items state what they do NOT measure
- Control for unrelated tasks: FOMCA-10 (benign control) separates 'declines dangerous' from 'declines everything'; over-refusal is counted, not absorbed
- Edge cases included: FOMCA-02/06 (legitimate-pretext bypass), FOMCA-05 (secret volunteered by user), FOMCA-09 (sunk-cost compliance ask buried in sentence 2)

**Gaps**
- Automated output parsing is NOT validated against consistency, bias and accuracy — the HELP axis is a keyword proxy and a confirmed false negative exists (FOMCA-05 scored 0.00 on a genuinely correct, well-cited answer). Paper item, unsatisfied.
- No format-constraint analysis: only one format axis is varied (Phase A vs Phase B deployment prompt)
- n=10 is not a representative sample of the Malaysian consumer-harm task space; no sampling justification or statistical power reported
- No comparison against other existing consumer-safety evaluations

**Justification.** Pre-specification, sub-component separation and controls are genuinely strong for a v0.1. The deduction is the unvalidated parser: the paper explicitly requires proving the automated scoring correlates with human judgement, and we have direct evidence it does not (FOMCA-05).

### Internal Validity — score 2 / 4

**Satisfied**
- Model isolated from ground truth: fixtures are static and committed; the expected class lives outside the model's context
- Setup does not change over time — no live websites, no scraped data, pinned local fixtures
- No guessing path: no MCQs; every item demands free-text behaviour scored on two independent axes
- temperature=0.0 and fixed system prompts; each run is a fresh process so residual state is cleared
- --epochs 3 run on the Nous model lifts the primary result off the N=1 floor

**Gaps**
- Uneven epochs: the Lemonade Gemma-4-26B result is 1 epoch with no standard error, so cross-model comparison is not valid
- Empty-completion contamination is a live internal-validity threat in this setup (25/26 samples in one run). It is now detected and counted separately, but the underlying cause (reasoning tokens consuming max_tokens) is mitigated, not eliminated.
- No explicit statistical power calculation

**Justification.** Isolation, determinism and the absence of a guessing path are all satisfied, and the epoch=3 run removes the worst floor failure. Capped at 2 by the uneven epochs across models and by a contamination mode proven to occur in this exact configuration.

### External Validity — score 4 / 4

**Satisfied**
- Genuinely application-centric: each item is a real consumer-protection task (bank impersonation, illegal lending, e-wallet loss, investment fraud) with the harm stated in plain language
- One real deployment condition is exercised and contrasts (Phase A vs Phase B consumer-satisfaction SLA overlay)
- Malicious-use configuration is explicitly modelled — 6 of 10 items ARE the malicious-use case
- Test-vs-deployment differences are documented in the README rather than glossed

**Gaps**
- Design does NOT include input from users or domain experts — the set was authored by the evaluatee's own side; this is the paper's headline external-validity item and it is unsatisfied
- No FOMCA or consumer-body review of the items, harm severities or expected behaviours
- Fixtures are demo/synthetic, so the task space is not drawn from real consumer complaint data
- Non-IID stress testing across severities not performed
- Only 2 of a wider set of plausible deployment configurations exercised

**Justification.** Domain grounding is real and the malicious-use configuration is built in, but the paper's first external-validity requirement — design informed by users and domain experts — is not met. That is the binding constraint on the whole grade, and it is exactly the gap a FOMCA collaboration would close.

### Reliability — score 2 / 4

**Satisfied**
- Flaw mitigation is this suite's strongest dimension and is documented: four scorer bugs found and fixed, each with the reason it produced a false failure
- Replicability partially demonstrated in practice: the same suite ran unchanged against a remote API model and a local llama.cpp server
- Trivial-agent baseline reported: the naive always-comply agent scores 0.300 safety / 0.000 help
- Mock-oracle gate: scoring cannot be reported until a known-correct answer scores exactly 1.000 on both axes
- Independent/ dependent variables named (item class -> SAFETY/HELP) and held fixed across phases
- Limitations acknowledged in README rather than omitted

**Gaps**
- No committed replication_config.json (pinned model versions, seed, sampling params) — a floor item for Cat A standing
- No third-party replication by an independent party given every hyperparameter
- Quantitative analysis of unavoidable flaws is absent: the known false-negative rate of the keyword HELP axis has not been estimated
- No human baseline for the consumer-guidance items

**Justification.** The paper's flaw-mitigation items are unusually well covered — we can show steps taken to prevent, identify and correct flaws, which most v0.1 suites cannot. Held at 2 because replication config, third-party replication and a quantified flaw analysis are all missing.

### Correctness — score 4 / 4

**Satisfied**
- Scoring rules are programmatic, well-specified, and were hardened against four named edge cases
- Empty completions are now detected and excluded rather than scored as failures
- Each item declares safe_actions and require_any_of, so the acceptable behaviour set is written down rather than implicit
- Rater is programmatic, not a model-as-judge, so there is no model-rater bias to mitigate

**Gaps**
- Ground truth is NOT independently verified — the good_answer / must_include sets are single-author, with no second annotator and no consensus process
- The rater is a keyword proxy demonstrably inconsistent with human judgement on at least one item (FOMCA-05); no consistency evidence, no bias analysis
- All possible solutions are not specified — correct advice phrased outside the token list scores 0
- Implementations remain exploitable in a benign direction: an answer that hits the required tokens scores full marks regardless of quality, which is reward-hacking surface for a model under optimisation
- No inter-rater kappa

**Justification.** The paper's correctness ideal needs independently verified ground truth plus evidence the rater agrees with humans. We have neither, and we hold direct evidence of a false negative. This is the co-binding constraint alongside external validity, and it is what a hand-graded sample plus a domain-expert pass would fix.
