---
title: "Planning with Agents"
teaching: 12
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- Why plan before letting an agent write code — and what does the evidence say?
- What goes into a plan, and where does the agent get the context to make one?
- What is a minimum viable pipeline, and why start there?
- How do I plan with an agent without being led somewhere I can't follow?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain how a plan changes what an agent does with its context and tokens.
- Supply the context an agent needs to plan: goal, constraints, existing code, standards, prior decisions.
- Use an agent in a read-only/plan mode to review and improve a plan before any code exists.
- Produce a `plan.md` with ordered features and a check for each, and commit it before implementing anything.
- Evaluate AI design suggestions critically: probe what you don't understand, and don't build on ideas you can't defend.

::::::::::::::::::::::::::::::::::::::::::::::::

## Start with a plan

The most common agentic failure mode is letting the agent write code before either of
you understands the problem. The research on planning is consistent:

- Structured planning before implementation improved coding success by up to **26.7%**,
  reducing failed generations and repeated implementation attempts (Jiang et al., 2023).
- Removing the blueprint-planning agent from a structured coding pipeline reduced
  accuracy by **14.8 percentage points** (Mao et al., 2025).
- Runs on the *same* coding task varied by up to **30×** in total token usage, and
  higher token consumption did not produce greater accuracy (Bai et al., 2026).

Those studies measured accuracy, not token savings, but the mechanism is easy to
see. No plan → exploratory and redundant tool calls → often *more* tokens for *worse*
accuracy. A good plan → fewer wasted turns and less rework → often fewer tokens with
better accuracy. A bad plan → anchoring to incorrect assumptions → the worst of both.

Without a plan, an agent tends to make unnecessary repository searches, re-read the
same files, modify the wrong layer, expand beyond the requested scope, make
contradictory edits, loop on debugging, and claim completion prematurely. With one, it
searches purposefully, reads only the relevant files, understands constraints before
implementing, detects missing information early, sequences dependent changes
correctly, tracks what's done, verifies the acceptance criteria, and *stops* when the
task is complete.

A plan gives the agent direction. It gives you a review point *before*
implementation. And it gives both sides a shared definition of "done." The goal is
**proportional** planning — a three-line plan for a three-line task — not maximum
planning.

## How to make a plan: add context

Ask an agent to "make a plan" with nothing else and you get the average-case plan
for the average-case project. A plan is only as good as the context it's built from.
Examples of context worth handing over, in rough order of how often they're missing:

- **The goal and constraints** — the research question, the challenge page, the
  scoring rule, the compute you actually have.
- **`plan.md` from last time**, or the previous plan's discoveries and blockers.
- **Skeleton code** — a stub of the function or module you want, so the shape is
  yours, not the agent's.
- **A GitHub issue or story** describing the feature in your words.
- **`future-work.md`** — what's deliberately out of scope.
- **Rules and coding-standards files** — the project context file below, plus any
  style guide your lab follows.

For long tasks — multi-hour work, anything spanning several sessions, handoffs
between people or agents — keep the plan in a file the agent updates as it goes.
Aaron Friel's [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)
describes the pattern; a persistent plan file typically holds:

- Goal and context
- Scope and acceptance criteria
- Architectural decisions
- Ordered implementation steps
- Progress and completion status
- Discoveries, assumptions, and blockers
- Test commands and results
- Final outcome

Planning is iterative. The first plan is a draft you argue with; a plan you'd sign
is the deliverable.

## Plan mode: read, don't write

Most tools have a read-only mode built for exactly this stage, in which the agent
reads files and answers questions **without making any changes**. It's the safest
possible first contact with a repository — and the right mode for reviewing a plan.

:::::::::::::::: group-tab

### Claude Code

Press <kbd>Shift</kbd>+<kbd>Tab</kbd> until the status line shows **plan mode**.
Claude can now read and answer, but not edit or run anything. On the web, start the
prompt with "Plan mode, do not edit" — or ask for a plan and review it before
approving implementation.

### GitHub Copilot

Pick **Ask** (or **Plan**) in the chat panel's mode dropdown, and start your message
with `@workspace` so the question covers the whole repo. Switch to **Agent** only
when you're ready for it to edit.

::::::::::::::::::::::::

## Start from a minimum viable pipeline

Before the exercise, a framing you may have met in your project kickoff. A
**minimum viable pipeline (MVP)** is whatever you can get running quickly and
understand end to end. Not always the *simplest* model — a pretrained model you
understand beats a from-scratch one you don't. The point is fewer friction and
failure points: a slice of the data, one model, your laptop. Every extra step or
fancier setup is another place to break.

- **Functional, not perfect.** Borrowed code is fine if you can explain what it does.
  Skip the edge cases for now.
- **Don't skip the understanding.** A pipeline you understand shows you the real
  relationships, the processing bugs, and the data problems that a system you don't
  understand would hide.

The MVP is also the ideal first plan for an agent: small enough to specify fully,
and every feature in it is something you can check.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Plan your MVP with an agent (10 minutes)

1. **Open your project's MVP plan.** No plan yet? Write three lines now: the data
   slice, one model, how you score it. (No project? Pick a public dataset or
   competition you know and plan an MVP for it.)
2. **Ask the agent to review it**, in plan mode, against your project's goal — the
   challenge page, the paper's research question, or your grant aim:

   > Review our MVP plan against the challenge page.
   >
   > **MVP plan**
   > \<paste from your shared doc\>
   >
   > **Challenge page**
   > \<paste challenge text, scoring, data description\>
   >
   > The point of the MVP is something we can get running quickly and understand
   > end to end. Is this a good starting point, or is there a better one? Say why.
   > If it is good, propose `plan.md` with the first three features in order and how
   > we will know each works. Do not write any code yet.
   >
   > **Compute available**
   > \<laptops; hosted models and their API; cloud credits and when\>

3. **Argue with the plan until you would sign it.** Push back on anything you can't
   explain; ask why this over the obvious alternative.
4. **Commit `plan.md` to your repo.** No code until the plan is in.

:::::::::::::::::::::::: solution

## What a good `plan.md` looks like

Three features, each one thing you can check — e.g. *(1) load and validate the data
slice: row count and class balance printed; (2) train one baseline: a scored number
on a held-out split; (3) write the scoring function: matches the challenge metric on
a hand-computed example.* If the agent's plan has a feature you can't describe a check
for, it isn't a feature yet — split it or drop it. And notice what the agent
*couldn't* know: which data is trustworthy, what compute you really have, what the
kickoff decided. That's the context you supplied; without it the plan would have
been someone else's.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## Don't build on ideas you can't defend

AI design advice is fluent even when it's wrong, and it is most persuasive exactly
where your own domain knowledge is thinnest. An architecture, statistical approach,
or library choice you don't understand is a liability even if it's good — you can't
debug, extend, or defend it in review (or peer review).

So probe before you adopt. Ask "why this over the obvious alternative?", "what are the
failure modes?", "what's the simplest version that could work?" — and push back; the
agent folds quickly when an idea is weak, which is itself information. Be especially
wary the further a suggestion sits outside your domain: a clever-looking method from a
field you don't know is a place to consult a human expert or the literature, not a
thing to build on because the chat sounded confident. If you can't explain it, you
don't own it yet.

::::::::::::::::::::::::::::::::::::::::::::::::

## Ready to begin: write the context file

Planning surfaces the knowledge that lives only in your head — the *why*, the
conventions, what the data means. Before the first real feature, capture it in a
**project context file**, the rules file from the safety episode. Claude Code reads
`CLAUDE.md` from your project root at the start of every session; Copilot reads
`.github/copilot-instructions.md`; nearly everything also reads `AGENTS.md`. Think of
it as a README for the agent:

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
budget. And remember from the safety episode: context files are advisory — back
safety-critical rules with permissions, hooks, or branch protection.

::::::::::::::::::::::::::::::::::::: keypoints

- Plan before code: planning measurably improves accuracy, and a good plan usually costs fewer tokens, not more. Proportional, not maximal.
- A plan is only as good as its context — hand over the goal, constraints, compute, existing code, standards, and prior decisions; for long work keep the plan in a file the agent updates.
- Use plan mode (read-only) to review a plan; the deliverable is a `plan.md` with ordered features and a check for each, committed before any code.
- Start from a minimum viable pipeline: a slice of data, one model, something you understand end to end.
- Probe AI design ideas before adopting them, hardest where your domain knowledge is thinnest: if you can't explain it, you don't own it yet.
- Write the project context file (`CLAUDE.md` / `AGENTS.md` / `copilot-instructions.md`) at project birth — short, operational, advisory-aware.

::::::::::::::::::::::::::::::::::::::::::::::::
