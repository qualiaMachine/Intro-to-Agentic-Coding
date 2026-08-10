---
title: "Reconnaissance: Read Before You Write"
teaching: 8
exercises: 16
---

:::::::::::::::::::::::::::::::::::::: questions

- What can an agent infer about a codebase on its own — and what can't it?
- What is plan mode / read-only exploration, and when should I use it?
- Why do project context files (like `CLAUDE.md`) exist?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use an agent in a read-only/plan mode to survey an unfamiliar repository.
- Identify the kinds of knowledge an agent cannot recover from code alone.
- Write a minimal project context file that supplies that missing knowledge.

::::::::::::::::::::::::::::::::::::::::::::::::

## Explore first, then plan, then code

The most common agentic failure mode is letting the agent write code before either of
you understands the project. Most tools have a read-only or "plan" mode (in Claude Code,
toggle with <kbd>Shift</kbd>+<kbd>Tab</kbd>) in which the agent reads files and answers
questions **without making any changes**.

This is the safest possible first contact with an agent: it can't edit anything, so you
can hand it a whole repository and simply ask what it sees. It's also genuinely useful —
onboarding onto a colleague's project, returning to your own code from two years ago,
or auditing a repo before you build on it.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise 1: Recon (8 minutes)

Point your agent at the practice repository (see [setup](../learners/setup.md)) — or any
real project you have handy — in plan/read-only mode, and prompt:

> Read this repo and tell me what it's doing, or attempting to do.

While it works, note:

1. What did it get right that would have taken you longer to figure out by hand?
2. What did it state confidently that you can't actually verify from the code alone?
3. What did it *not* mention that you know matters (why the project exists, who uses it,
   what "done" looks like, which parts are load-bearing vs. abandoned)?

:::::::::::::::::::::::: solution

## Debrief

Typical pattern: the agent is excellent at *what* and *how* — structure, dependencies,
data flow, what each module does. It is blind to *why* and *for whom*:

- Why this approach was chosen over the obvious alternative (the failed experiments
  aren't in the repo).
- Which code is trusted and which is a half-finished experiment — both look the same.
- Project conventions that live in your head or your lab's wiki: how to run tests,
  what never to touch, what the data actually means.
- Anything about the *data* itself beyond what filenames and column names reveal.

The agent's summary is a hypothesis about your project, phrased with the confidence of
a fact. Treat it as the former.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Context files: writing down the "why"

The gaps you just found are exactly what **project context files** exist to fill.
Claude Code reads `CLAUDE.md` from your project root at the start of every session;
Copilot reads `.github/copilot-instructions.md`; a cross-tool convention, `AGENTS.md`,
is emerging. Think of it as a README for the agent:

```markdown
## Project structure
- Analysis pipelines live in `src/pipelines/`; each mirrors a notebook in `notebooks/`
- Raw data in `data/raw/` is read-only — NEVER modify it; derived data goes to `data/processed/`

## Conventions
- Run tests with `pytest tests/` after changes; don't commit with failing tests
- Use type hints; don't add dependencies without asking

## Safety
- Never force-push; never commit directly to main
- The `results/` directory is generated — edit the code, not the outputs
```

Keep it short and operational (aim well under 300 lines): it is injected into every
session, so everything in it competes for the model's attention with the actual task.
If a linter can enforce a rule deterministically, use the linter and save the context
budget. And remember from the last episode: context files are advisory — back
safety-critical rules with hooks or deny rules.

## The same task at three autonomy levels

Recall the autonomy spectrum from episode 1. This recon task makes it concrete:

- **Chat**: you would paste selected files into a browser tab and ask. Fast, safe, but
  the summary only covers what you chose to paste — *you* did the recon.
- **Interactive agent**: what you just did. The agent explores everything, and you can
  interrogate it.
- **Async agent**: you could file an issue ("document this repo") and get a PR back.
  Least effort — and the least opportunity to notice what the summary got wrong,
  because you weren't watching it form.

More autonomy isn't automatically better. For understanding-type tasks, the interactive
middle of the spectrum is usually the sweet spot: full access for the agent, full
visibility for you.

::::::::::::::::::::::::::::::::::::: keypoints

- Start unfamiliar work in read-only/plan mode: let the agent explore before either of you writes code.
- Agents recover *what* and *how* from code, but not *why*, *for whom*, or anything that lives outside the repo.
- Project context files (`CLAUDE.md`, `copilot-instructions.md`, `AGENTS.md`) exist to write down that missing knowledge — keep them short, operational, and advisory-aware.
- An agent's confident summary of your project is a hypothesis to verify, not a fact.

::::::::::::::::::::::::::::::::::::::::::::::::
