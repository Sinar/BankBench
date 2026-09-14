[IDFR_ CH-5_AI_Safety.md](https://github.com/user-attachments/files/32178171/IDFR_.CH-5_AI_Safety.md)# **CHAPTER 5**

**AI Safety and Operational Safeguards for Diplomacy**

*From principle to practice: making AI safe in the daily work of statecraft*

*The question for foreign ministries is no longer whether artificial intelligence will be used in diplomatic work, but whether its use will be deliberate, verified and accountable. Safety is not a feature added after deployment; it is the discipline that allows AI to enlarge diplomatic judgement without displacing it.*

# **Introduction**

Earlier chapters established what artificial intelligence can do for diplomacy, what can go wrong, and where the technology reaches its limits. Chapter 1 framed intelligent statecraft as augmentation rather than replacement, arguing that AI should enlarge the diplomat's field of view while human responsibility for interpretation and representation remains intact. Chapters 2 and 3 showed, respectively, the risks AI introduces into diplomatic practice and the limitations it cannot reliably overcome. Chapter 4 located these concerns within a framework of ethical dilemmas and accountability.

This chapter moves from diagnosis to architecture. It asks the practical question every ministry must answer before adoption outpaces governance: what concrete safeguards make AI safe to use in diplomatic work? The framing is deliberately operational. Risk and limitation describe where harm may arise; accountability and ethics describe the principles that should govern use. This chapter describes the mechanisms that connect the two.

Before setting out those mechanisms, the chapter draws an important distinction — one that is frequently overlooked in institutional policy discussions. 

Cybersecurity protects systems and networks from intrusion. Information security protects the confidentiality, integrity and availability of data. AI safety addresses something different: the behaviour of systems that can generate novel outputs, infer unintended patterns, or fail in ways that are not visible at the moment of use. 

A model may be perfectly secure against external attack and yet produce a confident, fluent and wrong diplomatic brief. The International AI Safety Report 2026 stresses that advanced AI can aggravate existing harms and that important failure modes may only become visible in real-world use (International AI Safety Report, 2026). Shah et al. (2024) draw a parallel analytic distinction between safety — preventing unintentional, emergent harm from the system itself — and security — preventing deliberate adversary exploitation. Both are needed in foreign ministries, but they demand different routines, different vocabularies and different institutional owners.

The through-line connecting all four sections of this chapter is Malaysia's emerging role in ASEAN AI safety. A foreign ministry that can demonstrate disciplined, documented safeguard practice is better placed to shape regional AI-safety norms than one that merely adopts tools. The sections that follow show what that practice looks like in diplomatic work.

***Figure I.1  The chapter's framework — AI safety for diplomatic statecraft***

┌──────────────────────────────────────────────────────────────────────┐

│            THREE PROTECTIVE DISCIPLINES                              │

│                                                                      │

│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐  │

│   │   AI SAFETY     │   │  CYBERSECURITY   │   │ INFORMATION     │  │

│   │ System behaviour│   │ Systems/networks │   │   SECURITY      │  │

│   │ Hallucination,  │   │ Intrusion,       │   │ Data CIA triad  │  │

│   │ bias, emergence │   │ exfiltration     │   │ Confidentiality │  │

│   └────────┬────────┘   └────────┬─────────┘   └────────┬────────┘  │

│            └──────────────────────┼──────────────────────┘           │

│                                   ▼                                  │

│          ┌────────────────────────────────────────────┐              │

│          │   DIPLOMATIC AI SAFETY                      │              │

│          │   safe · sovereign · accountable statecraft │              │

│          └──────────┬─────────────────────────────────┘              │

│      ┌──────────────┼──────────────────┬─────────────┐               │

│      ▼              ▼                  ▼             ▼               │

│  \[Model layer\] \[Application\]   \[Institutional\] \[Infrastructure\]      │

│  Capability,   Retrieval,      Workflows,      Cloud, data centres,  │

│  hallucination translation,    authorisation,  APIs, vendors,        │

│  bias          drafting        human review    jurisdiction           │

│                                                                      │

│              ──────────────────────────────────────                  │

│              AI-ENABLED FOREIGN-AFFAIRS SYSTEM                       │

└──────────────────────────────────────────────────────────────────────┘

*Source: Our synthesis from Shah et al. (2024), International AI Safety Report (2026).*

# **5.1  AI Risk Assessment and Classification for Diplomatic Use Cases**

Effective AI safety begins not with technology but with classification. 

The NIST AI Risk Management Framework (AI RMF 1.0) treats risk management as a continuous function — Govern, Map, Measure, Manage — whose first task is to frame risk in the specific context of a system's use rather than rely on generic assurances (National Institute of Standards and Technology, 2023). For a foreign ministry, that framing decides, before any tool is adopted, what level of care each use case demands.

A useful way to make classification concrete is to read every use case through the four-layer system introduced in Figure I.1. Risk does not live in one place; it accumulates across layers, and a classification that ignores a layer is incomplete.

***Table 5.1a  The four-layer AI-enabled foreign-affairs system — classification lens***

| Layer | What can go wrong | Diplomatic example |
| :---- | :---- | :---- |
| Model | Hallucination, bias, miscalibration in the model's own outputs. | A translation model confidently mistranslates a binding legal term. |
| Application | How the model is wired into work — retrieval, drafting, summarisation. | A retrieval step pulls a poisoned embassy cable the model alone would never surface. |
| Institutional | Who approves, reviews and is accountable. | A consular brief accepted without a named reviewer. |
| Infrastructure | Where data and compute sit, under whose jurisdiction. | A vendor with silent update rights changes model behaviour after approval. |

*Source: Our synthesis.*

Classification tags each use case by the highest layer at which a serious failure could occur, then assigns review accordingly. The nine-category diplomatic risk taxonomy below supplies the vocabulary for what harm a layer might cause; the tier model (Table 5.1b) supplies the how much care. **The ninth category — catastrophic — is why classification can never be cosmetic.** The International AI Safety Report 2026 treats catastrophic AI risk, including escalation and loss of control, as a live policy concern rather than a distant scenario (International AI Safety Report, 2026).

***Table 5.1b  The nine-category diplomatic risk taxonomy***

| \# | Category | Diplomatic example of what can go wrong |
| :---- | :---- | :---- |
| 1 | Epistemic | Confident hallucination — a fluent briefing note that quietly states a wrong figure. |
| 2 | Linguistic-cultural | Lost nuance or culturally tone-deaf phrasing that offends or misleads a counterpart. |
| 3 | Information-integrity | Fabricated sources, deepfakes or manipulated evidence entering the diplomatic record. |
| 4 | Cybersecurity | Prompt injection or poisoned retrieval from a connected classified repository. |
| 5 | Decision | AI distorting or crowding out human judgement in a high-stakes call. |
| 6 | Institutional | Unclear ownership or missing review when something breaks. |
| 7 | Sovereignty | Data or jurisdiction held offshore; vendor control of silent model updates. |
| 8 | Systemic | Contagion across missions and partners; gradual erosion of institutional trust. |
| 9 | Catastrophic | A single failure cascading to bilateral rupture, conflict escalation or loss of life. |

*Source: Authors' synthesis from International AI Safety Report (2026) and NIST AI RMF 1.0 (2023).*

***Table 5.1c  Risk classification matrix for diplomatic AI use cases***

| Tier | Example use case | Sensitivity | Consequence if wrong | Required review |
| :---- | :---- | :---- | :---- | :---- |
| Low | Summarising open-source news; meeting-note tidy-up | Low | Minimal | Self-check; spot review |
| Moderate | Research synthesis for a briefing; first-draft public explainer | Medium | Reputational; minor policy | Named desk officer |
| High | Negotiation position support; consular advice; counterpart risk assessment | High | Bilateral; legal; personal safety | Senior review \+ source verification \+ approval chain |
| Critical | Autonomous action on classified material; external national-position commitment | Highest | National interest; sovereignty | Executive sign-off; legal; recorded authority |

*Source: Our synthesis from NIST AI RMF 1.0 (2023) and our survey and interview data.*

### **Case studies — 5.1  AI Risk Assessment and Classification for Diplomatic Use Cases**

Our survey of 64 diplomatic officers reveals that officers already reason in layers without naming them. Forty-six respondents (71.9%; SE \= 5.6 percentage points; 95% CI: 60.9%–83.0%) spontaneously raised confidentiality or data-leakage concerns — an instinctive infrastructure-layer worry — while 15 (23.4%; SE \= 5.3 pp; 95% CI: 13.0%–33.8%) pointed to high-stakes decisions and negotiations, an institutional-layer concern (Survey for Diplomats, 2026). We classify precisely to make that instinct auditable and actionable.

The International AI Safety Report 2026 underscores why a **model-only classification is inadequate: advanced AI can aggravate existing harms, and failure modes surface only in real-world conditions rather than on a vendor's benchmark** (International AI Safety Report, 2026). This is precisely why the four-layer view is needed — a model that passes a vendor's evaluation may still fail at the application, institutional or infrastructure layers once deployed.

The catastrophic category is not abstract. Consider a scenario drawn from the synthetic-identity breach examined in Chapter 2: a convincing AI-generated message, attributed to a senior official, commits a government to a negotiating position it has not endorsed. If verified too late, such an output could harden positions in an ongoing dispute, endanger a parallel negotiation track or — in the most acute circumstances — contribute to an escalation that proves difficult to reverse. Classification at the Critical tier, with executive sign-off required, is the administrative mechanism designed to prevent exactly that chain of events.

**Entry-level AI safety action (5.1) — model and institutional layers:** Label every AI-assisted task with one line: the layer most likely to fail (model / application / institutional / infrastructure), the tier (Low–Critical), and the name of the reviewer. This habit — tag the layer, tag the tier, name the reviewer — requires no new software and is the seed of a full classification scheme. Chapter 6 develops the vendor-disclosure and sovereignty clauses that underpin the infrastructure-layer tiers described here.

# **5.2  Evaluation, Validation and Continuous Monitoring**

Classification tells a ministry what level of care a use case requires. Evaluation and validation determine whether a system actually deserves that trust — and, as the four-layer model makes clear, the answer differs at every layer. Shevlane et al. (2023) argue that model evaluation is critical for addressing extreme risks because developers must identify dangerous capabilities before deployment, while recognising that models can display new capabilities unforeseen even by their creators.

For diplomacy, the lesson is direct: a tool should not enter sensitive workflows on the strength of a vendor's claim alone. Evaluation must be run at each layer, and the NIST Generative AI Profile — the companion document to the AI RMF 1.0 — supports this by treating evaluation, red-teaming, incident response and lifecycle monitoring as integrated components of organisational risk management rather than one-time gates (National Institute of Standards and Technology, 2023). A model that performs well in chat may behave very differently when connected to classified repositories, email systems, document databases or external communications channels; the full deployed system is the object of evaluation, not the model in isolation.

***Table 5.2  What to evaluate at each layer***

| Layer | What to evaluate |
| :---- | :---- |
| Model | Capability and accuracy on real diplomatic tasks; probe for hallucination, bias, poor calibration. Shevlane's "dangerous-capability evaluation" belongs here. |
| Application | The system as wired: retrieval quality, translation fidelity, draft coherence using the ministry's own documents. A model that passes in chat can fail the moment it touches a cable database. |
| Institutional | Whether officers notice errors, challenge recommendations and retain the expertise to operate without the tool — the human-factor evaluation Ganguli et al. (2022) and the International AI Safety Report 2026 treat as essential. |
| Infrastructure | Continuity: does the workflow survive a vendor outage, a silent model update or a jurisdiction change? Monitoring here is often the only warning that a system has drifted. |

*Source: Our synthesis from Shevlane et al. (2023), Ganguli et al. (2022), NIST AI RMF 1.0 (2023).*

Sidhu and Scholefield et al. (2026) extend this to the post-deployment phase: AI systems may produce failures that pre-deployment assessments do not anticipate, and adequate AI incident governance requires consistent definitions, taxonomies, monitoring practices and reporting mechanisms. Their analysis finds existing frameworks inconsistent in how incidents are defined and classified — a gap that a ministry closes by monitoring at all four layers rather than trusting a one-time model certificate.

### **Case studies — 5.2  Evaluation, Validation and Continuous Monitoring**

Shevlane et al. (2023) show that dangerous capabilities can emerge without developer intent — a model may gain a capacity that no benchmark tested for, which is precisely why model-layer evaluation must be assumption-breaking rather than checklist-based in diplomatic adoption. Our survey reinforces this: 47 of 64 respondents raised accuracy, hallucination or verification concerns unprompted (Survey for Diplomats, 2026), indicating that officers already practise informal validation at the institutional layer and should be given a formal counterpart.

The Deloitte case highlighted in Chapter 3 is instructive at the application layer. A consulting firm submitted a government report containing AI-generated content that had not been verified against primary sources; the document was retracted and a refund agreed (Tadros and Karp, 2025). The lesson for foreign ministries is not that AI cannot assist research but that evaluation of the full application — not the model in isolation — must confirm that retrieval, synthesis and attribution all perform as expected on the ministry's actual documents before that application enters a sensitive workflow.

Open-source tooling makes model-layer evaluation accessible even to ministries with limited technical capacity. Tools such as Garak and Microsoft's PyRIT allow a small team to probe a model for jailbreaks and prompt injection at near-zero cost; running an open-weight model locally via Ollama ensures that diplomatic data never leaves ministry hardware, addressing the infrastructure-layer sovereignty concern at the same time.¹

**Entry-level AI safety action (5.2) — model and application layers:** Before trusting any AI output in a brief or note, apply a one-step rule: find the primary source for the key claim, or do not use the claim. Verifying a single loaded fact against an authoritative source turns passive consumption into active, model-layer validation. Chapter 7 addresses how this habit is scaled into formal training and AI literacy for the service.

# **5.3  Red-Teaming and Adversarial Testing**

Evaluation answers whether a system works as intended under ordinary conditions. Red-teaming asks whether it fails dangerously under pressure. Ganguli et al. (2022) define red-teaming as using manual or automated methods to adversarially probe a language model for harmful outputs, treating it as one essential tool among many for addressing harm. In diplomacy, the threat is not only technical malfunction but deliberate exploitation across the stack.

A concept particularly relevant to diplomatic deployment is sandbox transgression: the risk that a bounded AI assistant — a translator, summariser or drafter — whose access to tools, documents and workflows allows it to act outside its approved assumptions. 

Red-team scenarios for diplomatic systems include: a poisoned briefing document that induces the model to output false attributed statements; an indirect prompt injection embedded in an external report the model retrieves; a translation step that subtly shifts a negotiating position; an agent that sends an unauthorised communication; and a vendor outage that removes analytic capacity during a regional crisis. Each represents a different layer of failure requiring a different probe.

***Table 5.3  What to red-team at each layer***

| Layer | What to probe |
| :---- | :---- |
| Model | Jailbreaks, biased or manipulable outputs, emergent harmful capabilities the vendor did not test. |
| Application | Sandbox transgression — poisoned briefing docs, indirect prompt injection in external reports, translations that shift a negotiating position. |
| Institutional | The human and procedural perimeter — can a synthetic authority induce an officer to skip review, or an agent send an unauthorised communication? |
| Infrastructure | Channel and continuity — can an adversary exploit a vendor's update path, or remove analytic capacity during a crisis? |

*Source: Our synthesis from Ganguli et al. (2022).*

Ganguli et al. (2022) document a scaling behaviour in red-teaming: a model's resistance to adversarial probing changes non-linearly as capability grows. 

This means a ministry's red-team cadence must track model updates rather than be treated as a one-off gate — a direct infrastructure-layer concern, since vendors frequently update silently. Open-source toolkits such as Garak and PyRIT allow a small team to run these probes at near-zero cost; combining them with local open-weight model deployment via Ollama ensures sensitive diplomatic data remains on ministry hardware throughout testing.¹

### **Case studies — 5.3  Red-Teaming and Adversarial Testing**

The Rubio impersonation incident examined in Chapter 2 illustrates an institutional-layer red-team failure: an adversary used AI to generate convincing synthetic communications attributed to a senior official, which reached foreign counterparts before verification was complete (Lee, 2025). A red-team exercise that explicitly tests whether synthetic authority can induce officers to skip the call-back protocol would have surfaced this vulnerability at low cost.

The KLIA travel-advice incident, in which AI-generated guidance led travellers to incorrect conclusions about entry requirements with legal consequences at the border, illustrates an application-layer failure — the system retrieved and synthesised information without verifying the regulatory context (Malay Mail, 2026). A red-team probe that submits an intentionally ambiguous policy document to the application and checks whether the output correctly flags uncertainty would test precisely this failure mode.

The International AI Safety Report 2026 frames adversarial testing as part of a broader evaluation culture across states — a norm Malaysia can import into ASEAN security exercises rather than treat as a vendor service, thereby building regional capacity rather than dependence (International AI Safety Report, 2026).

**Entry-level AI safety action (5.3) — institutional and infrastructure layers:** Treat any unusual instruction or flattering message arriving through a new channel as unverified until authenticated out-of-band. A junior officer's daily habit of calling back on a known number for anything unexpected is, in miniature, the red-teaming lesson Ganguli et al. (2022) describe: assume the plausible is potentially adversarial. Chapter 6 addresses how this practice is embedded in procurement standards and vendor accountability clauses.

# **5.4  Internal AI Guidelines, Escalation Protocols and Safe-Use Policies for Foreign Ministries**

Classification, evaluation and red-teaming are necessary but insufficient unless embodied in clear internal rules and a working escalation path. Read through the four layers, the guideline must specify something at each.

***Table 5.4  What internal AI guidelines must specify at each layer***

| Layer | What the guideline must specify |
| :---- | :---- |
| Model | Which models are approved for which tiers; prohibition of unvetted models on sensitive work; any deployed model must carry a current evaluation record. |
| Application | What may be entered into a system, what must remain on approved platforms, and constraints on retrieval and tool access. The OWASP Gen AI Top 10 categories — prompt injection, supply-chain risk, excessive agency, data leakage — map here (OWASP, 2024). |
| Institutional | Named human review per tier; who approves tools at missions; and the escalation protocol — who is notified, through what secure channel, on what timeline, with what containment action. The NIST AI RMF Govern function makes accountable, transparent use an organisational prerequisite (National Institute of Standards and Technology, 2023). |
| Infrastructure | Data-residency and jurisdiction rules; vendor-update notification requirements; continuity and exit clauses — the sovereignty dimension the guideline must not omit. |

*Source: Authors' synthesis from NIST AI RMF 1.0 (2023), OWASP Gen AI Top 10 (2024), and MOSTI National Guidelines on AI Governance and Ethics (2024).*

Our survey points to a readiness gap these guidelines must close: only 15 of 64 respondents agreed that procedures for using AI were clear and systematic (23.4%; SE \= 5.3 pp; 95% CI: 13.0%–33.8%), while 31 disagreed (Survey for Diplomats, 2026). 

The MOSTI National Guidelines on AI Governance and Ethics supply national principles — privacy, security, transparency, accountability — but those require translation into foreign-affairs operating rules (Ministry of Science, Technology and Innovation Malaysia, 2024). The Public Sector AI Adoption Guidelines establish parallel requirements for data classification and vendor disclosure at the agency level; the foreign-affairs translation of both is addressed in Chapter 6\.

The guideline and protocol are **most effective when anchored to a diplomatic AI safety case: a structured, evidence-backed argument that a deployment is acceptably safe for a defined use**. For each significant use case, the ministry documents the intended purpose, prohibited uses, users and affected parties, data classification, model and vendor, tools and permissions, known limitations, evaluation results, red-team results, human decision points, incident-response procedures, fallback arrangements, and conditions for suspension. This converts "responsible AI" into something approvable and auditable.

Our interviews reinforce that guidance is only as strong as the training that carries it. Ambassador Zamshari Shaharan was direct: awareness cannot be built by announcing that AI exists; officers need to understand hallucination, prompting, source limits and the boundary between personal and official use, and "you need to do training."² Training and guideline are two faces of the same requirement — the institution must make safe use the path of least resistance.

***Figure 5.4  Escalation-protocol flow for AI incidents in diplomatic work***

   ┌────────────────────────────────────────────────┐

   │  Anomaly detected (any layer)                  │

   └──────────────────────┬─────────────────────────┘

                          │

              ┌───────────▼────────────┐

              │  Confirmed incident?    │

              └───┬───────────────┬────┘

                 No              Yes

                  │               │

             Log & monitor   ┌────▼──────────────────────────────────┐

                             │ CONTAIN: out-of-band auth,             │

                             │ freeze output, secure channel          │

                             └────────────────┬──────────────────────┘

                                              │

                             ┌────────────────▼──────────────────────┐

                             │ NOTIFY: owner \+ security \+ legal       │

                             │ within agreed SLA                      │

                             └────────────────┬──────────────────────┘

                                              │

                             ┌────────────────▼──────────────────────┐

                             │ CLASSIFY: Tier (5.1c) \+ layer of origin│

                             │ Triage: severity \+ national-interest   │

                             └────────────────┬──────────────────────┘

                                              │

                 ┌────────────────────────────▼───────────┐

                 │ Critical/High? → Executive/legal sign-off│

                 └────────────────────────────┬───────────┘

                                              │

                             ┌────────────────▼──────────────────────┐

                             │ Post-incident review → revise guideline│

                             │ \+ safety case → feeds back to 5.1–5.3  │

                             └───────────────────────────────────────┘

*Source: Our synthesis from Sidhu & Scholefield (2026), NIST AI RMF 1.0 (2023), OWASP Gen AI Top 10 (2024).*

### **Case studies — 5.4  Internal AI Guidelines, Escalation Protocols and Safe-Use Policies**

Our survey's readiness gap — only 15 of 64 officers found AI procedures clear and systematic — is itself the mandate. Guidelines written along the four layers close exactly the ambiguity officers report, giving each layer a named responsible party and a defined action chain.

Sidhu and Scholefield (2026) find that incident definitions are inconsistent across regulators globally, meaning that our safety-case template is not a bureaucratic extra but the **only reliable internal record of what was tested, by whom, and with what result**. It also serves as the seed of the regional incident database that Chapters 6 and 7 propose for ASEAN-level cooperation.

The Deloitte case (Chapter 3\) demonstrates what the absence of a safety case produces at scale. No documented evaluation record, no named reviewer, no suspension condition — and the consequence was a AU$440,000 contract refund and reputational damage (Croft, 2025). A safety case would have required the firm to specify, before deployment, what verification was applied to AI-assisted research and under what conditions the tool was not to be used.

**Entry-level AI safety action (5.4) — institutional layer:** Keep a one-page personal rule sheet: what I may paste into AI, what I never paste, and who I call if something looks wrong. Distributing this to every officer — not just AI champions — is the cheapest possible safe-use policy and the foundation the full guideline builds on. Chapter 7 positions the ministry as a shaper of regional AI-safety training standards that extend this discipline across ASEAN.

# **5.5  Technical AI Governance for Foreign Affairs**

For a foreign ministry, technical governance is not about building an evaluation harness — it is about knowing what questions to ask of vendors and partners. 

A diplomat negotiating a digital-partnership agreement, a cyber attaché assessing a counterpart's AI capacity, or a mission evaluating whether to adopt a foreign-hosted system all benefit from a working literacy in the levers that determine what an AI system can do before a diplomat ever touches it.

Technical governance strengthens the model layer by establishing what capabilities a system has before deployment; underpins the application layer by constraining what the deployed system is allowed to do; sets the standard the institutional layer enforces as a condition of adoption; and bears most directly on the infrastructure layer by asking who controls compute, supply chains and update paths.

Three technical governance levers are increasingly relevant to foreign affairs. 

1. The first is evaluation of dangerous capabilities: the practice Shevlane et al. (2023) and Shah et al. (2024) describe as identifying, before deployment, whether a model can enable harmful acts such as manipulation or cyber offence.   
2. The second is compute governance — the argument, advanced by Ramiah et al. (2025) in a proposal for a global "compute governance" regime with a pause mechanism, that the large clusters used to train frontier models are a tractable control point for international assurance.   
3. The third is hardware-level governance, where Ansari (2026) offers a feasibility taxonomy for verifying compliance and even treaty obligations at the chip and data-centre level.

The UK AISI's Emerging Processes for Frontier AI Safety (2023) and the Emerging Practices in Frontier AI Safety Frameworks review (Frontier Safeguards, 2025\) show these ideas moving from theory into state practice, while the International AI Safety Report 2026 situates them in a multilateral agenda that Malaysia can engage through ASEAN. The governance need is therefore **twofold: externally, Malaysia should be able to represent its interests in emerging compute and safety frameworks; internally, it should require vendors to disclose capability-evaluation and incident-history information as a condition of adoption**.

### **Case studies — 5.5  Technical AI Governance for Foreign Affairs**

The Rubio synthetic-identity breach (Chapter 2\) is also a technical governance failure at the platform level: identity assurance is now a model-and-channel property, not only a human protocol. The technical levers described here — capability evaluation, compute assurance, hardware verification — are what would have constrained the underlying system before it could be weaponised for impersonation.

The International AI Safety Report 2026 demonstrates the multilateral track: states are already building shared vocabularies for frontier risk, and Malaysia's ASEAN chairmanship experience in strategic communication (Chapter 1\) positions it to shape rather than inherit those vocabularies (International AI Safety Report, 2026).

Ramiah et al.'s (2025) compute-governance proposal illustrates a concrete diplomatic artefact — a verifiable "pause button" for frontier model training — that a middle power can champion as a confidence-building measure in ASEAN forums. This is precisely the kind of technical-governance contribution that translates AI safety expertise into diplomatic leverage.

**Entry-level AI safety action (5.5) — model and infrastructure layers:** When evaluating any AI tool for mission use, ask the vendor three questions: what dangerous-capability testing did you run, where is my data stored, and what is your incident-reporting history? Demanding these answers shifts the burden of proof to the supplier and is the user-facing edge of technical governance — no technical depth required.

# **5.6  From Model Safety to Diplomatic System Safety**

The preceding sections have treated AI safety as a sequence of practices: classify, evaluate, red-team, govern. This final section reframes them as layers of a single object — the AI-enabled foreign-affairs system. The central point is that safety cannot be located in the model alone. A ministry that procures a well-evaluated model has addressed only the bottom of a stack.

The model layer carries capability, hallucination, bias and uncertainty. 

The application layer is where retrieval, translation, summarisation, drafting and decision support actually run. 

The institutional layer comprises workflows, authorisation, accountability and human review — the routines this chapter has argued are non-negotiable. 

The infrastructure layer is cloud, data centres, networks, identity, APIs and vendors — the substrate a ministry rarely controls when it adopts commercial models.

A system may perform well at the model layer and still be unsafe because it retrieves poisoned information, holds excessive access to diplomatic files, emits output that is accepted without review, is silently changed by a vendor update, or simply cannot be operated when the service is withdrawn. 

The International AI Safety Report 2026 treats technical safeguards, monitoring, evaluation and institutional risk management as complementary rather than interchangeable — the same posture this chapter has taken throughout (International AI Safety Report, 2026).

The implication is the book's central argument about diplomacy applied at the system level: technical safety is necessary but not sufficient. 

It does not determine political legitimacy, acceptable risk, or the distribution of power. From trusting the model, the ministry moves to governing the entire workflow — and, at the infrastructure layer, to the sovereignty question of who controls data, operations, updates and jurisdiction. Chapter 6 takes up the sovereign and governance dimensions of that distribution; Chapter 7 addresses how the service builds the capacity to sustain it.

***Figure 5.6  The four-layer AI-enabled foreign-affairs system and its failure modes***

   ┌──────────────────────────────────────────────────────────────┐

   │  \[1\] MODEL LAYER                                             │

   │  Capability · Hallucination · Bias · Uncertainty            │

   └──────────────────────────────┬───────────────────────────────┘

                                  │ feeds

   ┌──────────────────────────────▼───────────────────────────────┐

   │  \[2\] APPLICATION LAYER                                       │

   │  Retrieval · Translation · Summarisation · Drafting          │

   │  Decision support                                            │

   └──────────────────────────────┬───────────────────────────────┘

                                  │ governs

   ┌──────────────────────────────▼───────────────────────────────┐

   │  \[3\] INSTITUTIONAL LAYER                                     │

   │  Workflows · Authorisation · Accountability · Human review   │

   └──────────────────────────────┬───────────────────────────────┘

                                  │ hosted on

   ┌──────────────────────────────▼───────────────────────────────┐

   │  \[4\] INFRASTRUCTURE LAYER                                    │

   │  Cloud · Data centres · Networks · Identity · APIs · Vendors │

   └──────────────────────────────┬───────────────────────────────┘

                                  │

   Failure modes that cross layers:

   · Model safe → but retrieves poisoned data (layers 1→2)

   · Output accepted without review (layers 2→3)

   · Vendor silently updates / service withdrawn (layer 4→all)

   · Institutional gap means no one sees the failure (layer 3\)

                                  │

                    ┌─────────────▼──────────────┐

                    │  DIPLOMATIC SYSTEM UNSAFE   │

                    │  despite safe model         │

                    └─────────────────────────────┘

*Source: Our synthesis from International AI Safety Report (2026) and the four-layer system model.*

### **Case studies — 5.6  From Model Safety to Diplomatic System Safety**

Our survey's readiness gap is most acute at the institutional layer: only 15 of 64 officers (23.4%; SE \= 5.3 pp) found AI procedures clear and systematic (Survey for Diplomats, 2026). This is precisely where the four-layer model must be made operational first. A system-safety posture is only as strong as the institutional layer that enforces it; without clear procedures and named reviewers, the model, application and infrastructure layers are invisible to the officers using them.

The travel-advice and synthetic-identity incidents drawn on throughout this chapter are not model failures alone but failures that propagate upward through all four layers. In the KLIA case, the model retrieved information that was technically accurate in some contexts but misleading given the regulatory specifics; the application layer failed to flag uncertainty; no institutional reviewer was named; and the infrastructure hosting the service was outside the traveller's verification reach. The four-layer model predicts exactly this pattern (Malay Mail, 2026).

The International AI Safety Report 2026 is itself the proof of the four-layer thesis at the policy level: it treats technical safeguards, monitoring, evaluation and institutional risk management as complementary rather than interchangeable — the same posture this chapter has maintained (International AI Safety Report, 2026). For Malaysia, building these routines is also a regional opportunity: a foreign ministry that can speak credibly about capability evaluation, compute governance and system-level resilience is better placed to contribute to ASEAN AI safety norms than one that merely adopts tools.

**Entry-level AI safety action (5.6) — all four layers:** Before adopting any AI tool, map it on one page across the four layers: which model, which application, which approval process, whose servers. Circle the layer you do not control. That single map reveals where dependence lives and is the seed of the full system-safety view described in this chapter.

# **Conclusion**

AI safety in diplomacy is not a separate subject from the craft itself; it is the craft adapted to a new instrument. This chapter has treated safety as a set of operational routines rather than an aspiration.

Classification gives each use case its due level of care, building on Chapter 1's augmentation premise by deciding where human review is mandatory. Evaluation and monitoring establish whether a system earns trust and keeps watch after deployment, answering the verification problem Chapter 3 identified as the technology's central limitation. Red-teaming probes how systems fail under pressure, hardening against the impersonation and manipulation risks of Chapter 2\. Guidelines and escalation protocols ensure that human authority is never ambiguous and that failure, when it occurs, is contained rather than compounded — the operational expression of Chapter 4's accountability principles.

The distinction drawn at the opening — between AI safety, cybersecurity and information security — runs through all six sections. Securing a network does not make a model truthful. Protecting data does not make a summary faithful. Evaluating a system for adversary resistance is necessary but insufficient if its own emergent behaviour is unexamined. AI safety addresses the behaviour of systems that generate, infer and decide, often without a human seeing the moment of error.

For Malaysia, **building these routines is also a regional opportunity.** A foreign ministry that can demonstrate disciplined, documented safeguard practice — and speak credibly about capability evaluation, compute governance, hardware assurance and system-level resilience — is better placed to contribute to ASEAN AI safety norms than one that merely adopts tools. The safeguards described here exist so that technology gives diplomats more time and analytical space to do what the profession has always required: understand, persuade, negotiate and exercise judgement on behalf of the state.

This chapter has been the operational core — the safeguards a ministry can run today. The book now turns outward. Chapter 6 steps from internal routine to the institutional and international frame: the governance frameworks, procurement and sovereignty clauses, and cross-border cooperation that make safe use durable across ministries and partners. Chapter 7 asks how the service builds the capacity to sustain it — AI literacy, training needs and Malaysia's role in shaping regional AI-safety norms.

# **Endnotes**

1\. Garak, PyRIT and Ollama are open-source tools not yet in the project Drive corpus. Per the new-file workflow, these are listed in "Proposed Additional Sources" below and must be added to the /CHAPTER 5 Drive folder before finalisation.

2\. Interview with Ambassador Zamshari Shaharan, clean verbatim transcription, conducted by Dr Murni Wan Mohd Nor, 2026\. Quotation preserved verbatim.

# **References**

Ansari, S. (2026). Hardware-level governance of AI compute: A feasibility taxonomy for regulatory compliance and treaty verification. arXiv:2604.04712. [https://arxiv.org/abs/2604.04712](https://arxiv.org/abs/2604.04712)

Croft, D. (2025, October 9). Deloitte to refund government after using AI in $440k report. Accounting Times.

Frontier Safeguards. (2025). Emerging practices in frontier AI safety frameworks. [https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/67aa1ef13654dc168a71e83a\_EmergingPracticesInFrontierAISafetyFrameworksA.pdf](https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/67aa1ef13654dc168a71e83a_EmergingPracticesInFrontierAISafetyFrameworksA.pdf)

Ganguli, D., Lovitt, L., Kernion, J., Askell, A., Bai, Y., Kadavath, S., … (2022). Red teaming language models to reduce harms: Methods, scaling behaviors, and lessons learned. arXiv:2209.07858. [https://arxiv.org/abs/2209.07858](https://arxiv.org/abs/2209.07858)

International AI Safety Report. (2026). International AI Safety Report 2026\. [https://internationalaisafetyreport.org/sites/default/files/2026-02/international-ai-safety-report-2026.pdf](https://internationalaisafetyreport.org/sites/default/files/2026-02/international-ai-safety-report-2026.pdf)

Lee, M. (2025, July 9). Impostor uses AI to impersonate Rubio and contact foreign and US officials. Associated Press.

Malay Mail. (2026, March 30). AI travel advice backfires: Israelis detained at KLIA during transit, envoy warns against Malaysia trips.

Ministry of Science, Technology and Innovation Malaysia. (2024). The National Guidelines on AI Governance & Ethics (AIGE).

National Institute of Standards and Technology. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST. [https://doi.org/10.6028/NIST.AI.100-1](https://doi.org/10.6028/NIST.AI.100-1)

Generative AI Profile (companion to AI RMF 1.0). NIST. [https://www.nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework)

OWASP. (2024). OWASP Gen AI Security Project — Top 10 for LLM Applications. [https://genai.owasp.org/](https://genai.owasp.org/)

Ramiah, A. A., Koopmanschap, R., Thorsteinson, J., & Khan, S. (2025). Toward a global regime for compute governance: Building the pause button. arXiv:2506.20530. [https://arxiv.org/abs/2506.20530](https://arxiv.org/abs/2506.2530)

Shah, R., Irpan, A., Turner, A. M., Wang, A., … (2024). An approach to technical AGI safety and security. arXiv:2504.01849. [https://arxiv.org/abs/2504.01849](https://arxiv.org/abs/2504.01849)

Shevlane, T., Farquhar, S., Garfinkel, B., Phuong, M., Whittlestone, J., Leung, J., … (2023). Model evaluation for extreme risks. arXiv:2305.15324. [https://arxiv.org/abs/2305.15324](https://arxiv.org/abs/2305.15324)

Sidhu, H. K., Scholefield, R., Annan, N., Hernandez, K., Hou, I. N., Alshaikhi, A., Chin, Z. S., & Gipiškis, R. (2026). Open problems in AI incident governance. arXiv:2607.05163. [https://arxiv.org/abs/2607.05163](https://arxiv.org/abs/2607.05163)

Survey for Diplomats: Innovating Diplomacy (Responses). (2026). Unpublished survey dataset \[64 responses\]. Institute of Diplomacy and Foreign Relations.

Tadros, E., & Karp, P. (2025, October 5). Deloitte to refund government, admits using AI in $440k report. Australian Financial Review.

UK AISI. (2023). Emerging processes for frontier AI safety. [https://assets.publishing.service.gov.uk/media/653aabbd80884d000df71bdc/emerging-processes-frontier-ai-safety.pdf](https://assets.publishing.service.gov.uk/media/653aabbd80884d000df71bdc/emerging-processes-frontier-ai-safety.pdf)

