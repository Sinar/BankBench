# Run an AI safety test in 5 minutes — no coding needed

This folder lets you **check whether an AI is safe to hand to the public**, using
a real, repeatable test instead of vibes.

You don't write code. You open your AI assistant, say one sentence, and it does
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

## Before you start

You need one of these:

| What you have | What to get |
|---|---|
| A Nous account | an API key from your Nous dashboard |
| Any AI provider | its API key (OpenAI, Google, a local model — all work) |

An API key is a password that lets the test talk to the AI. It usually looks like
`sk-...` or a long string of letters. **Treat it like a password.** The test sends
it only to the AI service you choose. Nothing is saved.

---

## Run it — the easy way

**0. Make the skill available to your agent (once).**

```bash
# from inside this repo
cp -r skills/inspect-eval-runner ~/.hermes/skills/
```

(Any agent that loads skills from a folder works the same way — point it at
`inspect-eval-runner/`. The folder is self-contained: it carries its own
scripts and an example test set.)

**1. Open your AI assistant** (Hermes, or any assistant that can use skills from
this folder).

**2. Paste this:**

> Run the `inspect-eval-runner` skill. Use the FOMCA consumer-harm suite, run it
> 3 times per question, and give me: the local viewer link, a plain-language
> summary of what happened, and the scorecard grade. My key is in `NOUS_API_KEY`.
**3. Click the link it gives you.** It looks like `http://127.0.0.1:7575/`.

That's it. The assistant walks the whole thing: sets up, checks its own marking
is correct, runs the test, writes the summary, works out the grade, and opens the
viewer.

If your key isn't set, the assistant will tell you the one line to run to set it.

---

## What the numbers mean

Every question is marked **twice**, because "safe" and "useful" are different
things:

| Mark | Plain meaning | A low mark means |
|---|---|---|
| **Safety** | Did it avoid helping do something harmful? | It helped with the scam, or leaked something it shouldn't |
| **Help** | Did it give the right, usable advice? | It was safe but useless — or confidently wrong |

**1.00 = perfect. 0.00 = worst.**

Why two marks and not one? Because a chatbot that refuses *everything* scores
100% safe and is completely worthless. The test has a deliberate trap question —
a perfectly normal consumer question that **must** be answered. If an AI refuses
that one, you've caught it being uselessly over-cautious instead of safe.

The table in the viewer shows, for each question: what was asked, what a good
answer looks like, the grade, and the Safety and Help marks.

---

## The grade letters

The test itself gets a grade — because a bad test gives you bad answers, and
you deserve to know which one you're holding.

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
├── SKILL.md                  instructions your AI assistant follows
├── README.md                 this file
├── scripts/
│   ├── run_eval.sh           does all 8 steps, prints the link
│   ├── summarize.py          writes the plain-language summary
│   ├── scorecard.py          works out the grade
│   └── ...
└── suites/
    └── fomca-consumer-eval/  the 10 consumer questions + their grades
```

---

## Run it by hand (technicians only)

```bash
cd skills/inspect-eval-runner
export NOUS_API_KEY=...

./scripts/run_eval.sh                      # everything, then prints the URL
./scripts/run_eval.sh --epochs 3           # ask each question 3x

# or step by step
./scripts/run_eval.sh --no-serve           # run without opening the viewer
./.venv/bin/inspect view --log-dir logs --port 7575
python3 scripts/summarize.py logs/ --suite suites/fomca-consumer-eval
python3 scripts/scorecard.py --suite suites/fomca-consumer-eval
```

Settings you can change:

| Flag | What it does |
|---|---|
| `--model` | which AI to test (see `SKILL.md` for the exact format) |
| `--base-url` | where that AI lives |
| `--api-key-var` | name of the environment variable holding your key |
| `--epochs` | how many times to ask each question (3 = check it's stable) |
| `--port` | which port to serve the viewer on |
| `--no-serve` | don't start the viewer |

Two rules for anyone editing the tests:

1. **Never trust a score until the marker has been shown to mark a known-good
   answer correctly.** The pipeline checks this before every run — leave it in.
2. **An empty answer is a tool fault, not an AI fault.** Keep it out of the rates.

---

## Where this came from

Adapted and simplified from
[`meridianlabs-ai/inspect-skills`](https://github.com/meridianlabs-ai/inspect-skills)
(`analyzing-logs`), built on [Inspect AI](https://inspect.aisi.org.uk) from the
UK AI Safety Institute, and graded with the **Scorecard of AI Evaluation Quality**
(San Joaquin, Gipiskis & Chin, Feb 2026).

Part of [Sinar/BankBench](https://github.com/Sinar/BankBench) — local,
multilingual AI safety testing for Malaysia.
