---
title: "What Is Agentic Coding?"
teaching: 15
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- What distinguishes an agentic coding tool from autocomplete or a chat assistant?
- What is inside an agent — and what does the "harness" do that the model doesn't?
- Which tool should I pick, and does the choice matter much?
- Is more autonomy automatically better?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Define agentic coding and contrast it with chat-based and autocomplete-based AI assistance.
- Describe an agent as a model plus a harness plus tools running an agent loop.
- Place a request on the spectrum of autonomy, from "write this loop" to "build the whole thing".
- Explain why this lesson focuses on principles rather than any single tool.

::::::::::::::::::::::::::::::::::::::::::::::::

## A definition

**Agentic coding** is a software-development approach in which AI agents plan, write,
test, debug, and revise code with limited human intervention.

::::::::::::::::::::::::::::::::::::: callout

## "Agentic" is an overloaded term

"Agent" now gets attached to almost anything with a chat box, so let's pin the word
down. Computer science has long used it precisely: an agent is a system that **takes
actions** in an environment and observes the results, in pursuit of a goal. An
assistant or chatbot produces text and *you* act on it; an agentic tool acts for
itself — editing files, running commands, reading the output, deciding what to do
next. The litmus test for any tool wearing the label: *does it act, or does it only
advise?* In agentic coding, action is everywhere — which is both the point and, as
this lesson explores, the risk.

::::::::::::::::::::::::::::::::::::::::::::::::

An AI coding agent is more than a chatbot. It is a persistent, tool-enabled process
powered by a large language model. Traditional AI code assistants (early GitHub
Copilot, ChatGPT in a browser tab) work in a simple loop: you ask, they suggest, you
accept or reject. You are the middleware — you paste context in, you copy code out,
you run everything yourself. An agent can instead:

- Read and navigate a codebase — not just the snippet you pasted.
- Create and modify files, several at a time.
- Run terminal commands.
- Execute tests and inspect the failures — it sees the actual output, not your summary.
- Search documentation.
- Develop and follow a plan.
- Iterate on its own work until the task is complete or it hits a blocker.

So you can ask it to fix a bug, add a feature, refactor existing code, write and run
tests, review a pull request, investigate a failing job, or build a small application
from a specification. This is powerful. It also means the tool has real access to your
system — your files, your shell, your credentials if you leave them lying around — and
the potential to do real damage if not managed carefully. That tension between
capability and control is the subject of this whole lesson.

## The spectrum of agentic coding

The same tool can be used at very different levels of autonomy. Three requests, from
tightly directed to fully delegated:

1. *"Write this for loop for me."* — one function, you watch every line.
2. *"Implement the method stubs in this file."* — a bounded task with a clear "done";
   the agent plans a little, you review the diff.
3. *"Build the whole service from scratch; do all the planning yourself."* — the agent
   invents dozens of decisions you never made, and you review a project.

Notice the pattern: **the more autonomy you grant, the more of your judgment has to
be encoded in advance** — in the prompt, in project context files, and in tests — and
the more you have to review afterwards. That is the thread we pull on for the rest of
this lesson. Nearly everything the workshop teaches lives in the middle of this
spectrum: bounded tasks with a plan and a check.

::::::::::::::::::::::::::::::::::::: callout

## More autonomy is not automatically better

The same task — "add a utility function, write tests, open a PR" — can be done at any
point on this spectrum. Moving right means less friction *during* the work and more
review burden *after* it. The right choice depends on the task:

- Sensitive work or unfamiliar codebase → interactive, guardrails on. The
  interruptions are a feature.
- Quick question, brainstorming, explaining an error → plain chat is hard to beat.
- Well-scoped, clearly described task in a repo with good tests → hand it off, because
  the specification and the tests carry your intent for you.

::::::::::::::::::::::::::::::::::::::::::::::::

## Inside an agent: model, harness, tools, loop

There are now many tools designed for agentic coding — Claude Code, Codex, GitHub
Copilot's agent mode, OpenCode, Cursor, and a growing list of open-source harnesses.
Most can drive several different underlying language models. It helps to separate the
two parts:

- **The model** provides the reasoning and code generation.
- **The harness** — the application around the model — provides everything that lets
  that reasoning operate on a real codebase: file-system access, terminal and test
  execution, context management, planning and task tracking, tool integrations,
  memory, permission controls, and the loop that ties them together.

The harness runs an **agent loop**: request → understand → plan → act → observe →
revise → repeat. Each turn, the model decides what to do next, the harness executes
it (edit a file, run the tests), and the result goes back into the model's context.
An agent, in one line: **LLM + harness + tools + agent loop.**

More advanced harnesses add an orchestrator–worker pattern: a primary agent breaks a
larger problem into smaller tasks and delegates them to subagents that work in parallel
on research, implementation, testing, and review. Multi-agent workflows became
prominent toward the end of 2025. They are the far-right end of the spectrum above —
powerful, and the hardest to review.

## Which tool? Less important than you'd think

As of September 2026, the leading agents are close on capability. On
[Terminal-Bench 2.1](https://www.tbench.ai/leaderboard/terminal-bench/2.1), a
benchmark of realistic command-line tasks, Claude Code and Codex land within about a
point of each other, and GitHub Copilot runs the same Claude and GPT models underneath.
The harness matters — the same model scores differently in different agents — but the
gap between the top commercial tools is small.

Open-weight models are a real option and improving every month. The top Terminal-Bench
score at time of writing is an open-weight model (DeepSeek V4.1 Flash), but at hundreds
of billions of parameters it needs a cluster to run. Open-weight models that fit on a
single GPU trail the frontier by tens of points — closing that gap is an active
research problem, and running your own model brings its own trust questions (the
[trust](trust.md) episode covers those).

So don't memorize a tool table; it will be out of date within months. The
[setup page](../learners/setup.md) lists routes to get an agent running — including
free ones (Copilot's education tier, OpenCode with free models) if you don't have a
paid plan or workshop credits.

::::::::::::::::::::::::::::::::::::: callout

## Using GitLab instead of GitHub?

Everything interactive in this lesson is host-agnostic — an agent on a checkout does
ordinary git, so GitHub, GitLab (self-hosted included), and Bitbucket work identically.
Only the cloud-agent surfaces are GitHub-centric today (assigning issues to agents,
cloud sandboxes). One caution: self-hosted GitLab doesn't change where inference
happens — code still goes to the model provider, so the data-policy rules still apply.

::::::::::::::::::::::::::::::::::::::::::::::::

## Demo: the same project, three levels of autonomy

::::::::::::::::::::::::::::::::::::: instructor

Run this live with Claude Code in VS Code (or OpenCode) on the project the rest of the
workshop returns to. Show three examples along the spectrum:

1. A tightly directed coding task — one function, watch it type.
2. A task in which the agent creates and follows a plan — use plan mode first, then
   let it implement.
3. A more autonomous, multi-agent workflow — *explain* this one but don't run it live;
   it takes longer and introduces variability.

Ask the room: "Anyone want to share something impressive their agent did?" — it warms
people up and surfaces the range of experience in the room.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Place your own work on the spectrum (5 minutes)

Think about the last time you used AI for anything code-related (pasting an error into
a chatbot counts).

1. Where does that use sit on the spectrum — a directed edit, a bounded task with a
   plan, or "build it all"?
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

## Why principles, not one tool

Every practice in this lesson — limiting access, planning, specifying, verifying,
managing cost — applies unchanged to whichever tool you or your lab ends up using, so
the main text stays tool-agnostic. Where the mechanics differ (a command name, a mode
toggle, a settings page), episodes give the equivalents for the two tools workshop
participants most commonly have: **Claude Code** and **GitHub Copilot**. Translate
freely if you brought something else — the concepts map one-to-one. The tools will
churn; the discipline won't.

::::::::::::::::::::::::::::::::::::: keypoints

- Agentic coding: AI agents plan, write, test, debug, and revise code with limited human intervention. An agent acts; a chatbot advises.
- Agent = LLM + harness + tools + agent loop. The model reasons; the harness gives it files, a terminal, tests, permissions, and memory.
- Requests sit on a spectrum from "write this loop" to "build it all". More autonomy shifts your effort from approving actions to specifying intent up front and reviewing results afterward.
- The leading tools are within a point or two of each other; pick what you can access and learn the principles.

::::::::::::::::::::::::::::::::::::::::::::::::
