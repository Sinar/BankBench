# No Safety Card, No Problem? What to Do When Your Open-Weight Model Ships Without One

*An AI safety guidance article for public education — practitioners, policymakers, and the people who procure AI. Draft v1, based on the AI Lab Watch scorecard lens (ailabwatch.org).*

---

## The situation

Your organisation has adopted an open-weight language model. Perhaps it is a translation engine, a drafting assistant for a mission or ministry, a document-summariser for a bank's compliance team, or the reasoning core of a customer-facing agent. The model is capable, cheap, and yours to control.

You look for the safety card — the document that tells you what the model can do, what it was tested for, and where it is known to fail. You find nothing. No risk assessment. No evaluation results. No list of dangerous capabilities probed. Sometimes, no documentation at all.

This article is written for the people who will encounter exactly this moment — in government agencies, financial institutions, diplomatic services, and mid-size companies — and who are not sure what the absence of a safety card should mean, or what to do next.

The short answer: **a missing safety card is not a green light. It is a red flag that you must process manually.** The good news is that a red flag can be handled with a process — and the process is cheaper and more public than most people realise.

---

## Context: the standard everyone assumes

For frontier models, the safety documentation convention has become more visible — and contested. The AI Lab Watch initiative collects safety recommendations for frontier AI companies and scores the companies' performance against them (Stein-Perlman, AI Lab Watch). Its scorecard tracks categories such as risk assessment, misuse prevention, scheming-risk prevention, extreme-security preparation, and risk information sharing; as of the September 2025 snapshot, the top-scoring company scored 28 per cent overall (ailabwatch.org). The site now carries a notice that it stopped being maintained in September 2025, and points readers to follow-on work by METR, Guidelight, and Midas.

The point for a procurer of open-weight models is not the scores — it is the *expectation* the scorecard encodes: a responsible AI release tells you what it assessed, and how. When a model publisher ships no such documentation, the safety burden does not disappear. It moves to you.

Aligned national guidance says the same. The NIST AI Risk Management Framework treats Govern and Map as the first functions of responsible use: before you rely on a system, you should know the context of its use, its capabilities, and its limits (National Institute of Standards and Technology, 2023). A model without a safety card does not fail NIST — *your organisation fails NIST if it adopts the model without asking what the card would have said.*

---

## Why open-weight models need scrutiny more, not less

It is tempting to relax because the model is open. You can see the weights. You can run it yourself. Surely that is safer?

It is not. Open weights change the risk profile in two important ways:

1. **Anyone can fine-tune.** A safety card that describes the model *as released* tells you little about the model *after fine-tuning*. TamperBench shows that safety training can be systematically undone with fine-tuning, and that evaluation must distinguish capabilities that are genuinely absent from those that are merely suppressed and easily re-elicited (Hossain et al., 2026). Recent estimates of worst-case risks for open-weight models reach the same conclusion: post-training can restore or amplify capabilities the release-time evaluation did not surface (Wallace et al., 2026).

2. **The deployer is the operator.** With a frontier API, the provider retains responsibility for updates, monitoring, and incident response. With an open-weight model, your organisation becomes the operator. If nothing documented the model's failure modes, you will only learn them in production.

This is the gap a missing safety card leaves open: the model's *known* risks were never written down, and its *worst-case* risks — what a motivated user with fine-tuning compute could re-elicit — are exactly what card-less releases leave unaddressed.

---

## What a good safety card actually contains

If the card is missing, the first task is to know what you are missing. Based on the categories of the AI Lab Watch scorecard and the capability-evaluation literature, a useful safety card for an open-weight model answers at least:

| The card should say | The question behind it |
| -- | -- |
| What the model was trained on and how | Can the data explain its biases and limits? |
| What capabilities were evaluated | Were dangerous capabilities probed at all? |
| What failure modes were found | Hallucination, bias, calibration, refusal gaps |
| How evaluation was run | Reproducible configs, test sets, inter-rater checks |
| What known harms are possible | Misuse vectors; which categories were tested |
| What the release-time risk assessment judged | And what it *didn't* test |
| How to report an incident | Named channel, response expectations |

The AI Lab Watch scorecard also tracks categories that a card-less release almost certainly ignores — preparedness for extreme security, planning and monitoring — but for most open-weight adopters the non-negotiables are the first four rows: *capabilities tested, failure modes found, reproducible evaluation, and a reporting channel.*

---

## What to do, in order

### 1. Treat the absence as a documented finding
Do not silently proceed. Open an entry in your risk register: *model X adopted without a safety card; capability and failure-mode profile unknown.* The finding itself changes the risk tier you assign to the use case (tier design follows your existing guidelines — see Chapter 5 of the guidance series for the four-layer classification).

### 2. Run your own lightweight evaluation battery
You do not need a lab. Free, maintained, open-source tooling — for example the Garak vulnerability scanner and Microsoft's PyRIT red-teaming framework — lets a small team probe the model for jailbreaks, prompt injection, and refusal degradation at near-zero cost. This gives you a *model-layer* baseline the publisher never supplied.

### 3. Probe the capabilities that matter to *your* domain
A translation model for diplomatic cables and a summariser for financial-crime analysts have different danger surfaces. Define 10–20 domain-specific scenarios — patterns relevant to your sector (in banking: structuring guidance, identity fabrication, reporting evasion; in diplomacy: impersonation, misinformation, prompt injection) — and test the model against them. You are not red-teaming the whole model; you are red-teaming *your* use of it.

### 4. Test tamper-resistance with a small fine-tuning sweep
Because open weights mean anyone can fine-tune, run a small sweep yourself: take the model, fine-tune it on plausible training material (even a few hundred examples), and re-run the domain probes from step 3. The question is not whether it is useful after fine-tuning — it is **which harmful capabilities return, and how quickly**. This is the marginal-risk measurement the research literature is just beginning to formalise (Hossain et al., 2026; Wallace et al., 2026).

### 5. Write your own mini safety case — the "supplement card"
You cannot reconstruct the publisher's card, but you can write a use-case supplement: what the model will be used for, what you tested, what you found, what is prohibited, who reviews output, and what happens when it fails. This converts "no card" from an unmanaged gap into a documented residual risk that a reviewer can see and sign.

### 6. Connect to the incident path
Add the model to your escalation and incident-response routine — the same path you would use for any failure: detect, contain, escalate, communicate, document, learn. A card-less model is more likely to fail in surprising ways, so the reporting channel matters more, not less. (The CSET work on AI-incident reporting components is a useful template for what the record should contain.)

### 7. Where you can, demand disclosure
On the procurement side: make the request for a safety card a standard question in vendor and model-publisher meetings. The answer — a card, a promise to publish one, or a refusal — is information. Over time, repeated demand from public-sector buyers is how a documentation norm becomes an industry default; this is the soft-law route that model cards followed, and that a "fine-tune disclosure profile" could follow next.

---

## What policymakers can do with this

The policy bridge is three steps:

1. **Require disclosure as a condition of public procurement.** Ministries and regulators do not need new criminal law to change behaviour; they need a procurement rule: *open-weight models used in public service must carry a capability-and-evaluation disclosure.*
2. **Ask for incident reporting, not just release notes.** If the risk is what happens *after* fine-tuning, the reporting hook should be the incident, not the launch.
3. **Fund the norm and the tools.** Open-source evaluation and red-teaming tooling, benchmark suites like the finance-domain tamper suite, and independent scorecards are public goods. A small public investment moves the burden of proof from individual adopters to publishers — which is exactly the direction the AI Lab Watch tradition argues for.

---

## The bottom line

A missing safety card is not a technicality, and it is not a reason to abandon the model either. It is a transfer of responsibility: the publisher did not do the assessment, so the deployer must. With a documented finding, a lightweight evaluation battery, a domain-specific probe, a small tamper sweep, and a written supplement card, an organisation can run the assessment itself — and, in doing so, start to set the expectation that publishers should publish the card in the first place.

---

## Sources and notes (verified)

- AI Lab Watch (Zach Stein-Perlman). Scorecard of frontier-lab safety practice; site notice confirms maintenance stopped September 2025, redirecting to METR, Guidelight, Midas. https://ailabwatch.org/ (accessed and quoted via live fetch; no model-card content found on the homepage).
- Hossain et al. (2026). *TamperBench: Systematically Stress-Testing LLM Safety under Fine-Tuning and Tampering.* arXiv:2602.06911.
- Wallace et al. (2026). *Estimating Worst-Case Frontier Risks of Open-Weight LLMs.* arXiv:2508.03153.
- National Institute of Standards and Technology. (2023). *AI Risk Management Framework (AI RMF 1.0)*.
- CSET. *AI Incidents: Key Components for a Mandatory Reporting Regime.* Georgetown University.
- Garak (NVIDIA/open-source) and PyRIT (Microsoft/open-source): red-teaming and vulnerability-scanning toolkits.
- Model-card convention popularised via Hugging Face documentation; draft status: the "fine-tune disclosure profile" under step 7 is a proposal of this article, not an existing standard.

*Draft v1 — dates/byline/publishing target TBD. British English; guidebook tone for non-technical readers. Not legal or procurement advice.*
