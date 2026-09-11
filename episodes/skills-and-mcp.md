---
title: "Skills and MCP: Extending Your Agent"
teaching: 15
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- What's actually inside a skill, and how does an agent decide to use one?
- How is an MCP server different from a skill — what can it do that instructions alone can't?
- Where do I find good skills and MCP servers other people have already built?
- What extra scrutiny does connecting an MCP server deserve?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Build and trigger a minimal custom skill.
- Explain the difference between a skill (packaged instructions) and an MCP server (new tool calls to an external system).
- Connect a read-only MCP server and use it for one real task.
- Apply the trust episode's minimum-access lens to a new MCP connection.
- Locate community skill and MCP directories worth checking before you build your own.

::::::::::::::::::::::::::::::::::::::::::::::::

The [common workflows](common-workflows.md) episode named skills, hooks, and MCP as
the last two rungs of a progression: write instructions once as a skill when you catch
yourself repeating them, reach for MCP when the agent genuinely needs to touch an
external system. This episode makes both concrete — you'll build one of each.

## Skills: instructions, packaged and triggered on demand

A skill is a folder the agent can load mid-session: a short **description** that says
when to use it, and a body of instructions (and optionally scripts or reference files)
that only enter context when that description matches what you're doing. That's the
whole mechanism — a skill can't make the agent do anything it couldn't already do by
reading and writing files and running commands. It just saves you from re-typing the
same instructions every session, and it stays out of the way (and out of your context
window) the rest of the time.

The description is the important part: it's what the agent matches against, so vague
wording ("helps with releases") triggers unreliably, while specific wording ("use when
the user asks to cut a release, bump a version, or write release notes") triggers when
you actually mean it.

::::::::::::::::::::::::::::::::::::: callout

## Demo: the caveman skill

A deliberately silly, zero-risk skill is the fastest way to *see* the mechanism work —
nothing it touches matters, so the whole room can watch the trigger fire.

:::::::::::::::: group-tab

### Claude Code

Create `.claude/skills/caveman/SKILL.md` in a project:

```markdown
---
name: caveman
description: Use when the user asks to talk like a caveman, or wants "caveman mode" responses.
---

Respond in short grunts. Drop articles ("the", "a"). Present tense only. Never use a
word longer than two syllables if a shorter one works. Stay helpful and accurate —
just say it like a caveman would.
```

Start a fresh session and say "talk like a caveman for the rest of this chat" (or
invoke it directly with `/caveman`). Then ask it something ordinary — "explain what a
for loop does" — and watch the style carry through.

### GitHub Copilot

Copilot's closest equivalent is a reusable **prompt file**:
`.github/prompts/caveman.prompt.md` with the same instructions in the body. Invoke it
explicitly in chat with `/caveman`.

The real difference from Claude Code skills is worth naming: a Copilot prompt file
never auto-triggers from a description match — you always invoke it by name. Claude
Code skills can fire on their own when your request matches the description.

::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

The caveman skill proves the mechanism, but the payoff is packaging something you'd
otherwise repeat: a lab's analysis conventions, a release checklist, this lesson's own
"new episode" template. Pick one instruction you find yourself re-typing in your own
project and turn it into a skill next.

## MCP: new tools, not just new instructions

A skill only ever gives the agent *words* — instructions it applies with capabilities
it already had. MCP (Model Context Protocol) is different: it's a live connection to
an external system that hands the agent tool calls it did not have a moment ago —
`list_issues`, `create_pull_request`, `query_database`. Claude Code and Copilot are MCP
*clients*; an MCP *server* (run locally or hosted remotely) exposes the tools.

::::::::::::::::::::::::::::::::::::: callout

## Demo: connect the GitHub MCP server (read-only)

GitHub's official MCP server is a good first connection — most people in a research
computing workshop already have the account, and you can keep it strictly read-only
for the demo.

:::::::::::::::: group-tab

### Claude Code

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer $GH_TOKEN"
```

Then, in a session: "what are the 5 most recently opened issues on `<org>/<repo>`?" or
"summarize the open PRs on this repo and flag anything that's been idle for two
weeks." The agent is now calling real GitHub API tools, not guessing from training
data.

### GitHub Copilot (VS Code)

Command Palette → **MCP: Open User Configuration**, add an entry pointing at the same
endpoint:

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

Click **Start**, then switch Copilot Chat to **Agent** mode and ask the same kind of
question.

::::::::::::::::::::::::

Use a token with **read-only** scopes for this demo — see
[setup](../learners/setup.md#optional-github-token-for-the-mcp-demo).

::::::::::::::::::::::::::::::::::::::::::::::::

### The trust lens, applied to MCP specifically

Everything an MCP tool call returns flows into context exactly like a README or a PR
you didn't write — the [trust](trust.md) episode's warning about prompt injection
applies to an issue body or a PR description fetched over MCP just as much as to a
file you opened yourself. Two rules follow directly:

- **Scope the token to the minimum the task needs.** A read-only PAT for a "summarize
  these issues" demo; never a token with delete or admin scope, and never your
  everyday token with org-wide access wired into a workshop laptop.
- **Configure per-project, not globally**, where your tool supports it — a connection
  made for one repository shouldn't be able to reach every repository you own.

## Where to find more of both

Before building your own, it's often faster to check what the community has already
published:

- **[mattpocock/skills](https://github.com/mattpocock/skills)** — Matt Pocock's public
  Claude Code skills covering workflow enforcement: TDD, planning, debugging, git
  guardrails.
- **GStack** — Garry Tan's public Claude Code skills setup, covering plan review, code
  review, and shipping workflows.
- **[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)** —
  the official reference MCP servers, plus pointers into the broader MCP Registry.
- **[Parse](https://parse.bot/)** — an MCP server that turns arbitrary websites into
  typed, callable APIs (scraping and multi-step actions like form submission), useful
  when the data or system you need has no purpose-built MCP server of its own.

Treat these the same way the [trust](trust.md) episode treats a package: read before
you install. A skill is instructions an agent will follow, and an MCP server is code
that runs with whatever access you grant it — popularity and a well-known author are a
reason to look first, not a substitute for looking.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Build or connect (10 minutes)

Pick one:

**(a) Build a skill** for something you actually repeat in your own work — a commit
message convention, a data-checking routine, a lab report template. Write the
`SKILL.md` (or prompt file), trigger it, and check the output matches what you
intended.

**(b) Connect a read-only MCP server** (GitHub, or pick one from
[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)) and
use it for one real task against a repository or system you actually use.

Either way, write one sentence: what *wider* access would this need to do the next
thing you'd want it to do — and would you grant it?

:::::::::::::::::::::::: solution

## What people typically find

Skill-builders usually discover their first draft of the description is too vague to
trigger reliably — a good forcing function for writing precise instructions in
general. MCP-connectors usually stop at "read issues" or "read files" and, when asked
about the next step (file a PR, write to a database), hesitate — which is exactly the
minimum-access instinct this exercise is meant to surface.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- A skill is packaged instructions loaded on demand by a description match; it can't do anything the agent couldn't already do.
- An MCP server is a live connection that hands the agent genuinely new tool calls to an external system.
- Everything an MCP tool returns is untrusted input, same as a README or PR — apply the trust episode's lens.
- Scope MCP tokens to the minimum needed, and vet a skill or MCP server before installing it, even from a well-known author.
- mattpocock/skills, GStack, and modelcontextprotocol/servers are good starting points for both.

::::::::::::::::::::::::::::::::::::::::::::::::
