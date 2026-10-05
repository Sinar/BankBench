# BankBench — funder impact one-liners (draft v1)

Early results, pilot-stage. Numbers pulled live from the repo (Cetavals Uni rater CSV,
TamperBank live export 2026-09-03). Draft only — nothing here has been sent anywhere.

## BankBench as a whole
BankBench-MY is a multilingual (EN / BM / Manglish) safety evaluation for Malaysian
banking-agent LLMs — does a banking chatbot leak OTPs/PII, process unauthorised
transfers, or follow phishing links when the conversation register shifts? Built on
Inspect AI under the Sinar fellowship. Live, bring-your-own-key: https://bankbench-sinar.pages.dev

## 1. The Uni strand (Cetavals Uni rater pilot — RKFF 0413 / IIUM)
24 raters completed the bilingual reliability-calibration module; mean module accuracy
was 3.9/10 and only 39% of trust judgements matched the correct reliability state
(mean 0.95 categories off) — the exact gap the module exists to close. After it, 4.5/5
called the module relevant and 4.46/5 said they would check citations, and 15/24 chose
"verify" on a fabricated-fatwa scenario.
Dashboard: https://bankbench-sinar.pages.dev/outreach/uni/rate-dashboard.html

## 2. The IDFR strand (diplomacy)
Chapter 5, "AI Safety and Operational Safeguards for Diplomacy", was delivered to the
IDFR book *AI: Innovating Diplomacy* (Sep 2026) — a six-section, from-principle-to-
practice chapter on making AI safe in daily statecraft, tying Malaysian safeguards to
Malaysia's ASEAN AI-safety agenda. (Book chapter — no public URL.)

## 3. The Consumer strand (public education)
A live bilingual (EN/BM) interactive scam-scenario demo plus one published consumer
explainer, with five more in progress — all built from the same eval findings, so the
public sees the same evidence the benchmark produces.
Demo: https://bankbench-sinar.pages.dev/public-education/interactive.html

## 4. The TamperBank pilot (BankBench core result)
3 low-cost open-weight models × 20 adversarial Malaysian banking-crime scenarios + 2
benign controls, live inference: ΔADVOCACY +9.5pp overall (GLM-5 and Kimi-K2.5 +14.3pp
each; DeepSeek-V4-Flash 0) — a compliance-SLA prompt overlay pushed low-cost models
toward harmful financial-crime facilitation. N=1 pilot, self-graded Cetavals D overall
(needs N≥3 to stand); reported as early signal, not a settled finding.
Site: https://bankbench-sinar.pages.dev · Code: https://github.com/Sinar/BankBench

---
### Flags before this leaves the building
- External/funder send: needs Sha's explicit go-ahead (never auto-sent).
- TamperBank findings reference BNM/RMiT obligations → route to @clo for a
  compliance-tier pass before any external use.
- "IDFR" chapter is a book contribution — check with the editors before quoting
  findings outside it.