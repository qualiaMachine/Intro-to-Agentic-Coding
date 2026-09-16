---
title: "Planning with Agents"
teaching: 12
exercises: 25
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
- Agree team collaboration conventions with an agent's help and commit them as a `CONTRIBUTING.md` that people and agents both read.
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
  scoring rule, the compute you have.
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

:::::::::::::::::::::::::::::::::::: challenge

## Exercise: Agree how your team will work together (10 minutes)

Every one of you is about to use a coding agent on the same repository, so you will
generate more branches, more commits, and bigger diffs than a normal project. Decide
the rules before the first feature — and let the agent draft them.

1. **Decide branches or forks first.** One shared repo and branches is the usual
   answer for a team that trusts each other: every teammate's work is a `git fetch`
   away, so an agent can read another branch, diff against it, and merge without
   anyone adding remotes.
2. **Ask the agent.** Give it your team size and what you are building:

   > Our team of \<n\> is working in one GitHub repo on \<challenge\>. Every one of us
   > is using a coding agent, so we will be generating more branches, more commits
   > and bigger diffs than a normal class project.
   >
   > Propose collaboration conventions that keep `main` clean and reviewable. Cover
   > branch naming, how small a pull request should be, who reviews, what an agent is
   > allowed to touch without asking, how we avoid two agents editing the same file,
   > and what goes in commit messages.
   >
   > Give me a `CONTRIBUTING.md` we can commit today. Short enough that people read it.

3. **Argue with what it gives you.** Keep the rules you will follow; cut the
   rest.
4. **Commit `CONTRIBUTING.md` to the team repo.** Your agents read it too.
5. Share the link with whoever advises your team, so they can see what you agreed.

Working solo? Do the same for yourself in three to five lines — a branch convention,
a PR size, what the agent may never touch — and put them in your context file.

:::::::::::::::::::::::: solution

## What a usable answer looks like

Short. A branch name pattern (`<name>/<feature>`), a PR size people will
review (a few hundred lines at most), one named reviewer per PR, a list of paths the
agent may not touch without asking (`data/raw/`, the scoring function, `main`), a
rule for avoiding collisions (one feature per branch, claim it in the plan), and a
commit-message shape. Agents draft a good first version because conventions are the
average case; the value you add is deleting what your team won't do. The rules are
advisory for the agent — back the important ones with branch protection.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Start from a minimum viable pipeline

Before the exercise, a framing you may have met in your project kickoff. A
**minimum viable pipeline (MVP)** is whatever you can get running quickly and
understand end to end. Not always the *simplest* model — a pretrained model you
understand beats a from-scratch one you don't. The aim is fewer friction and
failure points: a slice of the data, one model, your laptop. Every extra step or
fancier setup is another place to break.

- **Functional, not perfect.** Borrowed code is fine if you can explain what it does.
  Skip the edge cases for now.
- **Don't skip the understanding.** A pipeline you understand shows you the real
  relationships, the processing bugs, and the data problems that a system you don't
  understand would hide.

The MVP is the baseline you A/B new components against, before you invest in
solutions that take time to build. It is also the ideal first plan for an agent:
small enough to specify fully, and every feature in it is something you can check.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Plan your MVP with an agent (15 minutes)

1. **Open your project's MVP plan.** No plan yet? Write three lines now: the data
   slice, one model, how you score it. (No project? Pick a public dataset or
   competition you know and plan an MVP for it.)
2. **Ask the agent to review it**, in plan mode, against your project's goal — the
   challenge page, the paper's research question, or your grant aim:

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

3. **Argue with the plan until you would sign it.** Push back on anything you can't
   explain; ask why this over the obvious alternative.
4. **Commit `plan.md` to your repo.** No code until the plan is in.
5. **Finished early?** Interrogate your pre-modeling steps the same way — loading,
   cleaning, splitting, feature construction — and save the result as `prep.md`. Then
   ask the agent to review `plan.md` and `prep.md` together, holistically.

:::::::::::::::::::::::: solution

## What a good `plan.md` looks like

Three features, each one thing you can check — e.g. *(1) load and validate the data
slice: row count and class balance printed; (2) train one baseline: a scored number
on a held-out split; (3) write the scoring function: matches the challenge metric on
a hand-computed example.* If the agent's plan has a feature you can't describe a check
for, it isn't a feature yet — split it or drop it. Note also what the agent
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
agent tends to abandon a weak idea under questioning, which is itself evidence. Be especially
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
- Agree team conventions first — branches not forks, PR size, who reviews, what the agent may not touch — and commit them as a `CONTRIBUTING.md` your agents read too.
- Use plan mode (read-only) to review a plan; the deliverable is a `plan.md` with ordered features and a check for each, committed before any code.
- Start from a minimum viable pipeline: a slice of data, one model, something you understand end to end.
- Probe AI design ideas before adopting them, hardest where your domain knowledge is thinnest: if you can't explain it, you don't own it yet.
- Write the project context file (`CLAUDE.md` / `AGENTS.md` / `copilot-instructions.md`) at project birth — short, operational, advisory-aware.

::::::::::::::::::::::::::::::::::::::::::::::::
