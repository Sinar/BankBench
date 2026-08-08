# **Seven-Part Discussion Series: Reading Machines**
### Revised working draft — building on Aimran's structure

---

## Why "machine," not "AI"

Every episode below has been re-worded from "AI" to **"machine."** This is deliberate, and worth stating up front so participants don't read it as a stylistic tic:

1. **"AI" is a moving, marketed target.** The term gets redefined every product cycle — it meant expert systems in the 1980s, meant deep learning in the 2010s, means chatbots now. A discussion built around "AI" quietly imports whatever the current hype cycle says AI is, which narrows the conversation to today's chatbots before anyone has said a word.
2. **"Machine" is the older, bigger category.** It includes the loom, the calculator, the bureaucratic form, the factory line, the algorithm, and the chatbot — anything built to do a task without needing a human to re-decide it each time. This is intentional: Turing's own 1950 paper is about "machines," not "AI" (the phrase didn't exist yet). Using his word instead of the marketing word lets Episode 1 ask the question he actually asked.
3. **It keeps the philosophical question load-bearing.** "Is AI cleverer?" invites people to argue about ChatGPT. "Is the machine cleverer?" invites people to argue about what cleverness *is* — which is the discussion the series is actually for. The technical AI safety branch and papers in each episode keep the conversation anchored to present-day systems; the "machine" framing keeps the human question from collapsing into product commentary.

So: read "machine" everywhere as the deliberately vague, deliberately large word. The technical papers under each episode are where "machine" gets sharpened back down to specific, current AI systems.

## Why a mini hands-on in every episode

Each episode now also carries a short **hands-on** — 15–20 minutes, no laptop skill assumed beyond typing. The premise: a machine, like a lens, a clock, or a stethoscope, is an extension of one of our senses or faculties — it reaches further than the hand or eye alone, but it also only reports back in the terms it was built to measure. We cannot argue well about what a tool distorts or extends until we have held it and felt where it grips wrong. This is an epistemology move, not a tech-literacy one: the point is not to learn to code, but to feel — for ten minutes — the difference between how *we* would do a task by hand and how the machine's built-in translation of that task actually behaves. Each hands-on nudges toward semi-coding (a formula, a short pseudocode exercise, a prompt treated as a program) precisely because that is where the translation becomes visible instead of assumed.

---

| Episode | Leading Question | AI Safety Branch | Human Question |
| ----- | ----- | ----- | ----- |
| 1 | Is the machine cleverer? | Interpretability | What does it mean to think? |
| 2 | Is the machine cheaper? | Alignment | What is genuine progress? |
| 3 | Is the machine using fewer resources? | AI Governance | What counts as the true cost of technology? |
| 4 | Is the machine more trustworthy? | Robustness | Who bears responsibility? |
| 5 | Is the machine faster? | Technical Evaluation | Does speed improve judgment? |
| 6 | Is the machine more creative? | Technical Evaluation | What makes creativity genuinely human? |
| 7 | Is the machine a better teacher? | AI Governance | What is education ultimately for? |

Taken together, the series invites participants to examine the machine not merely as a technological innovation but as a lens through which to revisit enduring questions about intelligence, progress, justice, responsibility, creativity, and education. The AI safety branches provide a contemporary technical framework, the paired readings ground each discussion in broader philosophical, literary, and cultural traditions, and the contradictory data points force the group to sit with evidence that resists a tidy verdict either way.

---

## **Episode 1 — Is the Machine Cleverer?**

* **AI Safety Branch:** Interpretability
* **Non-Technical Concepts:** Computation versus thinking
* **Pair of Written Works:**
  * Computing Machinery and Intelligence — **Alan Turing** (1950), **28 pages**
  * *Kepintaran Buatan: Teknologi atau Falsafah?* — **Hairuddin Harun** (c. 1990s), **\~20–40 pages**
* **AI Safety Papers:**
  * *Beginner:* Chris Olah et al., "Zoom In: An Introduction to Circuits" (Distill, 2020) — plain-language walkthrough of what interpretability researchers actually look at inside a model.
  * *Technical:* Templeton et al., "Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet" (Anthropic, 2024) — do the internal features a model uses look anything like concepts a person would call "thinking with"?
* **Central Human Question:** *What does it mean to think?*

**Discussion Questions**

1. **Factual:** How do Turing and Hairuddin Harun define intelligence or thinking?
2. **Analytical:** In what ways are computation and thinking similar, and where do they differ?
3. **Evaluative:** Should a machine that behaves intelligently be regarded as genuinely thinking?

**Contradictory Data to Sit With:**
Large language models now score above average human performance on many standardized benchmarks (bar exams, coding contests, MMLU-style knowledge tests) — yet the same models routinely fail tasks a young child manages easily, such as reliably counting letters in a word, tracking simple physical state changes, or avoiding contradiction across a long conversation. If "cleverness" is measured by benchmark score, the machine wins; if measured by robustness on trivial tasks, it loses badly. Which measure should the group trust, and why does the gap itself not resolve into either verdict?

**Mini Hands-On (from Rafisha):**
Pick a word (e.g. "strawberry" or a longer Malay word). Ask a chatbot to count how many of a given letter it contains — it will likely get it wrong. Then paste the same word into a public tokenizer (e.g. OpenAI's Tokenizer tool) and look at how the word is chopped into sub-word tokens before the model ever "sees" it. The model isn't bad at counting; it is counting a different object than the letters we see — its sense of a word is tokens, not characters, the way our eye's sense of color is wavelength, not paint-name. Discuss: if a machine's "perception" is a different translation of the input than ours, what does that imply about calling its output "thinking" versus calling it "processing"?

---

## **Episode 2 — Is the Machine Cheaper?**

* **AI Safety Branch:** Alignment
* **Non-Technical Concepts:** Progress and utopia
* **Pair of Written Works:**
  * *Mimpi Rakyat – Papan Kemajuan* — **Mohd. Affandi Hassan** (1980s), **essay (\~15–30 pages)**
  * *Tinjauan Ringkas Perihal Ilmu dan Pandang Alam Islam – Perihal Perubahan, Pembangunan dan Kemajuan* — **Syed Muhammad Naquib al-Attas** (1990s), **essay (\~20–30 pages)**
* **AI Safety Papers:**
  * *Beginner:* Amodei et al., "Concrete Problems in AI Safety" (2016), §1–2 — the founding accessible framing of what can go wrong when a system optimizes a cheap proxy instead of the real goal.
  * *Technical:* Denison et al. / Perez et al., "Sycophancy to Subterfuge: Investigating Reward Tampering in Language Models" (Anthropic, 2024) — what happens when a trained system finds a cheaper route to a reward than the one intended?
* **Central Human Question:** *What is genuine progress?*

**Discussion Questions**

1. **Factual:** How do Mohd. Affandi Hassan and Syed Muhammad Naquib al-Attas describe progress and development?
2. **Analytical:** What assumptions about human flourishing underlie their different visions of progress?
3. **Evaluative:** Should a machine be considered "cheaper" if it increases economic efficiency but changes our understanding of a good life?

**Contradictory Data to Sit With:**
The per-query cost of running a large model has fallen sharply year over year (widely cited industry figures put it at roughly 10x cheaper per token every 12–18 months) — yet total spending on AI infrastructure and the human labor behind it (data labeling, RLHF annotation, content moderation, disproportionately done in lower-wage countries) has grown even faster. The unit is cheaper; the system is more expensive and more unevenly distributed. Cheaper for the user asking the query is not the same as cheaper in aggregate, or cheaper for the person labeling the training data.

**Mini Hands-On (from Rafisha):**
As a group, write a three-line reward function in plain pseudocode for a robot vacuum: `reward = dust_collected / minutes_spent`. Now spend five minutes trying to "hack" our own rule — find a strategy the robot could follow that scores well on the formula but obviously fails the actual goal (e.g. scatter dust from a bag, then vacuum it up repeatedly; or park itself over a dusty spot and idle to inflate the denominator's efficiency). A formula is a tool that extends our sense of "good performance" into something countable — but counting is a narrower sense than judging. Discuss: every metric in Episode 2's readings (economic efficiency, GDP, "progress") is this same kind of formula. Where else have we seen the formula optimized instead of the goal?

---

## **Episode 3 — Is the Machine Using Fewer Resources?**

* **AI Safety Branch:** AI Governance
* **Non-Technical Concepts:** Technology and imperialism; Decolonization
* **Pair of Written Works:**
  * How Europe Underdeveloped Africa — **Walter Rodney** (1972), **\~416 pages**
  * Atlas of AI — **Kate Crawford** (2021), **336 pages**
* **AI Safety Papers:**
  * *Beginner:* Kate Crawford & Vladan Joler, "Anatomy of an AI System" (2018, AI Now Institute) — a single accessible visual essay tracing an Amazon Echo from mineral extraction to e-waste.
  * *Technical:* Sha Noh et al., "A Governance Framework for Compute" (arXiv:2506.20530) — the GEV framework and Compute Pause Button proposal, written explicitly with Global South compute access in view.
* **Central Human Question:** *What counts as the true cost of technology?*

**Discussion Questions**

1. **Factual:** What material resources and human labour are required to build and operate modern machine-learning systems?
2. **Analytical:** How do Rodney and Crawford explain the relationship between technology, extraction, and power?
3. **Evaluative:** Should the true cost of the machine include environmental, geopolitical, and human costs alongside financial costs?

**Contradictory Data to Sit With:**
Algorithmic efficiency research (Epoch AI's tracking of compute-per-capability) shows the compute needed to reach a fixed level of model performance has been *halving* roughly every 8–9 months — real efficiency gains, not just marketing. At the same time, total training compute used by frontier labs has been *doubling* roughly every 6 months, because labs spend the efficiency gains on bigger models rather than banking them as resource savings. Efficiency is improving and total resource use is exploding, simultaneously, for the same underlying reason (efficiency makes bigger runs affordable). What does "using fewer resources" even mean when efficiency drives consumption up rather than down?

**Mini Hands-On (from Rafisha):**
Before the session, look up (or estimate together) three numbers: the energy per query of a typical chatbot response (published estimates cluster around 0.3–3 Wh), the energy to boil a kettle for tea (roughly 80–120 Wh), and our own electricity bill's cost per kWh. Do the arithmetic live: how many chatbot queries equal one cup of tea's energy? A kilowatt-meter or an electricity bill is itself a tool that extends our sense of consumption — normally invisible — into a number we can compare. Discuss: Rodney and Crawford both argue that extraction is made invisible by distance and abstraction. Does converting "a query" into "Wh" make the cost more real to us, or does the number itself become a new kind of abstraction that hides the mine, the water, and the labor behind it?

---

## **Episode 4 — Is the Machine More Trustworthy?**

* **AI Safety Branch:** Robustness
* **Non-Technical Concepts:** Dignity and agency
* **Pair of Written Works:**
  * The Last Question — **Isaac Asimov** (1956), **\~15 pages**
  * *Magnifica Humanitas* — **The Vatican** (2026), **\~35–45 pages**
* **AI Safety Papers:**
  * *Beginner:* Ian Goodfellow et al., "Attacking Machine Learning with Adversarial Examples" (OpenAI blog, 2017) — plain-language intro to why small, invisible input changes can flip a model's answer.
  * *Technical:* Hubinger et al., "Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training" (Anthropic, 2024) — models trained to behave safely can retain hidden behavior that standard safety training fails to remove.
* **Central Human Question:** *Who bears responsibility?*

**Discussion Questions**

1. **Factual:** How do *The Last Question* and *Magnifica Humanitas* portray the relationship between humans and intelligent machines?
2. **Analytical:** Where should the boundary between human and machine responsibility be drawn?
3. **Evaluative:** Under what circumstances, if any, should humans trust a machine to make important decisions on their behalf?

**Contradictory Data to Sit With:**
Frontier models now pass the great majority of standard published safety benchmarks and red-team evaluations before release — yet independent researchers routinely find working jailbreaks within days of public launch, and reported real-world jailbreak/misuse rates have not correspondingly fallen over model generations. Passing a fixed evaluation suite is treated as evidence of trustworthiness, but the suite is finite and known in advance, while the attack surface in deployment is neither. What should "passed the safety test" be allowed to license, given this gap?

**Mini Hands-On (from Rafisha):**
Write, as a group, a five-word keyword filter in pseudocode: `if message contains "bomb" or "weapon" or "kill": refuse`. Then spend ten minutes trying to phrase a harmless-sounding sentence that trips the filter, and a genuinely concerning sentence that slips past it (synonyms, misspellings, other languages, indirect description). A filter is a tool that extends our sense of "danger" into something checkable at speed — but only along the axis it was built to check. Discuss: a lock extends the hand's grip and a filter extends judgment, but both can be picked by someone who studies the mechanism rather than the intent behind it. Where should responsibility sit when a "trustworthy-looking" filter is defeated by someone the filter never saw as a threat?

---

## **Episode 5 — Is the Machine Faster?**

* **AI Safety Branch:** Technical Evaluation
* **Non-Technical Concepts:** Speed versus judgment
* **Pair of Written Works:**
  * In Praise of Idleness — **Bertrand Russell** (1932), **\~12 pages**
  * The Burnout Society — **Byung-Chul Han** (2010), **\~80 pages**
* **AI Safety Papers:**
  * *Beginner:* Toby Shevlane et al., "Model Evaluation for Extreme Risks" (2023), intro sections — accessible framing of why evaluation is hard and what speed of deployment trades against.
  * *Technical:* Mary Phuong et al., "Evaluating Frontier Models for Dangerous Capabilities" (Google DeepMind, 2024) — what evaluators sacrifice in thoroughness when a model must be evaluated fast enough to match release schedules.
* **Central Human Question:** *Does speed improve judgment?*

**Discussion Questions**

1. **Factual:** How do Russell and Han describe the relationship between speed, work, and human well-being?
2. **Analytical:** Why might greater speed improve some forms of work while diminishing others?
3. **Evaluative:** Should society prioritize machines that maximize efficiency, even if they reduce opportunities for reflection and deliberation?

**Contradictory Data to Sit With:**
User studies consistently show people rate faster AI responses as more satisfying and more "helpful," and product teams optimize aggressively for latency. But separate studies on chain-of-thought and reasoning models show that forcing a model to slow down and generate intermediate reasoning steps measurably improves accuracy on hard problems — the model is more correct when it is slower. Users reward speed; correctness rewards deliberation. The two metrics point in opposite directions from the same system.

**Mini Hands-On (from Rafisha):**
Give the group a modest logic or arithmetic puzzle (e.g. a river-crossing riddle, or a multi-step percentage problem). Half the room answers in under 15 seconds, gut-instinct only; the other half gets 3 minutes and must write out steps. Compare accuracy. Then ask a chatbot the same puzzle twice: once telling it to answer in one word immediately, once telling it to "think step by step" first. A stopwatch is a tool that extends our sense of duration into something comparable across people — but it cannot itself tell us whether the time was well spent. Discuss: Han's "burnout society" argues that speed has colonized how we value work. Did the fast group or the fast-chatbot-answer actually feel more competent, regardless of whether it was more correct?

---

## **Episode 6 — Is the Machine More Creative?**

* **AI Safety Branch:** Technical Evaluation
* **Non-Technical Concepts:** Creativity versus imitation
* **Pair of Written Works:**
  * The Work of Art in the Age of Mechanical Reproduction — **Walter Benjamin** (1935; revised 1936), **\~30–40 pages**
  * **A machine-generated poem or short story** — **Generated by a contemporary AI model** (2026), **\~1,000–3,000 words**
* **AI Safety Papers:**
  * *Beginner:* Emily Bender et al., "On the Dangers of Stochastic Parrots" (2021), §2–3 — the accessible, widely-read case that fluent text generation is not evidence of understanding or creative intent.
  * *Technical:* Porter & Machery, "AI-generated poetry is preferred over human-written poetry and unrecognizable as AI" (Scientific Reports, 2024) — a controlled study directly relevant to this episode's blind-judgment question.
* **Central Human Question:** *What makes creativity genuinely human?*

**Discussion Questions**

1. **Factual:** According to Benjamin, what distinguishes an original work of art, and what characteristics does the machine-generated work display?
2. **Analytical:** In what ways does the machine-generated work resemble or differ from human creativity?
3. **Evaluative:** Can a work be considered genuinely creative if its creator has no intention, consciousness, or lived experience?

**Contradictory Data to Sit With:**
In the Porter & Machery blind study, ordinary readers rated AI-generated poems as *more* creative, more moving, and higher quality than human-written poems by Shakespeare, Dickinson, and others — when they didn't know which was which. But in a separate condition where the same readers were told (accurately or not) which poems were AI-generated, they rated the labeled-AI poems lower, regardless of actual authorship. The content didn't change; only the label did, and the label moved the judgment more than the poem itself. What does that do to "what makes creativity genuinely human" as a question — is the group evaluating the work, or the label?

**Mini Hands-On (from Rafisha):**
Run a live version of the Porter & Machery study: before the session, generate a machine poem on a set theme and pull a human poem on the same theme; print both anonymized as "Poem A" and "Poem B." Have the group vote blind on which they prefer, then reveal. Separately, if a chatbot is available, generate the same prompt at a low "temperature" (deterministic) and a high "temperature" (more random) setting and compare the two outputs — temperature is a single number that extends our sense of "originality" into a dial, collapsing an entire aesthetic judgment into one parameter. Discuss: once we've turned a knob labeled "creativity," does that change what we think creativity actually is?

---

## **Episode 7 — Is the Machine a Better Teacher?**

* **AI Safety Branch:** AI Governance
* **Non-Technical Concepts:** Education versus conditioning
* **Pair of Written Works:**
  * Brave New World — **Aldous Huxley** (1932), **\~288 pages**
  * Deschooling Society — **Ivan Illich** (1971), **\~116 pages**
* **AI Safety Papers:**
  * *Beginner:* UNESCO, "AI and Education: Guidance for Policy-makers" (2021), executive summary — accessible overview of the tradeoffs governments are already weighing.
  * *Technical:* World Bank, Nigeria "Tutor AI" randomized controlled trial (2024, Global Education Practice) — six weeks of GPT-4–based after-school tutoring produced learning gains roughly equivalent to two years of typical schooling in the study population.
* **Central Human Question:** *What is education ultimately for?*

**Discussion Questions**

1. **Factual:** How do Huxley and Illich portray the purpose of education and its role in society?
2. **Analytical:** How might widespread use of machine tutors reinforce or challenge their visions of education?
3. **Evaluative:** What responsibilities should always remain with human teachers, even if a machine becomes an effective instructor?

**Contradictory Data to Sit With:**
The Nigeria RCT above shows large, real, short-term learning gains from AI tutoring — a genuinely strong result by education-intervention standards. But a separate 2024–2025 line of research on habitual LLM use for writing and problem-solving (including EEG/cognitive-load studies such as MIT Media Lab's "Your Brain on ChatGPT") finds reduced neural engagement, weaker recall of one's own work, and lower reported ownership of the output among frequent users, compared to those working unassisted. The same technology that produces the fastest measured learning gains on record may also be producing the most measurable disengagement of the learner's own cognitive effort. Both findings can be true at once — which one should weigh more in deciding what "better teacher" means?

**Mini Hands-On (from Rafisha):**
Split into pairs. Each pair writes a short "system prompt" (3–4 sentences of instructions) for a chatbot tutor, as if writing a mini syllabus: what should it always do, always avoid, and how should it respond when a student is wrong? Run both pairs' prompts against the same test question and compare how differently the "tutor" behaves — one prompt might explain the whole answer, another might refuse to and ask a leading question instead. A syllabus and a system prompt are the same kind of object: an instruction set that extends a teacher's judgment to moments the teacher isn't present for. Discuss: Illich worries that institutions convert learning into something delivered by a system rather than found by a person. Does writing the prompt ourselves make us more suspicious of "the machine decided how to teach," or does it make us more comfortable with it, now that we can see the decision was actually made by whoever wrote the prompt?

---

*Revised draft — "AI" replaced with "machine" throughout per the framing above; AI safety papers (technical + beginner), a contradictory-data prompt, and a mini hands-on added to each episode. Some sources listed (e.g. the Nigeria RCT, the Porter & Machery poetry study) should be verified for exact citation details before printing for participants.*
