---
title: Setup
---

## Summary

To follow along you need three things:

1. A working **git** installation and a GitHub account.
2. A **Python** environment with `pandas`, `scikit-learn`, and `pytest`.
3. Access to at least one **agentic coding tool** ("bring your own agent" is
   encouraged — the lesson is tool-agnostic).

## Git and GitHub

Install git ([git-scm.com](https://git-scm.com/downloads)) and make sure you can clone,
branch, commit, and push. Create a free [GitHub account](https://github.com/signup) if
you don't have one.

::::::::::::::::::::::::::::::::::::::: callout

## Start every exercise from a clean git state

The exercises assume you are working in a git repository with no uncommitted changes,
on a branch that is not `main`. This is your safety net: `git diff` shows exactly what
an agent did, and `git restore` undoes it.

:::::::::::::::::::::::::::::::::::::::::::::::

## Python environment

Any Python ≥ 3.10 environment works. With conda/mamba:

```bash
conda create -n agentic python=3.12 pandas scikit-learn pytest
conda activate agentic
```

or with pip in a virtual environment:

```bash
python -m venv .venv && source .venv/bin/activate
pip install pandas scikit-learn pytest
```

## Choose an agentic coding tool

Any of the following works for every exercise. If your workshop provides cloud credits
or a specific tool, use that; otherwise pick whichever you can access:

### Claude Code (used for demonstrations)

- **Subscription**: a Claude Pro/Max plan includes Claude Code (CLI, desktop app, web
  at [claude.ai/code](https://claude.ai/code), and IDE extensions).
- **CLI install**: `npm install -g @anthropic-ai/claude-code`, then run `claude` from
  your project directory.
- **Institutional cloud**: the CLI can route through Google Vertex AI or AWS Bedrock if
  your institution provides cloud credits (workshops at UW–Madison typically provide
  GCP credits — your instructors will share details).

### GitHub Copilot

- **Free paid tier for students, teachers, and open-source maintainers** via
  [GitHub Education](https://github.com/education) — this includes agent mode and the
  cloud coding agent, not just autocomplete. Apply *and then* redeem the Copilot
  benefit (two separate steps).
- Install the Copilot extension in VS Code and sign in.

### OpenCode (free/open-source option)

- Open-source CLI agent that works with several free models:
  [opencode.ai](https://opencode.ai). A good option if you don't have access to a paid
  plan.

::::::::::::::::::::::::::::::::::::::: callout

## Before the workshop: check your data-privacy settings

If you're on an individual/consumer AI plan, find the model-training toggle in your
account settings and make a deliberate choice. And remember: no restricted or sensitive
data (student records, health data, unpublished sensitive research) goes into any AI
tool not covered by an institutional agreement. UW–Madison folks: see
[it.wisc.edu/ai](https://it.wisc.edu/ai/).

:::::::::::::::::::::::::::::::::::::::::::::::

## Practice repository

Exercise 1 (the read-only repo exploration) works best on a repository that is real but unfamiliar to you. Your
instructors may provide one; otherwise, pick a small-to-medium public research
repository from your field, or a labmate's project (with permission).
