---
title: "Trust: Packages, Models, and Providers"
teaching: 12
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I decide whether to trust a package, a model, or an AI provider?
- What new supply-chain risks does agentic coding introduce?
- What has gone wrong in practice, and what would have prevented it?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Review every dependency an agent adds, and verify that packages exist and are official before installing.
- Treat downloaded model weights as executable code and apply provenance checks accordingly.
- Vet an AI provider's data policy by answering four questions before use.
- Connect each practice to a documented incident.

::::::::::::::::::::::::::::::::::::::::::::::::

The safety episode ended with the one limit no setting enforces: whom you trust. The
rest of this lesson assumes that the packages you install and the services you call
are what they claim to be. That assumption deserves the same scrutiny as the data.
Agentic coding raises the stakes in one specific way: the agent installs packages,
downloads models, and sends your code to a provider on your behalf. Decisions that
were once made one at a time are now made quickly and in bulk unless you deliberately
stay involved.

## Packages: the agent multiplies your supply-chain exposure

Open-source package ecosystems have always carried supply-chain risk. Even carefully
maintained infrastructure can be compromised; the 2024
[`xz-utils` backdoor](https://en.wikipedia.org/wiki/XZ_Utils_backdoor) was inserted
by a contributor who spent years building maintainer trust. Agents add two
new problems:

- **Hallucinated packages ("slopsquatting").** Language models sometimes recommend
  packages that do not exist. In one [large 2025 study](https://arxiv.org/abs/2406.10279),
  roughly a fifth of packages suggested by code-generating models were fabrications,
  and the same invented names recur across sessions. Attackers can register those
  names. Security researcher Bar Lanyado
  [demonstrated this](https://www.lasso.security/blog/ai-package-hallucinations) by
  registering `huggingface-cli`, a name models repeatedly invented; the empty
  placeholder received more than 15,000 downloads in three months and appeared in a
  major company's installation instructions.
- **Typosquatting and dependency confusion happen faster.** In December 2022, a
  malicious [`torchtriton`](https://pytorch.org/blog/compromised-nightly-dependency/)
  package on PyPI shadowed a PyTorch-nightly internal dependency and exfiltrated SSH
  keys and files from thousands of machines. In December 2024, compromised releases
  of [`ultralytics`](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/)
  (the widely used YOLO library) installed a cryptominer on any machine that installed
  during the affected window.
  Neither incident involved AI, but an agent that runs `pip install` unattended
  removes the moment at which a person might have noticed an unfamiliar name.

Practices that follow:

- **Do not auto-approve package installation.** Keep installs on the list of actions
  that require approval, or add "do not add new dependencies without asking" to the
  project context file, remembering that context files are advisory.
- **Before installing anything an agent suggests, verify that it exists and is
  official.** Check the registry page, the linked source repository, download counts,
  and release history. A brief check defeats most slopsquatting.
- **Pin versions in a lockfile** and prefer environments you can rebuild
  (`requirements.txt` or `environment.yml` under version control), so that a bad
  install is reverted rather than investigated.

## Model weights are code

Running open-weight models locally has a privacy advantage: the data never leaves your
machine. But downloaded weights deserve the same caution as downloaded executables,
because in the common formats they are executables. Four ways a model download can
cause harm, each with a documented case:

- **Weights can carry code.** Python's pickle serialization, used by many model files,
  runs arbitrary code on load. In 2024 [JFrog found](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/)
  on the order of a hundred malicious models on Hugging Face whose payloads included
  opening a reverse shell when loaded. Scanners have not caught everything since.
- **Fake repositories.** Check the organization, not the model card. In 2026
  [HiddenLayer identified](https://www.hiddenlayer.com/research/malware-found-in-trending-hugging-face-repository-open-oss-privacy-filter)
  `Open-OSS/privacy-filter`, posing as an OpenAI release with a copied model card and
  a loader that installed an infostealer, at the top of Hugging Face's trending list.
- **Values are trained in.** DeepSeek R1 censors certain topics; Perplexity's
  [R1 1776](https://www.perplexity.ai/hub/blog/open-sourcing-r1-1776) (2025) was
  post-trained specifically to remove that behavior. Whatever a model's builders
  trained it to do or avoid, it will do or avoid in your pipeline.
- **Hidden backdoors work, and no reliable detector exists.** In Mithril's
  [PoisonGPT](https://blog.mithrilsecurity.io/poisongpt-how-we-hid-a-lobotomized-llm-on-hugging-face-to-spread-fake-news/)
  demonstration (2023), an edited GPT-J spread a specific false fact, kept its
  benchmark scores, and was uploaded under a lookalike organization. No detector
  caught it. More below.

Practices that follow:

- Prefer **`safetensors`**, a weights-only format that cannot execute code, over
  pickle formats when available.
- Download from the **verified official organization account** (for example
  `meta-llama` or `mistralai`), not a re-upload, and check checksums where published.
- **Do not set `trust_remote_code=True` by default.** It runs whatever Python ships
  with the model. Tooling can get this wrong on your behalf: InstructLab hardcoded it
  on ([CVE-2026-6859](https://github.com/advisories/GHSA-rxpq-xgqx-fr7p)).
- "Open weights" does not mean audited. Provenance tells you who built the model, not
  that it is sound. Smaller local models also hallucinate more, including package
  names, which returns to the previous section.

### Backdoors in the weights themselves

Using safetensors closes the code-execution route. It does nothing about a separate
class of attack in which the malicious behavior is in the parameters rather than the
file format. A model can be built or modified to behave normally in almost all cases
and misbehave on a trigger:

- **Surgical weight edits.** In the PoisonGPT proof of concept (2023), researchers
  edited an open model to emit specific false facts, re-uploaded it under a
  typosquatted organization name, and showed that standard benchmarks barely changed.
  Benchmarks do not establish trust.
- **Sleeper agents.** Anthropic's [2024 research](https://www.anthropic.com/research/sleeper-agents-training-deceptive-llms-that-persist-through-safety-training)
  trained models that wrote secure code
  when the prompt said the year was 2023 and inserted exploitable vulnerabilities when
  it said 2024. Standard safety training failed to remove the behavior and sometimes
  taught the model to conceal it.
- **Data poisoning is inexpensive.** A [2025 study](https://www.anthropic.com/research/small-samples-poison)
  by Anthropic with the UK AI Security Institute found that a few hundred poisoned
  documents in a training corpus can implant a backdoor, roughly independent of model
  size. Earlier work (for example [TrojanPuzzle](https://arxiv.org/abs/2301.02344))
  showed that code-suggestion models can be poisoned to emit insecure patterns.
- **Graph-level backdoors.** Techniques such as
  [ShadowLogic](https://hiddenlayer.com/research/shadowlogic/) embed the backdoor in
  a model's computational graph (for example ONNX), again with no code execution.

This matters for agentic coding in particular because a backdoored code model does
not need to attack your machine; it needs only to write subtly vulnerable code that
you trust, run, and ship. In an agentic setup the trigger can also be delivered:
prompt injection through a poisoned README or issue, combined with a backdoored model
that has tool access, is worse than either alone.

Detecting behavioral backdoors is an open research problem. No scanner finds them and
benchmarks do not reveal them. The defenses are therefore the routine ones:
provenance from heavily scrutinized official sources, extra caution before connecting
a niche fine-tune to a pipeline with tool access or untrusted inputs, and treating
model output as untrusted regardless of where the weights came from. The last of
these is the review discipline this lesson already requires, and it protects you
whether the bad code comes from an average-case guess or a backdoor.

## The tools themselves are an attack surface

The agent's harness (the extension, the CLI, its hooks and configuration) is software,
and it is a valuable target because it holds your permissions:

- In July 2025, an attacker inserted a prompt into the **Amazon Q** VS Code extension
  through a GitHub pull request, instructing the embedded agent to wipe the user's
  files and cloud resources. The poisoned version shipped to users before it was
  caught ([404 Media](https://www.404media.co/hacker-plants-computer-wiping-commands-in-amazons-ai-coding-agent/)).
- In December 2025 a researcher disclosed more than 30 vulnerabilities across AI
  coding IDEs, with 24 CVEs assigned (the ["IDEsaster"](https://thehackernews.com/2025/12/researchers-uncover-30-flaws-in-ai.html)
  findings).
- Agents can also cause damage with no attacker. In July 2025, **Replit's** coding
  agent deleted a production database during a "vibe-coding" experiment despite
  explicit instructions to freeze changes, then produced misleading output about what
  it had done ([Fortune](https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/)).

Keep agent tooling updated, install extensions only from official marketplaces, and
never point an agent at production systems or irreplaceable data. Separation of
development and production, and backups, remain necessary.

## Vet the provider as you would vet a data source

Whichever provider you choose (Anthropic, GitHub/Microsoft, Google, a startup, a model
router), you are sending your code and prompts to them. Before committing, answer four
questions from the provider's policy documents rather than its marketing material:

1. **Are my data and code used for training, and is that the default?** Commercial and API
   terms typically prohibit it. Consumer plans often make it a setting, sometimes
   enabled by default. Find the setting and decide.
2. **How long is it retained, and who can see it?** Retention windows differ by an
   order of magnitude between plan tiers. Feedback buttons and safety reviews often
   extend them.
3. **Where does inference run, and under whose jurisdiction?** In January 2025,
   [Wiz researchers found](https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak)
   a publicly exposed **DeepSeek** database leaking user chat histories and API keys. Provider security practice and legal jurisdiction are part
   of the arrangement.
4. **Does an institutional agreement cover this, or is it a personal contract?** In
   2023, **Samsung** engineers pasted proprietary source code into ChatGPT while
   debugging; the company responded by
   [banning generative AI tools internally](https://www.bloomberg.com/news/articles/2023-05-02/samsung-bans-chatgpt-and-other-generative-ai-use-by-staff-after-leak). An
   individual subscription gives your institution no protection, which is why the
   safety episode's rule (restricted data stays off unvetted tools) exists.

### Claude and Copilot defaults (as of September 2026)

The two tools this lesson uses most illustrate how much the answers depend on plan
tier rather than provider:

| | Claude Code (Free, Pro, Max) | GitHub Copilot (Free, Pro, Pro+) |
|---|---|---|
| Trains by default? | Yes; opt out under Settings → Privacy ([consumer terms](https://www.anthropic.com/news/updates-to-our-consumer-terms)). Team, Enterprise, API, and Bedrock: no ([Claude Code data usage](https://code.claude.com/docs/en/data-usage)) | Yes, since April 2026; opt out in [Copilot settings](https://github.com/settings/copilot) ([GitHub docs](https://docs.github.com/en/copilot/how-tos/manage-your-account/manage-policies)). Business, Enterprise, and students: no |
| Retained how long? | 5 years if training is on, 30 days if off ([Privacy Center](https://privacy.anthropic.com/)) | 28 days |
| Where does it run? | Anthropic VMs in the US, or Amazon Bedrock on the university's AWS account | GitHub's Azure in the US; Claude and Gemini models via AWS, Anthropic, and Google Cloud |
| Institutional or personal? | Personal. The Bedrock route is institutional, with zero data retention through 2026 | Personal, via GitHub Education. Not on UW–Madison's vetted list |

Neither consumer route is on UW–Madison's list of vetted AI tools. Policies change;
consult the linked pages rather than this table.

::::::::::::::::::::::::::::::::::::: callout

## Free services have a cost

If a tool or model API is free and is not open source running on your own hardware,
consider what the provider receives. Often it is your prompts, and through them your
code and data. That may be acceptable for public workshop exercises and unacceptable
for unpublished research.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Vet the tool you are using now (5 minutes)

For the agentic tool you set up for this workshop, answer the four questions above
from the provider's privacy and data pages, not from memory.

1. Training: on or off by default for your plan? Where is the setting?
2. Retention: how long, and what extends it?
3. Where does inference run?
4. Are you covered by an institutional agreement, or is this a personal contract?

Compare notes with a neighbor using a different tool.

:::::::::::::::::::::::: solution

## Typical findings

Most participants find at least one surprise: a training setting they had not seen,
a retention clause tied to the feedback button, or the discovery that a tool they
assumed was institutional is a personal agreement. The answers vary by provider and
by plan tier within a provider, which is why vetting the policy cannot be delegated,
including to the agent.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Agents install packages and download models quickly and in bulk. Keep those decisions on the list that requires approval.
- Hallucinated package names are an attack vector (slopsquatting). Verify that a package exists and is official before installing anything an agent suggests.
- Model weights in pickle formats are executable code. Prefer safetensors, download from verified organizations, do not enable `trust_remote_code` by default, and check provenance.
- Backdoors can be in the weights themselves (poisoned training data, surgical edits, trigger behaviors). No scanner or benchmark detects them; provenance and reviewing model output are the defenses.
- The agent tooling is itself an attack surface. Keep it updated, and never point an agent at production or irreplaceable data.
- Vet the provider's data policy: training default, retention, jurisdiction, and whether an institutional agreement applies.
- Provider defaults differ by plan tier. Consumer Claude and Copilot plans train on your data unless you opt out; team, enterprise, API, and education tiers do not. Check the setting, not the brand.
- Each rule here has a named incident behind it: torchtriton, Ultralytics, huggingface-cli, Amazon Q, Replit, DeepSeek, Samsung, the fake OpenAI repository, InstructLab. None required a sophisticated attacker; all required a missing check.

::::::::::::::::::::::::::::::::::::::::::::::::
