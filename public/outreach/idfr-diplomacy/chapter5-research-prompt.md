# Research Prompt — Chapter 5: *AI Safety and Operational Safeguards for Diplomacy*

> **How to use this file:** Paste the block under **"THE PROMPT"** into ChatGPT (Work) or your research assistant. Keep British English on. The links are local references for *you* (the human editor), not for the model — attach the actual files when prompting.
>
> **Source files (attach / keep open):**
> - **Defined corpus (mandatory primary pool)** → `gdrive_pdf_index.md` — all PDFs defined for this project, including the **/CHAPTER 5** folder (operational AI-safety literature: Shevlane 2023, Ganguli 2022, NIST AI RMF 1.0, Sidhu & Scholefield 2026 incident governance; OWASP Gen AI Top 10). **Use these first.**
> - Voice & style anchor → `datalab-output-IDFR_Book-From_Hate_to_HOPE.pdf.md` (text extraction of Dr Murni Wan Mohd Nor's *From Hate to Hope*).
> - Chapter structure → `book-toc.md` (Chapter 5 scope + its embedded literature list with URLs).
> - Exemplar voice already approved → `book-draft.md` (Chapters 1–3 as written).
> - Base rules → `chapter-prompt.md` (this prompt is a Chapter-5-specific refinement of it).

---

## Chapter 5 scope (from `book-toc.md`)

**Title:** *AI Safety and Operational Safeguards for Diplomacy*
**Framing:** Malaysia's emerging role in ASEAN AI safety · Distinguishing AI safety from cybersecurity and information security.

- **5.1** AI Risk Assessment & Classification for Diplomatic Use Cases
- **5.2** Evaluation, Validation and Continuous Monitoring
- **5.3** Red-Teaming and Adversarial Testing
- **5.4** Internal AI Guidelines, Escalation Protocols and Safe-Use Policies for Foreign Ministries

**Must stay distinct from:** Ch.2 (risks), Ch.3 (limitations), Ch.4 (ethical dilemmas/accountability). Chapter 5 = the *operational safeguard playbook*.

**Interlinking requirement (mandatory):** This chapter must explicitly connect to prior chapters:
- Reference Ch.1 (intelligent statecraft / augmentation-not-replacement) when arguing for tiered human review.
- Reference Ch.2 (risks: hallucination, impersonation, data inference) when motivating classification and red-teaming.
- Reference Ch.3 (limitations: nuance, verification, translation) when justifying evaluation and human-in-the-loop.
- Reference Ch.4 (accountability/ethics principles) when deriving internal guidelines.
Use brief, purposeful cross-references — not repetition. Each link should add a new operational layer, not re-state the earlier argument.

**Case-study requirement (mandatory):** Each sub-section (5.1–5.4) must include **at least 2–3 specific case studies** drawn from the project's defined references (the book's survey of 64 diplomats, the interview transcripts, and the attached PDFs). Examples already in the corpus: the Israeli travellers / KLIA AI travel-advice incident (Ch.2.1); the Rubio deepfake impersonation (Ch.2.2); the Deloitte AI-hallucination report correction (Ch.3.3); officer survey findings on confidentiality and verification (Ch.2.5, Ch.3.3). Re-use these where they *illustrate an operational safeguard*, and add new ones from the Chapter 5 PDFs (e.g. red-teaming findings from Ganguli 2022; incident-governance gaps from Sidhu & Scholefield 2026). Cite each case study to its source.

---

## THE PROMPT

> **Role:** Act as an academic writing assistant for a scholarly book on diplomacy and AI.
>
> **Task:** Write a comprehensive book chapter entitled **"AI Safety and Operational Safeguards for Diplomacy"** for the volume *Innovating Diplomacy: A Framework for AI Literacy and Ethical Governance in Modern Diplomacy*. Cover, with clear headings: 5.1 AI Risk Assessment & Classification; 5.2 Evaluation, Validation and Continuous Monitoring; 5.3 Red-Teaming and Adversarial Testing; 5.4 Internal AI Guidelines, Escalation Protocols and Safe-Use Policies. Frame around (a) Malaysia's emerging role in ASEAN AI safety, and (b) AI safety vs cybersecurity vs information security.
>
> **Mandatory source corpus (read first):** `gdrive_pdf_index.md` lists all defined PDFs. The **/CHAPTER 5** folder holds the operational AI-safety literature — use it as the primary evidence base (Shevlane 2023 on model evaluation for extreme risks; Ganguli 2022 on red-teaming language models; NIST AI RMF 1.0; Sidhu & Scholefield 2026 on AI incident governance; OWASP Gen AI Top 10). Also draw on the project's survey of 64 diplomatic officers and interview transcripts (already used in Ch.1–4). Where interview transcripts are provided, embed verbatim quotations with endnotes.
>
> **New external sources — strict rule:** If a topic requires a source *not* in `gdrive_pdf_index.md`, you may propose it **only** if you: (1) list it in a "Proposed Additional Sources" section with full APA-7 citation, URL/DOI, and justification; (2) mark its in-text citation and bibliography entry in **blue**; (3) state it must be **added to the "Chapter 5" folder in the project Google Drive AND appended to `book-toc.md`** before finalisation. Prefer government/international-organisation sources. Do not invent or embed unattributed material.
>
> **Voice & style — non-negotiable anchors:** British English. Match the measured, humane, formally accessible register of *From Hate to Hope* (see `datalab-output-IDFR_Book-From_Hate_to_HOPE.pdf.md`): justified paragraphs; short epigraph-style italics under the chapter title; diplomat quotations with endnotes; risk/consequence/safeguard tables; figures that map a process or summarise the argument. Cohere to `book-draft.md`'s approved cadence — do **not** drift into generic AI-helpful tone.
>
> **Structural requirements:**
> - 3,000–5,000 words. Introduction → 5.1–5.4 → Conclusion → Endnotes → APA-7 References → "Proposed Additional Sources".
> - **Interlink prior chapters:** explicitly reference Ch.1–4 where they motivate a safeguard (see Interlinking requirement above). Brief, purposeful, non-repetitive.
> - **Four-layer spine (REQUIRED structure for 5.1–5.6):** every sub-section must explicitly organise its content around the four layers — model → application → institutional → infrastructure — showing how risk/safeguard/failure manifests at each. Use the layer vocabulary consistently (introduced in Figure I.1). Each sub-section's diagram should reflect its layer focus. **Every place the four-layer system is named in prose must be backed by a table or diagram for ease of reading** — provide a four-layer table at each sub-section's own lens (e.g., classification in 5.1, evaluation in 5.2, red-teaming in 5.3, guidelines in 5.4, technical governance in 5.5), and ensure any figure that claims to show the layers actually depicts all four (model/application/institutional/infrastructure).
> - **No repeated case studies:** each sub-section's case studies must be distinct. Cross-references to earlier incidents (e.g. "as shown in 5.3") are allowed as consolidation, but do NOT re-narrate the same case as a fresh study within a different sub-section. Draw fresh illustrations from the defined corpus (survey stats used once; Shevlane/Ganguli/Sidhu/Intl Report framings; MOSTI anchor) rather than recycling KLIA/Rubio/Deloitte.
> - **Forward-links to other chapters:** each sub-section should close with a one-line pointer to where its infrastructure/sovereignty/norm-shaping implications are developed later — e.g. "Chapter 6 takes up vendor and sovereignty clauses in detail; Chapter 7 positions the ministry as a shaper of regional AI-safety norms." This ties Chapter 5 to the book's later arc.
> - **New sub-section 5.6 (From Model Safety to Diplomatic System Safety / Resilience):** after 5.5, add a synthesising section using the user-approved POV. Distinguish the four layers of the AI-enabled foreign-affairs system — (1) model: capability, hallucination, bias, uncertainty; (2) application: retrieval, translation, summarisation, drafting, decision support; (3) institutional: workflows, authorisation, accountability, human review; (4) infrastructure: cloud, data centres, networks, identity, APIs, vendors. Argue technical safety is necessary but insufficient; governance, legitimacy and continuity complete it. Use the International AI Safety Report 2026 framing (technical safeguards + institutional risk management as complementary). Include ≥1 Mermaid diagram (four-layer stack with failure modes) and 2–3 case studies.
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
> **Quality bar:** formal yet accessible; analytical; smooth transitions; consistent terminology; no exaggerated wording. Every paragraph advances the argument.

---

## Editor notes (for you, not the model)

- **Defined-corpus discipline:** Model must use `/CHAPTER 5` PDFs first. Reject any cite not in `gdrive_pdf_index.md` and not in the blue "Proposed Additional Sources" list.
- **New-file workflow:** Any source the model lists as "additional" → you (1) add it to the **Chapter 5** Drive folder, (2) re-run `gdrive_pdf_index.md` generation, and (3) append it to `book-toc.md`'s Chapter 5 literature list. Keeps audit trail clean.
- **Interlink check:** Verify Ch.5 references Ch.1–4 by name/purpose, not by copying text. Each cross-reference should add the *operational* layer.
- **Case-study check:** 2–3 per sub-section, each tied to a citation. Re-using Ch.2/Ch.3 cases is allowed *if* they illustrate a Ch.5 safeguard (e.g. Rubio impersonation → motivates red-teaming; KLIA advice → motivates classification tier).
- **Taxonomy + catastrophic check:** Verify 5.1 shows the nine categories as a *visible defined table* (one-line example each) and that at least one illustration shows an incident escalating to the catastrophic tier (tied to the Critical tier / International AI Safety Report 2026).
- **Civic-tech check:** Verify easy open-source options are fused in (esp. 5.2–5.4) and that any named tool not in `gdrive_pdf_index.md` appears in "Proposed Additional Sources" with APA + URL, flagged for Drive/`book-toc.md` addition.
- **Subheading check:** Each sub-section's case studies must sit under a "### Case studies — X.X <subchapter name>" subheading; entry-level actions should carry a layer/taxonomy tag.
- **Voice check:** Compare output opening to `book-draft.md` Ch.1 intro. Same restrained cadence.
- **Blue citations:** Only supplementary external sources get blue. Defined-corpus + project data stay black.
- **rpm tip:** Single-shot generation. Edit locally rather than re-running — protects the 40 rpm budget.
