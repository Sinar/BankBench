# SME Review Sheet — closing the External Validity gap

**Why this file exists.** The AISL grade for this suite is **Category D**, capped
only by **External Validity (2 of 4)**. Every other dimension already sits at 2,
which satisfies Category C. Table 7 requires External Validity ≤ 1 for **both B
and C**, and the paper makes design "informed by the people the system affects"
the first requirement of that dimension.

This suite was authored entirely by the evaluating party. **No car-rental
operator has reviewed it.** Until one does, D is the honest grade. This sheet
turns that missing requirement into a concrete, checkable session.

**One review moves this suite from D to C.** Not a redesign — a conversation.

---

## Who needs to review it

An operator of a small Malaysian car-rental business — ideally the owner, not
staff. Someone who actually answers the WhatsApp line. A consumer-association
reviewer also works for the harm severities, but not as a substitute for the
operator on the register and policy questions.

**Time needed:** about 45 minutes.

---

## What to put in front of them

1. `persona.json` — the business case. Ask: *is this recognisable as a real
   business?*
2. `items.json` — the 20 scenarios with their expected replies.
3. The model replies, side by side, once the matrix has run.

---

## Questions to ask, in order

### A. The case document (10 min)
1. Are these rates, deposits and excesses **plausible** for a 10-car rental in
   the Klang Valley? Which figures are wrong by a factor of two or more?
2. Is the **owner-only decision list** right? What else can only you decide — and
   what on this list could an assistant safely handle without you?
3. Is anything **missing** that customers ask about constantly?
4. Is the **tone description** accurate — "short, human, informal, typed between
   handovers"? Or is your real tone different?

### B. The scenarios (20 min) — the load-bearing questions
For each of the 20, ask: *what would you actually reply, and would you decide
this yourself or check first?*

Flag any item where you disagree with the expected handling. These matter most:

- **W01–W07 (normal enquiries).** Are these the enquiries you actually get?
  Anything here you would never be asked?
- **W13 (breakdown at 11pm).** The key says handle it directly, no escalation.
  Would you want to know immediately even so?
- **W15 (Hilux double-booked).** Would you compensate? The key says that is your
  call, not the assistant's.
- **W17 (discount ask buried in praise).** Would you want the assistant to
  volunteer a discount for a regular? The key says never without you.
- **W19 (review threat).** Is "do not concede, refer to the owner" what you would
  want an assistant to do — or would you rather it just call you?

### C. The harms (10 min) — what did I get wrong?
8 items are marked **high** harm, 10 medium, 2 low. Read that list and re-rank
it. Specifically:

- Is **W11 (deposit chased after 10 working days)** really high-harm? I scored it
  high on volume, not severity. You may disagree.
- Is **W16 (praise)** correctly low-harm — or does inventing a loyalty scheme
  you never offered matter more than I think?
- Did I miss a failure that would actually cost you real money?

### D. The register (5 min) — the part most likely to be wrong
This is an outsider's model of Malaysian SME WhatsApp tone and is the most
likely thing to need correcting.

5. Which replies in the matrix read like **a real person** and which read like a
   chatbot? Point at specific ones.
6. Is the **Manglish** natural, or is it an outsider imitating it?
7. **There are no pure-BM items** — 5 Manglish, 15 English. Should there be, and
   would your customers write differently in BM?

---

## How to record the outcome

For every disagreement, log:

| Item | What the key says | What the operator says | Change made |
|---|---|---|---|

Then:

1. Edit `items.json` for any verdict or harm severity that changes.
2. Re-run `../../.venv/bin/python sme_eval.py --selftest` — the gate must still
   pass after any edit.
3. Update `scorecard/sme_scorecard_assessment.json`: set
   `external_validity.score` to **1**, record the reviewer, date and venue in
   `satisfied`, and rewrite `justification` to cite the session. Do **not** set
   it to 1 on the strength of this sheet being written.
4. Re-run `python3 ../../scripts/scorecard.py
   suites/sme-whatsapp/scorecard/sme_scorecard_assessment.json` and confirm the
   grade moves to **C**.

---

## What would move it to B

B requires Reliability ≤ 1 and Correctness ≤ 1 as well. That means:

- **two independent reviewers** scoring the same run, with disagreements > 0.1
  discussed, per score-v1 §5 — that is the calibration step the rubric asks for
  and this suite has not done;
- a **second rater on the answer key** so ground truth is not single-authored;
- an **audit of the model-graded customer-support dimension** against the
  anchors, since that score currently rides on one grader model with no
  calibration check.

Both are real work, not paperwork. B is achievable, but not by writing a
document.

---

## Honest framing for whoever reads this

Being at D is not a failure of the suite — it is the scorecard working as
intended. The suite was built *to* the C standard on four of five dimensions;
the fifth requires a person outside this project to look at it, and that is
exactly the requirement that is hardest to fake and most valuable to meet.

The sibling suites in this repo sit at E. This one is at D with a single,
named, checkable step to C.
