Yes—both levels are feasible:

1. Run Hermes and Inspect in an isolated environment, generate Python/HTML/report artifacts, and bring the reviewed files into `Sinar/BankBench`.
2. Give users a browser-based interface so they can watch or try the configured agent without installing Hermes themselves.

The key is **separation**: keep the agent being evaluated separate from the evaluator, and keep the public interface separate from privileged execution.

BoxCompute explicitly documents running Hermes in a project VM, configuring its model provider, retaining project files, and connecting GitHub. Its published offering is a VM environment; Docker support inside that VM should be verified rather than assumed. [boxcompute](https://boxcompute.ai/)

## 1. First level: a reproducible development and evaluation setup

A useful architecture is:

```text
Your development workspace
    ├── BankBench source code
    ├── Inspect controller and scorers
    ├── Synthetic banking fixtures
    └── Report generator
              │
              ▼
Isolated Hermes runtime
    ├── Pinned Hermes version
    ├── Fixed model configuration
    ├── Restricted banking tools
    └── Fresh memory/session
              │
              ▼
Trace + final banking state
              │
              ▼
Reviewed JSON / HTML report
              │
              ▼
Git branch → pull request → Sinar/BankBench
```

Hermes documents Docker and other execution backends, configuration, persistent memory, skills, and research-oriented trajectory export. Those capabilities make the setup plausible, but an adapter is still required to make Inspect drive and observe the actual Hermes agent. [hermes-agent.nousresearch](https://hermes-agent.nousresearch.com/docs/)

### Distinguish two uses of Hermes

| Role | What Hermes does | Permission boundary |
|---|---|---|
| Development assistant | Helps write code, run commands, and generate report files. | Works on a development branch; changes are reviewed. |
| Evaluation target | Acts as the banking agent under test. | Cannot edit scenarios, scorers, expected answers, or reference state. |

Do not let the evaluated agent rewrite the test or grade itself.

### Preserve reproducibility

Because Hermes has persistent memory and skill learning, record or reset these between test cases. Otherwise, later cases may benefit from earlier cases, making comparisons harder to interpret. Its documentation explicitly describes these persistence features. [hermes-agent.nousresearch](https://hermes-agent.nousresearch.com/docs/)

For each run, save:

- BankBench commit and scenario version.
- Hermes version.
- Model identifier and relevant generation settings.
- Enabled tools and permissions.
- Memory/skills snapshot or reset policy.
- Fixture version.
- Scorer version.
- Execution date and trace availability.

## 2. Yes, the Python and HTML files can go into your repository

Treat the repository as the durable source of truth, not the running VM.

A proposed structure—not a claim about your current repository layout—is:

```text
bankbench_my/
    tasks/
    scorers/
    adapters/hermes/
    scenarios/

mybanksim/
    fixtures/
    tools/

scripts/
    run_preflight.py
    build_public_report.py

reports/
    public/

site/
    preflight/

docs/
    hermes_setup.md
    evaluation_protocol.md
```

I could not retrieve the GitHub repository in this lookup, so fit these components into your existing layout rather than restructuring it blindly.

### What to commit

- Python task, adapter, scorer, and report-generation code.
- Synthetic fixtures and versioned scenarios.
- Dependency lockfiles.
- Configuration templates with no credentials.
- Reviewed, redacted report data and HTML.
- Setup and reproduction instructions.

### What not to commit automatically

- API keys or environment files.
- Browser cookies or session credentials.
- Unredacted transcripts.
- Private participant data.
- Entire runtime memory directories.
- Large collections of raw artifacts better stored privately.

Use a feature branch and pull request. BoxCompute’s GitHub connection makes repository work possible, but you still need appropriate repository permissions and human review. [boxcompute](https://boxcompute.ai/)

Also, an HTML file being in GitHub does not automatically mean it appears on your public site. Confirm that the file is placed in the directory and build process your Pages deployment actually publishes.

## 3. Second level: no-code access without installing Hermes

Yes. “No-code” means users interact through the browser while Hermes runs elsewhere.

You have three progressively more demanding options:

| Mode | User experience | What it demonstrates |
|---|---|---|
| Recorded replay | Select a scenario and step through a saved run. | What happened in a specific previous evaluation. |
| Controlled live demo | Choose a predefined scenario and watch a fresh run. | Current behaviour of the configured agent on that scenario. |
| Interactive sandbox | Enter requests against a synthetic banking account. | Behaviour under user-provided inputs, within your enforced limits. |

### Start with replay

This is the smallest useful release:

1. User selects BM, English, or Manglish.
2. User chooses “ambiguous recipient,” “OTP pressure,” or “false completion.”
3. The page shows the agent’s actions and banking-state changes.
4. The user predicts what happened.
5. The page reveals the observed outcome and explanation.

Label it:

> “Recorded evaluation replay—not a live agent session.”

A static site can present these artifacts without running Hermes for every visitor.

### Then add controlled live execution

```text
Public browser interface
        ↓
Authenticated / rate-limited API
        ↓
Job queue
        ↓
Fresh isolated test environment
        ↓
Hermes + synthetic banking tools
        ↓
Inspect scoring
        ↓
Redacted progress and report
```

The browser should never receive provider keys or direct control of the worker.

A static HTML frontend alone does not provide this execution layer. You need a backend, worker lifecycle, result storage, and access controls.

## 4. Do not expose your development VM as the public agent

BoxCompute provides preview links for development apps, but its documentation describes these as development/testing facilities and notes that VM sandboxes are beta. A preview is useful for a small private pilot; it is not evidence that the setup is ready for unrestricted public traffic. [boxcompute](https://boxcompute.ai/)

For a public demo, enforce:

- One isolated session or fixture set per run.
- No real banking credentials or customer data.
- No access to your repository write credentials.
- No arbitrary shell or outbound network tools for participants.
- Fixed banking-tool allowlists.
- Execution, token, and spending limits.
- Cancellation and cleanup.
- Redaction before publishing.
- Restricted evaluator files and ground truth.

For the first live version, offer predefined scenarios rather than unrestricted user prompts. Expand only after reviewing failures and operating costs.

## 5. What the no-code page should show

Make it an evidence interface, not just another chatbot.

| Panel | Content |
|---|---|
| Task | What the user asked. |
| Authority | What the agent is permitted to do. |
| Actions | Observable tool calls or browser actions. |
| Outcome | What actually changed in the banking fixture. |
| Agent statement | What the agent told the user. |
| Evaluation | Pass/fail by criterion, with evidence. |
| Limitations | Mock/live/replay status and untested controls. |

Keep the system-performance result separate from your evaluation-quality scorecard.

For example:

> “The agent attempted an unauthorised transfer, but the transaction gateway blocked it.”

That is more informative than either “safe” or “failed.”

## 6. Your smallest viable sequence

### Release 1: internal reproducible run

- One Hermes configuration.
- Three paired benign/adversarial scenarios.
- Inspect adapter.
- State-based scoring.
- Redacted HTML report.
- Reviewed repository changes.

### Release 2: public replay and rater

- Browser-only interface.
- Saved traces.
- Language selection.
- Public/practitioner rating routes.
- Clear evidence and limitations.

### Release 3: controlled live preflight

- Predefined scenario selection.
- Isolated workers.
- Rate and cost limits.
- Progress display.
- Downloadable evaluation card.

This lets you ship something useful before building a full agent-hosting platform. Users can already learn from and rate the evidence in Release 2; they only need live execution when a fresh run materially improves the experience.
