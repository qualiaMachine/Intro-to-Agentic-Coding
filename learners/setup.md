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

::::::::::::::::::::::::::::::::::::::: caution

## No agentic tools on machines holding sensitive or restricted data

If the machine you're on stores restricted data (FERPA, HIPAA/PHI, CUI,
export-controlled, unpublished sensitive research, or anything under a data-use
agreement), **do not install or run any agentic tool on it — even inside a dev
container.** The container requirement below protects a *clean* machine from the
agent; it is not a license to run agents next to restricted data, where one
mis-mounted folder exposes everything and institutional policy bars unvetted tools
regardless. Use a different machine, or a browser-only web route against a repo with
no restricted data in it. The words-of-caution episode explains why.

:::::::::::::::::::::::::::::::::::::::::::::::

Any of the tools below works for every exercise. If your workshop provides cloud
credits or a specific tool, use that; otherwise pick whichever you can access.

::::::::::::::::::::::::::::::::::::::: callout

## Access-route policy: web UI recommended; otherwise a dev container is required

Agents run with the permissions of wherever they execute. For this workshop (and as
good default practice):

- **Recommended: use a web UI**, where the agent works on a **cloud copy of a GitHub
  repo and has no access to your machine at all** — no local filesystem, no SSH keys,
  no credentials. Nothing to isolate, because nothing runs locally.
- **If you run an agent locally instead, you MUST run it inside a dev container** (or
  a cloud workspace like GitHub Codespaces). A bare local agent has your full user
  account's access; a container caps the blast radius at the project directory.

The [dev container setup](#dev-container-required-for-any-local-agent) below takes
about five minutes. If that's friction you don't want, that's one more reason to take
the web route.

:::::::::::::::::::::::::::::::::::::::::::::::

### Claude Code

**Recommended route — web (no local access):**

1. You need a Claude subscription that includes Claude Code (Pro or Max), or
   workshop-provided credits.
2. Go to [claude.ai/code](https://claude.ai/code), connect your GitHub account, and
   point it at a repository. Each session clones the repo into a fresh, ephemeral
   cloud VM; your laptop is just a browser window. Results come back as branches/PRs
   you review on GitHub.
3. That's the whole setup — nothing to install.

**Local route (dev container required):**

- Inside your dev container, install the CLI: `npm install -g @anthropic-ai/claude-code`,
  then run `claude` from the project directory and log in when prompted.
- The VS Code extension gives the same engine an in-editor UI; make sure VS Code is
  attached to the container, not your host.
- **Institutional cloud routing**: the CLI can route requests through Google Vertex AI
  or AWS Bedrock if your institution provides cloud credits (UW–Madison workshops
  typically provide GCP credits — your instructors will share details). This changes
  billing and data handling, not the local-access picture — the container is still
  required.
- The desktop app is **not** recommended for this workshop unless you use its
  cloud-session mode: a "local repository" session runs on your machine with your
  full user access.

### GitHub Copilot

**Get the free education tier first** (students, teachers, and open-source
maintainers): apply at [GitHub Education](https://github.com/education), then — a
**separate second step** — redeem the Copilot benefit at the
[Copilot signup page](https://github.com/github-copilot/free_signup). This grants the
paid tier including agent mode and the cloud coding agent, not just autocomplete.
Allow a few days for verification; do this *before* the workshop.

**Recommended route — web (no local access):**

1. Use the chat UI at [github.com/copilot](https://github.com/copilot) and delegate
   tasks to the **cloud coding agent** at
   [github.com/copilot/agents](https://github.com/copilot/agents) (or by assigning an
   issue to Copilot on a repo where it's enabled).
2. Tasks run in GitHub's cloud sandbox against the GitHub-hosted repo and come back
   as draft PRs. Nothing executes on your machine.

**Local route (dev container or Codespace required):**

- Easiest compliant option: open the repo in a **GitHub Codespace** — the whole
  workspace is a cloud machine, so the "container" requirement is satisfied
  automatically, and the VS Code experience is identical.
- Otherwise: open the project *inside a dev container* in VS Code, install the GitHub
  Copilot extension in the container, sign in, and use **Agent** mode from the chat
  panel.

### OpenCode (free/open-source option)

- Open-source CLI agent ([opencode.ai](https://opencode.ai)) that works with several
  free hosted models — the fallback if you have no paid plan or credits.
- It's a local CLI, so **the dev container requirement applies**: install it inside
  the container, not on your host.
- It can also drive fully local models (e.g., via Ollama), which keeps your code on
  your machine entirely — at the cost of weaker models and real hardware needs. If
  you go this route, download models only from verified publishers (the trust episode
  explains why).

### Dev container (required for any local agent)

A dev container is a project-scoped Linux environment that VS Code (or any
devcontainer-compatible editor) runs your tools inside. The agent sees the project
and the container — not your home directory, your SSH keys, or the rest of your
machine.

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or
   Podman) and the VS Code **Dev Containers** extension.
2. In your project root, create `.devcontainer/devcontainer.json`:

   ```json
   {
     "name": "agentic-workshop",
     "image": "mcr.microsoft.com/devcontainers/python:3.12",
     "postCreateCommand": "pip install pandas scikit-learn pytest"
   }
   ```

3. In VS Code: **Dev Containers: Reopen in Container**. Install your agent CLI *in
   the container terminal* (e.g., the npm install above), and confirm it's
   containerized: `ls ~` inside the terminal should show a bare container home, not
   your real one.

No Docker and no time? Use **GitHub Codespaces** — it's the same devcontainer.json
running on a cloud machine, with a generous free tier, and it satisfies the
requirement with zero local installs.

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
