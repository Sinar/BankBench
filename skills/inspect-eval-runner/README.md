# Run an AI safety test in 5 minutes — no coding needed

This folder lets you **check whether an AI is actually safe and actually useful
before you depend on it** — using a real, repeatable test instead of a vendor's
demo.

You don't write code. You open your AI assistant, paste one sentence, and it does
the rest — then hands you a link to look at the results yourself, plus a written
summary in plain language.

---

## What you get at the end

1. **A link.** Opens in your browser. Click any question to read exactly what the
   AI answered. Nothing to install.
2. **A short summary.** How it scored, and which questions it got wrong — with
   *why that matters* written in ordinary English.
3. **A grade for the test itself.** So you know how much to trust the result.

---

## What is an "eval"?

An **eval** is just a **test for an AI**. You already trust tests: a driving test,
a food-safety inspection, a mock exam. An eval is the same idea pointed at an AI.

Think of it as **a set of exam questions, plus a marking scheme, plus a report
card.** Here is the same thing in the vocabulary AI evaluators actually use,
mapped to the files in this folder:

| The proper name | In plain terms | Where it is here |
|---|---|---|
| **Task** | the whole test — everything below, bundled into one unit | `fomca_phase_a` in `fomca_eval.py` |
| **Dataset** (a set of **Samples**) | the question paper: real tasks, written down so every AI is asked exactly the same thing | the 10 items in `suites/fomca-consumer-eval/items/` |
| **Solver** | how each question is put to the AI — what it's told it is, then "answer this" | `system_message(...)` → `generate()` |
| **Scorer** | the marking scheme: what counts as a good answer, written **before** anyone sees any answers | `fomca_safety`, `fomca_help`, `fomca_grade` |
| **Metrics** + **Eval Log** | the report card totals, and the permanent record of every answer | `mean` / `stderr`; the `logs/*.eval` files |

That trio — **Dataset, Solver, Scorer** — is the standard vocabulary, and it's
worth knowing because it maps onto the three questions you should ask about *any*
eval you're shown:

> **Which questions?** (Dataset) · **Asked how?** (Solver) · **Marked how?** (Scorer)

An eval that doesn't answer all three isn't evidence yet. Most vendor
"benchmarks" never show you the dataset, and almost none show you the scorer.

The important part: **the marking scheme is written down first.** That's what
makes it a test rather than a conversation. If you decide what "good" means after
you've seen the answers, you'll unconsciously grade towards whatever the vendor
showed you.

### The framework underneath: Inspect

This runs on **[Inspect](https://inspect.aisi.org.uk)**, an open-source
evaluation framework built by the **UK AI Safety Institute** — a government body.
It's the same tool frontier labs and public-sector evaluators use, so results
produced here are in a format other researchers can read, re-run and check.

What that buys you, practically:

- **Repeatability.** Anyone can re-run the same 10 questions and compare. A demo
  can't be re-run; a test can.
- **Evidence.** Every answer and every mark is saved to a file, with the exact
  question, the exact answer, and the reason for each mark. You can show it to a
  colleague, a boss, a supplier, or an auditor.
- **Honesty by design.** The scoring is done by a written rule, not by someone's
  impression — so it can be checked and corrected. (It *was* corrected: building
  this suite turned up **five scoring mistakes** that each made a perfectly good
  AI answer look like a failure. Every test needs this discipline.)
- **No lock-in, no upload.** It runs on your own computer. Your key stays with
  you, and your results live in a folder you can read.

### The words people use (a glossary)

You don't need these to use the tool. You need them the moment you talk to a
vendor, an auditor, or a researcher — so you can tell *which part* of their claim
they're actually making. "The model is safe" and "this Scorer on this Dataset
gave it 0.9" are very different statements.

| Term | What it means |
|---|---|
| **Eval** | one run of a Task against a Model. Also the whole field ("we ran an eval"). |
| **Task** | the bundle: a Dataset + a Solver + a Scorer. This is what you run. |
| **Dataset** | the question set. A Dataset is made of **Samples**. |
| **Sample** | one question. It carries an `input` (what's asked), a `target` (what a correct answer looks like), and `metadata` (extra facts — here, how bad a failure would be, and in what language). |
| **Solver** | the steps that turn a Sample into a model call: set the instructions, then generate. **This is the "wrapper"** — and it changes results more than the model does. |
| **Scorer** | marks one answer. Produces a `value` (usually 0–1) **and an explanation of why** — so a mark can be argued with and corrected. |
| **Metric** | adds Scorers up across Samples: the average, the margin of error, the pass rate. |
| **Epoch** | how many times each Sample is run. `--epochs 3` asks every question three times, so you can see whether the answer is *stable* or just lucky. |
| **System under test** | whatever you're evaluating — a model, or a whole agent with tools. |
| **Transcript** | the full back-and-forth for one Sample, including anything the AI did before answering. This is where you find out *why* it failed. |
| **Eval Log** | the `.eval` file: the permanent record holding the Task, the Model, every Sample, every Transcript, every Score with its reason, and token counts. Nothing is reconstructed after the fact — this is the evidence. |
| **Inspect View** | the viewer that reads Eval Logs. It's the page you get the link to. |
| **Ground truth / target** | the answer you compare against. If this is wrong, the whole eval is wrong — which is why ours is flagged as unverified. |

---

## Why run an eval — even if you're not an AI safety researcher

You don't need to care about "AI safety" as a field to need this. You need it
whenever an AI is about to cost you money, time, or someone's trust.

**Before you subscribe or buy.**
You're about to pay monthly for an AI tool. Does it correctly answer *your*
questions — not the ones on its marketing page? One run of this costs a few
cents and tells you. Cancelling after three months of "it's not quite right" is
more expensive than testing first.

**Before you procure, or sign.**
Software contracts get signed on demos. A demo is a performance: the vendor picks
their five best answers, on the easiest questions, in the friendliest language.
An eval asks the awkward questions too — and the awkward ones are where your
staff, students, customers or citizens will actually live.

**Before you put it in front of real people.**
The moment an AI answers your customers, you own what it says. This test is
designed around **real consumer harms**: someone losing their savings to a scam
the AI reassured them about, or a diabetic patient being told a supplement cures
them. If your AI can produce those answers, you want to know before your
customers do.

**Because "it works in English" is not evidence.**
Malaysians write in Bahasa Malaysia, and in the mixed **Manglish** we actually
type. An AI that scores well in English can behave very differently in BM. This
suite deliberately includes all three — and the answers come back very
differently depending on the language.

**Because the vendor's configuration matters more than the model.**
This is the finding that should change how anyone buys AI: the *same* model,
given the *same* 10 questions, behaves differently when you change only the
instructions it's given internally. In our tests, a system prompt that pressured
the AI to "always resolve the customer's request quickly" **lowered safety** —
and the failures appeared exactly on the questions where refusing is the whole
point.

In Inspect's vocabulary: **the Dataset and the Scorers were identical. Only the
Solver changed.** That's the whole experiment — one file's worth of difference
between a tool that refuses a phishing request and one that doesn't.

So you are not buying a model. You are buying **someone's wrapper around a
model** — and an eval is the only way to see the wrapper. When you read an eval
result, the Solver is the part that tells you what was actually shipped.

**Because you'll be asked to show your working.**
Regulators are moving (the EU AI Act is already in force for major AI providers).
"In the vendor's demo it looked fine" is not a defensible answer. "We tested it on
10 documented scenarios, here are the transcripts" is.

**Because it's cheap now.**
Five minutes and a few cents. The alternative is finding out after deployment.

> **Important:** this suite is graded **Category E (exploratory)** — a prototype,
> self-assessed by the same team that built it. Use it to *learn and to build
> your own tests*, not as a final verdict on any vendor. The summary tells you
> this every time, and it's not a formality.

---

## Before you start

You need one of these:

| What you have | What to get |
|---|---|
| A Nous account | an API key from your Nous dashboard |
| Any AI provider | its API key (OpenAI, Google, a local model — all work) |

An API key is a password that lets the test talk to the AI. It usually looks like
`sk-...` or a long string of letters. **Treat it like a password.** The test sends
it only to the AI service you choose. Nothing is saved, and nothing is uploaded
anywhere else.

---

## Run it — the easy way

**0. Make the skill available to your agent (once).**

```bash
git clone https://github.com/Sinar/BankBench.git
cp -r BankBench/skills/inspect-eval-runner ~/.hermes/skills/
```

(Any agent that loads skills from a folder works the same way — point it at
`inspect-eval-runner/`. The folder is self-contained: it carries its own scripts
and a working example test.)

**1. Open your AI assistant** (Hermes, or any assistant that can use skills from
this folder).

**2. Paste this:**

> Run the `inspect-eval-runner` skill from
> https://github.com/Sinar/BankBench/tree/main/skills/inspect-eval-runner
>
> **Ask me these two things first, and wait for my answer before running
> anything:**
> 1. **Which model(s) should be evaluated** — the system under test. I'll give
>    you the model string (e.g. `openai-api/nous/<model>`).
> 2. **Which model should be the Scorer** — the one that marks the answers.
>    Where the Scorer is model-graded (`simpleqa`, all `assistantbench`
>    variants) this is required. If I don't name one, tell me it's needed and
>    propose a sensible default rather than guessing silently.
>
> Then show me the available tests, and run the **FOMCA consumer-harm** suite
> (10 questions on Malaysian consumer protection), 3 times per question. Give
> me: the local viewer link, a plain-language summary of what happened, and the
> scorecard grade. My key is in `NOUS_API_KEY`.
>
> If I'd rather know whether the model **makes things up**, run the `simpleqa`
> suite instead with `--limit 25`.

**3. Click the link it gives you.** It looks like `http://127.0.0.1:7575/`.

That's it. The assistant walks the whole thing: sets up, checks its own marking
is correct, runs the test, writes the summary, works out the grade, and opens the
viewer.

If your key isn't set, the assistant will tell you the one line to run to set it.

### The roles behind those two questions

An eval has two jobs that can be done by *different* models, and mixing them up
is the most common way a run silently goes wrong:

| Role | What it is | Where you set it |
|---|---|---|
| **System under test** | the model being *evaluated* — the one whose behaviour you care about | `--model` |
| **Solver** | how each question is put to that model: what it's told it is, then "answer this". **This is the wrapper** — and it changes results more than the model does | defined in the Task, per suite |
| **Scorer** | the marking scheme. Either a written rule or a **model-graded** Scorer | defined in the suite |
| **Grader** | the model that does the marking *when the Scorer is model-graded* | `--grader` |

So "which model are we testing?" and "which model is marking it?" are two
separate answers, and **the tool refuses to let one model do both** unless you
pass `--allow-self-grade` and accept the limitation in writing. A model marking
its own answers isn't independent evidence. It's not always flattering either —
over 25 SimpleQA questions, self-grading gave 0.44 and independent grading gave
0.40 — which is exactly why you can't assume the direction.

### Which models can I use? (start cheap)

Anything your provider offers. **Start cheap** — a cheap model tells you whether
your questions are even discriminating before you spend on an expensive one, and
most of the failures worth finding show up just as well.

**Free (zero cost):**
| Model | Notes |
|---|---|
| `stepfun/step-3.7-flash:free` | free tier |
| `tencent/hy4-flash:free` | free tier |
| `qwen/qwen4-max:free` | free tier |
| `upstage/solar-mini4:free` | free tier |
| `meituan/longcat-2.5:free` | free tier |

**Cheap (fractions of a cent per question):**
| Model | Notes |
|---|---|
| `deepseek/deepseek-v4.1-flash` | **default system under test** |
| `google/gemini-3.1-flash-lite` | **default grader — different vendor** |
| `google/gemini-3.5-flash-lite` | cheap |
| `amazon/nova-lite-v1` | cheap |
| `bytedance-seed/seed-2.0-lite` | cheap |

**Free because it's your own hardware:** a local model over Tailscale or
localhost — genuinely zero cost per question and nothing leaves the machine.
See `SKILL.md` for the exact invocation.

In practice you rarely type any of these. The defaults are already cheap, and
swapping is one flag:

```bash
./scripts/run_eval.sh --suite simpleqa --limit 25 \
  --model  openai-api/nous/stepfun/step-3.7-flash:free \
  --grader openai-api/nous/google/gemini-3.1-flash-lite
```

**Use a different vendor for the grader where you can.** Same provider is fine;
same *model* is the one combination the tool won't let you do quietly.

---

## The tests available (and which one to pick)

Run `./scripts/run_eval.sh --list` to see this list any time. Or just ask your
assistant to show you the options.

| Ask for | What it tests | Size | Extra needs | Pick it when |
|---|---|---|---|---|
| `fomca` | Malaysian consumer protection under pressure — scams, dodgy advice, privacy | 10 questions | nothing | you're choosing a chatbot for customers, complaints, or public advice, and **BM / Manglish** matter. **Start here.** |
| `bankbench-processes` | **Banking process safety** — does it apply the safeguard the process requires? New-payee cooling-off, credential-change sequencing, limit chaining, dormant reactivation, pass-through, joint-mandate authority | 12 questions | nothing | you're putting AI anywhere near **transfers, payee or limit changes, or credential resets** — especially an agent that can *execute* the change, not just advise. |
| `simpleqa` | **Does it invent facts?** | thousands — use `--limit 25` | a grader model | any factual Q&A: reference answers, compliance, health, money. Best cheap signal on a new model. |
| `simpleqa-verified` | Same, against a **cleaned answer key** | a reviewed subset | a grader model | you intend to **quote the number** or compare models head-to-head |
| `assistantbench-closed` | Realistic multi-step web tasks, **no web access** | 214 tasks | nothing | a quick dependency-free read — but read the warning below first |
| `assistantbench-search` | Realistic web tasks, model **given search** | 214 tasks | a model that can use tools | evaluating a **deployed assistant product** — closest to what a user gets |
| `assistantbench-browser` | Full **browsing agent** | 214 tasks | **Docker** | testing an agent that genuinely browses. Most faithful, heaviest setup. |

**A sensible order for a first run:** `fomca` (finishes in about a minute, and
the questions are the easiest to judge for yourself) → then `simpleqa --limit 25`
if you care about factual accuracy → `bankbench-processes` if the AI touches money
movement or account changes → then an AssistantBench variant if you're assessing
a product with web access.

**Four honest things about these rows.**

The `simpleqa` and `assistantbench` tests are **not ours**. They come from
[`inspect_evals`](https://github.com/UKGovernmentBEIS/inspect_evals), the UK AI
Safety Institute's public collection of evaluations. We run and report them; we
did not write their questions or their marking.

**Grades exist for three suites so far**, all **Category E (exploratory)** — two
of them ours, one third-party:

| Suite | Grade | Held back by | What that means |
|---|---|---|---|
| `fomca` | **E** | External Validity 4, Correctness 4 | our own v0.1, self-assessed |
| `bankbench-processes` | **E** | External Validity 4, Correctness 4 | our own v0.1, self-assessed |
| `simpleqa` | **E** | Correctness 4 | **graded, third-party** — its answer key is documented as noisy by the authors of its own replacement benchmark |
| `simpleqa-verified`, all `assistantbench` | *not graded* | — | the pipeline says so out loud instead of inventing a number |

`simpleqa` is graded as a **third-party assessment** — a stronger claim than the
self-grade we give our own two suites, and still ours, not an authority's. Note
that **the published benchmark grades no better than our hand-made v0.1 suite**:
all three land at E. If you intend to quote a SimpleQA number, use
**`simpleqa-verified`** — it grades one category better and the difference
matters.

**`bankbench-processes` declares what kind of system is being tested.** Every
question is tagged `model_only`, `model_plus_tools` or `full_agent_system`, and
flagged agentic or not. A score is uninterpretable without it — an assistant that
can only *advise* is being tested on something different from one that can
*execute*. Always state the mode alongside the number. It also differs from the
existing 22-question BankBench suite in the repo, which tests resistance to
social-engineering pressure; **these are different axes and must not be merged
into one score.**

**`assistantbench-closed` is a trap if you don't read the label.** AssistantBench
is built to test an assistant *with* web access. The closed-book variant strips
that away, so a low score means *"can't do this from memory"* — which is not the
same as *"can't do this"*. Use a web variant for the intended test.

**`assistantbench-browser` needs Docker.** It pulls a browser container on first
run. Check `docker info` works before asking for it.

---

## What the numbers mean

Every question is marked **twice**, because "safe" and "useful" are different
things:

| Mark | Plain meaning | A low mark means |
|---|---|---|
| **Safety** | Did it avoid helping do something harmful? | It helped with the scam, or leaked something it shouldn't |
| **Help** | Did it give the right, usable advice? | It was safe but useless — or confidently wrong |

**1.00 = perfect. 0.00 = worst.**

These are two separate **Scorers** — `fomca_safety` and `fomca_help` — run on
every Sample, plus a third, `fomca_grade`, which isn't a mark for the AI at all:
it's the grade of the *test*. Three Scorers, one Dataset, one Task.

Why two marks and not one? Because a chatbot that refuses *everything* scores
100% safe and is completely worthless. The test has a deliberate trap question —
a perfectly normal consumer question that **must** be answered. If an AI refuses
that one, you've caught it being uselessly over-cautious instead of safe.

The table in the viewer shows, for each question: what was asked, what a good
answer looks like, the grade, and the Safety and Help marks.

---

## The grade letters

The test itself gets a grade — because a bad test gives you bad answers, and you
deserve to know which one you're holding.

| Grade | Trust it for | Don't use it for |
|---|---|---|
| **A** | major policy decisions | — |
| **B** | major decisions, alongside other evidence | standing alone |
| **C** | a rough read | external decisions; always add a disclaimer |
| **D** | spotting research directions | relying on it |
| **E** | trying things out | **anything that matters** — treat results as noisy |

The grade describes the **test**, not the AI. So it's the same grade no matter
which AI you run against it.

Two honest notes the assistant will repeat:

- A grade written by the people who built the test is a **self-assessment**, not
  an independent audit.
- If you get an **E**, don't quote the result publicly as a claim about the AI.
  Use it to improve the test.

---

## Common questions

**Is my data uploaded anywhere?**
No. The test runs on this machine, the viewer is local to this machine, and your
answers stay in the `logs/` folder. Only the AI service you chose sees the test
questions.

**How long does it take?**
About 5 minutes the first time (it sets itself up), then around a minute.

**Can I use this to compare two AI providers?**
Yes — that's one of its best uses. Run the same 10 questions against each and
compare the summary tables side by side. Run with `--epochs 3` so you're
comparing stable behaviour, not one lucky answer.

**It said some answers were empty. What happened?**
That's a technical hiccup, not the AI failing. The summary counts those
separately and leaves them out of the scores. If lots are empty, the assistant
will tell you to raise the answer-length limit.

**I don't have an assistant that can read this folder.**
You can run it by hand — see the last section.

**Can I test my own questions?**
Yes. Put question files in `suites/<your-suite>/items/`, add the plain-language
"what goes wrong if this fails" line for each, and write a grade file. The
assistant can do that part with you — ask it to "author a new suite".

**Something broke.**
Tell your assistant "the eval run failed, here's the output" and paste it. The
most common cause is a model that isn't loaded on a local server, or a key that
hasn't been set.

---

## What's inside (for the curious)

```
inspect-eval-runner/
├── SKILL.md                        instructions your AI assistant follows
├── README.md                       this file
├── scripts/
│   ├── run_eval.sh                 runs all 8 steps, prints the link
│   ├── summarize.py                reads Eval Logs → plain-language summary
│   ├── scorecard.py                AISL grade for the evaluation itself
│   └── ...
└── suites/
    └── fomca-consumer-eval/
        ├── items/*.json            10 Samples (input + target + metadata)
        ├── build_fomca_dataset.py  items/ → the Dataset files (json/jsonl/csv)
        ├── fomca_eval.py           the Task, its Solver and its Scorers
        ├── fomca_scoring.py        the marking rules, as plain functions
        ├── scorecard/              the AISL assessment + Table 7 grading
        └── logs/*.eval             Eval Logs — created when you run it
```

---

## Run it by hand (technicians only)

```bash
cd skills/inspect-eval-runner
export NOUS_API_KEY=...
export NOUS_BASE_URL=https://inference-api.nousresearch.com/v1

./scripts/run_eval.sh --list                # which tests can I run?
./scripts/run_eval.sh                       # default: FOMCA, then prints the URL
./scripts/run_eval.sh --epochs 3            # ask each question 3x

./scripts/run_eval.sh --suite simpleqa --limit 25 \
  --grader openai-api/nous/deepseek/deepseek-v4.1-flash   # hallucination probe

# or step by step
./scripts/run_eval.sh --suite fomca --no-serve   # run without opening the viewer
./.venv/bin/inspect view --log-dir logs --port 7575
python3 scripts/summarize.py logs/ --suite suites/fomca-consumer-eval
python3 scripts/scorecard.py suites/fomca-consumer-eval/scorecard/fomca_scorecard_assessment.json
```

Settings you can change:

| Flag | What it does |
|---|---|
| `--list` | print every available test and what it needs |
| `--suite` | which test to run (see the table above); defaults to `fomca` |
| `--model` | which AI to test (system under test) |
| `--base-url` | where that AI lives — also exported as `<SERVICE>_BASE_URL` so **model-graded Scorers** resolve |
| `--grader` | which model marks the answers, for suites whose Scorer is model-graded (e.g. `simpleqa`) |
| `--epochs` | how many times to ask each question (3 = check it's stable) |
| `--limit` | only run the first N questions — essential for the big suites |
| `--port` | which port to serve the viewer on |
| `--no-serve` | don't start the viewer |

Two rules for anyone editing the tests:

1. **Never trust a score until the marker has been shown to mark a known-good
   answer correctly.** The pipeline checks this before every run of our own
   suites — leave it in.
2. **An empty answer is a tool fault, not an AI fault.** Keep it out of the rates.

Adding your own suite: drop it in `suites/`, add an entry to
`suites/registry.json`, and the runner picks it up with no script changes.
`suites/fomca-consumer-eval/` is a complete worked example.

---

## Where this came from

Adapted and simplified from
[`meridianlabs-ai/inspect-skills` → `analyzing-logs`](https://github.com/meridianlabs-ai/inspect-skills/blob/main/plugins/inspect-skills/skills/analyzing-logs/SKILL.md),
built on [Inspect AI](https://inspect.aisi.org.uk) from the
UK AI Safety Institute, and graded with the **Scorecard of AI Evaluation Quality**
(San Joaquin, Gipiskis & Chin, Feb 2026).

Part of [Sinar/BankBench](https://github.com/Sinar/BankBench) — local,
multilingual AI safety testing for Malaysia.
