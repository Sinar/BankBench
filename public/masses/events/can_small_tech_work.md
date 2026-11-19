Here are 30 questions organised into six connected strands for *Can Small Tech Work?* They move from philosophy and public debate to practical experiments, inclusion, governance, and industry-building.

I would treat this as a **curriculum** to draw from—not a commitment to run 30 events immediately. Each question could become a reading circle, panel conversation, workshop, essay, or project clinic.

For each, I suggest two readings: a starting point and a companion that adds depth or a contrasting perspective. The list mixes books, journal articles, conference papers, reports, and practical handbooks; it does not force every format into every session. Repeated texts are intentional, allowing participants to build a shared vocabulary without buying or reading 60 separate works.

## Strand A — What does “small tech” actually mean?

### 1. Small in what sense: size, cost, ownership, complexity, or power?

Use this as the opening question. Ask participants to distinguish a small device from a small organisation, a decentralised system, and a technology people can meaningfully control.

- Start — E. F. Schumacher, *Small Is Beautiful: Economics as if People Mattered* (book, 1973), especially “Buddhist Economics.” A foundational argument for assessing economic arrangements through human needs rather than output alone. [centerforneweconomics](https://centerforneweconomics.org/publications/buddhist-economics/)
- Companion — Ivan Illich, *Tools for Conviviality* (book, 1973). Shifts the discussion from physical size to whether tools support people’s autonomy and chosen purposes. [arl.human.cornell](https://arl.human.cornell.edu/linked%20docs/Illich_Tools_for_Conviviality.pdf)

Session output: a shared definition of “small,” with examples that meet one criterion but fail another.

### 2. When does a tool empower us—and when does it make us dependent?

Examine the difference between being able to use a product and being able to understand, alter, repair, or refuse it.

- Start — Illich, *Tools for Conviviality* (book), particularly its account of convivial tools and institutional dependence. [arl.human.cornell](https://arl.human.cornell.edu/linked%20docs/Illich_Tools_for_Conviviality.pdf)
- Companion — *Explore Community Technology* (practical curriculum), especially its introduction and digital-stewardship activities. It connects technology with mutual learning, collective governance, and community control. [communitytechnology.github](https://communitytechnology.github.io/docs/intro-ct/)

Session output: an “agency audit” of a familiar app, AI service, or community tool.

### 3. Is technological progress always about making something new?

A useful discussion for a bookshop audience: what happens when novelty receives more recognition than reliability, upkeep, or care?

- Start — Andrew Russell and Lee Vinsel, “Hail the Maintainers” (public essay, *Aeon*, 2016). An accessible introduction to the maintenance perspective. [cultureofrepair](https://www.cultureofrepair.org/academic-research)
- Companion — Lee Vinsel and Andrew L. Russell, *The Innovation Delusion: How Our Obsession with the New Has Disrupted the Work That Matters Most* (book, 2020). Develops the distinction between useful change and “innovation-speak.” [spectrum.ieee](https://spectrum.ieee.org/decoding-the-innovation-delusion-nurturing-the-maintenance-mindset)

Session output: a map of essential local work that rarely gets called innovation.

### 4. Can ordinary people be technology producers rather than merely consumers?

Explore the difference between consultation, customisation, user innovation, and genuine participation in development.

- Start — Eric von Hippel, *Free Innovation* (book, 2016). Examines innovations developed by people for their own needs and shared freely. [muse.jhu](https://muse.jhu.edu/book/60817)
- Companion — *Explore Community Technology* (practical curriculum), focusing on participatory planning and peer learning. [communitytechnology.github](https://communitytechnology.github.io/docs/intro-ct/)

Session output: a collection of participant-created workarounds worth developing further.

### 5. When should we choose a simpler technology—or no new technology at all?

Make this a comparative workshop, not an argument that old tools are inherently better.

- Start — Low-tech Magazine, “Low-tech Solutions” collection (articles and practical guides). Explores combinations of older approaches, new knowledge, and different material choices. [solar.lowtechmagazine](https://solar.lowtechmagazine.com/low-tech-solutions/)
- Companion — Schumacher, “Buddhist Economics” (essay). Provides a framework for questioning the resources consumed to meet a need. [centerforneweconomics](https://centerforneweconomics.org/publications/buddhist-economics/)

Session output: three responses to one problem—manual, simple digital, and technically sophisticated—with explicit trade-offs.

## Strand B — Can small, local AI be genuinely useful?

### 6. What can an AI running on an ordinary computer actually do well?

Keep this empirical: participants should evaluate a bounded task rather than debate “AI capability” in general.

- Start — AMD, “What is llama.cpp?” (technical documentation). Introduces a framework for language-model inference on CPUs and GPUs. [rocmdocs.amd](https://rocmdocs.amd.com/projects/llama-cpp/en/docs-25.09/what-is-llama-cpp.html)
- Companion — *A Survey of Small Language Models* (research survey, arXiv preprint, 2024). Covers small-model architectures, training, compression, and resource constraints. [arxiv](https://arxiv.org/html/2410.20011)

Session output: a task-and-hardware report documenting successes, failures, and setup requirements.

### 7. When is a smaller AI model preferable to a larger one?

Consider quality alongside memory, latency, affordability, and the conditions under which a model must operate.

- Start — *A Survey of Small Language Models* (research survey, preprint, 2024), focusing on its discussion of constraints and optimisation approaches. [arxiv](https://arxiv.org/html/2410.20011)
- Companion — Roy Schwartz, Jesse Dodge, Noah A. Smith, and Oren Etzioni, “Green AI” (*Communications of the ACM*, 2020; earlier preprint 2019). Argues that efficiency should be an evaluation criterion alongside performance. [dl.acm](https://dl.acm.org/doi/10.1145/3381831)

Session output: a model-selection rubric that does not automatically reward the biggest model.

### 8. Does running AI locally make it private, safe, or independent?

Treat these as separate claims to investigate, not benefits to assume from the word “local.”

- Start — NIST, *AI Risk Management Framework 1.0* (framework, 2023). Supplies a structure for examining risks across a system’s context, design, use, and evaluation. [nist](https://www.nist.gov/itl/ai-risk-management-framework)
- Companion — AMD, “What is llama.cpp?” (technical documentation). Establishes what local inference means technically, allowing the group to distinguish execution location from broader governance questions. [rocmdocs.amd](https://rocmdocs.amd.com/projects/llama-cpp/en/docs-25.09/what-is-llama-cpp.html)

Session output: a dependency and data-flow diagram covering the model, software, documents, updates, and operators.

### 9. How do we know whether a small AI system is good enough for a real task?

Move from impressive demonstrations to documented acceptance criteria.

- Start — Margaret Mitchell and colleagues, “Model Cards for Model Reporting” (conference paper, FAT*, 2019). A foundation for documenting intended uses, evaluation, and limitations. [airc.nist](https://airc.nist.gov/docs/AI_RMF_Playbook.pdf)
- Companion — NIST, *AI RMF Playbook* (practical guide), especially its measurement and management guidance. [airc.nist](https://airc.nist.gov/docs/AI_RMF_Playbook.pdf)

Session output: a small test set, a minimum acceptable result, and a model card.

### 10. Can local-language AI be built with communities rather than merely for them?

Use Bahasa Melayu, code-switching, or another participant-selected language context as the workshop application—not as an assumed property of existing models.

- Start — Masakhane’s account of its grassroots language-technology community and participatory research approach (project articles and research gateway). It offers a comparative case from African-language NLP, not evidence about Malaysian-language performance. [masakhane](https://www.masakhane.io/)
- Companion — Timnit Gebru and colleagues, “Datasheets for Datasets” (*Communications of the ACM*, 2021). Provides questions about data motivation, composition, collection, uses, and maintenance. [airc.nist](https://airc.nist.gov/docs/AI_RMF_Playbook.pdf)

Session output: a community-reviewed language-data and evaluation plan, including consent, credit, and compensation.

## Strand C — Can small experiments advance ambitious energy and space technologies?

For Razlan’s strand, distinguish small experiments toward space-based solar power from claims that a small orbital system already offers viable electricity supply.

### 11. What has space-based solar power actually demonstrated—and what remains unproven?

This should be an evidence-reading session before a speculative futures discussion.

- Start — Caltech, “In a First, Caltech’s Space Solar Power Demonstrator Wirelessly Transmits Power in Space” (institutional research article, 2023). Read carefully for the difference between experimental transmission and useful electricity delivery. [caltech](https://www.caltech.edu/about/news/in-a-first-caltechs-space-solar-power-demonstrator-wirelessly-transmits-power-in-space)
- Companion — NASA Office of Technology, Policy, and Strategy, *Space-Based Solar Power* (technical-policy report, 2024). Examines conceptual systems, costs, emissions, uncertainties, and development challenges. [nasa](https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf)

Session output: a claims table labelled “demonstrated,” “modelled,” “assumed,” and “still unknown.”

### 12. What useful contribution can a small team make to a very large technological system?

Explore subsystem development without implying that a successful component establishes whole-system feasibility.

- Start — Caltech, “Caltech to Launch Space Solar Power Technology Demo into Orbit in January” (institutional article, 2023). Introduces the demonstrator’s separate experimental components. [caltech](https://www.caltech.edu/about/news/caltech-to-launch-space-solar-power-technology-demo-into-orbit-in-january)
- Companion — NASA, *Systems Engineering Handbook*, Revision 2 (handbook, 2016). Use selected sections on requirements, system decomposition, interfaces, and verification. [nasa](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)

Session output: a subsystem opportunity map with dependencies and required expertise.

### 13. What is the cheapest experiment that would genuinely reduce uncertainty?

“Cheap” should mean proportionate to the question—not merely visually impressive or easy to demonstrate.

- Start — NASA, *Systems Engineering Handbook* (handbook), focusing on verification, validation, and technical assessment. [nasa](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)
- Companion — NASA, “Technology Readiness Levels” (explanatory article). Helps distinguish basic principles, laboratory proof of concept, relevant-environment testing, and operational performance. [nasa](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/)

Session output: an experiment brief with a hypothesis, measurement, success threshold, and explicit limitations.

### 14. When would space solar be preferable to terrestrial solar, storage, or other alternatives?

Let participants challenge the premise rather than requiring them to defend the technology.

- Start — NASA, *Space-Based Solar Power* (report, 2024), particularly the comparative cost and sensitivity analyses. [nasa](https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf)
- Companion — NASA, “New Study Updates NASA on Space-Based Solar Power” (accessible article, 2024). Summarises the study’s assumptions, capability gaps, and findings about terrestrial alternatives. [nasa](https://www.nasa.gov/directorates/stmd/space-based-solar-power-report/)

Session output: a comparison sheet specifying the application, alternatives, assumptions, and conditions that would change the conclusion.

### 15. Can communities shape energy systems without owning every part of the infrastructure?

This connects the space discussion to a more immediate question about participation and ownership in energy.

- Start — Gill Seyfang, Jung Jin Park, and Adrian Smith, “A thousand flowers blooming? An examination of community energy in the UK” (*Energy Policy*, 2013). An empirical study of community-energy initiatives and their opportunities and vulnerabilities. [econpapers.repec](https://econpapers.repec.org/RePEc:eee:enepol:v:61:y:2013:i:c:p:977-989)
- Companion — *Explore Community Technology* (practical curriculum). Use its collective-governance questions as a comparative exercise rather than as an energy-engineering manual. [communitytechnology.github](https://communitytechnology.github.io/docs/intro-ct/)

Session output: an energy-governance map distinguishing users, owners, operators, regulators, and affected communities.

## Strand D — What would technological diversity look like?

This is a possible co-designed strand with AOD: not just increasing representation at events, but examining who defines problems, makes decisions, and can challenge outcomes.

### 16. Who gets to decide which problems technology should solve?

Start before product design: whose inconvenience becomes an investment opportunity, and whose needs remain invisible?

- Start — Sasha Costanza-Chock, *Design Justice: Community-Led Practices to Build the Worlds We Need* (book, 2020), introduction and selected cases. The full text is open access. [designjustice.mitpress.mit](https://designjustice.mitpress.mit.edu/)
- Companion — *Explore Community Technology* (practical curriculum), particularly activities for identifying community-defined digital-justice issues. [communitytechnology.github](https://communitytechnology.github.io/docs/intro-ct/)

Session output: a problem-selection process in which affected participants can reject or reframe the proposed problem.

### 17. Is diversity in technology about who participates—or also about which technologies exist?

Distinguish representation within one dominant system from the possibility of different systems and institutional arrangements.

- Start — Costanza-Chock, *Design Justice* (book). Connects design decisions with structural inequality and community leadership. [designjustice.mitpress.mit](https://designjustice.mitpress.mit.edu/)
- Companion — “Introduction to the special issue on Digital Solidarity Economies” (*Internet Policy Review*, 2026). Introduces cooperation, mutual aid, shared ownership, and alternative infrastructure governance. [policyreview](https://policyreview.info/articles/analysis/introduction-digital-solidarity-economies)

Session output: a “technology choices” map covering commercial services, public provision, cooperatives, community tools, and non-digital approaches.

### 18. Can a technology work well on average and still fail particular communities?

Make the session about how to recognise uneven outcomes rather than assuming a single overall score is sufficient.

- Start — Mitchell and colleagues, “Model Cards for Model Reporting” (conference paper, 2019). Provides a basis for documenting performance across relevant conditions and groups. [airc.nist](https://airc.nist.gov/docs/AI_RMF_Playbook.pdf)
- Companion — Ruha Benjamin, *Race After Technology: Abolitionist Tools for the New Jim Code* (book, 2019). Offers a broader analysis of how technological systems can reproduce racial hierarchy; discuss its relevance and limits when applying it to Malaysia. [designjustice](https://designjustice.org/external-resources)

Session output: an evaluation plan that reports meaningful differences instead of only an overall average.

### 19. What makes participation meaningful rather than tokenistic?

Ask what participants can actually change—and whether they have the time, resources, and authority to do so.

- Start — Costanza-Chock, *Design Justice* (book), focusing on community-led practice and the distribution of benefits and decision-making. [designjustice.mitpress.mit](https://designjustice.mitpress.mit.edu/)
- Companion — *Explore Community Technology* (practical curriculum), especially participatory planning, mutual learning, and collective self-governance. [communitytechnology.github](https://communitytechnology.github.io/docs/intro-ct/)

Session output: a participation agreement specifying decision rights, payment, credit, withdrawal, and feedback.

### 20. Can people refuse a technology without losing access to an essential service?

A strong public-panel question: when does “convenience” become an obligation to adopt?

- Start — Illich, *Tools for Conviviality* (book). Its account of tools that do not impose an obligation to use them supplies the central provocation. [arl.human.cornell](https://arl.human.cornell.edu/linked%20docs/Illich_Tools_for_Conviviality.pdf)
- Companion — OECD, *Digital Public Infrastructure for Digital Governments* (policy paper, 2024). Provides a contemporary institutional perspective on human-centred infrastructure, rights, safeguards, and governance. [oecd](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/12/digital-public-infrastructure-for-digital-governments_11fe17d9/ff525dc8-en.pdf)

Session output: a service-design proposal with an alternative access route and a practical appeal mechanism.

## Strand E — Can small tech support public accountability and shared infrastructure?

This strand would be a natural discussion to develop with Sinar Project, while leaving its actual contribution to be agreed.

### 21. Can a small civic-tech project produce public value without becoming a large platform?

Keep the focus on a narrow public-information need and an identifiable group of users.

- Start — Sinar Project, “About Sinar Project” and its partner profile (organisational and case material). Introduces its combination of open technology, open data, and policy analysis. [sinarproject](https://sinarproject.org/about)
- Companion — OECD, *Digital Public Infrastructure for Digital Governments* (policy paper, 2024). Provides a contrasting perspective on shared, interoperable systems and public governance. [oecd](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/12/digital-public-infrastructure-for-digital-governments_11fe17d9/ff525dc8-en.pdf)

Session output: a one-page public-value brief with a user, task, evidence of need, and realistic scope.

### 22. What should be shared infrastructure, and what should remain locally controlled?

Explore the tension between useful common foundations and excessive centralisation.

- Start — OECD, *Digital Public Infrastructure for Digital Governments* (policy paper, 2024). Covers shared systems, interoperability, safeguards, and multi-stakeholder governance. [oecd](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/12/digital-public-infrastructure-for-digital-governments_11fe17d9/ff525dc8-en.pdf)
- Companion — Illich, *Tools for Conviviality* (book). Supplies a critical counterpoint about institutional scale and the relationship between tools and autonomy. [arl.human.cornell](https://arl.human.cornell.edu/linked%20docs/Illich_Tools_for_Conviviality.pdf)

Session output: an architecture diagram marking what is centralised, federated, locally operated, or optional.

### 23. What would it mean for a community to govern a digital tool together?

Move beyond the label “community-owned” to concrete rules, responsibilities, and dispute resolution.

- Start — *Explore Community Technology* (practical curriculum), focusing on common ownership, digital stewardship, and collective governance. [communitytechnology.github](https://communitytechnology.github.io/docs/intro-ct/)
- Companion — “Introduction to the special issue on Digital Solidarity Economies” (*Internet Policy Review*, 2026). Examines shared ownership and co-governance across digital infrastructures. [policyreview](https://policyreview.info/articles/analysis/introduction-digital-solidarity-economies)

Session output: a draft governance charter covering membership, decisions, responsibilities, conflicts, and exit.

### 24. Is open source enough to make technology accountable?

Separate access to code from the ability to inspect a system, influence decisions, or sustain its operation.

- Start — *Explore Community Technology* (practical curriculum). Adds participation, equity, stewardship, and governance to the discussion of technical openness. [communitytechnology.github](https://communitytechnology.github.io/docs/intro-ct/)
- Companion — von Hippel, *Free Innovation* (book, 2016). Its discussion of freely shared innovation and the difficulties of diffusion helps test what sharing alone accomplishes. [muse.jhu](https://muse.jhu.edu/book/60817)

Session output: an accountability checklist that goes beyond the software licence.

### 25. Can public institutions buy small, testable solutions instead of oversized promises?

Use a simulated procurement exercise rather than presenting this as jurisdiction-specific legal guidance.

- Start — NASA, *Systems Engineering Handbook* (handbook). Adapt its approach to requirements, verification, and validation to a modest public-service problem. [nasa](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)
- Companion — OECD, *Digital Public Infrastructure for Digital Governments* (policy paper, 2024). Adds interoperability, public-interest safeguards, and institutional governance. [oecd](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/12/digital-public-infrastructure-for-digital-governments_11fe17d9/ff525dc8-en.pdf)

Session output: a sample purchasing brief with acceptance criteria, maintenance responsibilities, and an exit plan.

## Strand F — What would make small tech a durable field of work?

This is the bridge from Tintabudi’s public programme to a project-development circle, paid pilots, and longer-term capability-building.

### 26. Who pays for small tech when its benefits are widely shared?

Distinguish paying customers, beneficiaries, contributors, public funders, and sponsors.

- Start — von Hippel, *Free Innovation* (book, 2016). Explores why people innovate without conventional producer incentives and why spreading those innovations can remain difficult. [muse.jhu](https://muse.jhu.edu/book/60817)
- Companion — “Introduction to the special issue on Digital Solidarity Economies” (*Internet Policy Review*, 2026). Broadens the institutional possibilities to cooperative, commons-based, and civic-public arrangements. [policyreview](https://policyreview.info/articles/analysis/introduction-digital-solidarity-economies)

Session output: a funding map that separates public-good work from paid delivery and commercial opportunities.

### 27. Who maintains a tool after the workshop, grant, or founder is gone?

A useful requirement for every project in the series: someone must be able to explain its continuing operation.

- Start — Andrew L. Russell and Lee Vinsel, “After Innovation, Turn to Maintenance” (*Technology and Culture*, 2018). A scholarly argument for treating maintenance as central to technology. [read.uolpress.co](https://read.uolpress.co.uk/read/reframing-failure-in-digital-scholarship-a56118ab-e4eb-4eb4-9dca-e8c343c6441b/section/262fdc42-cc2c-4803-b5aa-9aae85cd44c2)
- Companion — Vinsel and Russell, *The Innovation Delusion* (book, 2020). Develops a maintenance-oriented approach to organisations and technological change. [spectrum.ieee](https://spectrum.ieee.org/decoding-the-innovation-delusion-nurturing-the-maintenance-mindset)

Session output: a maintenance budget, responsibility chart, handover plan, and retirement condition.

### 28. Can repair and adaptation become a credible local industry?

Ask what skills, documentation, spare parts, service arrangements, and recognition would be needed—not merely whether people enjoy tinkering.

- Start — Steven J. Jackson, “Rethinking Repair,” in *Media Technologies: Essays on Communication, Materiality, and Society* (scholarly book chapter, 2014). Treats breakdown and repair as central to understanding technological life. [read.uolpress.co](https://read.uolpress.co.uk/read/reframing-failure-in-digital-scholarship-a56118ab-e4eb-4eb4-9dca-e8c343c6441b/section/262fdc42-cc2c-4803-b5aa-9aae85cd44c2)
- Companion — Low-tech Magazine, “Low-tech Solutions” collection (articles and practical guides). Offers material for discussing adaptation, reuse, and combinations of old approaches with new knowledge. [solar.lowtechmagazine](https://solar.lowtechmagazine.com/low-tech-solutions/)

Session output: a local repair-and-adaptation opportunity map with potential users and required capabilities.

### 29. How can successful small tech spread without losing local control?

Distinguish growing one organisation from helping others replicate, adapt, or federate an approach.

- Start — von Hippel, *Free Innovation* (book, 2016). Its treatment of diffusion and the division of labour between innovators and producers provides one route into the problem. [muse.jhu](https://muse.jhu.edu/book/60817)
- Companion — Seyfang, Park, and Smith, “A thousand flowers blooming?” (*Energy Policy*, 2013). Provides an empirical case of a diverse community-based sector, including its networking needs, vulnerabilities, and dependence on wider policy conditions. [econpapers.repec](https://econpapers.repec.org/RePEc:eee:enepol:v:61:y:2013:i:c:p:977-989)

Session output: a replication plan specifying what must remain common and what others should be free to change.

### 30. How do we decide whether a small-tech project should continue, change direction, or stop?

End with judgment rather than a showcase in which every project must be declared a success.

- Start — NASA, *Systems Engineering Handbook* (handbook). Use its technical-assessment and decision-making material to structure evidence-based review. [nasa](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf)
- Companion — NIST, *AI RMF Playbook* (practical guide). For AI projects, use its governance, measurement, and management prompts to assess whether identified risks are acceptably addressed. [airc.nist](https://airc.nist.gov/docs/AI_RMF_Playbook.pdf)

Session output: a review memo with five sections: usefulness, evidence, risks, operating capacity, and the next decision. Apply the NIST material specifically to AI rather than treating it as a universal standard for every technology.

## How I would package this for the proposed collaboration

Rather than advertise 30 sessions at once, use the questions as the programme’s editorial backbone:

| Format | Purpose | Suggested questions |
|---|---|---|
| Opening panel | Establish the central tension | 1, 2, 17 |
| Tintabudi reading circles | Develop shared concepts and informed disagreement | 3, 5, 16, 20 |
| Local-AI workshop | Test usefulness under real constraints | 6–10 |
| Razlan’s space-energy workshop | Separate ambition, evidence, and experiment design | 11–14 |
| Possible AOD co-designed workshop | Examine participation and technological diversity | 16–20 |
| Possible Sinar Project clinic | Develop accountable public-interest tools | 21–25 |
| Project-development circle | Address funding, maintenance, replication, and stopping | 26–30 |

For an initial six-event season, I would select questions 1, 6, 11, 17, 21, and 27. Together they cover the premise, AI, space energy, diversity, civic technology, and the work of keeping things alive.

Assign only one starting reading or a selected excerpt before each event. Keep the companion reading for facilitators and interested participants. Over time, the 30 questions could become a public essay series, annotated reading catalogue, and collection of documented experiments—not just an events calendar.
