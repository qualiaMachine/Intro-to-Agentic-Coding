---
title: "MCP Tools and Skills: Extending Your Agent"
teaching: 10
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- How is MCP different from an API — and when do I want each?
- What is an MCP server, and what happens when I connect one?
- What is inside a skill, and how does an agent decide to use one?
- What extra scrutiny does connecting an MCP server or installing a skill deserve?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain the difference between an API (you write the calling code) and MCP (the agent discovers and calls tools itself).
- Connect an MCP server and use it for one real task without naming the tool.
- Install a published skill, trigger it, and explain what changed.
- Apply the safety episode's trust lens to a new MCP connection or skill.
- Locate community skill and MCP directories worth checking before you build your own.

::::::::::::::::::::::::::::::::::::::::::::::::

## MCP vs API

An **API** is a contract you write custom code against — one integration per service.
You read the docs, write the request, parse the response.

**MCP (Model Context Protocol)** is a standard way to plug tools and data into any
agent. Write the integration once and every MCP-compatible client can use it. With an
API, *you* write the calling code. With MCP, **the agent discovers the available tools
itself and decides when to call them.** Anthropic open-sourced MCP in November 2024;
it is now supported by Claude, Copilot, and most other agents.

Rule of thumb: **MCP when the agent should reach a system on its own. Direct API when
you're writing the pipeline code yourself.**

This is why MCP matters for agentic coding specifically: the agent decides when to
reach for GitHub, a database, or a lab notebook — not you.

## What is an MCP server?

A lightweight server that exposes **tools**, **resources**, and **prompts** to an agent
over a standard protocol. It runs locally over stdio or remotely over HTTP. Examples:
GitHub MCP, filesystem MCP, Slack MCP, Postgres MCP. When the session starts, the
agent lists the server's available tools — `search_issues`, `run_query` — and then
calls them like any built-in tool.

Connecting an MCP server is comparable to installing a plugin: you are not writing
new agent code, you are giving the agent a new capability.

And the safety flag, tying back to that episode: **only add MCP servers you trust.**
Tool output goes straight into the agent's context and it will act on it — an issue
body or PR description fetched over MCP is exactly as untrusted as a README you didn't
write. Two rules follow:

- **Scope the token to the minimum the task needs.** A read-only token for a
  "summarize these issues" task; never delete or admin scope, and never your everyday
  org-wide token wired into a workshop laptop.
- **Configure per-project, not globally**, where your tool supports it.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Connect an MCP server (5 minutes)

GitHub's official MCP server is a good first connection — most people already have
the account, and it can stay strictly read-only. Use a token with read-only scopes
(see [setup](../learners/setup.md#optional-github-token-for-the-mcp-exercise)).

:::::::::::::::: group-tab

### Claude Code

```bash
claude mcp list                       # before: nothing (or only existing servers)
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer $GH_TOKEN"
claude mcp list                       # after: github listed
```

Restart the session so the tools load.

### GitHub Copilot (VS Code)

Command Palette → **MCP: Open User Configuration**, add an entry pointing at the
same endpoint, then click **Start** and switch Copilot Chat to **Agent** mode:

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${input:gh_token}" }
    }
  }
}
```

::::::::::::::::::::::::

Then give a natural-language prompt that *needs* the tool, without naming it:

> What are the five most recently opened issues on `<org>/<repo>`, and which look
> stale?

Watch for two things: the agent chose the tool — you did not name it — and the
approval prompt when it first calls the server. That prompt is the same guardrail
from the safety episode.

:::::::::::::::::::::::: solution

## What this shows

The agent is now calling real GitHub API tools, not guessing from training data.
Ask yourself the question this exercise is designed to surface: what *wider* access
would it need to do the next thing you'd want (file a PR, close an issue, write to a
database) — and would you grant it? Most people hesitate. That hesitation is the
minimum-access instinct working.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## What is a skill?

A **skill** is a packaged, reusable set of instructions — a folder with a `SKILL.md`
file, plus optional scripts — that the agent loads on demand. Unlike MCP, a skill
needs no running server and no network call: it's markdown and maybe a script,
sitting in a folder. It's triggered automatically when the task matches its
description, or invoked directly with `/skill-name`.

If MCP is a plugin that gives the agent a new tool, a skill is a **playbook** —
written instructions for one job, that the agent loads without you re-explaining it
every session. Good for repeatable workflows: a review checklist, a repo-specific
release process, a data-format spec, your lab's analysis conventions.

A skill can't make the agent do anything it couldn't already do by reading files and
running commands. The description is the important part: it's what the agent
matches against, so vague wording ("helps with releases") triggers unreliably, while
specific wording ("use when the user asks to cut a release, bump a version, or write
release notes") triggers when you intend it to.

Skills also help with **cost**: the full skill content is only expanded when it's
relevant, instead of sitting in context the whole session the way an overgrown
context file does. That's one of the token-saving levers in the next episode.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Add the caveman skill (5 minutes)

A deliberately silly, zero-risk skill is the fastest way to *see* the mechanism work.
[Caveman](https://github.com/JuliusBrussee/caveman) is a real, public plugin that
rewrites the agent's replies into terse "caveman speak" — the author measured about
65% fewer output tokens with technical accuracy intact. The effect is immediately
visible, which makes the token saving concrete.

:::::::::::::::: group-tab

### Claude Code

```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

Restart the session. Ask an ordinary question — "what is a closure in Python?" —
then type `/caveman` and ask it again. To prove it's toggled rather than a fluke:

```bash
cat ~/.claude/.caveman-active
```

The VS Code extension reads the same `~/.claude` config: run the same two commands,
then reload the chat panel.

### GitHub Copilot

Caveman ships rule files for Copilot too:

```bash
npx -y github:JuliusBrussee/caveman -- --only copilot --with-init
```

Copilot's closest native equivalent to a skill is a reusable **prompt file**
(`.github/prompts/<name>.prompt.md`), invoked explicitly with `/<name>` — it never
auto-triggers from a description match the way a Claude Code skill can.

::::::::::::::::::::::::

Note this is a *plugin install*, not a skill file you hand-wrote — the same
underlying mechanism, packaged for distribution. To write your own, create
`.claude/skills/<name>/SKILL.md` with a `name`, a `description` that says when to use
it, and the instructions:

```markdown
---
name: caveman
description: Use when the user asks to talk like a caveman, or wants "caveman mode" responses.
---

Respond in short grunts. Drop articles. Present tense only. Keep code, commands, and
exact errors intact. Stay accurate; only the phrasing changes.
```

:::::::::::::::::::::::: solution

## Beyond the joke

The caveman skill demonstrates the mechanism; the practical use is packaging
something you would otherwise repeat. Pick one instruction you find yourself re-typing in your own
project — a commit-message convention, a data-checking routine, a report template —
and turn it into a skill next. Skill-builders usually discover their first
description is too vague to trigger reliably, which is useful practice in writing
precise instructions generally.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Where to find more of both

Before building your own, check what the community has already published:

- **[Parse.bot MCP marketplace](https://parse.bot/marketplace)** — turns arbitrary
  websites into typed, callable APIs and exposes them over MCP; thousands of
  prebuilt endpoints for sites with no purpose-built server of their own.
- **[Matt Pocock's skills](https://github.com/mattpocock/skills)** — workflow
  enforcement: TDD, planning, debugging, git guardrails.
- **[gstack](https://github.com/garrytan/gstack)** — Garry Tan's Claude Code setup:
  plan review, code review, QA, and shipping workflows as skills.
- **[Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)** —
  Anthropic's workbench for scientists, with analysis specialists and access to
  scientific databases as skills and connectors.
- **[ToolUniverse](https://github.com/mims-harvard/ToolUniverse)** — Harvard's open
  platform of thousands of scientific tools (databases, models, workflows), exposed
  over MCP with a Claude Code plugin.
- **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)** —
  the official reference MCP servers and the broader registry.

Treat these the way the [trust](trust.md) episode treats a package: **read before you
install.** A skill is instructions an agent will follow, and an MCP server is code
that runs with whatever access you grant it — popularity and a well-known author are a
reason to look first, not a substitute for looking.

::::::::::::::::::::::::::::::::::::: keypoints

- API: you write the calling code. MCP: the agent discovers the tools and decides when to call them. MCP when the agent should reach a system on its own; direct API when you're writing the pipeline.
- An MCP server exposes tools, resources, and prompts over a standard protocol; connecting one is like installing a plugin.
- A skill is a playbook — packaged instructions loaded on demand, no server, no network — and it saves context because it expands only when relevant.
- Everything an MCP tool returns is untrusted input; scope tokens to the minimum and configure per project.
- Vet a skill or MCP server before installing it, even from a well-known author; Parse, Matt Pocock's skills, gstack, Claude Science, and ToolUniverse are good places to start looking.

::::::::::::::::::::::::::::::::::::::::::::::::
