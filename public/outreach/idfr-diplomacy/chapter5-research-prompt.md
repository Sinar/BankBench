# Research Prompt — Chapter 5: *AI Safety and Operational Safeguards for Diplomacy*

> **How to use this file (three-tool pipeline):** This is the governing brief for Chapter 5. It feeds three tools in sequence — do **not** paste the whole file into one model:
> - **Perplexity — wider research narrative / chapter discovery.** Use Perplexity to build the broader research narrative and to surface material that may justify *new* sub-sections or chapters (e.g. the diplomatic risk taxonomy, sandbox transgression, compute/hardware governance, the four-layer spine). Perplexity findings are folded back into `book-toc.md` and into the scope block below before drafting. Perplexity is *research only* — it does not draft the chapter.
> - **Inkling (in Hermes) — drafting + GDrive sync.** Paste **THE PROMPT** block (below) into Inkling. Inkling drafts the chapter and **auto-syncs the live draft to the project Google Drive** (the **/CHAPTER 5** folder). Keep British English on. The source-file links here are for *you* (the human editor), not the model — attach the actual files / point Inkling at the GDrive corpus when prompting.
> - **Claude — evaluation.** After Inkling produces a draft, run the **EVALUATION PROMPT (for Claude)** block (bottom of this file) to score the draft against every requirement here. Iterate in Inkling, re-evaluate in Claude, until all checks pass.
>
> **Source files (attach / point Inkling at the GDrive corpus):**
> - **Defined corpus (mandatory primary pool)** → `gdrive_pdf_index.md` — all PDFs defined for this project, including the **/CHAPTER 5** folder (operational AI-safety literature: Shevlane 2023, Ganguli 2022, NIST AI RMF 1.0, Sidhu & Scholefield 2026 incident governance; OWASP Gen AI Top 10). **Use these first.**
> - Voice & style anchor → `datalab-output-IDFR_Book-From_Hate_to_HOPE.pdf.md` (text extraction of Dr Murni Wan Mohd Nor's *From Hate to Hope*).
> - Chapter structure → `book-toc.md` (Chapter 5 scope + its embedded literature list with URLs).
> - Exemplar voice already approved → `book-draft.md` (Chapters 1–3 as written).
> - Base rules → `chapter-prompt.md` (this prompt is a Chapter-5-specific refinement of it; **all** its instructions — British English, Hate-to-Hope voice/format, GDrive/Docx output, source-integration, diversity, APA-7, endnotes, quality bar — are now embedded directly inside **THE PROMPT** below, so pasting that block alone into Inkling is sufficient).

---

## Chapter 5 scope (from `book-toc.md`)

**Title:** *AI Safety and Operational Safeguards for Diplomacy*
**Framing:** Malaysia's emerging role in ASEAN AI safety · Distinguishing AI safety from cybersecurity and information security.

- **5.1** AI Risk Assessment & Classification for Diplomatic Use Cases
  - **Contribution (AI safety):** apply a structured AI risk taxonomy / likelihood–severity framing, plus a graduated safety-tier model (e.g., admin support → analysis → negotiation/decision support).
    - Bengio, Y. et al. (2024). "Managing Extreme AI Risks amid Rapid Progress." *Science*, 384(6698), 842–845. https://www.science.org/doi/10.1126/science.adn0117
    - NIST (2023). *AI Risk Management Framework (AI RMF 1.0)*. https://www.nist.gov/itl/ai-risk-management-framework
    - EU AI Act (2024) — risk-tier classification (unacceptable/high/limited/minimal risk). https://artificialintelligenceact.eu/the-act/
    - Reuel, A., Bucknall, B. et al. (2024). "Open Problems in Technical AI Governance." *TMLR*. https://arxiv.org/abs/2407.14981 *(filed in project Drive as "Chp 2.4")*
    - **Add — Diplomatic risk taxonomy (perplexity):** organise risks by harm type — epistemic (fabricated facts/citations), linguistic-cultural (translation distortion, pragmatic mismatch), information-integrity (deepfakes, impersonation, synthetic statements), cybersecurity (prompt injection, exfiltration), decision (automation bias, over-reliance), institutional (deskilling, weakened accountability), sovereignty (vendor lock-in, service withdrawal), systemic (correlated errors across ministries), catastrophic (irreversible escalation / loss of critical capacity).
    - **Four-layer spine:** classify by *which layer can fail most severely* — model / application / institutional / infrastructure — then assign review tier (Table 5.1).
- **5.2** Evaluation, Validation and Continuous Monitoring
  - **Contribution (AI safety):** contribute evaluation & benchmarking practices (capability evals, scenario testing) adapted for diplomatic workflows.
    - Shevlane, T. et al. (2023). "Model Evaluation for Extreme Risks." *arXiv:2305.15324*. https://arxiv.org/abs/2305.15324
    - **Add — model-level vs system-level evaluation (perplexity):** a model may be safe in chat but unsafe when connected to classified repos, email, document systems, browsers, databases, external channels. Evaluate the full system, not vendor benchmarks. Dimensions: factual accuracy, source reliability, uncertainty calibration, multilingual/cultural competence, prompt-injection resistance, tool-use safety, impersonation resilience, crisis robustness, post-update stability.
    - **Add — NIST Generative AI Profile** (companion to AI RMF 1.0): treats red-teaming, incident response, evaluation, lifecycle monitoring as organisational risk management. https://www.nist.gov/itl/ai-risk-management-framework
    - **Four-layer spine:** evaluate at each layer — model (capability/accuracy), application (retrieval/draft fidelity), institutional (human review/expertise), infrastructure (continuity/update control); loop in Figure 5.2 spans all four.
- **5.3** Red-Teaming and Adversarial Testing
  - **Contribution (AI safety) — strongest single contribution:** adversarial testing, jailbreak/resilience probing, and tabletop exercises for diplomatic AI misuse.
    - Ganguli, D. et al. / Anthropic (2022). "Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned." https://arxiv.org/abs/2209.07858
    - Anthropic. "Claude System Card." https://www.anthropic.com/claude-4-system-card
    - OpenAI. "GPT-4 System Card." https://cdn.openai.com/papers/gpt-4-system-card.pdf
    - **Add — sandbox transgression (perplexity):** system appears a bounded assistant but its access to tools/docs/workflows lets it act outside approval assumptions. Red-team scenarios: poisoned briefing doc, indirect prompt injection in external report, AI-generated false statement attributed to a minister, translation that shifts a negotiation position, agent sending unauthorised comms, vendor outage during regional crisis.
    - **Four-layer spine:** red-team per layer — model (jailbreak/capability), application (sandbox transgression/poisoned retrieval), institutional (synthetic authority/skip-review), infrastructure (update path/channel exploit); probe flow in Figure 5.3 by layer.
- **5.4** Internal AI Guidelines, Escalation Protocols and Safe-Use Policies for Foreign Ministries
  - **Contribution (AI safety):** draft concrete safe-use policy templates for foreign ministries (model access tiers, human-in-the-loop mandates, prohibited uses).
    - NIST AI RMF 1.0. https://www.nist.gov/itl/ai-risk-management-framework
    - OWASP Gen AI Security Project — Top 10 for LLM Applications. https://genai.owasp.org/
    - **Add — the diplomatic AI safety case (perplexity):** for each significant use case, document intended purpose, prohibited uses, users/affected parties, data classification, model+vendor, tools/permissions, known limitations, eval results, red-team results, human decision points, incident-response, fallback, conditions for suspension. Converts "responsible AI" into an approvable/auditable artifact.
    - **Four-layer spine:** guideline specifies something at each layer — model (approved models/tiers), application (OWASP controls on retrieval/tools), institutional (named review + escalation protocol), infrastructure (data-residency/jurisdiction + vendor-update/exit clauses); safety case anchors it (Figure 5.4).
- **5.5** Technical AI Governance for Foreign Affairs
  - **Contribution (AI safety):** link frontier technical governance (capability eval, compute governance, hardware governance) to foreign-affairs adoption decisions and Malaysia's ASEAN role.
    - Shah, R. et al. (2024). *An Approach to Technical AGI Safety and Security.* arXiv:2504.01849.
    - Ramiah, A. A. et al. (2025). *Toward a Global Regime for Compute Governance.* arXiv:2506.20530.
    - Ansari, S. (2026). *Hardware-Level Governance of AI Compute.* arXiv:2604.04712.
    - UK AISI (2023). *Emerging Processes for Frontier AI Safety.*
    - Frontier Safeguards (2025). *Emerging Practices in Frontier AI Safety Frameworks.*
    - International AI Safety Report (2026).
    - **Four-layer spine:** technical governance maps onto all four layers — strengthens model (capabilities), underpins application (allowed actions), sets institutional standard (adoption requirement), bears on infrastructure (compute/supply-chain control); levers in Figure 5.5.
- **5.6** From Model Safety to Diplomatic System Safety *(new — user-approved POV "From Model Safety to Diplomatic Resilience")*
  - **Contribution (AI safety):** frame AI safety as protection of judgment, communication, institutional autonomy and sovereignty — not only model behaviour. Distinguish four layers of the AI-enabled foreign-affairs system: (1) model (capability, hallucination, bias, uncertainty); (2) application (retrieval, translation, summarisation, drafting, decision support); (3) institutional (workflows, authorisation, accountability, human review); (4) infrastructure (cloud, data centres, networks, identity, APIs, vendors). A system may pass at the model layer yet fail because it retrieves poisoned data, has excessive file access, its output is accepted without review, a vendor silently changes the model, or the ministry cannot operate if the service is withdrawn. Ties technical safety (necessary but insufficient) to governance, legitimacy and continuity — the through-line of the chapter.
    - **Four-layer spine:** this section IS the four-layer model as the chapter's unifying mental model (Figure 5.6); "necessary but not sufficient" is the thesis.

**Must stay distinct from:** Ch.2 (risks), Ch.3 (limitations), Ch.4 (ethical dilemmas/accountability). Chapter 5 = the *operational safeguard playbook*.

**Interlinking requirement (mandatory):** This chapter must explicitly connect to prior chapters:
- Reference Ch.1 (intelligent statecraft / augmentation-not-replacement) when arguing for tiered human review.
- Reference Ch.2 (risks: hallucination, impersonation, data inference) when motivating classification and red-teaming.
- Reference Ch.3 (limitations: nuance, verification, translation) when justifying evaluation and human-in-the-loop.
- Reference Ch.4 (accountability/ethics principles) when deriving internal guidelines.
Use brief, purposeful cross-references — not repetition. Each link should add a new operational layer, not re-state the earlier argument.

**Case-study requirement (mandatory):** Each sub-section (5.1–5.6) must include **at least 2–3 specific case studies** drawn from the project's defined references (the book's survey of 64 diplomats, the interview transcripts, and the attached PDFs). Examples already in the corpus: the Israeli travellers / KLIA AI travel-advice incident (Ch.2.1); the Rubio deepfake impersonation (Ch.2.2); the Deloitte AI-hallucination report correction (Ch.3.3); officer survey findings on confidentiality and verification (Ch.2.5, Ch.3.3). Re-use these where they *illustrate an operational safeguard*, and add new ones from the Chapter 5 PDFs (e.g. red-teaming findings from Ganguli 2022; incident-governance gaps from Sidhu & Scholefield 2026; compute-governance implications from Ramiah 2025; hardware-governance feasibility from Ansari 2026). Cite each case study to its source.

---

## THE PROMPT

> **Role:** Act as an academic writing assistant for a scholarly book on diplomacy and AI.
>
> **Task:** Write a comprehensive book chapter entitled **"AI Safety and Operational Safeguards for Diplomacy"** for the volume *Innovating Diplomacy: A Framework for AI Literacy and Ethical Governance in Modern Diplomacy*. Cover, with clear headings: 5.1 AI Risk Assessment & Classification; 5.2 Evaluation, Validation and Continuous Monitoring; 5.3 Red-Teaming and Adversarial Testing; 5.4 Internal AI Guidelines, Escalation Protocols and Safe-Use Policies; 5.5 Technical AI Governance for Foreign Affairs; 5.6 From Model Safety to Diplomatic System Safety. Frame around (a) Malaysia's emerging role in ASEAN AI safety, and (b) AI safety vs cybersecurity vs information security. Organise the entire chapter around the four-layer spine (model → application → institutional → infrastructure) as the unifying analytical frame.
>
> **Mandatory source corpus (read first):** `gdrive_pdf_index.md` lists all defined PDFs. The **/CHAPTER 5** folder holds the operational AI-safety literature — use it as the primary evidence base (Shevlane 2023 on model evaluation for extreme risks; Ganguli 2022 on red-teaming language models; NIST AI RMF 1.0; Sidhu & Scholefield 2026 on AI incident governance; OWASP Gen AI Top 10). Also draw on the project's survey of 64 diplomatic officers and interview transcripts (already used in Ch.1–4). Where interview transcripts are provided, embed verbatim quotations with endnotes.
>
> **New external sources — strict rule:** If a topic requires a source *not* in `gdrive_pdf_index.md`, you may propose it **only** if you: (1) list it in a "Proposed Additional Sources" section with full APA-7 citation, URL/DOI, and justification; (2) mark its in-text citation and bibliography entry in **blue**; (3) state it must be **added to the "Chapter 5" folder in the project Google Drive AND appended to `book-toc.md`** before finalisation. Prefer government/international-organisation sources. Do not invent or embed unattributed material.
>
> **Voice & style — non-negotiable anchors:** British English. Match the measured, humane, formally accessible register of *From Hate to Hope* (see `datalab-output-IDFR_Book-From_Hate_to_HOPE.pdf.md`): justified paragraphs; short epigraph-style italics under the chapter title; diplomat quotations with endnotes; risk/consequence/safeguard tables; figures that map a process or summarise the argument. Cohere to `book-draft.md`'s approved cadence — do **not** drift into generic AI-helpful tone.
>
> **Structural requirements:**
> - 3,000–5,000 words. Introduction → 5.1–5.6 → Conclusion → Endnotes → APA-7 References → "Proposed Additional Sources".
> - **Interlink prior chapters:** explicitly reference Ch.1–4 where they motivate a safeguard (see Interlinking requirement above). Brief, purposeful, non-repetitive.
> - **Four-layer spine (REQUIRED for 5.1–5.6):** every sub-section must explicitly organise its content around the four layers — model → application → institutional → infrastructure — showing how risk/safeguard/failure manifests at each. Use the layer vocabulary consistently (introduced in Figure I.1). Each sub-section's diagram should reflect its layer focus. **Every place the four-layer system is named in prose must be backed by a table or diagram for ease of reading** — provide a four-layer table at each sub-section's own lens (classification in 5.1, evaluation in 5.2, red-teaming in 5.3, guidelines in 5.4, technical governance in 5.5, system safety synthesis in 5.6), and ensure any figure that claims to show the layers actually depicts all four (model/application/institutional/infrastructure).
> - **No repeated case studies:** each sub-section's case studies must be distinct. Cross-references to earlier incidents (e.g. "as shown in 5.3") are allowed as consolidation, but do NOT re-narrate the same case as a fresh study within a different sub-section. Draw fresh illustrations from the defined corpus (survey stats used once; Shevlane/Ganguli/Sidhu/Intl Report framings; MOSTI anchor; compute-governance implications from Ramiah 2025; hardware-governance feasibility from Ansari 2026; frontier-safeguards survey) rather than recycling KLIA/Rubio/Deloitte.
> - **Forward-links to other chapters:** each sub-section should close with a one-line pointer to where its infrastructure/sovereignty/norm-shaping implications are developed later — e.g. "Chapter 6 takes up vendor and sovereignty clauses in detail; Chapter 7 positions the ministry as a shaper of regional AI-safety norms." This ties Chapter 5 to the book's later arc.
> - **Sub-section 5.5 — Technical AI Governance for Foreign Affairs:** link frontier technical governance (capability evaluation, compute governance, compute-tracing / hardware governance) directly to foreign-affairs adoption decisions and Malaysia's ASEAN leadership role. Apply the four-layer spine: technical governance strengthens the model layer (capabilities), constrains the application layer (allowed actions), sets institutional standards (adoption requirements), and bears on the infrastructure layer (compute supply-chain control). Map each lever from Shah 2024, Ramiah 2025, Ansari 2026, and the International AI Safety Report 2026 to its layer. Close with a forward-link to Ch.6 (international norm-making) and Ch.7 (capacity building). Include ≥1 Mermaid diagram and 2–3 case studies (e.g., frontier-model access disparities between ASEAN members; a compute-traceability requirement as a sovereignty safeguard).
> - **Sub-section 5.6 — From Model Safety to Diplomatic System Safety / Resilience:** this section is the chapter's synthesising anchor and the clearest expression of the "necessary but not sufficient" thesis. Distinguish the four layers of the AI-enabled foreign-affairs system and show how a system can pass model-level safety yet fail catastrophically at any other layer. Use the International AI Safety Report 2026 framing (technical safeguards + institutional risk management as complementary). Argue that diplomatic AI safety is ultimately about protecting judgment, communication, institutional autonomy, and national sovereignty — not just preventing model misbehaviour. This is the section that closes the chapter's through-line, so tie together threads from 5.1–5.5 and point forward to Ch.6 and Ch.7. Include ≥1 Mermaid diagram (four-layer stack with failure modes) and 2–3 case studies drawn from the full corpus.
> - **Diplomatic risk taxonomy (in 5.1):** organise the classification around the nine harm types — epistemic, linguistic-cultural, information-integrity, cybersecurity, decision, institutional, sovereignty, systemic, catastrophic. **Present the taxonomy visibly** as a defined table with a one-line diplomatic example for each category (so the reader can see the full range, from everyday error to the catastrophic end), not merely a list in the prose.
> - **Incidents can be catastrophic (in 5.1 and 5.6):** explicitly show that AI failures in diplomacy are not always minor. Include at least one illustration of how a single unverified or misused AI output can escalate to bilateral rupture, conflict, or loss of life, and tie it to the ninth ("catastrophic") taxonomy category and the Critical tier. Use the International AI Safety Report 2026 framing and/or corpus cases (e.g., the Rubio synthetic-identity breach, Ch.2.2) as consolidation.
> - **System-level vs model-level evaluation (in 5.2):** state that a model safe in chat may be unsafe when connected to classified repos, email, document systems, browsers, databases, external channels; evaluate the full system. Cite NIST Generative AI Profile alongside AI RMF 1.0.
> - **Sandbox transgression (in 5.3):** define it and give red-team scenarios (poisoned briefing doc, indirect prompt injection, false attributed statement, translation shifting a position, agent unauthorised comms, vendor outage in crisis).
> - **Civic-tech / open-source options (fuse into 5.2–5.4):** where relevant, fuse in easy, low-cost open-source tools a ministry can adopt — e.g., open red-teaming toolkits (Garak, Microsoft PyRIT), local open-weight models for data sovereignty (Ollama), and open policy/guidance templates (OWASP Gen AI Top 10). Show these are the cheapest credible first step, not a second-best. Any named tool not already in `gdrive_pdf_index.md` must be listed in "Proposed Additional Sources" with full APA + URL and flagged for addition to the Chapter 5 Drive folder and `book-toc.md`.
> - **The diplomatic AI safety case (in 5.4):** define as a structured, evidence-backed argument that a deployment is acceptably safe; list its required fields (intended purpose, prohibited uses, data classification, model+vendor, eval/red-team results, human decision points, incident-response, fallback, suspension conditions).
> - **AI safety vs AI security vs information security:** the Introduction must draw this three-way distinction explicitly (use Shah 2024's safety/security analytic split and the International AI Safety Report 2026), and the distinction should recur where relevant.
> - **Entry-level AI safety action per sub-section:** after each of 5.1–5.6, include a short callout box ("Entry-level AI safety action (X.X)") describing one concrete, low-tooling habit an inexperienced officer can adopt immediately. These make the chapter usable at every rank. **Use the chapter's own method/format:** tag each action with the layer(s) it protects (model / application / institutional / infrastructure) and/or the taxonomy category it addresses, keeping it concrete. Example: "**Entry-level AI safety action (5.1) — model & institutional layers:** …".
> - **First-person for our own data (lead-author instruction):** when writing about the survey and interviews *we ourselves conducted*, use "we / our / us" — never third-person "the survey" or "the project's survey." This makes clear to the reader that the data and interviews are our own primary research, and reads more human. Examples: "Our survey of 64 diplomatic officers shows…"; "We classify…"; "Our safety-case template…". Reserve third-person ("the survey", "respondents") only where a citation-to-others context demands it; the (Survey for Diplomats, 2026) citation stays as the source tag. Apply this consistently in case studies, source notes, and the Conclusion.
> - **Case studies:** each of 5.1–5.6 must contain **2–3 specific case studies** from the defined references (survey, interviews, attached PDFs, or cases already in Ch.1–4 that illustrate an operational safeguard). Cite each. Each sub-section's cases must be distinct (no repeats across sub-sections). **Format each sub-section's case studies under a subheading that names the subchapter**, e.g. "### Case studies — 5.1 AI Risk Assessment & Classification for Diplomatic Use Cases" (repeat for 5.2–5.6).
> - Include **one orientation diagram in the Introduction** (Figure I.1) showing the chapter's POV: AI safety at the intersection of AI safety / cybersecurity / information security, converging on "safe · sovereign · accountable diplomatic statecraft", with the four-layer system (model/application/institutional/infrastructure) feeding the AI-enabled foreign-affairs system. Then ≥1 Mermaid diagram per sub-section (5.1–5.6).
>
> **Citations:** APA 7th. Endnotes for interviews. Blue only for listed supplementary external sources.
>
> **Source integration & diversity (from base brief):**
> - Integrate literature, policy documents, reports, survey data and interview transcripts **naturally throughout** the discussion — as flowing evidence — rather than presenting them as isolated, boxed citations. Each source should appear where it adds unique value; avoid relying on the same reference repeatedly. The reference list must be comprehensive, non-repetitive and directly relevant.
> - Prioritise high-quality, credible and up-to-date academic and institutional sources (governments, international organisations, trusted outlets) over weaker ones. Where we attach references, prioritise those first; any additional references must follow the blue-citation rule above.
> - Do not repeat content already covered in Ch.1–4. Assume earlier chapters have addressed their topics; where overlap is unavoidable, give a brief cross-reference then expand on new, chapter-specific perspectives. Refer to `book-toc.md` so this chapter stays distinct in argument from the others.
>
> **Output & format (from base brief, adapted for Inkling/GDrive):**
> - Draft in **Inkling (Hermes)**; the live draft **auto-syncs to the project Google Drive** (`/CHAPTER 5` folder) as a Google Doc. Match the format, look, and font/font size of *From Hate to Hope*; justify all paragraphs. Export to **Microsoft Word (.docx)** when handing to typesetting.
> - Structure: Chapter title → epigraph-style italic line → Introduction → 5.1–5.6 → Conclusion → Endnotes → APA-7 References → "Proposed Additional Sources".
> - Include figures (flowcharts / infographics / tables) where appropriate, serving two explicit purposes: (1) map the core process/argument within the chapter (the Introduction orientation diagram, Figure I.1, does this; each sub-section's Mermaid does this for its lens); and (2) summarise the chapter's main points (provide at least one summary infographic, e.g. a closing figure consolidating the four-layer spine and the safeguard stack across 5.1–5.6).
>
> **Quality bar:** formal yet accessible; analytical; smooth transitions; consistent terminology; no exaggerated wording. Every paragraph advances the argument.

---

## Editor notes (for you, not the model)

- **Defined-corpus discipline:** Model must use `/CHAPTER 5` PDFs first. Reject any cite not in `gdrive_pdf_index.md` and not in the blue "Proposed Additional Sources" list.
- **New-file workflow (Inkling/GDrive):** Any source Inkling lists as "additional" (blue) → you (1) drop the PDF into the **Chapter 5** Drive folder (Inkling already syncs drafts there), (2) re-run `gdrive_pdf_index.md` generation, and (3) append it to `book-toc.md`'s Chapter 5 literature list. Keeps audit trail clean.
- **Interlink check:** Verify Ch.5 references Ch.1–4 by name/purpose, not by copying text. Each cross-reference should add the *operational* layer.
- **Case-study check:** 2–3 per sub-section, each tied to a citation. Re-using Ch.2/Ch.3 cases is allowed *if* they illustrate a Ch.5 safeguard (e.g. Rubio impersonation → motivates red-teaming; KLIA advice → motivates classification tier).
- **Taxonomy + catastrophic check:** Verify 5.1 shows the nine categories as a *visible defined table* (one-line example each) and that at least one illustration shows an incident escalating to the catastrophic tier (tied to the Critical tier / International AI Safety Report 2026).
- **Civic-tech check:** Verify easy open-source options are fused in (esp. 5.2–5.4) and that any named tool not in `gdrive_pdf_index.md` appears in "Proposed Additional Sources" with APA + URL, flagged for Drive/`book-toc.md` addition.
- **Subheading check:** Each sub-section's case studies must sit under a "### Case studies — X.X <subchapter name>" subheading; entry-level actions should carry a layer/taxonomy tag.
- **Voice check:** Compare output opening to `book-draft.md` Ch.1 intro. Same restrained cadence.
- **Blue citations:** Only supplementary external sources get blue. Defined-corpus + project data stay black.
- **Claude evaluation gate:** Before sign-off, run the **EVALUATION PROMPT (for Claude)** block below on the Inkling draft. Iterate in Inkling, re-evaluate in Claude, until every item is PASS. Treat Claude's report as the acceptance checklist.
- **Pipeline tip:** Perplexity = research only (expand `book-toc.md` + scope first). Inkling = draft + GDrive sync. Claude = evaluate. Keep THE PROMPT in Inkling and the EVALUATION PROMPT in Claude; don't mix them.

---

## EVALUATION PROMPT (for Claude)

> **Role:** You are a meticulous senior book-chapter evaluator and copy-editor for an academic volume on diplomacy and AI.
>
> **Task:** Evaluate the Chapter 5 draft I paste below against the acceptance checklist. Be strict and evidence-based: quote the exact draft passage that proves (or fails) each item. Do **not** rewrite the chapter — return a scored checklist plus a prioritised revision list.
>
> **Inputs I will paste:** (1) the Inkling draft of Chapter 5; (2) when useful, the `book-toc.md` Chapter 5 scope and the `chapter5-research-prompt.md` requirements for reference.
>
> **Acceptance checklist (mark each PASS / FAIL / WARN with evidence + fix):**
> 1. **Structure & coverage:** all six sub-sections present with correct titles — 5.1 Risk Assessment & Classification; 5.2 Evaluation, Validation & Monitoring; 5.3 Red-Teaming & Adversarial Testing; 5.4 Internal Guidelines, Escalation & Safe-Use Policies; 5.5 Technical AI Governance for Foreign Affairs; 5.6 From Model Safety to Diplomatic System Safety. Plus Introduction, Conclusion, Endnotes, APA-7 References, "Proposed Additional Sources".
> 2. **Length:** 3,000–5,000 words.
> 3. **Four-layer spine (5.1–5.6):** every sub-section organises its content around model → application → institutional → infrastructure; each carries a four-layer table or diagram; any figure claiming to show the layers depicts all four. Flag any sub-section missing the spine or showing <4 layers.
> 4. **Interlinking (Ch.1–4):** explicit, purposeful cross-references that add an *operational* layer, not repetition. List any missing link (esp. Ch.1 tiered-review, Ch.2 risks, Ch.3 limitations, Ch.4 accountability).
> 5. **Case studies:** 2–3 distinct, cited case studies per sub-section (5.1–5.6); none repeated across sub-sections; each under a "### Case studies — X.X <subchapter name>" subheading.
> 6. **Risk taxonomy (5.1):** the nine harm types (epistemic, linguistic-cultural, information-integrity, cybersecurity, decision, institutional, sovereignty, systemic, catastrophic) appear as a *visible defined table* with a one-line diplomatic example each.
> 7. **Catastrophic illustration:** ≥1 incident shown escalating to the catastrophic tier / Critical tier, tied to the International AI Safety Report 2026.
> 8. **System- vs model-level eval (5.2):** stated that a chat-safe model can be unsafe when wired to repos/email/docs/browsers/DBs/channels; NIST Generative AI Profile cited alongside AI RMF 1.0.
> 9. **Sandbox transgression (5.3):** defined with the listed scenarios (poisoned briefing doc, indirect injection, false attributed statement, translation shifting a position, unauthorised agent comms, vendor outage in crisis).
> 10. **Civic-tech (5.2–5.4):** open-source options fused in (Garak, Microsoft PyRIT, Ollama, OWASP Gen AI Top 10); any tool *not* in `gdrive_pdf_index.md` appears in "Proposed Additional Sources" with APA + URL, flagged blue.
> 11. **Diplomatic AI safety case (5.4):** defined with its required fields (intended purpose, prohibited uses, data classification, model+vendor, eval/red-team results, human decision points, incident-response, fallback, suspension conditions).
> 12. **5.5 technical governance:** maps Shah 2024, Ramiah 2025, Ansari 2026, Intl AI Safety Report 2026 to the four layers; carries ≥1 diagram; 2–3 cases; forward-links to Ch.6/Ch.7.
> 13. **5.6 system safety:** synthesises the four layers; states the "necessary but not sufficient" thesis; ties together 5.1–5.5; forward-links to Ch.6/Ch.7; ≥1 Mermaid (four-layer stack with failure modes); 2–3 cases.
> 14. **AI safety vs security vs information security:** three-way distinction explicit in the Introduction and recurs where relevant (Shah 2024 + Intl AI Safety Report 2026).
> 15. **Entry-level actions:** one "Entry-level AI safety action (X.X)" callout per sub-section (5.1–5.6), each tagged with layer(s) and/or taxonomy category.
> 16. **First-person for own data:** "we/our/us" used for the survey & interviews we conducted; "(Survey for Diplomats, 2026)" tag retained; third-person reserved for external citations.
> 17. **Voice & style:** British English; *From Hate to Hope* register (restrained, humane, formal-accessibile); justified paragraphs; epigraph-style italics under title; diplomat quotations with endnotes; risk/consequence/safeguard tables; figures mapping process or summarising argument.
> 18. **Citations:** APA-7; endnotes for interviews; blue used *only* for supplementary external sources absent from `gdrive_pdf_index.md`; no fabricated or unattributed material.
> 19. **Figures:** Figure I.1 orientation diagram (AI safety ∩ cybersecurity ∩ information security → safe/sovereign/accountable statecraft, four-layer system feeding the AI-enabled foreign-affairs system); ≥1 Mermaid diagram per sub-section (5.1–5.6); ≥1 summary infographic consolidating the chapter's main points.
> 20. **Source integration & diversity:** literature/transcripts woven naturally (not isolated); each source used where it adds unique value; reference list comprehensive, non-repetitive, relevant; credible/up-to-date institutional sources prioritised.
> 21. **Distinctness:** does not re-litigate Ch.2 (risks), Ch.3 (limitations), or Ch.4 (ethics/accountability); adds operational safeguards instead.
> 22. **Quality bar:** analytical; smooth transitions; consistent terminology/definitions; no exaggerated or dramatic wording; every paragraph advances the argument.
>
> **Output format:** For each item: `PASS / FAIL / WARN` + the draft quote that proves it + a concrete fix if failing. Then: overall verdict (Accept / Revise), and a numbered **priority revision list** (highest-impact first) the Inkling drafter should action next.
