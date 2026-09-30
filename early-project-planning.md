---
title: "Planning with Agents"
teaching: 15
exercises: 25
---

:::::::::::::::::::::::::::::::::::::: questions

- Why should you plan the analysis yourself before an agent writes any code?
- What goes into a plan, and where does the agent get the context to make one?
- What is a minimum viable pipeline, and why start there?
- How do I plan with an agent without adopting designs I cannot defend?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Plan a research software project yourself, from the research question down, using an agent to research options and critique the plan rather than to originate it.
- Explain how a plan changes what an agent does with its context and tokens.
- Supply the context an agent needs to plan: goal, constraints, existing code, standards, prior decisions.
- Use plan mode to have the agent critique the plan, propose the structure of the code it will write, and surface open questions before any code exists.
- Agree team collaboration conventions with an agent's help and commit them as a `CONTRIBUTING.md` that people and agents both read.
- Produce a `plan.md` with ordered features and a check for each, and commit it before implementing anything.
- Evaluate AI design suggestions critically: question what you do not understand, and do not build on ideas you cannot defend.

::::::::::::::::::::::::::::::::::::::::::::::::

## Plan the research software yourself

Research software exists to answer a question, and the plan for it is the analysis
design. Before an agent writes any code, you should be able to state the research
question, the claim a result would support, the data and what you already know about
it, the comparison or baseline that makes the result meaningful, and the figures,
tables, or numbers that will end up in the paper. You should also be able to say what
would show the approach is wrong. None of that is programming, and none of it should
be delegated. The ideas come from you, from the literature, and from the people you
work with, because you are the ones who will defend them in a lab meeting, in peer
review, and in the methods section.

An agent is useful at this stage in two roles. As a research assistant it can
summarize the options for a step, find the library that implements a method, and keep
the plan file current as work proceeds. As a critic it can point out a gap in the
plan, ask a question you had not considered, or notice that a step assumes something
the data description does not support. In both roles it works from the context you
give it, and it does not know your field's standards unless you state them.

Agents will also propose ideas of their own, and some are good. Treat each one as a
suggestion from a fluent but unaccountable colleague: ask why this rather than the
obvious alternative, what the failure modes are, whether it is standard practice in
your field, and what the simplest workable version would be. Adopt it only when the
reasoning holds up and you could explain it without the agent. A method you cannot
explain cannot go in a methods section. The section
[below](#do-not-build-on-ideas-you-cannot-defend) covers this in more detail. This is
what staying in the driver's seat means before any code exists.

The most common failure in agentic work is skipping this step and letting the agent
write code before you understand the problem. Planning first also changes how the
agent works. Structured planning before implementation improved coding success by up
to 26.7%, reducing failed generations and repeated implementation attempts
([Jiang et al., 2023](https://arxiv.org/abs/2303.06689)). The mechanism is
straightforward. Without a plan, an agent makes exploratory and redundant tool calls:
unnecessary repository searches, re-reading the same files, modifying the wrong layer,
expanding beyond the requested scope, looping on debugging, and reporting completion
prematurely. With a plan, it reads only the relevant files, understands constraints
before implementing, sequences dependent changes correctly, checks the acceptance
criteria, and stops when the task is complete. With a bad plan, it anchors on
incorrect assumptions, which costs both accuracy and tokens.

A plan gives the agent direction. It gives you a review point before implementation.
It gives both parties a shared definition of done. Planning should be proportional to
the task: a three-line plan for a three-line task.

## Supply context

An agent asked to "make a plan" with no other input produces the average plan for the
average project, and research projects are rarely the average case. The plan is only
as good as the context it is built from. Context worth providing, in rough order of
how often it is missing:

- **The research question and the constraints**: what a result has to show, the
  scoring rule or evaluation metric, the compute available (a laptop, a cluster
  allocation, cloud credits), and any deadline.
- **What you know about the data**: provenance, units, sampling, known artifacts,
  missingness, and which subsets are trustworthy. Nobody but you and your
  collaborators knows this.
- **The analysis you would have done by hand**: the splits, the controls, the
  baseline, and the statistics your field expects.
- **The previous `plan.md`**, or its discoveries and blockers.
- **Skeleton code**: a stub of the function or module you want, so the shape is yours.
- **A GitHub issue** describing the feature in your words.
- **`future-work.md`**: what is deliberately out of scope for this paper or release.
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

## Plan mode: the agent plans the implementation

Plan mode is a different activity from the planning above, and the two are easy to
confuse because the tools use the same word. The analysis design is yours. Plan mode
is where the agent, given that design, works out how it will build the code: which
files it will create or change, in what order, what it needs to know before it starts,
and where it is uncertain. Most tools provide it as a read-only mode in which the
agent reads the repository and answers questions without editing or running anything,
which also makes it the safest first contact with an unfamiliar codebase.

Used well, plan mode does three things before any code exists:

- **Feedback on your plan.** The agent reads `plan.md` and the repository together and
  reports what does not line up: a feature with no check, a step that assumes data in
  a format the repository does not contain, a dependency that is not installed.
- **A structure for the code it will write.** It proposes the modules, functions, and
  tests it intends to produce, so you can correct the shape (where the scoring
  function lives, what the data loader returns) while it is still cheap to change.
- **Loose ends surfaced first.** Anything it would otherwise have guessed at during
  implementation becomes a question now: which column is the label, which split is
  held out, what to do with missing values. Answer these before approving the plan,
  because an agent that guesses mid-implementation guesses the average case.

The output of plan mode is an implementation plan you approve, edit, or reject. It is
not the analysis design, and it should not change the analysis design without you
noticing. If the agent's implementation plan quietly substitutes a different model,
metric, or split, that is a plan to reject.

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

- The plan is the analysis design, and it is yours: research question, data, baseline, outputs, and what would show the approach is wrong. The agent assists and critiques; ideas it proposes are adopted only when you can defend the reasoning.
- Plan before code. Planning measurably improves accuracy, and a good plan usually reduces token use. Keep planning proportional to the task.
- A plan is only as good as its context. Provide the research question, what you know about the data, the analysis you would do by hand, compute, existing code, and standards; for long work, keep the plan in a file the agent updates.
- Agree team conventions first (branches rather than forks, pull-request size, who reviews, what the agent may not modify, where new files go) and commit them as a `CONTRIBUTING.md` that agents also read.
- Plan mode is distinct from planning the analysis: the agent critiques your plan, proposes the code structure, and raises loose ends for you to settle before it implements. The deliverable is a `plan.md` with ordered features and a check for each, committed before any code.
- Start from a minimum viable pipeline: a slice of data, one model, something you understand end to end.
- Question AI design suggestions before adopting them, most carefully where your domain knowledge is weakest. If you cannot explain it, you do not yet own it.
- Write the project context file (`CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`) at the start of the project. Keep it short, operational, and backed by permissions where it matters.

::::::::::::::::::::::::::::::::::::::::::::::::
