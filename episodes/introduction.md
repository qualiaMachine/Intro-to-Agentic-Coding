---
title: "What Does 'Agentic' Mean?"
teaching: 10
exercises: 4
---

:::::::::::::::::::::::::::::::::::::: questions

- What distinguishes an agentic coding tool from autocomplete or a chat assistant?
- What does the current tooling landscape look like, and how should I choose?
- Is more autonomy automatically better?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Define agentic coding and contrast it with chat-based and autocomplete-based AI assistance.
- Map the major tools onto a spectrum of autonomy, from chat to IDE agents to fully asynchronous agents.
- Explain why this lesson focuses on principles rather than any single tool.

::::::::::::::::::::::::::::::::::::::::::::::::

## From autocomplete to agents

Traditional AI code assistants (early GitHub Copilot, ChatGPT in a browser tab) work in a
simple loop: you ask, they suggest, you accept or reject. You are the middleware — you
paste context in, you copy code out, you run everything yourself.

Agentic coding tools go further. They can:

- **Read and navigate your entire codebase** — not just the snippet you pasted.
- **Execute shell commands and run tests** — they see the actual output, not your summary of it.
- **Edit multiple files in a single pass.**
- **Iterate on their own output** — hit an error, read it, fix the code, re-run.
- **Operate semi-autonomously over multi-step tasks** — "add this feature, write tests,
  open a PR" as one request.

This is powerful. It also means these tools have real access to your system — your files,
your shell, your credentials if you leave them lying around — and the potential to do
real damage if not managed carefully. That tension between capability and control is the
subject of this whole lesson.

## The landscape at a glance

The space is crowded and moving fast. As of early 2026, the tools you are most likely to
encounter:

| Tool             | Interface                       | Notable traits                                                        |
|------------------|---------------------------------|-----------------------------------------------------------------------|
| Claude Code      | CLI, desktop app, IDE extensions, web | Anthropic's own agent harness; explicit permission model; `CLAUDE.md` project config |
| GitHub Copilot   | VS Code/IDEs, GitHub.com        | Multi-model (Claude, GPT, Gemini); free paid tier for students/teachers; async cloud coding agent |
| Cursor           | Custom IDE                      | Polished IDE experience, fast inline edits                            |
| Windsurf         | Custom IDE                      | Low-friction agentic workflow, free tier                              |
| OpenCode         | CLI                             | Open source; works with several free models — a good bring-your-own-agent option |
| Amazon Q / Gemini Code Assist / GitLab Duo | IDE + cloud consoles | Deep integration with their respective platforms |

Don't memorize this table — it will be out of date within months. What is stable is the
**spectrum of autonomy** these tools occupy:

1. **Chat** (claude.ai, ChatGPT): no system access. You do all the manual work, but
   there is zero risk of the tool running a bad command. Often the *lowest-friction*
   option for brainstorming precisely because nothing needs approval.
2. **Interactive agent** (Claude Code, Copilot agent mode, Cursor): the agent works in
   your repository with your permissions, and you approve or review as it goes.
3. **Asynchronous agent** (Copilot cloud coding agent, Claude Code on the web, assigning
   an issue to `@claude`): you hand off a task, the agent works in a cloud sandbox, and
   you review a finished pull request.

::::::::::::::::::::::::::::::::::::: callout

## More autonomy is not automatically better

The same task — "add a utility function, write tests, open a PR" — can be done at any
point on this spectrum. Moving right means less friction *during* the work and more
review burden *after* it. The right choice depends on the task:

- Sensitive work or unfamiliar codebase → interactive agent, guardrails on. The
  interruptions are a feature.
- Quick question, brainstorming, explaining an error → chat is hard to beat.
- Well-scoped, clearly described task in a repo with good tests and CI → async agent
  works well, because the specification and the tests carry your intent for you.

Notice the pattern: **the more autonomy you grant, the more of your judgment has to be
encoded in advance** — in the prompt, in project context files, and in tests. That's the
thread we pull on for the rest of this lesson.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Map your own workflow (4 minutes)

Think about the last time you used AI for anything code-related (pasting an error into
a chatbot counts).

1. Where does that use sit on the autonomy spectrum — chat, interactive agent, or
   async agent?
2. Name one task in your current research where you'd *want* more autonomy from an AI
   tool, and one where you absolutely wouldn't. What's different about them?

Compare with a neighbor.

:::::::::::::::::::::::: solution

## Typical patterns

Most researchers cluster at the chat end — and the tasks people refuse to delegate are
almost always the ones where they'd struggle to *check* the result (their core
analysis) rather than the ones that are hardest to do. That instinct is sound, and
it's the central theme of this lesson: how much autonomy you can grant is set by how
well you can verify.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## Using GitLab instead of GitHub?

Everything interactive in this lesson is host-agnostic — an agent on a local checkout
does ordinary git, so GitHub, GitLab (self-hosted included), and Bitbucket work
identically. Only the **async tier** is GitHub-centric today (assigning issues to
agents, cloud sandboxes); GitLab offers CI/CD integrations instead, less turnkey. One
caution: self-hosted GitLab doesn't change where inference happens — code still goes
to the model provider, so the data-policy rules still apply.

::::::::::::::::::::::::::::::::::::::::::::::::

## Why principles, not one tool

Every practice in this lesson — scoping, secrets hygiene, specification, verification,
documentation, cost awareness — applies unchanged to whichever tool you or your lab
ends up using, so the main text stays tool-agnostic. Where the mechanics differ (a
command name, a mode toggle, a settings page), episodes give the equivalents for the
two tools workshop participants most commonly have: **Claude Code** and **GitHub
Copilot**. Use whichever you set up (the [setup page](../learners/setup.md) lists
options, including free routes), and translate freely if you brought something else —
the concepts map one-to-one. The tools will churn; the discipline won't.

::::::::::::::::::::::::::::::::::::: keypoints

- Agentic tools read your repo, run commands, edit files, and iterate on their own output — they are collaborators with real system access, not autocomplete.
- Tools occupy a spectrum of autonomy: chat → interactive agent → asynchronous agent.
- More autonomy shifts your effort from approving actions to specifying intent up front and reviewing results afterward.
- Learn the principles; the specific tools will keep changing.

::::::::::::::::::::::::::::::::::::::::::::::::
