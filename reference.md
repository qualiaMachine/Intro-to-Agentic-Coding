---
title: 'Reference'
---

## Glossary

**Agentic coding**
: Working with an AI tool that can read a repository, execute commands, edit files, and
iterate on its own output semi-autonomously — as opposed to suggest-and-accept
assistants.

**Agentic loop**
: A cycle in which an agent tries an approach, observes failure, gathers more context,
and tries again. Productive in small doses; a token-burning spiral when the task is
underspecified.

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

**Feature-driven development**
: Delegating work to an agent one well-scoped, verifiable feature at a time, rather than
project-sized requests — keeping diffs small enough to genuinely review.

**Model backdoor (trojaned model)**
: A model engineered — via poisoned training data, fine-tuning, or surgical weight
edits — to behave normally except on a trigger input (e.g., emitting vulnerable code
when a condition is met). Lives in the parameters, so file-format defenses like
safetensors don't help and no scanner or benchmark reliably detects it.

**MCP (Model Context Protocol)**
: An open protocol for connecting agents to external tools and data sources (databases,
trackers, browsers).

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

## Command quick reference (Claude Code)

| Command | Purpose |
|---------|---------|
| `/clear` | Reset context between unrelated tasks |
| `/compact` | Summarize the conversation to reclaim context |
| `/cost` | Show token usage for the session |
| `/context` | Show what is consuming the context window |
| <kbd>Shift</kbd>+<kbd>Tab</kbd> | Toggle plan (read-only) mode |
| <kbd>Esc</kbd> | Interrupt the agent mid-action |

## Further reading

- [Anthropic: Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Simon Willison: Agentic engineering patterns](https://simonwillison.net/)
- [METR: Measuring the impact of AI on experienced open-source developer productivity](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)
- [ML+X Nexus: Claude Code Best Practices](https://uw-madison-datascience.github.io/ML-X-Nexus/) — the community guide this lesson draws on
