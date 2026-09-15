---
title: "Safety and Security: Limit What the Agent Can Access"
teaching: 20
exercises: 8
---

:::::::::::::::::::::::::::::::::::::: questions

- What can an agent actually access on my machine, and why does that matter?
- Which protections are real limits, and which are just requests the model may ignore?
- How do I keep credentials and sensitive or restricted data away from AI tools?
- How do I get an agent running safely on my own project?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Apply institutional data policies before pointing an agent at any project.
- Limit an agent along six axes: where it runs, which commands it may run, which credentials it can see, what it can commit, what it can reach on the network, and whom you trust.
- Distinguish instructions (which shape behavior) from permissions (which constrain it).
- Keep secrets out of local plaintext files entirely, loading them at runtime from a password manager.
- Start an agent session on your own repository using a cloud VM, a feature branch, and no keys on disk.

::::::::::::::::::::::::::::::::::::::::::::::::

## Follow your institution's GenAI policies

AI tools do not get an exemption from your institution's data rules. Like GenAI
itself, the policies are developing rapidly, so look out for changes. At UW–Madison
specifically:

- Follow all UW–Madison, UW System, and Board of Regents GenAI policies.
- DoIT overviews policies and vetted tools at [it.wisc.edu/ai](https://it.wisc.edu/ai/).
  If you are unsure of your data's classification level, reach out to a data steward
  via that page — or to your data governance office, IRB office, or IT office. They
  will be happy to help.
- **Never enter sensitive or restricted information into unvetted AI services**:
  student records (FERPA), health data (HIPAA/PHI), unpublished research, CUI,
  export-controlled data, or anything under a data use agreement (DUA) that prohibits
  third-party processing.

Remember: your code and prompts are sent to the model provider's servers for
inference. Every route in this episode protects your *machine*; none of them changes
where your *repository contents* go.

## Recognize what an agent can and cannot do

Mitigating risk starts with a realistic picture of the tool:

| A GenAI agent **can** | A GenAI agent **cannot** |
|---|---|
| Write or translate code | Work safely with sensitive or restricted data or secrets |
| Explain basic logic | Explain *human* logic — why your field does it this way |
| Execute validation steps you specify | Determine all the necessary validation steps |
| Run commands from your terminal (!) | Prevent all bad commands from running |

That last row is the one people underestimate. When you launch an agent from your
terminal or IDE, it operates with your user account's full filesystem and shell
access. It can read your SSH keys, your `.env` files, your notes — anything you can.
And agents *automatically scan for context*: that is their job. A credentials file in
your working directory is, from the agent's point of view, just more context.

## Limit what the agent can access

The rest of this episode is six limits, in this order:

1. **Where it runs.** A throwaway cloud VM, not your laptop.
2. **Which commands it may run.** Allow and deny rules.
3. **Which credentials it can see.** A password manager, never the repo.
4. **What it can commit.** Feature branch, pull request, you merge.
5. **What it can reach on the network.** An egress allowlist against prompt injection.
6. **Whom you trust.** Providers, their data policies, and downloaded repos and weights.

One distinction organizes all six. An *instruction* (a rules file, a line in a prompt)
asks the model to behave. A *permission* (a VM boundary, a deny rule, a branch
protection) removes the ability. **Instructions shape behavior; permissions constrain
it.** Prefer the second wherever you can get it.

### 1. Prefer a cloud VM over your own machine

Run the agent on a cloud virtual machine, not your local machine. There is then no
risk it wipes your filesystem, reads your password store, or finds last year's `.env`.

- **Claude Code on the web** ([claude.ai/code](https://claude.ai/code)) and **GitHub
  Copilot's cloud coding agent** ([github.com/copilot/agents](https://github.com/copilot/agents))
  both clone your repository into a throwaway VM. The work comes back as a branch or a
  pull request.
- **The desktop apps do both.** Claude Desktop and the VS Code extensions can run a
  cloud session *or* a local one. A "local repository" session runs on your machine
  with your full user access. **Check which mode you are in before you prompt.**
- Running locally anyway? Use a dev container, and know its limits.

::::::::::::::::::::::::::::::::::::: callout

## Dev containers are not a security boundary

A dev container caps the blast radius at the project directory, which is worth
having. But AWS does not consider containers a security boundary (see its bulletin on
the November 2025 `runc` container escapes), and Anthropic says the same of its own
[Claude Code dev container](https://code.claude.com/docs/en/devcontainer): use it
only with trusted repositories. The hierarchy, when local exposure is the concern:
**cloud VM (nothing runs locally) → dev container (contained local access) → bare
local agent (full user access).**

::::::::::::::::::::::::::::::::::::::::::::::::

### 2. Command permissions help, and are not sufficient

Allow, ask, and deny rules decide which commands run without asking. The defaults
usually deny nothing, so set them: deny `rm -rf`, force-push, and reads of `.env` and
`~/.ssh`. Claude Code's docs on
[permissions versus sandboxing](https://code.claude.com/docs/en/permissions) explain
the two mechanisms.

Understand what a permission rule is, though: **the check reads the command text, not
what the command does when run.** In January 2026, Cursor's allowlist was bypassed
([CVE-2026-22708](https://github.com/cursor/cursor/security/advisories/GHSA-82wg-qcm4-fp2w),
found by Pillar Security): prompt injection set an environment variable through a
shell built-in the allowlist did not check, and the next approved `git` command ran
the attacker's code. Deny rules are a layer. The VM is the wall.

### 3. Credentials: a password manager, never the repo

Agent instruction files help here too, but first the mechanism that actually removes
the risk. **A secret that isn't on disk can't be read, echoed, committed, or
exfiltrated** — by an agent, by malware, or by you at 11pm.

- Do not store passwords or API keys in `.env` files, JSON configs, or shell profiles.
- Keep keys in a password manager and load them once per session. Every UW–Madison
  NetID can (and should) request a free
  [1Password account](https://it.wisc.edu/services/1password/); the 1Password CLI
  (`op`) reads a secret by reference:

```bash
# bash / zsh — load the key once per session
export OPENAI_API_KEY=$(op read 'op://Private/bbadger/credential')
```

```powershell
# PowerShell
$env:OPENAI_API_KEY = op read "op://Private/bbadger/credential"
```

For a Jupyter workflow, keep a file of *references* (safe to commit — an `op://` path
is not a secret) and launch through `op run`, so every kernel inherits the variables
and no key ever appears in a notebook:

```bash
# .env.op  (references, not secrets; safe to commit)
OPENAI_API_KEY=op://Private/BadgerBrain/credential
OPENAI_BASE_URL=https://deepthought.doit.wisc.edu/v1

# launch JupyterLab through 1Password
op run --env-file=.env.op -- jupyter lab
```

```python
# in any notebook, in any kernel
import os
from openai import OpenAI
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
```

Never print the key and never paste it into a cell. 1Password prompts on each read;
your OS keychain, by contrast, hands secrets to any process running as you. Cloud
equivalents (AWS Secrets Manager, Azure Key Vault) work the same way. See the
[1Password CLI docs](https://developer.1password.com/docs/cli/secrets-environment-variables/).

::::::::::::::::::::::::::::::::::::: callout

## Agent instruction files: helpful, but not 100% reliable

An instruction file is a markdown file the agent reads at the start of every session:
project context, commands, conventions. Claude Code reads `CLAUDE.md`; Copilot reads
`.github/copilot-instructions.md`; nearly everything, Copilot included, also reads
`AGENTS.md`. Commit it to the repo and keep it short — test command, data location,
what not to touch. (The [planning](early-project-planning.md) episode shows one.)

But know what it is. In April 2026 a Cursor agent working a staging task for the
startup PocketOS hit a credential mismatch, found a Railway API token in an unrelated
file, and used it — deleting the production database and its backups in nine seconds.
The rules file lives in the same context window as everything else. **It is text the
model weighs, not a permission it lacks.** Instructions shape behavior; permissions
constrain it.

::::::::::::::::::::::::::::::::::::::::::::::::

### 4. Version control: feature branch, pull request, you merge

Version control is what makes agent mistakes cheap instead of catastrophic.

- Always use version control (GitHub, GitLab, Bitbucket).
- **Do not let an agent commit to `main`.** The agent creates a feature branch and
  opens a pull request; *you* review and merge.
- Review and test code before committing. Make small, frequent commits — each one is
  a save point.
- Start from a clean git state, so `git diff` shows exactly what the agent did and
  `git restore` undoes it.

Protect `main` on the host so that this is a permission, not a habit: require a pull
request and a passing check before merge (the verification episode sets that up).

### 5. Network: treat everything the agent reads as untrusted

An agent treats the text it reads as instructions. A README, an issue, a web page, or
a dependency's install script can carry commands it will follow. This is **prompt
injection**, and it is not hypothetical:

- **GitHub MCP, May 2025.** Invariant Labs showed that a malicious issue in a public
  repository could steer an agent with GitHub access into leaking data from the
  user's private repositories.
- **Nx on npm, August 2025.** A compromised package's install script prompted the
  victim's *own* Claude Code, Gemini CLI, or Amazon Q to search the machine for
  secrets; thousands of credentials were leaked to public GitHub repositories. (Wiz's
  analysis found Claude refused about a quarter of the time — a layer, not a wall.)

Reduce the risk:

- **Be careful what you install and clone.** Every dependency's install script and
  every file in a repository is code the agent runs and text it reads.
- **Treat anything the agent reads as untrusted** — issues, PR comments, web pages. A
  prompt that sends it to the web brings back whatever the page says.
- **Use the web session and keep its defaults.** Claude Code on the web and Copilot's
  cloud agent limit network access to an allowlist and keep your keys out of the
  sandbox. Do not turn the firewall off to fix a blocked request.
- **Review the PR before you merge.** The last wall of defense.

Simon Willison's ["lethal trifecta"](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
names the combination to avoid: private data, exposure to untrusted content, and a way
to send data out. Remove any one leg and the attack fails.

### 6. Whom you trust: providers, models, and repos

The last limit is the one no setting enforces: which providers, packages, and model
weights you let into the loop at all. Vet a provider's data policy (is my data used
for training, and is that the default? how long is it retained? where does inference
run? does an institutional agreement cover this?), and treat downloaded weights and
packages with the suspicion you'd give any executable. The next episode,
[trust](trust.md), goes through each with the incidents behind the rules.

::::::::::::::::::::::::::::::::::::: callout

## No agents on machines that hold sensitive or restricted data

To be explicit: **running an agent locally on any machine that stores sensitive or
restricted data is not recommended at this time — full stop.** Permission settings,
deny rules, and containers don't change this: local agents scan for context, anything
on the machine can end up in a prompt, and "the agent shouldn't have looked there" is
not a control your compliance office will accept.

If you must work on a repository from such a machine, use a route with **no local
access by construction** — a web UI where the agent operates only on a cloud-hosted
copy of the repo. The repo itself must still be free of sensitive or restricted data,
since its contents do go to the provider. Until your institution establishes vetted
secure routes, the operating rule is simple: **agents and sensitive or restricted data
live on separate machines.**

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Get your agent running (8 minutes)

Everyone gets an agent open on their own repository, safely, before any real work.

1. **Use a web session.** Claude Code on the web ([claude.ai/code](https://claude.ai/code))
   or Copilot's cloud agent ([github.com/copilot/agents](https://github.com/copilot/agents)).
   Nothing runs on your machine. (Other routes, including free ones, are on the
   [setup page](../learners/setup.md).)
2. **Use your own project repository.** For a team project, the primary owner
   creates a `<username>-main` branch to merge tonight's work into; everyone else
   forks the repo to get a clean copy. Agents generate many branches — keep them
   yours. No project yet? Create a small repository now.
3. **Confirm cloud before you prompt.** The session should be pointed at a cloud VM
   clone of a GitHub repo, not a local folder on your laptop.
4. **Keys via `op read`, not `.env`.** No `.env` anywhere in the repo, and preferably
   no keys stored on your machine at all.
5. Prompt: *"Read this repo and tell me what it's doing, or attempting to do. Do not
   change anything."* While it works, note what it gets right, what it states
   confidently that you can't verify, and what it doesn't know that you do.

:::::::::::::::::::::::: solution

## What to check

If step 3 is wrong — the session is local — stop and switch before prompting; that is
the single most common mistake with the desktop apps. The read-only prompt in step 5
also previews the planning episode: agents are excellent at *what* and *how* (structure,
dependencies, data flow) and blind to *why* and *for whom*, which is exactly the
knowledge a plan and an instruction file have to supply.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Institutional data policies apply unchanged: sensitive or restricted data stays away from unvetted AI services, on every route.
- Agents run with your permissions and scan your workspace for context — assume anything on disk in plaintext can be read.
- Limit six things: where it runs (cloud VM), which commands (allow/deny), which credentials (password manager), what it commits (branch + PR), what it reaches (network allowlist), whom you trust.
- Instructions shape behavior; permissions constrain it. A rules file is text the model weighs, not a permission it lacks.
- The only secret an agent can't leak is one that isn't there: load keys at runtime with `op read`.
- Prompt injection is real: treat everything the agent reads as untrusted, keep the web session's firewall on, and review the PR before you merge.

::::::::::::::::::::::::::::::::::::::::::::::::
