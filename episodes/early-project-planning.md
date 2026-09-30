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

- Plan a research software project yourself, using an agent to research options and critique the plan rather than to originate it.
- Supply the context an agent needs: the research question, the data, the analysis you would do by hand, existing code, and standards.
- Use plan mode to refine a request until the structure the agent proposes matches the result you intend.
- Agree collaboration conventions and commit them as a `CONTRIBUTING.md`; produce a `plan.md` with ordered features and a check for each before implementing anything.
- Question AI design suggestions, and do not build on ideas you cannot defend.

::::::::::::::::::::::::::::::::::::::::::::::::

## Plan the research software yourself

Research software exists to answer a question, so the plan for it is the analysis
design. That design is yours: you will defend it in lab meetings, in peer review, and
in the methods section. Before an agent writes any code, you should be able to state:

- **The research question**, and the claim a result would support.
- **The data**: what you already know about its provenance, quality, and quirks.
- **The baseline or comparison** that makes a result meaningful.
- **The outputs**: the figures, tables, or numbers that will go in the paper.
- **What would show the approach is wrong.**

The agent's role here is research assistant and critic, not author:

- **Research assistant.** Summarize the options for a step; find the library that
  implements a method; keep the plan file current as work proceeds.
- **Critic.** Point out a gap in the plan; ask the question you had not considered;
  notice a step that assumes something the data description does not support.
- **Source of suggestions, taken under scrutiny.** It will propose ideas of its own.
  Treat each as a suggestion from a fluent but unaccountable colleague: ask why this
  rather than the obvious alternative, what the failure modes are, and whether it is
  standard in your field. Adopt it only when you could explain it without the agent.
  A method you cannot explain cannot go in a methods section.

Skipping this step and letting the agent write code before you understand the
problem is the most common failure in agentic work. Keep the plan proportional to the
task: a three-line plan for a three-line task.

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

## Plan mode: refine the request before any code

**Plan mode** is a setting on the agent, not a way of thinking. Switched on, the agent
can read the repository, answer questions, and propose an approach, but it cannot
edit a file or run a command. Claude Code toggles it with <kbd>Shift</kbd>+<kbd>Tab</kbd>;
Copilot calls it **Ask** or **Plan** in the chat panel's mode selector. The tabs below
give the details.

Its use is this. Once the analysis design is settled, you still have to turn it into
a request the agent can carry out, and the first version of that request is never
precise enough. In plan mode you describe what you want, the agent describes how it
would build it, and you correct the description until the structure it proposes
matches the result you intend. Only then do you switch plan mode off and let it
write code.

This is a different activity from the planning above, although the tools use the
same word. The analysis design is yours and is settled before plan mode starts. Plan
mode is about the prompt: making sure what you are asking for is specific enough that
the code the agent writes is the code you meant.

The refinement is worth the extra turns. Structured planning before implementation
improved coding success by up to 26.7%, reducing failed generations and repeated
implementation attempts
([Jiang et al., 2023](https://arxiv.org/abs/2303.06689)). The mechanism is
straightforward. Without a plan, an agent makes exploratory and redundant tool calls:
unnecessary repository searches, re-reading the same files, modifying the wrong layer,
expanding beyond the requested scope, looping on debugging, and reporting completion
prematurely. With a plan, it reads only the relevant files, understands constraints
before implementing, sequences dependent changes correctly, checks the acceptance
criteria, and stops when the task is complete. With a bad plan, it anchors on
incorrect assumptions, which costs both accuracy and tokens.

Used well, a plan-mode exchange sharpens the request in three ways:

- **Feedback on the request.** The agent reads your request, `plan.md`, and the
  repository together and reports what does not line up: a feature with no check, a
  step that assumes data in a format the repository does not contain, a dependency
  that is not installed. Each mismatch is something to fix in the request.
- **A structure for the intended result.** It proposes the modules, functions, and
  tests it would produce, so you can correct the shape (where the scoring function
  lives, what the data loader returns) while it is still a description rather than
  code.
- **Loose ends surfaced first.** Anything it would otherwise have guessed at during
  implementation becomes a question now: which column is the label, which split is
  held out, what to do with missing values. Your answers go into the request, because
  an agent that guesses mid-implementation guesses the average case.

The output is a request and an implementation outline you approve, edit, or reject.
It should not change the analysis design without you noticing. If the proposed
structure quietly substitutes a different model, metric, or split, correct it before
approving.

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
Decide the rules that matter before the first feature: who reviews, what the agent
may never touch, and where data, code, and results live. Then have the agent draft the
document from those decisions.

1. **Decide between branches and forks.** One shared repository with branches is the
   usual choice for a team that trusts each other: every teammate's work is a
   `git fetch` away, so an agent can read another branch and compare against it
   without anyone adding remotes. Merging stays with a person.
2. **Ask the agent**, giving it your team size and what you are building:

   > Our research group of \<n\> is working in one GitHub repo on \<project, for
   > example the analysis for a paper\>. Every one of us
   > is using a coding agent, so we will be generating more branches, more commits
   > and bigger diffs than a normal project.
   >
   > We have decided: \<who reviews each pull request; paths the agent may not
   > modify; where raw data, processed data, code, and results live\>. Turn these into
   > contributing conventions that keep `main` clean and reviewable. Fill in the
   > routine parts (branch naming, how small a pull request should be, commit-message
   > format, how we avoid two agents editing the same file, where new files go) and
   > mark each rule you added so we can accept or remove it.
   >
   > Write `CONTRIBUTING.md`. Commit it to a development branch named for me, not to
   > `main`, and open a pull request for it. Short enough that people read it.

3. **Edit what it produces.** Keep the rules the team will follow and remove the
   rest.
4. **Merge it through the process it describes.** `CONTRIBUTING.md` goes on your own
   branch, not directly to `main`. Open a pull request, have a teammate review it,
   then merge. This is the first use of the rules you have just written. Most agents
   open a pull request by default; note that when it happens.
5. Share the link with your PI or project lead, so they can see what was agreed.

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
claimed in the plan); and a commit-message format. Agents draft the routine parts well because conventions are the average case. The
decisions that matter (who reviews, what the agent may not touch, where results live)
are the group's; your contribution is making those and removing what the group will
not do. The rules are advisory for the agent; back the important ones
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

   > Review our Minimum Viable Pipeline (MVP) plan against our project goal. The
   > MVP should be something we can get running quickly and understand end-to-end.
   > It is the baseline we compare new components against, before we invest in
   > solutions that take time to build.
   >
   > **MVP plan**
   > \<paste from your shared doc\>
   >
   > **Project goal**
   > \<paste the research question or grant aim, the evaluation metric, and the data
   > description\>
   >
   > **Compute available**
   > \<laptops; cluster allocation; hosted models and how they're accessed; cloud
   > credits and when\>
   >
   > Is this a good MVP? Say why or why not, and list any step that is missing,
   > unclear, or assumes something the data description does not support. Do not
   > propose a replacement design; if something should change, say what and why, and
   > we will decide. Then write our MVP up as a `plan.md` with each step in order and
   > how we will know each one works. Do not write any code yet.

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
score on a held-out split; (3) write the scoring function, matching the metric your
field or paper uses on a hand-computed example. If `plan.md` contains a feature for which
you cannot describe a check, it is not yet a feature; split it or remove it. Note also
what the agent could not know: which data is trustworthy, what compute you have, what
your group has already decided. You supplied that context; without it the plan would have been
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

- The plan is the analysis design, and it is yours: research question, data, baseline, outputs, and what would show the approach is wrong. The agent assists and critiques; ideas it proposes are adopted only when you can defend the reasoning. Record it as a `plan.md` with ordered features and a check for each, committed before any code.
- Plan before code. Planning measurably improves accuracy, and a good plan usually reduces token use. Keep planning proportional to the task.
- A plan is only as good as its context. Provide the research question, what you know about the data, the analysis you would do by hand, compute, existing code, and standards; for long work, keep the plan in a file the agent updates.
- Agree team conventions first (branches rather than forks, pull-request size, who reviews, what the agent may not modify, where new files go) and commit them as a `CONTRIBUTING.md` that agents also read.
- Plan mode is distinct from planning the analysis. It is where you refine the request: the agent critiques it, proposes the structure of the intended result, and raises loose ends for you to settle, and you approve the outline before any code is written.
- Start from a minimum viable pipeline: a slice of data, one model, something you understand end to end.
- Question AI design suggestions before adopting them, most carefully where your domain knowledge is weakest. If you cannot explain it, you do not yet own it.
- Write the project context file (`CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`) at the start of the project. Keep it short, operational, and backed by permissions where it matters.

::::::::::::::::::::::::::::::::::::::::::::::::
