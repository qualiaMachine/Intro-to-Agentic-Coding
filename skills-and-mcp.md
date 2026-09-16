---
title: "MCP Tools and Skills: Extending Your Agent"
teaching: 10
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- How does MCP differ from an API, and when is each appropriate?
- What is an MCP server, and what happens when I connect one?
- What is inside a skill, and how does an agent decide to use one?
- What additional scrutiny does connecting an MCP server or installing a skill require?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain the difference between an API (you write the calling code) and MCP (the agent discovers and calls tools itself).
- Connect an MCP server and use it for one task without naming the tool.
- Install a published skill, trigger it, and explain what changed.
- Distinguish a context file, a skill, a hook, and an MCP server, and choose the right one for a recurring workflow.
- Apply the safety episode's trust rules to a new MCP connection or skill.
- Locate community skill and MCP directories to check before building your own.

::::::::::::::::::::::::::::::::::::::::::::::::

## MCP compared with an API

An **API** is a contract you write code against: one integration per service. You
read the documentation, write the request, and parse the response.

**MCP (Model Context Protocol)** is a standard for connecting tools and data to any
agent. The integration is written once, and every MCP-compatible client can use it.
With an API, you write the calling code. With MCP, the agent discovers the available
tools and decides when to call them. Anthropic open-sourced MCP in November 2024; it is
now supported by Claude, Copilot, and most other agents.

The rule of thumb: use MCP when the agent should reach a system on its own; use a
direct API when you are writing the pipeline code yourself. MCP matters for agentic
coding specifically because the agent, not the user, decides when to consult GitHub, a
database, or a lab notebook.

## What an MCP server is

An MCP server is a small program that exposes tools, resources, and prompts to an
agent over a standard protocol. It runs locally over stdio or remotely over HTTP.
Examples include the GitHub, filesystem, Slack, and Postgres servers. When a session
starts, the agent lists the server's tools (`search_issues`, `run_query`, and so on)
and calls them like any built-in tool. Connecting a server is comparable to installing
a plugin: it gives the agent a new capability without any change to the agent itself.

The safety episode's rules apply. Only add MCP servers you trust: tool output enters
the agent's context directly and the agent acts on it. An issue body or pull-request
description fetched over MCP is exactly as untrusted as a README you did not write.
Two rules follow:

- **Scope the token to the minimum the task needs.** A read-only token for
  summarizing issues; never a token with delete or administrative scope, and never
  your everyday organization-wide token on a workshop laptop.
- **Configure per project rather than globally**, where the tool allows it.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Connect an MCP server (5 minutes)

GitHub's official MCP server is a suitable first connection: most participants already
have an account, and it can be kept read-only. Use a token with read-only scopes (see
[setup](../learners/setup.md#optional-github-token-for-the-mcp-exercise)).

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

Command Palette → **MCP: Open User Configuration**, add an entry for the same
endpoint, click **Start**, and switch Copilot Chat to **Agent** mode:

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

Then give a natural-language request that requires the tool, without naming it:

> What are the five most recently opened issues on `<org>/<repo>`, and which look
> stale?

Two things to observe: the agent chose the tool without being told which one, and an
approval prompt appears when it first calls the server. That prompt is the same
control described in the safety episode.

:::::::::::::::::::::::: solution

## What this shows

The agent is now calling GitHub's API rather than answering from training data. Ask
yourself what wider access it would need to do the next thing you would want (open a
pull request, close an issue, write to a database), and whether you would grant it.
Most people hesitate. That hesitation is the minimum-access principle applied
correctly.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## What a skill is

A **skill** is a packaged, reusable set of instructions: a folder containing a
`SKILL.md` file and optionally scripts, which the agent loads on demand. Unlike MCP, a
skill needs no running server and no network call. It is markdown and possibly a
script in a folder. It is triggered automatically when a task matches its
description, or invoked directly with `/skill-name`.

If an MCP server gives the agent a new tool, a skill gives it a procedure: written
instructions for one job, loaded without re-explanation in each session. Skills suit
repeatable workflows: a review checklist, a repository-specific release process, a
data-format specification, a group's analysis conventions.

A skill cannot make the agent do anything it could not already do by reading files
and running commands. The description is the important component, because it is what
the agent matches against. A vague description ("helps with releases") triggers
unreliably; a specific one ("use when the user asks to cut a release, bump a version,
or write release notes") triggers when intended.

Skills also reduce cost. The full skill content is expanded only when relevant,
rather than occupying context for the whole session as an overlong context file
does. This is one of the token-saving measures in the next episode.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Add the caveman skill (5 minutes)

A trivial, zero-risk skill is the quickest way to observe the mechanism.
[Caveman](https://github.com/JuliusBrussee/caveman) is a public plugin that rewrites
the agent's replies in a terse, telegraphic style. The author measured about 65% fewer
output tokens with technical content intact. The effect is immediately visible, which
makes the token saving concrete.

:::::::::::::::: group-tab

### Claude Code

```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

Restart the session. Ask an ordinary question ("what is a closure in Python?"), then
type `/caveman` and ask it again. To confirm the mode is set rather than coincidental:

```bash
cat ~/.claude/.caveman-active
```

The VS Code extension reads the same `~/.claude` configuration: run the same two
commands, then reload the chat panel.

### GitHub Copilot

Caveman provides rule files for Copilot:

```bash
npx -y github:JuliusBrussee/caveman -- --only copilot --with-init
```

Copilot's closest native equivalent to a skill is a reusable **prompt file**
(`.github/prompts/<name>.prompt.md`), invoked explicitly with `/<name>`. It does not
trigger automatically from a description match as a Claude Code skill can.

::::::::::::::::::::::::

This is a plugin install rather than a hand-written skill file; the mechanism is the
same, packaged for distribution. To write your own, create
`.claude/skills/<name>/SKILL.md` with a `name`, a `description` stating when to use
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

## From the demonstration to real use

The caveman skill demonstrates the mechanism. The practical use is packaging an
instruction you would otherwise repeat. Choose one thing you find yourself re-typing
in your own project (a commit-message convention, a data-checking routine, a report
template) and turn it into a skill. Most people find that their first description is
too vague to trigger reliably, which is useful practice in writing precise
instructions generally.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Hooks, and when to codify what

Skills and MCP are two of four ways to record a recurring workflow instead of
re-prompting it. The other two:

- **The project context file** (`CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`)
  holds standing instructions the agent reads every session. It is advisory.
- **Hooks** are deterministic scripts that run at fixed points, such as after every
  edit or before every commit. Unlike context-file instructions and skills, which the
  model may or may not follow, hooks always run. Use them for rules that must never
  be skipped: run the linter, block writes to `data/raw/`.

A reasonable progression: context file first; a skill when you notice yourself
repeating instructions; a hook when a rule needs enforcement rather than a reminder;
MCP when the agent needs an external system.

## Where to find more

Before building your own, check what has already been published:

- **[Parse.bot MCP marketplace](https://parse.bot/marketplace)**: turns websites into
  typed, callable APIs exposed over MCP, with thousands of prebuilt endpoints for
  sites that have no purpose-built server.
- **[Matt Pocock's skills](https://github.com/mattpocock/skills)**: workflow
  enforcement, including test-driven development, planning, debugging, and git
  guardrails.
- **[gstack](https://github.com/garrytan/gstack)**: Garry Tan's Claude Code setup,
  with plan review, code review, QA, and shipping workflows as skills.
- **[Claude Science](https://www.anthropic.com/news/claude-science-ai-workbench)**:
  Anthropic's workbench for scientists, with analysis specialists and access to
  scientific databases as skills and connectors.
- **[ToolUniverse](https://github.com/mims-harvard/ToolUniverse)**: Harvard's open
  platform of thousands of scientific tools (databases, models, workflows), exposed
  over MCP with a Claude Code plugin.
- **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)**:
  the official reference MCP servers and the wider registry.

Treat these as the [trust](trust.md) episode treats a package: read before you
install. A skill is a set of instructions the agent will follow, and an MCP server is
code that runs with whatever access you grant it. A well-known author is a reason to
look first, not a substitute for looking.

::::::::::::::::::::::::::::::::::::: keypoints

- API: you write the calling code. MCP: the agent discovers the tools and decides when to call them. Use MCP when the agent should reach a system on its own, and a direct API when you are writing the pipeline.
- An MCP server exposes tools, resources, and prompts over a standard protocol. Connecting one is comparable to installing a plugin.
- A skill is a procedure: packaged instructions loaded on demand, with no server and no network. It saves context because it expands only when relevant.
- Context file, then skills, then hooks (which always run), then MCP: codify a workflow at the lowest level that enforces what you need.
- Everything an MCP tool returns is untrusted input. Scope tokens to the minimum and configure per project.
- Vet a skill or MCP server before installing it, regardless of the author. Parse, Matt Pocock's skills, gstack, Claude Science, and ToolUniverse are reasonable starting points.

::::::::::::::::::::::::::::::::::::::::::::::::
