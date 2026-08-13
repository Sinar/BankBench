For **_Innovating Diplomacy_**, your contribution can frame AI safety not as a purely technical concern, but as a condition for **safe, sovereign, and accountable diplomatic statecraft**.

A strong central argument would be:

> AI can improve diplomatic capacity only when ministries can understand, evaluate, constrain, and, where necessary, discontinue the systems on which they rely. AI safety is therefore not separate from diplomacy: it concerns the protection of judgment, communication, institutional autonomy, and national sovereignty.

## Suggested scope

The book should cover AI use across the foreign-affairs ecosystem:

- Ministry of Foreign Affairs headquarters.
- Embassies, consulates, and permanent missions.
- Diplomatic academies and training institutions.
- National security, intelligence, trade, immigration, and development agencies.
- Government communication and public-diplomacy units.
- Crisis-management and emergency-communications systems.
- External vendors, cloud providers, model developers, and local technology firms.
- International organisations and diplomatic networks.

This avoids reducing “diplomatic AI” to chatbots used by individual officers. The relevant object is an **AI-enabled foreign-affairs system** consisting of models, data, tools, people, institutions, vendors, and infrastructure.

## Proposed core chapter

I suggest adding a dedicated chapter after Chapter 4 or before Chapter 5:

# Chapter 5: Safe and Sovereign Intelligent Statecraft

This can then make the existing AI Safety chapter more directly relevant to diplomacy.

### 5.1 AI Safety as a Diplomatic Capacity

- AI safety as protection against error, misuse, loss of control, and institutional dependency.
- Why technical safety is necessary but not sufficient for governance.
- The relationship between model safety, system safety, organisational safety, and national resilience.
- From “trusting the model” to governing the entire AI-enabled workflow.
- Safety as a precondition for legitimate delegation.

The key argument should be that technical safety provides the evidence and control mechanisms that make governance meaningful. However, it does not determine political legitimacy, acceptable risk, or the distribution of power. The 2026 International AI Safety Report similarly treats technical safeguards, monitoring, evaluation, and institutional risk management as complementary rather than interchangeable. [internationalaisafetyreport](https://internationalaisafetyreport.org/sites/default/files/2026-02/international-ai-safety-report-2026.pdf)

### 5.2 From Model Safety to Diplomatic System Safety

This section could distinguish four layers:

1. **Model layer:** capability, hallucination, bias, refusal, uncertainty.
2. **Application layer:** retrieval, translation, summarisation, drafting, decision support.
3. **Institutional layer:** workflows, authorisation, accountability, human review.
4. **Infrastructure layer:** cloud, data centres, networks, identity, APIs, and vendors.

A system may perform well at the model layer but still be unsafe because:

- it retrieves poisoned information;
- it has excessive access to diplomatic files;
- its output is accepted without review;
- a vendor changes the model without notice;
- the ministry cannot operate when the service is unavailable.

### 5.3 Diplomatic Risk Taxonomy

Organise risks according to the harm they can cause:

- **Epistemic risks:** fabricated facts, false citations, incorrect analysis.
- **Linguistic and cultural risks:** translation distortion, pragmatic misunderstanding, offensive or misleading phrasing.
- **Information-integrity risks:** deepfakes, impersonation, synthetic diplomatic statements.
- **Cybersecurity risks:** prompt injection, data exfiltration, malicious documents, tool abuse.
- **Decision risks:** automation bias, over-reliance, unexamined recommendations.
- **Institutional risks:** deskilling, weakened accountability, loss of institutional memory.
- **Sovereignty risks:** foreign jurisdiction, vendor lock-in, service withdrawal, model dependence.
- **Systemic risks:** shared vendors or models producing correlated errors across ministries or states.
- **Catastrophic risks:** rare failures that create irreversible diplomatic escalation, major national-security compromise, or prolonged loss of critical state capacity.

### 5.4 Diplomatic AI Safety Cases

Introduce the idea of a **safety case**: a structured argument, supported by evidence, that a particular AI deployment is acceptably safe for a defined use.

Each safety case should specify:

- intended purpose;
- prohibited uses;
- users and affected parties;
- data classification;
- model and vendor;
- available tools and permissions;
- known limitations;
- evaluation results;
- red-team results;
- human decision points;
- incident-response procedures;
- fallback arrangements;
- conditions for suspension or withdrawal.

This would translate the abstract idea of “responsible AI” into something that a ministry can approve, audit, and revisit.

### 5.5 Evaluation and Red-Teaming for Foreign Affairs

This is your strongest technical contribution.

The book could propose evaluation across:

- factual accuracy and source reliability;
- multilingual and low-resource-language performance;
- cultural and diplomatic nuance;
- uncertainty calibration;
- prompt-injection resistance;
- confidential-data protection;
- tool-use safety;
- impersonation and deepfake resilience;
- crisis communication;
- model-update stability;
- vendor outage and fallback performance.

Red-teaming should test not only the model but the full system:

- Can a malicious document manipulate the model?
- Can retrieved content cause data leakage?
- Can an agent send an unauthorised message?
- Can a model generate a false attribution?
- Can an attacker exploit language switching?
- Can staff be socially engineered through AI-generated diplomatic content?
- Can the system be safely shut down during a crisis?

NIST’s Generative AI Profile is useful here because it treats red-teaming, incident response, evaluation, and lifecycle monitoring as parts of organisational risk management rather than as optional technical exercises. [nist](https://www.nist.gov/itl/ai-risk-management-framework)

## Sovereignty and foreign vendors

A second new chapter or major section should address infrastructure.

# Chapter 6: Sovereignty, Vendors, and the Diplomatic AI Supply Chain

This is especially relevant to Wisma Putra because using Gemini, Claude, OpenAI, or other commercial models involves more than data privacy. It involves dependence on foreign infrastructure and foreign corporate decisions.

### 6.1 The Diplomatic AI Supply Chain

Map the layers:

- Data and archives.
- Model provider.
- Cloud and compute provider.
- Identity and access management.
- Retrieval and document systems.
- APIs and software integrations.
- Human operators and contractors.
- Audit, monitoring, and incident-response providers.

### 6.2 Six Dimensions of AI Sovereignty

A useful framework comes from Canada’s sovereign-AI infrastructure discussion, which identifies sovereignty across:

- data;
- infrastructure;
- operations;
- technological origin and supply chain;
- freedom to choose among solutions;
- legal jurisdiction. [ised-isde.canada](https://ised-isde.canada.ca/site/spectrum-management-telecommunications/sites/default/files/documents/Sovereign-AI-Infrastructure-Resilience-v2-Eng.pdf)

For foreign affairs, add a seventh:

- **diplomatic continuity:** the ability to continue essential functions if a vendor is unavailable, politically restricted, compromised, or commercially withdrawn.

Territorial data residency alone is therefore insufficient. A server may be located in Malaysia while the software, keys, administrators, updates, legal obligations, and incident-response authority remain externally controlled.

### 6.3 Vendor Dependency as Foreign-Policy Risk

Discuss:

- foreign export controls;
- sanctions and procurement restrictions;
- vendor safety policies;
- model-access withdrawal;
- cloud outages;
- silent model updates;
- dependency on one provider;
- inability to migrate prompts, evaluations, or workflows;
- foreign access requests;
- concentration of diplomatic data and institutional memory.

The Brookings discussion of AI sovereignty is useful for presenting sovereignty as a spectrum rather than as complete self-sufficiency. Similarly, the framework on AI infrastructure sovereignty defines sovereignty as the ability to design, operate, and control AI systems without excessive dependence on external actors. [brookings](https://www.brookings.edu/wp-content/uploads/2026/02/20260217_AI_sovereignty_final.pdf)

### 6.4 Sovereign, Hybrid, and Non-Sovereign Workloads

The book could propose three deployment categories:

- **Non-sovereign:** public information, generic drafting, non-sensitive translation.
- **Hybrid:** internal policy analysis and administrative work, subject to contractual and technical controls.
- **Sovereign or nationally controlled:** classified material, diplomatic cables, negotiation red lines, intelligence-informed assessments, crisis communications, and systems affecting national-security decisions.

The argument need not be “never use foreign vendors”. It should be:

> Dependence must be consciously classified, tested, diversified, and bounded according to diplomatic consequence.

### 6.5 Vendor Governance Requirements

Recommend procurement clauses covering:

- no training on government content without explicit authorisation;
- model-version notification;
- audit and evaluation access;
- incident reporting;
- data deletion and retention;
- subcontractor disclosure;
- location and jurisdiction of processing;
- continuity and service-level requirements;
- portability and exit;
- independent security testing;
- emergency suspension;
- government-controlled logging and evidence preservation.

## Diplomacy as a safety function

The book should also show that ministries are not merely users of AI governance. They are potential **designers of international AI safety norms**.

# Chapter 7: Diplomacy for AI Safety and Global Resilience

### 7.1 Foreign Ministries as AI Safety Actors

Foreign ministries can contribute through:

- confidence-building measures;
- international incident reporting;
- crisis communication protocols;
- norms against impersonating officials;
- cooperation on synthetic-media authentication;
- coordination on cyber-enabled AI threats;
- safe information exchange;
- diplomatic engagement with AI vendors;
- regional evaluation and red-teaming initiatives.

### 7.2 AI Safety for Middle Powers

For Malaysia and ASEAN, the focus should be practical rather than maximalist:

- preserve strategic autonomy without seeking total technological autarky;
- develop domestic inference capacity for priority workloads;
- diversify vendors;
- build local evaluation expertise;
- test Malay and other regional languages;
- develop shared ASEAN standards;
- support public-interest and non-extractive AI providers;
- retain manual and non-AI fallback systems.

The recent literature on AI infrastructure sovereignty is particularly relevant because it treats control over compute, networks, operations, and legal jurisdiction as a resilience issue rather than simply a technology-development issue. [arxiv](https://arxiv.org/html/2602.10900v4)

### 7.3 Diplomatic AI Safety Cooperation

Possible initiatives:

- ASEAN diplomatic-AI safety working group.
- Shared multilingual benchmark.
- Regional red-team exercises.
- Foreign-ministry incident database.
- Crisis protocols for AI-generated false statements.
- Common procurement principles for LLM vendors.
- Regional secure-compute or inference infrastructure.
- Joint training for diplomats, cybersecurity officers, and procurement officials.

## Revised book argument

The book could be organised around this progression:

1. Diplomacy is becoming AI-mediated.
2. AI-mediated diplomacy creates new epistemic, security, institutional, and sovereignty risks.
3. These risks cannot be managed by vendor assurances or ethics principles alone.
4. Technical evaluation, red-teaming, monitoring, and secure infrastructure make governance enforceable.
5. Governance must also address accountability, law, legitimacy, international coordination, and political economy.
6. Foreign ministries can become active participants in shaping safer and more sovereign AI ecosystems.

A concise thesis for the book would be:

> **Innovating Diplomacy** examines how AI is transforming diplomatic practice and argues that meaningful innovation requires more than adoption. It requires the capacity to evaluate, constrain, audit, and govern AI systems across their full lifecycle—from models and data to vendors, infrastructure, institutions, and international relations.

And a more specific thesis for your contribution:

> AI safety in diplomacy is the preservation of human and institutional control over AI-mediated judgment, communication, and infrastructure. A diplomatic AI system is safe only when its failures are detectable, its actions are bounded, its decisions remain contestable, its dependence is manageable, and the ministry can continue operating when the system or vendor fails.

That framing gives your AI safety background a clear role in the book without making the project purely technical. It connects evaluation and red-teaming to the actual concerns of foreign affairs: **trust, crisis stability, national security, sovereignty, continuity, and diplomatic accountability**.

## Proposed single chapter

# Chapter X: Safe and Sovereign Diplomacy in the Age of AI

This chapter can be the book’s main contribution on AI safety. It should argue that **innovating diplomacy is not simply about adopting AI tools; it is about preserving human judgment, institutional accountability, operational continuity, and national agency while using them**.

AI safety is therefore treated as a diplomatic and foreign-affairs concern—not only as a technical discipline. Technical evaluations, red-teaming, monitoring, and secure infrastructure are necessary because they make governance claims testable. However, they are not sufficient: law, institutional accountability, international cooperation, and political legitimacy are also required. This balanced position is consistent with the International AI Safety Report, NIST’s AI Risk Management Framework, and current work on AI sovereignty and managed interdependence. [internationalaisafetyreport](https://internationalaisafetyreport.org/sites/default/files/2026-02/international-ai-safety-report-2026.pdf)

## 1. AI and the transformation of diplomatic authority

### 1.1 From digital tools to AI-mediated statecraft

- AI-assisted translation, drafting, research, scenario analysis, communication, and knowledge management.
- The difference between a chatbot, retrieval system, agent, and decision-support system.
- AI as part of a larger socio-technical system involving people, institutions, vendors, data, and infrastructure.

### 1.2 What must remain human

- Political judgment.
- Interpretation of ambiguity and context.
- Responsibility for official statements.
- Negotiation strategy and diplomatic discretion.
- Decisions involving national security, escalation, sanctions, and crisis response.

### 1.3 The foreign-affairs AI ecosystem

Scope the chapter across:

- Foreign ministries.
- Embassies, consulates, and permanent missions.
- Diplomatic academies.
- National-security and intelligence agencies.
- Trade, immigration, development, and public-communication agencies.
- External model vendors, cloud providers, and system integrators.

This prevents the discussion from treating AI safety as merely an individual diplomat’s “prompt hygiene” problem.

## 2. The risk landscape for diplomatic AI

### 2.1 Epistemic and linguistic risks

- Hallucinated facts, sources, or quotations.
- False confidence and poor uncertainty calibration.
- Outdated information and knowledge-cutoff problems.
- Translation errors and culturally inappropriate interpretation.
- Misreading diplomatic ambiguity, politeness, irony, or indirect speech.
- Low-resource-language and regional-context failures.

### 2.2 Information integrity and foreign influence

- Deepfakes and impersonation of ministers, ambassadors, and officials.
- Fabricated diplomatic statements and forged correspondence.
- AI-generated influence operations.
- Automated multilingual persuasion.
- The “liar’s dividend”, where genuine communications are dismissed as fake.
- Difficulty attributing synthetic content to a state or non-state actor.

### 2.3 Cybersecurity and sandbox transgression

- Prompt injection and indirect prompt injection.
- Malicious documents entering retrieval systems.
- Data exfiltration through connected tools.
- Model or system-prompt extraction.
- Unauthorised email, file, browser, or database actions.
- Excessive agency in AI agents.
- Compromised APIs, plugins, models, or cloud infrastructure.

The key concept here is **sandbox transgression**: a system appears to be a bounded assistant, but its access to tools, documents, and workflows allows it to act outside the assumptions under which it was approved.

### 2.4 Institutional and systemic risks

- Automation bias and over-reliance.
- Deskilling and loss of institutional memory.
- Common vendors creating correlated failure across agencies.
- Model updates changing behaviour without adequate review.
- Vendor outages during a diplomatic crisis.
- Foreign governments or companies affecting access to critical AI capabilities.
- Loss of public trust in official communication.

### 2.5 Catastrophic and high-consequence risks

The chapter should define “catastrophic” in a foreign-affairs context without relying only on speculative AGI scenarios:

- A false AI-generated assessment contributes to crisis escalation.
- A compromised system exposes sensitive diplomatic communications.
- Synthetic messages create confusion between governments during a rapidly developing event.
- A cyberattack assisted by AI disrupts foreign-ministry or critical financial systems.
- A shared model or cloud failure affects multiple ministries simultaneously.
- A vendor becomes unavailable because of sanctions, export controls, geopolitical conflict, or commercial failure.
- The ministry loses the ability to operate independently because essential institutional knowledge has been externalised into a foreign AI platform.

## 3. From technical AI safety to diplomatic governance

### 3.1 Technical safety as a necessary foundation

Explain that meaningful governance requires technical means to:

- evaluate capabilities;
- identify dangerous failure modes;
- test safeguards;
- monitor systems;
- control access;
- investigate incidents;
- secure model weights and data;
- verify compliance;
- suspend or shut down unsafe deployments.

This is the strongest and most defensible version of the argument that technical AI safety is essential to governance. Governance cannot reliably regulate systems that it cannot evaluate or monitor.

### 3.2 Why technical safety is not sufficient

Technical measures cannot decide:

- Which diplomatic uses are legitimate.
- What level of risk is politically acceptable.
- Who should be accountable.
- Whether foreign dependence is compatible with national sovereignty.
- How harms should be remedied.
- Which values should govern an AI system.
- Whether a ministry should adopt a system at all.

The chapter should therefore reject both extremes:

- **technological solutionism:** “better engineering will solve governance”; and
- **governance without technical capacity:** “principles and policies are enough without testing or enforcement.”

### 3.3 The diplomatic AI safety case

For each significant use case, the ministry should document:

- intended purpose;
- users and affected groups;
- data classification;
- model and vendor;
- tools and permissions;
- known limitations;
- evaluation results;
- red-team findings;
- human approval points;
- incident-response procedures;
- fallback arrangements;
- conditions for suspension or withdrawal.

This converts “responsible AI” from a general aspiration into an evidence-based deployment decision.

## 4. Evaluating and red-teaming diplomatic AI

### 4.1 Evaluation dimensions

A diplomatic AI evaluation framework should assess:

- factual accuracy;
- source reliability;
- uncertainty calibration;
- multilingual and cultural competence;
- privacy and confidential-data protection;
- prompt-injection resistance;
- tool-use safety;
- resistance to impersonation and manipulation;
- robustness under crisis conditions;
- consistency after model updates;
- human ability to detect and correct errors.

### 4.2 Model-level versus system-level evaluation

A model can be safe in a chat interface but unsafe when connected to:

- classified repositories;
- email;
- diplomatic document-management systems;
- browsers;
- databases;
- external communication channels;
- automated workflow systems.

Evaluation must therefore examine the complete system rather than relying solely on vendor benchmarks.

### 4.3 Red-team scenarios

Use controlled, fictional, and non-operational scenarios such as:

- a poisoned briefing document;
- an indirect prompt injection in an external report;
- an AI-generated false statement attributed to a foreign minister;
- a translation that changes a negotiation position;
- a request to reveal confidential cable content;
- an attempt to make an agent send an unauthorised communication;
- a vendor outage during a regional crisis;
- coordinated misinformation targeting multiple diplomatic missions.

### 4.4 Human factors

Evaluate whether diplomats:

- over-trust fluent outputs;
- notice uncertainty;
- independently verify sources;
- challenge model recommendations;
- understand the model’s limitations;
- retain sufficient expertise to operate without it.

Safety depends not just on model performance but on whether humans can exercise meaningful control.

## 5. Sovereignty, vendors, and infrastructure

### 5.1 AI sovereignty as strategic choice

The chapter should avoid presenting sovereignty as complete technological self-sufficiency. A more realistic concept is **managed interdependence**: preserving strategic choice while using external capabilities where appropriate. [brookings](https://www.brookings.edu/wp-content/uploads/2026/02/20260217_AI_sovereignty_final.pdf)

Ask:

- Who controls the data?
- Who controls the infrastructure?
- Who operates the system?
- Who controls the model and updates?
- Which jurisdiction applies?
- Can the ministry switch providers?
- Can it continue operating during an outage or political dispute?

### 5.2 Workload classification

Propose three deployment categories:

- **Non-sovereign workloads:** public statements, public-information translation, generic administrative drafting.
- **Controlled hybrid workloads:** internal analysis and policy support under strong contractual and technical controls.
- **Sovereign or nationally controlled workloads:** classified material, negotiation red lines, intelligence-informed assessments, crisis communications, and national-security decisions.

### 5.3 Vendor governance

Require contracts to address:

- data use and retention;
- model training;
- model updates;
- audit rights;
- incident notification;
- subcontractors;
- jurisdiction and access;
- portability;
- service continuity;
- exit and migration;
- independent evaluation;
- government-controlled logging;
- emergency suspension.

### 5.4 Infrastructure resilience

Maintain:

- vendor diversity;
- manual fallback procedures;
- alternative models;
- independent records and archives;
- local or regional inference capacity for priority functions;
- the ability to suspend AI without paralysing the ministry.

AI sovereignty should therefore be presented as a question of **agency, continuity, and freedom of choice**, not autarky.

## 6. A practical governance model for foreign ministries

Conclude the chapter with a compact model:

### Govern

- Assign accountability.
- Establish approved and prohibited uses.
- Create an AI safety and security function.
- Include diplomats, cybersecurity experts, legal officers, procurement specialists, and language experts.

### Map

- Identify data, stakeholders, vendors, tools, harms, and dependencies.
- Classify use cases by sensitivity, agency, and consequence.

### Measure

- Conduct capability evaluations.
- Test robustness, security, privacy, multilingual performance, and human factors.
- Red-team the entire workflow.
- Re-evaluate after model or system changes.

### Manage

- Apply least privilege.
- Require human approval for high-impact actions.
- Maintain audit logs and incident response.
- Use vendor diversification and fallback systems.
- Suspend or retire systems when risk exceeds the approved threshold.

This adaptation of NIST’s Govern–Map–Measure–Manage approach gives the chapter a practical backbone. [nist](https://www.nist.gov/itl/ai-risk-management-framework)

## Proposed chapter conclusion

End with this claim:

> **Innovating diplomacy with AI requires more than adopting powerful models. It requires preserving the conditions under which diplomatic judgment remains humanly accountable, institutionally governable, operationally resilient, and nationally sovereign. Technical AI safety makes those conditions testable; diplomacy, law, and public institutions determine how they should be used.**

This single chapter would integrate your contribution across the book’s existing themes:

- Chapter 1: AI-mediated statecraft.
- Chapter 2: real-world and systemic risks.
- Chapter 3: limitations and uncertainty.
- Chapter 4: accountability and human control.
- Chapter 5: evaluation, red-teaming, and safe use.
- Chapter 6: vendor sovereignty and international governance.
- Chapter 7: Malaysian and Global South capacity.
- Chapter 8: training, resilience, and institutional implementation.

A suitable final title is:

# **Chapter X: Safe and Sovereign Diplomacy in the Age of AI**

Alternative titles:

- **Governing AI-Mediated Diplomacy**
- **When Diplomacy Leaves the Sandbox**
- **AI Safety, Sovereignty, and Intelligent Statecraft**
- **From Model Safety to Diplomatic Resilience (I like this)**