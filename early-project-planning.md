---
title: "Planning with Agents"
teaching: 12
exercises: 25
---

:::::::::::::::::::::::::::::::::::::: questions

- Why plan before letting an agent write code, and what does the evidence say?
- What goes into a plan, and where does the agent get the context to make one?
- What is a minimum viable pipeline, and why start there?
- How do I plan with an agent without adopting designs I cannot defend?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain how a plan changes what an agent does with its context and tokens.
- Supply the context an agent needs to plan: goal, constraints, existing code, standards, prior decisions.
- Use an agent in a read-only or plan mode to review and improve a plan before any code exists.
- Agree team collaboration conventions with an agent's help and commit them as a `CONTRIBUTING.md` that people and agents both read.
- Produce a `plan.md` with ordered features and a check for each, and commit it before implementing anything.
- Evaluate AI design suggestions critically: question what you do not understand, and do not build on ideas you cannot defend.

::::::::::::::::::::::::::::::::::::::::::::::::

## Start with a plan

The most common failure in agentic work is letting the agent write code before either
party understands the problem. The research on planning is consistent:

- Structured planning before implementation improved coding success by up to 26.7%,
  reducing failed generations and repeated implementation attempts (Jiang et al.,
  2023).
- Removing the blueprint-planning agent from a structured coding pipeline reduced
  accuracy by 14.8 percentage points (Mao et al., 2025).
- Runs on the same coding task varied by up to 30× in total token usage, and higher
  token consumption did not produce greater accuracy (Bai et al., 2026).

These studies measured accuracy rather than token use, but the mechanism is
straightforward. Without a plan, the agent makes exploratory and redundant tool calls,
which usually means more tokens for lower accuracy. With a good plan, it makes fewer
wasted turns and less rework, which usually means fewer tokens and higher accuracy.
With a bad plan, it anchors on incorrect assumptions, which produces both lower
accuracy and higher token use.

Without a plan, an agent tends to make unnecessary repository searches, re-read the
same files, modify the wrong layer, expand beyond the requested scope, make
contradictory edits, loop on debugging, and report completion prematurely. With a
plan, it searches purposefully, reads only the relevant files, understands constraints
before implementing, detects missing information early, sequences dependent changes
correctly, tracks what is done, verifies the acceptance criteria, and stops when the
task is complete.

A plan gives the agent direction. It gives you a review point before implementation.
It gives both parties a shared definition of done. Planning should be proportional to
the task: a three-line plan for a three-line task.

## Supply context

An agent asked to "make a plan" with no other input produces the average plan for the
average project. The plan is only as good as the context it is built from. Context
worth providing, in rough order of how often it is missing:

- **The goal and constraints**: the research question, the challenge page, the scoring
  rule, the compute available.
- **The previous `plan.md`**, or its discoveries and blockers.
- **Skeleton code**: a stub of the function or module you want, so the shape is yours.
- **A GitHub issue or story** describing the feature in your words.
- **`future-work.md`**: what is deliberately out of scope.
- **Rules and coding-standards files**: the project context file described below,
  plus any style guide your group follows.

For long tasks (multi-hour work, anything spanning several sessions, handoffs between
people or agents), keep the plan in a file the agent updates as it works. Aaron
Friel's [Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans)
describes the pattern. A persistent plan file typically contains:

- Goal and context
- Scope and acceptance criteria
- Architectural decisions
- Ordered implementation steps
- Progress and completion status
- Discoveries, assumptions, and blockers
- Test commands and results
- Final outcome

Planning is iterative. The first plan is a draft to be questioned; the deliverable is
a plan you would sign.

## Plan mode: read without writing

Most tools have a read-only mode for this stage, in which the agent reads files and
answers questions without making changes. It is the safest first contact with a
repository and the appropriate mode for reviewing a plan.

:::::::::::::::: group-tab

### Claude Code

Press <kbd>Shift</kbd>+<kbd>Tab</kbd> until the status line shows **plan mode**.
Claude can then read and answer but not edit or run anything. On the web, begin the
prompt with "Plan mode, do not edit", or ask for a plan and review it before approving
implementation.

### GitHub Copilot

Select **Ask** (or **Plan**) in the chat panel's mode dropdown, and begin the message
with `@workspace` so the question covers the whole repository. Switch to **Agent**
only when you are ready for it to edit.

::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Agree how your team will collaborate (10 minutes)

Every member of the team is about to use a coding agent on the same repository, which
will produce more branches, more commits, and larger diffs than a typical project.
Decide the rules before the first feature, and have the agent draft them.

1. **Decide between branches and forks.** One shared repository with branches is the
   usual choice for a team that trusts each other: every teammate's work is a
   `git fetch` away, so an agent can read another branch, compare against it, and
   merge without anyone adding remotes.
2. **Ask the agent**, giving it your team size and what you are building:

   > Our team of \<n\> is working in one GitHub repo on \<challenge\>. Every one of us
   > is using a coding agent, so we will be generating more branches, more commits
   > and bigger diffs than a normal project.
   >
   > Propose contributing conventions that keep `main` clean and reviewable. Cover
   > branch naming, how small a pull request should be, who reviews, what an agent
   > may touch without asking, how we avoid two agents editing the same file, and
   > what goes in commit messages. Also suggest how to organize the repo structure so
   > any new files go in the correct spot.
   >
   > Write `CONTRIBUTING.md`. Commit it to a development branch named for me, not to
   > `main`, and open a pull request for it. Short enough that people read it.

3. **Edit what it produces.** Keep the rules the team will follow and remove the
   rest.
4. **Merge it through the process it describes.** `CONTRIBUTING.md` goes on your own
   branch, not directly to `main`. Open a pull request, have a teammate review it,
   then merge. This is the first use of the rules you have just written. Most agents
   open a pull request by default; note that when it happens.
5. Share the link with whoever advises the team, so they can see what was agreed.

If you are working alone, write the same thing for yourself in three to five lines (a
branch convention, a pull-request size, what the agent may never modify) and put it
in your context file.

:::::::::::::::::::::::: solution

## What a usable result contains

It is short. A branch-name pattern (`<name>/<feature>`); a pull-request size people
will review in full (a few hundred lines at most); one named reviewer per pull
request, and whether review happens at the pull request or on every change (the
verification episode compares the two); a list of paths the agent may not modify without asking (`data/raw/`, the
scoring function, `main`); a rule for avoiding collisions (one feature per branch,
claimed in the plan); and a commit-message format. Agents draft a reasonable first
version because conventions are the average case. Your contribution is removing what
the team will not do. The rules are advisory for the agent; back the important ones
with branch protection.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Start from a minimum viable pipeline

A **minimum viable pipeline (MVP)** is whatever you can get running quickly and
understand end to end. It is not necessarily the simplest model: a pretrained model
you understand is preferable to a from-scratch model you do not. The aim is to
minimize points of friction and failure: a slice of the data, one model, your laptop.
Each additional step or more elaborate setup is another place for the pipeline to
break.

- **Functional, not polished.** Borrowed code is acceptable if you can explain what it
  does. Defer the edge cases.
- **Do not defer the understanding.** A pipeline you understand reveals the real
  relationships in the data, the processing bugs, and the data problems that a
  system you do not understand would conceal.

The MVP is the baseline against which new components are compared, before investing
in solutions that take time to build. It is also the appropriate first plan for an
agent: small enough to specify fully, with every feature something you can check.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Plan your MVP with an agent (15 minutes)

1. **Open your project's MVP plan.** If there is none, write three lines now: the data
   slice, one model, and how you score it. If you have no project, choose a public
   dataset or competition you know and plan an MVP for it.
2. **Ask the agent to review it** in plan mode, against your project's goal (the
   challenge page, the paper's research question, or the grant aim):

   > Review our Minimum Viable Pipeline (MVP) plan against the challenge page. The
   > MVP should be something we can get running quickly and understand end-to-end.
   > It is the baseline we A/B new components against, before we invest in
   > solutions that take time to build.
   >
   > **MVP plan**
   > \<paste from your shared doc\>
   >
   > **Challenge page**
   > \<paste challenge text, scoring, data description\>
   >
   > **Compute available**
   > \<laptops; hosted models and how they're accessed; cloud credits and when\>
   >
   > Is this a good MVP? Say why or why not. If it is good, propose a `plan.md` with
   > each step in order and how we will know each one works. If it is not, propose a
   > better starting point and do the same for that. Do not write any code yet.

3. **Question the plan until you would sign it.** Challenge anything you cannot
   explain, and ask why a given choice is preferable to the obvious alternative.
4. **Commit `plan.md` to your repository.** No code until the plan is committed.
5. **If you finish early**, apply the same review to your pre-modeling steps
   (loading, cleaning, splitting, feature construction) and save the result as
   `prep.md`. Then ask the agent to review `plan.md` and `prep.md` together.

:::::::::::::::::::::::: solution

## What a good `plan.md` contains

Three features, each one thing you can check. For example: (1) load and validate the
data slice, with row count and class balance printed; (2) train one baseline, with a
score on a held-out split; (3) write the scoring function, matching the challenge
metric on a hand-computed example. If the agent's plan contains a feature for which
you cannot describe a check, it is not yet a feature; split it or remove it. Note also
what the agent could not know: which data is trustworthy, what compute you have, what
the kickoff decided. You supplied that context; without it the plan would have been
for a different project.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## Do not build on ideas you cannot defend

AI design advice is fluent whether or not it is correct, and it is most persuasive
where your own domain knowledge is weakest. An architecture, statistical approach, or
library choice you do not understand is a liability even if it is good, because you
cannot debug, extend, or defend it in review or in peer review.

Question a suggestion before adopting it. Ask why this rather than the obvious
alternative, what the failure modes are, and what the simplest workable version would
be. An agent tends to abandon a weak idea under questioning, which is itself evidence.
Be most cautious about suggestions from outside your field: a method from a discipline
you do not know is a reason to consult a human expert or the literature, not something
to adopt because the response sounded confident. If you cannot explain it, you do not
yet own it.

::::::::::::::::::::::::::::::::::::::::::::::::

## Before the first feature: write the context file

Planning surfaces knowledge that exists only in your head: the reasons for decisions,
the conventions, what the data means. Before the first feature, record it in a
**project context file**, the rules file introduced in the safety episode. Claude Code
reads `CLAUDE.md` from the project root at the start of every session; Copilot reads
`.github/copilot-instructions.md`; nearly every tool also reads `AGENTS.md`. It is a
README addressed to the agent:

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

Keep it short and operational (well under 300 lines). It is injected into every
session, so everything in it competes for the model's attention with the task at
hand. If a linter can enforce a rule deterministically, use the linter and save the
context. As the safety episode explained, context files are advisory; back
safety-critical rules with permissions, hooks, or branch protection.

::::::::::::::::::::::::::::::::::::: keypoints

- Plan before code. Planning measurably improves accuracy, and a good plan usually reduces token use. Keep planning proportional to the task.
- A plan is only as good as its context. Provide the goal, constraints, compute, existing code, standards, and prior decisions; for long work, keep the plan in a file the agent updates.
- Agree team conventions first (branches rather than forks, pull-request size, who reviews, what the agent may not modify, where new files go) and commit them as a `CONTRIBUTING.md` that agents also read.
- Use plan mode (read-only) to review a plan. The deliverable is a `plan.md` with ordered features and a check for each, committed before any code.
- Start from a minimum viable pipeline: a slice of data, one model, something you understand end to end.
- Question AI design suggestions before adopting them, most carefully where your domain knowledge is weakest. If you cannot explain it, you do not yet own it.
- Write the project context file (`CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`) at the start of the project. Keep it short, operational, and backed by permissions where it matters.

::::::::::::::::::::::::::::::::::::::::::::::::
