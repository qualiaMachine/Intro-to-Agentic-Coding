---
title: 'Reference'
---

## Glossary

**Agentic coding**
: Working with an AI tool that can read a repository, execute commands, edit files, and
iterate on its own output semi-autonomously — as opposed to suggest-and-accept
assistants.

**Agent loop**
: The cycle a harness runs: request → understand → plan → act → observe → revise →
repeat. Productive when the task is well specified; a token-burning spiral when it
isn't.

**Context window**
: The bounded working memory of a model. Everything — your prompt, file contents,
command output, conversation history — competes for space and attention within it.

**Context accumulation**
: The growth of conversation context over a session; each new message resends the
accumulated history, so late messages cost far more than early ones.

**Context file / project context**
: A file (`CLAUDE.md`, `.github/copilot-instructions.md`, `AGENTS.md`) loaded at session
start that gives the agent persistent knowledge about a project: structure, conventions,
commands, safety rules. Advisory, not enforced.

**Data poisoning**
: Inserting crafted examples into a model's training data to implant hidden behaviors.
Research suggests a few hundred poisoned documents can suffice, roughly independent of
model size.

**Data leakage**
: Any path by which information from outside the training data (typically from the test
set or the future) influences model training or evaluation. Produces inflated scores
from code that runs cleanly.

**Feature-based development**
: Delegating work to an agent one well-scoped, verifiable feature at a time — one
feature per session, a small diff, one pull request — rather than project-sized
requests. A feature is one thing you can check.

**Group leakage**
: Data leakage caused by splitting on rows when the unit that repeats (subject, image,
document, site) appears on both sides of the split. The model learns the unit, not the
signal. Fix: split by group (`GroupShuffleSplit`, `GroupKFold`) and assert disjointness.

**Harness**
: The application around a language model that lets it act on a real codebase: file
access, terminal and test execution, context management, planning, tool integrations,
memory, permission controls, and the agent loop. Agent = LLM + harness + tools + loop.

**Hook**
: A deterministic script configured to run at a fixed point in an agent's workflow
(after every edit, before every commit). Unlike a context file or a skill, a hook is
*guaranteed* to fire rather than advisory.

**Model backdoor (trojaned model)**
: A model engineered — via poisoned training data, fine-tuning, or surgical weight
edits — to behave normally except on a trigger input (e.g., emitting vulnerable code
when a condition is met). Lives in the parameters, so file-format defenses like
safetensors don't help and no scanner or benchmark reliably detects it.

**Instructions vs. permissions**
: An instruction (a rules file, a prompt) asks the model to behave and is text it
weighs; a permission (a VM boundary, a deny rule, branch protection) removes the
ability. Instructions shape behavior; permissions constrain it.

**MCP (Model Context Protocol)**
: An open standard for plugging tools and data into any agent. Unlike an API, where you
write the calling code, the agent discovers an MCP server's tools and decides when to
call them.

**MCP server**
: A lightweight program that exposes tools, resources, and prompts to an agent over
MCP, locally over stdio or remotely over HTTP. Its output enters the agent's context
as untrusted input.

**Minimum viable pipeline (MVP)**
: Whatever you can get running quickly and understand end to end: a slice of the
data, one model, your laptop. Fewer friction and failure points, and the ideal first
plan for an agent.

**Plan file (`plan.md` / `PLANS.md`)**
: A committed, living document holding goal, scope and acceptance criteria, ordered
steps, progress, discoveries and blockers, and test results. The agent's direction,
your review point before implementation, and a shared definition of done.

**Plan mode / read-only mode**
: An agent mode in which files can be read and questions answered but nothing is
modified. The safest first contact with any repository.

**Prompt injection**
: An attack in which content the agent reads (a README, issue, data file) contains
instructions crafted to hijack the agent's behavior.

**Safetensors**
: A weights-only serialization format for model files that, unlike pickle-based
formats, cannot execute code when loaded. Prefer it when downloading models.

**Slopsquatting**
: Registering a malicious package under a name that LLMs habitually hallucinate, so
that agents (or people following AI suggestions) install it. Cousin of typosquatting
(lookalike names) and dependency confusion (shadowing an internal package name on a
public registry).

**Supply-chain attack**
: Compromising software by attacking something it depends on — a package, a build
pipeline, a model file, or the agent tooling itself — rather than the software
directly.

**Skill**
: A reusable, on-demand instruction package for an agent (e.g., a deployment checklist
or a lab's analysis conventions) that loads only when relevant.

**Test as contract**
: Encoding a requirement — especially a data property — as an executable test the agent
must satisfy, turning specification into verification.

**Underspecification**
: Leaving decisions unstated in a request. The agent resolves each gap with the most
statistically typical ("average case") choice, which is rarely your case.

## Tool equivalents quick reference

| Task | Claude Code | GitHub Copilot |
|------|-------------|----------------|
| Cloud VM session (nothing local) | [claude.ai/code](https://claude.ai/code) | Copilot app in cloud mode; [github.com/copilot/agents](https://github.com/copilot/agents); assign an issue to Copilot |
| Read-only exploration / plan review | Plan mode (<kbd>Shift</kbd>+<kbd>Tab</kbd>; built in on the web) | Explicit plan mode in the Copilot app; on the web, ask for a plan in the prompt; Ask mode in VS Code chat |
| Network allowlist | Session **Network access** (No network / Trusted / All); account extras at claude.ai/settings/capabilities | Repo Settings → Copilot → Cloud agent → Internet access (firewall, recommended/custom allowlist) |
| Reset context between tasks | `/clear` | New chat |
| Tame a long conversation | `/compact` | Carry a summary into a fresh chat |
| See usage/cost | `/cost` (and `/context`) | [Copilot settings](https://github.com/settings/copilot) usage |
| Switch model | `/model` | Model picker in the chat panel |
| Interrupt the agent | <kbd>Esc</kbd> | Stop button |
| Project context file | `CLAUDE.md` (also reads `AGENTS.md`) | `.github/copilot-instructions.md` (also reads `AGENTS.md`) |
| Command allow/deny rules | `/permissions`, `settings.json` | Terminal auto-approve settings |
| Add an MCP server | `claude mcp add …`; `claude mcp list` | **MCP: Open User Configuration** |
| Skills | `.claude/skills/<name>/SKILL.md`; plugins via `claude plugin install` | Prompt files `.github/prompts/<name>.prompt.md` |

## Further reading

**Tools and workflow**

- [Anthropic: Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Aaron Friel: Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)
- [Terminal-Bench 2.1 leaderboard](https://www.tbench.ai/leaderboard/terminal-bench/2.1) — agent and model pairs
- [OpenRouter session-cost rankings](https://openrouter.ai/rankings#session-cost)
- [ML+X Nexus](https://uw-madison-datascience.github.io/ML-X-Nexus/) — the UW–Madison community guides this lesson draws on

**Safety and security**

- [Simon Willison: The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- [Claude Code: permissions vs. sandboxing](https://code.claude.com/docs/en/permissions) and [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)
- [Copilot cloud agent firewall](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/customize-the-agent-firewall)
- [Nx "s1ngularity" postmortem](https://nx.dev/blog/s1ngularity-postmortem) and [Wiz's aftermath analysis](https://www.wiz.io/blog/s1ngularitys-aftermath)
- [Invariant Labs: GitHub MCP vulnerability](https://invariantlabs.ai/blog/mcp-github-vulnerability)
- [Cursor allowlist bypass, CVE-2026-22708](https://github.com/cursor/cursor/security/advisories/GHSA-82wg-qcm4-fp2w)
- [1Password CLI: secrets in environment variables](https://developer.1password.com/docs/cli/secrets-environment-variables/)

**Research**

- [METR: Measuring the impact of AI on experienced open-source developer productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [Anthropic: How AI assistance impacts the formation of coding skills](https://www.anthropic.com/research/AI-assistance-coding-skills)
- [Demirer, Musolff & Yang: Writing Code vs. Shipping Code](https://www.nber.org/papers/w35275)
- [Faros AI: 2026 AI Engineering Report](https://pages.faros.ai/hubfs/AI_Engineering_Report_2026_The_Acceleration_Whiplash_Faros.pdf)
- [Simon Couch: Electricity use of AI coding agents](https://simonpcouch.com/blog/2026-01-20-cc-impact/) and [Zeke Hausfather: The real energy use of agentic AI](https://www.theclimatebrink.com/p/the-real-energy-use-of-agentic-ai)
