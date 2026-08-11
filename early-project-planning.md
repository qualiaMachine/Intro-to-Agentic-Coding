---
title: "Early Project Planning"
teaching: 10
exercises: 16
---

:::::::::::::::::::::::::::::::::::::: questions

- How do I put an agent to work before any code gets written?
- What can an agent infer about an existing project on its own — and what can't it?
- How do I plan a *new* project with AI without being led somewhere I can't follow?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use an agent in a read-only/plan mode to survey an unfamiliar repository.
- Use chat or plan mode to develop a design for a new project — producing documentation and specs, not code.
- Identify the kinds of knowledge an agent cannot recover from code alone, and write a minimal project context file that supplies it.
- Evaluate AI design suggestions critically: probe what you don't understand, and don't build on ideas you can't defend.

::::::::::::::::::::::::::::::::::::::::::::::::

## Plan first, code second

The most common agentic failure mode is letting the agent write code before either of
you understands the problem. The planning phase — where the deliverables are
*understanding, documentation, and specs*, not code — is where agents are both safest
and most underused. There are two entry points, depending on whether a project already
exists.

Most tools have a read-only mode built for exactly this — in Claude Code it's *plan
mode* (toggle with <kbd>Shift</kbd>+<kbd>Tab</kbd>); in GitHub Copilot it's *Ask* mode
(the mode dropdown in the chat panel) — in which the agent reads files and answers
questions **without making any changes**.

## Entry point 1: an existing project

The safest possible first contact with an agent: it can't edit anything, so you can
hand it a whole repository and simply ask what it sees. It's also genuinely useful —
onboarding onto a colleague's project, returning to your own code from two years ago,
or auditing a repo before you build on it.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise 1: First look (8 minutes)

Point your agent at the practice repository (see [setup](../learners/setup.md)) — or any
real project you have handy — in read-only mode:

:::::::::::::::: group-tab

### Claude Code

Launch `claude` from the repository root, then press <kbd>Shift</kbd>+<kbd>Tab</kbd>
until the status line shows **plan mode** — Claude can now read and answer, but not
edit or run anything.

### GitHub Copilot

Open the repository folder in VS Code, open the Copilot chat panel
(<kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>I</kbd>), and pick **Ask** in
the mode dropdown. Start your message with `@workspace` so the question covers the
whole repo.

::::::::::::::::::::::::

Then prompt:

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

## Entry point 2: a blank page

When nothing exists yet, there is nothing to explore — all the knowledge has to flow
from your head into the project. This is where general AI chat (or plan mode) shines
as a *design partner*: talk through the problem before any code exists, and make the
deliverables **documentation and specs, not code**. Useful asks:

- "Here's my research question and my data situation. Sketch two or three ways to
  structure this analysis, with trade-offs."
- "Draft a README for this project: goal, planned structure, data sources, what
  'done' looks like." — a README written *before* the code is a spec.
- "Write a data plan: expected inputs, formats, validation checks we should run."
- "Turn this conversation into a first `AGENTS.md` / `CLAUDE.md` for the project."

Once the design conversation has produced specs you believe in, the transition to code
is deliberate and small: initialize git *before* the agent writes anything, let it
scaffold the skeleton (directory layout, environment file, that README — boilerplate
is the one place the agent's average-case instincts are exactly what you want), and
then stop scaffolding and switch to feature-by-feature work (next episode). "Build me
the whole project" is precisely the underspecified mega-prompt that goes wrong. A new
repo is also the cheapest moment to write the context file: two paragraphs now beat
archaeology later.

::::::::::::::::::::::::::::::::::::: callout

## Don't build on ideas you can't defend

A caution that matters most at the design stage: AI design advice is fluent even when
it's wrong, and it is most persuasive exactly where your own domain knowledge is
thinnest. An architecture, statistical approach, or library choice you don't
understand is a liability even if it's good — you can't debug, extend, or defend it
in review (or peer review).

So probe before you adopt. Ask "why this over the obvious alternative?", "what are
the failure modes?", "what's the simplest version that could work?" — and push back;
the agent folds quickly when an idea is weak, which is itself information. Be
especially wary the further a suggestion sits outside your domain: a clever-looking
method from a field you don't know is a place to consult a human expert or the
literature, not a thing to build on because the chat sounded confident. The rule from
the verification episode applies to designs too: if you can't explain it, you don't
own it yet.

::::::::::::::::::::::::::::::::::::::::::::::::

## Ready to begin: write the context file

Both entry points converge here. Exploring surfaced gaps — the *why*, the
conventions, what the data means — that live only in your head; designing produced
specs that live only in a chat transcript. Before the first real feature, capture
both in a **project context file**.
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
budget. And remember from the words-of-caution episode: context files are advisory — back
safety-critical rules with hooks or deny rules.

## The same task at three autonomy levels

Recall the autonomy spectrum from episode 1. This read-the-repo task makes it concrete:

- **Chat**: you would paste selected files into a browser tab and ask. Fast, safe, but
  the summary only covers what you chose to paste — *you* did the exploring.
- **Interactive agent**: what you just did. The agent explores everything, and you can
  interrogate it.
- **Async agent**: you could file an issue ("document this repo") and get a PR back.
  Least effort — and the least opportunity to notice what the summary got wrong,
  because you weren't watching it form.

More autonomy isn't automatically better. For understanding-type tasks, the interactive
middle of the spectrum is usually the sweet spot: full access for the agent, full
visibility for you.

::::::::::::::::::::::::::::::::::::: keypoints

- Plan before code: the planning phase's deliverables are understanding, documentation, and specs — territory where agents are safe and strong.
- For existing projects, start in read-only/plan mode; agents recover *what* and *how* from code, but not *why*, *for whom*, or what the data means.
- Project context files (`CLAUDE.md`, `copilot-instructions.md`, `AGENTS.md`) write down that missing knowledge — keep them short, operational, and advisory-aware.
- For new projects, design in chat first (README-as-spec, data plan), scaffold small, then go feature-by-feature — and write the context file at project birth.
- Probe AI design ideas before adopting them, hardest where your domain knowledge is thinnest: if you can't explain it, you don't own it yet.

::::::::::::::::::::::::::::::::::::::::::::::::
