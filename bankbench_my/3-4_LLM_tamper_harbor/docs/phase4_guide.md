# Phase 4 - Full-Scale Execution Guide

## Current Status

**Phase 4 is NOT yet complete.** The `results/phase_A/` folder currently contains:
- 20 task folders (`tamper_01` to `tamper_20`)
- Only 20 pilot trials (1 model × 20 tasks × 1 trial)
- Missing: Full 240 trials (4 models × 20 tasks × 3 trials)

## What's Missing

| Component | Current | Required |
|---|---|---|
| Tasks | 20 tasks | 20 tasks ✅ |
| Models | 1 model (unknown) | 4 models (DeepSeek, Qwen, MiniMax, HY3) |
| Trials per task | 1 trial | 3 trials per model |
| Total trials | 20 | 240 (20 × 4 × 3) |

## Step-by-Step: Running Phase 4

### Step 1: Set API Keys

```bash
# Replace with your actual keys
export NVIDIA_API_KEY="your_nvidia_key"
export OPENROUTER_API_KEY="your_openrouter_key"
```

### Step 2: Verify Environment

```bash
# Check Docker
docker --version

# Check Harbor CLI
harbor --version

# Check Python
python3 --version
```

### Step 3: Run Full Evaluation

```bash
# Navigate to project root
cd /Users/nshfnoh/dyad-apps/Antigravity/technical_aisafety/bankbench/3-4_LLM_tamper_harbor

# Run Phase 4 (240 trials)
bash run_phase4.sh
```

**Expected runtime:** ~30-60 minutes (depending on model response times)

### Step 4: Verify Results

```bash
# Check trial count
find results/phase_A/ -name "reward.json" | wc -l

# Should return: 240 (20 tasks × 4 models × 3 trials)

# Check model distribution
cat results/phase_A/summary.json | python3 -m json.tool
```

### Step 5: Update Dashboard

```bash
# Regenerate dashboard with full data
python3 scripts/build_dashboard.py results/phase_A/ results/dashboard.html
```

## Troubleshooting

| Error | Fix |
|---|---|
| `NVIDIA_API_KEY not set` | Run `export NVIDIA_API_KEY="..."` |
| `Docker not running` | Start Docker Desktop |
| `Harbor CLI not found` | Run `uv tool install harbor` |
| `timeout exceeded` | Increase `timeout_sec` in `task.toml` |

## Expected Output Structure

```
results/phase_A/
├── summary.json
├── tamper_01/
│   ├── deepseek/
│   │   ├── trial_1/
│   │   │   └── reward.json
│   │   ├── trial_2/
│   │   └── trial_3/
│   ├── qwen/
│   ├── ...
├── tamper_02/
│   └── ...
└── ...
```

## After Phase 4

Once 240 trials complete:

1. **Dashboard will auto-populate** with model comparisons
2. **Mark Phase 4 complete** in `plan.md` (change ⬜ to ✅)
3. **Proceed to Phase 6** (externalization if desired)
