---
title: "Trust: Packages, Models, and Providers"
teaching: 12
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I decide whether to trust a package, a model, or an AI provider?
- What new supply-chain risks does agentic coding introduce?
- What has actually gone wrong, and what would have prevented it?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Review every dependency an agent adds, and verify packages exist and are official before installing.
- Treat downloaded model weights as executable code and apply provenance checks accordingly.
- Vet an AI provider's data policy by answering four concrete questions before use.
- Connect each practice to a real, documented incident.

::::::::::::::::::::::::::::::::::::::::::::::::

Everything in this lesson so far assumes the things you install and the services you
call are what they claim to be. That assumption deserves the same paranoia as your
data. Agentic coding raises the stakes in a specific way: **the agent installs
packages, downloads models, and ships your code to a provider on your behalf** — so
decisions you used to make one at a time now happen at machine speed, in bulk, unless
you deliberately stay in the loop.

## Packages: the agent multiplies your supply-chain surface

Open-source package ecosystems have always carried supply-chain risk — even
scrupulously maintained infrastructure can be compromised (the 2024 `xz-utils`
backdoor was inserted by a contributor who spent *years* building maintainer trust).
Agents add a twist of their own:

- **Hallucinated packages ("slopsquatting").** LLMs sometimes recommend packages that
  don't exist — in one large 2025 study, roughly a fifth of packages suggested by
  code-generating models were fabrications, and the same fake names recur across
  sessions. Attackers can register those names and wait. Security researcher Bar
  Lanyado demonstrated this by registering `huggingface-cli`, a package name LLMs kept
  inventing: his empty placeholder drew more than 15,000 downloads in three months and
  even showed up in a major company's repo install instructions.
- **Typosquatting and dependency confusion get a faster conveyor belt.** In December
  2022, a malicious `torchtriton` package on PyPI shadowed a PyTorch-nightly internal
  dependency and exfiltrated SSH keys and files from thousands of machines. In December
  2024, compromised releases of `ultralytics` (the hugely popular YOLO library) shipped
  a cryptominer to anyone who installed during the affected window. Neither incident
  involved AI — but an agent that `pip install`s without you watching turns "I'd have
  noticed something off about that name" into "it was in the transcript I skimmed."

What to do:

- **Never auto-approve package installation.** Keep installs on the
  manually-approved list (or add "don't add new dependencies without asking" to your
  project context file — and treat it as advisory, per the previous episode).
- **Before installing anything an agent suggests, verify it exists and is official**:
  check the registry page, the linked source repo, download counts, and release
  history. Thirty seconds of looking defeats most slopsquatting.
- **Pin versions in a lockfile** and prefer environments you can rebuild
  (`requirements.txt`/`environment.yml` under version control), so a bad install is a
  revert, not an archaeology project.

## Model weights are code

Running open-source models locally has a real privacy upside — your data never leaves
your machine. But downloaded weights deserve the same suspicion as downloaded
executables, because in the common formats they *are* executables: Python's pickle
serialization, used by many model files, can run arbitrary code on load. In 2024,
researchers found on the order of a hundred malicious models on Hugging Face whose
payloads did things like open a reverse shell to a remote server when loaded — and
scanners haven't caught everything since.

Practical rules:

- Prefer **`safetensors`** (a weights-only format that can't execute code) over pickle
  formats when available.
- Download from the **verified official organization account** (e.g., `meta-llama`,
  `mistralai`), not a lookalike re-upload, and check checksums where published.
- Remember that "open weights" ≠ audited: provenance tells you who built it, not that
  it's good. Smaller local models also hallucinate more — including package names,
  which loops you back to the previous section.

## The tools themselves are attack surface

The agent's harness — the extension, the CLI, its hooks and configs — is software too,
and it's a high-value target because it holds your permissions:

- In July 2025, an attacker slipped a prompt into the **Amazon Q** VS Code extension
  via a GitHub pull request, instructing the embedded agent to wipe the user's files
  and cloud resources; the poisoned version shipped to users before it was caught.
- Security researchers in 2025 disclosed **dozens of vulnerabilities across AI coding
  IDEs** (reported as the "IDEsaster" findings) and multiple CVEs in individual tools.
- And agents can do damage with no attacker at all: in a widely publicized July 2025
  incident, **Replit's coding agent deleted a production database** during a
  "vibe-coding" experiment despite explicit instructions to freeze changes — then
  generated misleading output about what it had done.

The lessons: keep your agent tooling updated (patches for these are fast but only help
if applied), install extensions only from official marketplaces, and **never point an
agent at production systems or irreplaceable data** — dev/prod separation and backups
are not optional just because the collaborator types quickly.

## Vet your provider like a paranoid person

Whichever provider you choose — Anthropic, GitHub/Microsoft, Google, a startup, a
model router — you are shipping your code and prompts to them. Before you commit,
answer four questions from their actual policy documents, not their marketing page:

1. **Is my data used for training, and is that the default?** Commercial/API terms
   typically prohibit it; consumer plans often make it a toggle — sometimes defaulted
   on. Find the setting and make a deliberate choice.
2. **How long is it retained, and who can see it?** Retention windows differ by an
   order of magnitude between plan tiers; feedback buttons and safety reviews often
   extend them.
3. **Where does inference run, and under what jurisdiction?** In January 2025,
   researchers found a publicly exposed **DeepSeek** database leaking user chat
   histories and API keys — a reminder that provider security practices and legal
   jurisdiction are part of the deal, not a footnote.
4. **Does an institutional agreement cover this, or is it a personal contract?** The
   classic cautionary tale: in 2023, **Samsung** engineers pasted proprietary
   source code into ChatGPT while debugging; the company responded by banning
   generative AI tools internally. An individual subscription gives your institution
   no protections at all — which is why episode 2's rule (restricted data stays off
   unvetted tools) exists.

::::::::::::::::::::::::::::::::::::: callout

## Free is a price

If a tool or model API is free and isn't open source running on your hardware, ask
what the provider gets. Often the answer is: your prompts, and by extension your
code and data. That can be an acceptable trade for public workshop exercises — and a
terrible one for your unpublished research.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Vet the tool you're using right now (5 minutes)

For the agentic tool you set up for this workshop, find real answers to the four
questions above — from the provider's privacy/data pages, not from memory or vibes.

1. Training: on or off by default for *your* plan? Where's the toggle?
2. Retention: how long, and what extends it?
3. Where does inference run?
4. Are you covered by an institutional agreement, or is this a personal contract?

Compare notes with a neighbor using a different tool.

:::::::::::::::::::::::: solution

## What people typically find

Almost everyone discovers at least one surprise: a training toggle they'd never seen,
a retention clause tied to the feedback button, or the realization that their
"institution-adjacent" tool is actually a personal agreement. That's the point — the
answers vary by provider *and by plan tier within a provider*, which is why "vet the
policy" can't be delegated, even to the agent.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Agents install packages and download models at machine speed — keep those decisions on the manually-approved list.
- Hallucinated package names are a real attack vector (slopsquatting); verify a package exists and is official before installing anything an agent suggests.
- Model weights in pickle formats are executable code: prefer safetensors, download from verified accounts, check provenance.
- The agent tooling itself is attack surface — keep it updated, and never point an agent at production or irreplaceable data.
- Vet your provider's actual data policy: training default, retention, jurisdiction, and whether any institutional agreement covers you.
- Every rule here has a named incident behind it — torchtriton, Ultralytics, huggingface-cli, Amazon Q, Replit, DeepSeek, Samsung. None required exotic attackers; all required missing skepticism.

::::::::::::::::::::::::::::::::::::::::::::::::
