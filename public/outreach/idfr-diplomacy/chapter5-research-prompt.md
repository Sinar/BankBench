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
> - **New sub-section 5.5 (Technical AI Governance for Foreign Affairs):** add a section after 5.4 covering the technical governance levers relevant to diplomacy — capability evaluation (Shevlane 2023; Shah 2024), compute governance (Ramiah 2025), hardware-level governance (Ansari 2026), and emerging state practice (UK AISI 2023; Frontier Safeguards 2025; International AI Safety Report 2026). Frame Malaysia's ASEAN AI-safety role as distinctive here. Include ≥1 Mermaid diagram and 2–3 case studies.
> - **AI safety vs AI security vs information security:** the Introduction must draw this three-way distinction explicitly (use Shah 2024's safety/security analytic split and the International AI Safety Report 2026), and the distinction should recur where relevant.
> - **Entry-level AI safety action per sub-section:** after each of 5.1–5.5, include a short callout box ("Entry-level AI safety action (X.X)") describing one concrete, low-tooling habit an inexperienced officer can adopt immediately (e.g. tag-the-tier, find-the-source, call-back-verify, one-page-rule-sheet, vendor-three-questions). These make the chapter usable at every rank.
> - **Case studies:** each of 5.1–5.5 must contain **2–3 specific case studies** from the defined references (survey, interviews, attached PDFs, or cases already in Ch.1–4 that illustrate an operational safeguard). Cite each.
> - Include ≥1 **diagram per sub-section (5.1–5.4)** rendered in **Mermaid** (preferred — renders in Google Docs via the "Mermaid" add-on and in Markdown viewers; falls back to SVG if the target toolchain requires it). Each diagram must be a genuine figure (flowchart, matrix map, or process cycle), not a decorative box. At minimum: 5.1 a risk-classification matrix/map; 5.2 an evaluation-and-monitoring loop; 5.3 a red-teaming adversarial probe flow; 5.4 an escalation-protocol flowchart. Provide the Mermaid code block plus a one-line caption and a "*Source: Authors' synthesis…*" note.
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
- **Voice check:** Compare output opening to `book-draft.md` Ch.1 intro. Same restrained cadence.
- **Blue citations:** Only supplementary external sources get blue. Defined-corpus + project data stay black.
- **rpm tip:** Single-shot generation. Edit locally rather than re-running — protects the 40 rpm budget.
