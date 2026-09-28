---
title: Setup
---

## Setup

To follow along you need three things:

1. A **GitHub account** and, if you work locally, a working **git** installation.
2. Access to at least one **agentic coding tool**. The lesson is tool-agnostic, so
   any agent is acceptable.
3. A **repository to work on**, ideally your own project, and a way to load any API
   keys that keeps them off disk.

You do not need to install Python. On the recommended web route the agent runs code
in its own cloud sandbox and installs what the project needs; on the local route the
dev container image provides Python.

The safety episode's exercise *Get your agent running, safely* covers the first
session. The checklist at the [end of this page](#before-your-first-session) lists
the same steps in short form.

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

## Choose an agentic coding tool

::::::::::::::::::::::::::::::::::::::: caution

## No agentic tools on machines holding sensitive or restricted data

If the machine stores restricted data (FERPA, HIPAA/PHI, CUI, export-controlled
data, unpublished sensitive research, or anything under a data-use agreement), **do
not install or run any agentic tool on it, including inside a dev container.** The
container requirement below protects a clean machine from the agent. It does not make
it acceptable to run agents alongside restricted data, where one mis-mounted folder
exposes everything and institutional policy prohibits unvetted tools in any case. Use
a different machine, or a browser-only web route against a repository containing no
restricted data. The safety episode explains the reasoning.

:::::::::::::::::::::::::::::::::::::::::::::::

Any of the tools below works for every exercise. If your workshop provides cloud
credits or a specific tool, use that; otherwise use whichever you can access.

Agents run with the permissions of the environment they execute in, so the setup is
organized by **where the agent runs** rather than by tool:

- **Web route (recommended).** The agent works on a cloud copy of a GitHub
  repository and has no access to your machine: no local filesystem, no SSH keys, no
  credentials. Nothing to install and nothing to isolate.
- **Local route.** The agent runs on your machine, and a bare local agent has your
  full user account's access. For this workshop, and as a general default, a local
  agent runs **inside a dev container** (or a cloud workspace such as GitHub
  Codespaces), which limits it to the project directory.

Pick your tool in the tabs below; the choice carries across the page.

<!-- Contributors: to add a tool, add a tab with the same heading (### Tool name) to
each of the three group-tab blocks below (accounts, web route, local route), so the
tabs stay in sync. If a tool has no route of one kind, say so in that tab. -->

### Accounts and access

:::::::::::::::: group-tab

### Claude Code

You need a Claude subscription that includes Claude Code (Pro or Max), or
workshop-provided credits.

**Institutional cloud routing.** The CLI can route requests through Google Vertex AI
or AWS Bedrock if your institution provides cloud credits (UW–Madison workshops
typically provide GCP credits; your instructors will share details). This changes
billing and data handling only, not where the agent runs.

### GitHub Copilot

**Get the free education tier first** (students, teachers, and open-source
maintainers): apply at [GitHub Education](https://github.com/education), then, as a
**separate second step**, redeem the Copilot benefit at the
[Copilot signup page](https://github.com/github-copilot/free_signup). This grants the
paid tier including agent mode and the cloud coding agent, not just autocomplete.
Allow a few days for verification; do this *before* the workshop.

### OpenCode

[OpenCode](https://opencode.ai) is an open-source CLI agent that works with several
free hosted models: the fallback if you have no paid plan or credits. No account is
required for the free models. It can also drive fully local models (for example via
Ollama), which keeps your code on your machine entirely, at the cost of weaker models
and real hardware needs. If you go this route, download models only from verified
publishers (the trust episode explains why).

::::::::::::::::::::::::

### Web route (recommended)

:::::::::::::::: group-tab

### Claude Code

1. Go to [claude.ai/code](https://claude.ai/code), connect your GitHub account, and
   point it at a repository.
2. Each session clones the repository into a fresh, ephemeral cloud VM; your laptop is
   only a browser window. Results come back as branches and pull requests you review
   on GitHub.
3. That is the whole setup. Nothing to install.

The desktop app is acceptable only in its cloud-session mode. A "local repository"
session runs on your machine with your full user access, and belongs under the local
route.

### GitHub Copilot

1. Use the chat UI at [github.com/copilot](https://github.com/copilot) and delegate
   tasks to the **cloud coding agent** at
   [github.com/copilot/agents](https://github.com/copilot/agents), or assign an issue
   to Copilot on a repository where it is enabled.
2. Tasks run in GitHub's cloud sandbox against the GitHub-hosted repository and come
   back as draft pull requests. Nothing executes on your machine.

### OpenCode

OpenCode has no hosted web route. Use the local route, or open the repository in a
GitHub Codespace and install OpenCode there, which satisfies the container
requirement with nothing on your machine.

::::::::::::::::::::::::

### Local route (dev container required)

The web route above is the recommended one, and if you use it you can skip this
section entirely. Use the local route only if you need the agent on your own machine,
and then complete the dev container setup first, followed by the tool-specific steps
in the tabs that follow.

A dev container is a project-scoped Linux environment that VS Code (or any
devcontainer-compatible editor) runs your tools inside. The agent sees the project
and the container, not your home directory, your SSH keys, or the rest of your
machine. Setup takes about five minutes.

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or
   [Podman](https://podman.io/docs/installation)) and the VS Code **Dev Containers**
   extension. To use Podman with VS Code, open the Command Palette, choose
   **Preferences: Open User Settings (JSON)**, and add this setting so the Dev
   Containers extension runs `podman` rather than `docker`:

   ```json
   {
     "dev.containers.dockerPath": "podman"
   }
   ```
2. In your project root, create `.devcontainer/devcontainer.json`:

   ```json
   {
     "name": "agentic-workshop",
     "image": "mcr.microsoft.com/devcontainers/python:3.12",
     "remoteUser": "vscode",
     "runArgs": [
       "--userns=keep-id"
     ],
     "postCreateCommand": "python -m pip install pandas scikit-learn pytest"
   }
   ```

   **Podman Desktop (optional).** [Podman Desktop](https://podman-desktop.io/) is a
   graphical application for managing your local Podman containers. Open it and make
   sure the Podman engine is running. After VS Code creates the dev container, you can
   use Podman Desktop's **Containers** view to see that container, inspect its logs,
   or stop it when you are finished. Continue to open and work on the project in VS
   Code; Podman Desktop is only for monitoring and managing the local container.

3. In VS Code, open the Command Palette, choose **Dev Containers: Reopen in
   Container**, and wait for VS Code to rebuild and reopen the project. Install your
   agent CLI *in the container terminal* (your command prompt will be something like
   `vscode@containerID:/workspaces/Intro-to-Agentic-Coding$`), and confirm it is
   containerized: `ls ~` inside the terminal should show a bare container home, not
   your real one.

If you cannot install Docker, use **GitHub Codespaces**. It runs the same
`devcontainer.json` on a cloud machine, has a free tier, and satisfies the
requirement with no local installation.

With the container running, install your tool inside it:

:::::::::::::::: group-tab

### Claude Code

- In the container terminal, install the CLI with
  `npm install -g @anthropic-ai/claude-code`, then run `claude` from the project
  directory and log in when prompted.
- The VS Code extension gives the same engine an in-editor UI; make sure VS Code is
  attached to the container, not your host.
- Institutional cloud routing (Vertex AI or Bedrock, above) changes billing and data
  handling only. The container is still required.

### GitHub Copilot

- Easiest option: open the repository in a **GitHub Codespace**. The whole workspace
  is a cloud machine, so the container requirement is satisfied automatically, and
  the VS Code experience is identical.
- Otherwise, with the project open inside your dev container in VS Code, install the
  GitHub Copilot extension in the container, sign in, and use **Agent** mode from the
  chat panel.

### OpenCode

- In the container terminal, install OpenCode following
  [opencode.ai](https://opencode.ai), then run it from the project directory. Install
  it inside the container, not on your host.
- For fully local models, the model server (for example Ollama) also needs to be
  reachable from inside the container.

::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::: callout

## Before the workshop: check your data-privacy settings

If you are on an individual or consumer AI plan, find the model-training setting in
your account and make a deliberate choice. No restricted or sensitive data (student
records, health data, unpublished sensitive research) goes into any AI tool not
covered by an institutional agreement. UW–Madison users: see
[it.wisc.edu/ai](https://it.wisc.edu/ai/).

:::::::::::::::::::::::::::::::::::::::::::::::

## Optional: GitHub token (for the MCP exercise)

The [MCP tools and skills](../episodes/skills-and-mcp.md) episode connects your agent
to the GitHub MCP server. Create a
[fine-grained personal access token](https://github.com/settings/personal-access-tokens/new)
scoped to **read-only** access (Issues and Pull requests: read) on one repository
you do not mind exposing, not a token with write, delete, or organization-wide scope.
Set it as an environment variable (`GH_TOKEN`) rather than writing it into a
configuration file that might be committed.

## A repository to work on

The exercises run on **your own project repository** where possible. The team
conventions, the plan, the first feature, the assertions, and the CI workflow are all
committed to a repository you will continue to use. For a team project:

- **One shared repository, with branches rather than forks.** Each person works on a
  branch named for them. Teammates and their agents can fetch and read a branch; they
  cannot see a fork without adding remotes.
- **Obtain write access before the session.** If you lack it, ask the repository
  owner to add you as a collaborator.
- **Protect `main`** so that nothing is merged without a pull request. The
  verification episode adds a passing-check requirement.

If you have no project, create a small repository now with a README and a slice of
data you understand. The feature-based-development episode provides a scikit-learn
starter for anyone without a dataset.

## API keys: a password manager, never a file

If your project calls a model API (for example a hosted open-weight model with an
OpenAI-style endpoint), keep the key in a password manager and load it per session
instead of writing a `.env`. Every UW–Madison NetID can request a free
[1Password account](https://it.wisc.edu/services/1password/); with the
[1Password CLI](https://developer.1password.com/docs/cli/get-started/) installed:

```bash
export OPENAI_API_KEY=$(op read 'op://Private/<item>/credential')     # bash/zsh
```

```powershell
$env:OPENAI_API_KEY = op read "op://Private/<item>/credential"        # PowerShell
```

For JupyterLab, keep a `.env.op` file of `op://` references (safe to commit) and
launch with `op run --env-file=.env.op -- jupyter lab`. The safety episode shows the
full pattern. If you do not use 1Password, any secrets manager or your OS keyring
works the same way. The rule is that no key is stored in the repository or in a
plaintext file an agent could read.

## Before your first session

The checklist from the *Get your agent running, safely* exercise:

1. **Choose a cloud route with plan mode.** Claude: [claude.ai/code](https://claude.ai/code);
   nothing to install, and plan mode is built in. Copilot: install the
   [GitHub Copilot app](https://docs.github.com/en/copilot/concepts/agents/github-copilot-app)
   for an explicit plan mode (the agent asks questions and waits for your approval
   before editing) and start a **cloud** session, not a local one. If you cannot
   install it, the Copilot web works too: ask for a plan in the prompt and you get
   the same approve-or-exit gate, with less interaction. The desktop apps are
   acceptable provided the session is cloud-hosted.
2. **Confirm the session is cloud-hosted before you prompt.** It should show a cloud
   VM and a GitHub repository, not a local folder. Cloud sandboxes are billed by
   usage; confirm your account works first.
3. **Point it at your project repository**, on a branch named for you.
4. **Load keys with `op read`.** No `.env` in the repository.
5. **Start from a clean git state.**
