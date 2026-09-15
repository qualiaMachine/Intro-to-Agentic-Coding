---
title: "Feature-Based Development and Good Prompting"
teaching: 10
exercises: 15
---

:::::::::::::::::::::::::::::::::::::: questions

- Why work feature by feature instead of asking for whole projects?
- What actually happens when I give an agent a vague request?
- What does a good prompt look like for research code?
- Which routine tasks are agents reliably good at?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Decompose a plan into feature-sized, verifiable tasks and work them one per session.
- Predict how an agent fills gaps in an underspecified request.
- Distinguish context engineering (standing guidance) from prompt engineering (the specific ask).
- Write prompts that specify inputs, output, the check for "done", and what not to touch.
- Implement one feature from your plan and audit the decisions the agent made for you.

::::::::::::::::::::::::::::::::::::::::::::::::

## Work feature by feature, not project by project

**A feature is one thing you can check.** Load and validate the data slice. Train one
baseline. Write the scoring function. The `plan.md` you just wrote is the feature
list — work down it in order.

- **One feature per chat session.** Fresh context, a small diff, one pull request.
  (The cost episode explains why a fresh session matters; the short version is that
  everything in a long session competes for the model's attention.)
- **Specify each one.** Inputs, output, how you will know it works, what not to touch.
- **Small scope means small diffs** — which means you can actually review them, and
  stay in the driver's seat. A project-sized prompt doesn't just produce worse code;
  it produces a diff too large to meaningfully review, at which point you've silently
  handed over the wheel.

**Whole-project prompts produce whole-project guesses.**

## Underspecified does not mean random

When your request is ambiguous, the agent doesn't fail and it doesn't guess randomly.
It does something more subtle and more dangerous: **it fills every gap with the most
statistically typical choice from its training data** — the most common file layout,
the default hyperparameters, the standard preprocessing for data that looks like
yours.

That's why underspecified requests so often produce code that *runs* and *looks
reasonable*: average-case answers usually do. The problem is that your data and code
are rarely the average case. Your weird instrument artifact is not in the training
data. Your field has a convention the average GitHub repo doesn't follow. Your
"duplicate rows" are actually repeated measures. Every unstated assumption gets
resolved in favor of someone else's typical project — silently.

Two consequences:

1. **Precision in, precision out.** The specification work you'd have to do for a
   colleague doesn't disappear; it moves into the prompt.
2. **The failure mode is plausible-but-wrong**, not obviously-broken. Which is why
   the next episode, on verification, is the heart of this lesson.

## Guide the agent with clear instructions

Two levers, at two time scales:

- **Context engineering** defines the standing guidelines for generating code and
  what resources the agent can reach: the project context file (`CLAUDE.md`,
  `AGENTS.md`, `copilot-instructions.md`), coding-standards files, `plan.md`. Written
  once, read every session. Sharing a context file among collaborators is a cheap way
  to keep a team's code consistent.
- **Prompt engineering** phrases the specific request to get the best possible
  result for *this* task.

These aren't competing approaches; they are concentric layers around the model, and
each contains the one inside it. The harness (the loop, tools, memory, sandbox) is the
outermost layer and mostly not yours to change; context and prompt are.

![Prompt, context, and harness engineering as three concentric layers around the model.](fig/prompt-context-harness.png){alt='Diagram of concentric circles. Innermost: Model. Around it: Prompt, the wording of a single instruction. Around that: Context, everything the model sees in its context window. Outermost: Harness, the whole system around the model: loop, tools, memory, sandbox. Caption: each layer contains the one inside it.'}

The same request at two levels of specification:

**Bad prompt:**

> Fix this bug.

**Better prompt:**

> Here is the error, the code that raised it, and what was running as input.
>
> **Error log**
> \<paste full traceback\>
>
> **Code**
> \<paste the function or file\>
>
> **Input**
> \<what data or arguments it was called with\>
>
> Before changing anything, explain what you think is causing this and how you would
> confirm it. Wait for me to agree before you apply a fix.

The better prompt supplies the *evidence* (traceback, code, input), asks for a
*diagnosis before a change*, and keeps the decision with you. Notice what "fix" would
have left to the average case: the agent would have to invent what "fixed" means —
and an agent told to make an error go away sometimes does exactly that, by deleting
the check that raised it.

A checklist for research-code prompts — specify:

- **Where**: which files or functions to touch, and which to leave alone.
- **What**: the behavior you want, including the edge cases you know about.
- **Constraints**: conventions, dependencies allowed, things to preserve.
- **Verification**: how the agent should check its own work — run the tests, confirm
  the row count is unchanged, print the class balance before and after.

That last item is the bridge to the next episode: a prompt that includes its own
check is worth two that don't.

## Maintenance tasks agents do well

Not every feature is new science. Agents are reliably good at the unglamorous work
that keeps a research repo usable — provided you give each task the same treatment
as a feature: small, specified, checkable, one pull request, and you review it.

- **Refactoring.** Split the 400-line notebook into functions and a script. Tests
  pass before and after, or it did not work.
- **Docstrings and type hints** on every function. Ask for a diff that changes no
  logic, then check that it didn't.
- **A README that matches the code.** "Read the repo and list what the README says
  that is no longer true."
- **Environment files.** Pin `requirements.txt` or `environment.yml` from what the
  code actually imports.
- **Weekly merge prep.** "Summarize what changed on this branch since `main`, for
  the teammates who were not here."

(The [documentation](documentation.md) episode goes deeper on the first three, and
on why documentation feeds back into agent performance.)

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Implement feature 1 from your plan (15 minutes)

Take feature 1 from your `plan.md` — or any feature you want to try adding.

1. **Write the prompt.** Fill in the template below. Point the agent at `plan.md`
   and your project's goal page.

   > Implement feature 1 from `plan.md`.
   >
   > **Feature**
   > \<name and what it does\>
   >
   > **Inputs** (if applicable)
   > \<files or data it reads; the slice we agreed on\>
   >
   > **Output** (if applicable)
   > \<what it produces and where\>
   >
   > **Done when**
   > \<the check that proves it works: a test, or a printed baseline number\>
   >
   > **Do not touch**
   > \<other files, `data/raw/`, the scoring function\>
   >
   > Work on a new branch (most coding agents do this automatically). When finished,
   > list every choice you made that I did not specify.

2. **Run it.** Read the diff before anything else.
3. **Audit.** Did it do only what you asked? What did it decide that you did not
   specify?

:::::::::::::::: group-tab

### Claude Code

Start a fresh session (or `/clear`) so the feature begins with a clean context. On
the web, the work comes back as a branch; locally, confirm it created one before it
edits.

### GitHub Copilot

Use **Agent** mode in a **New Chat**, or delegate the prompt to the cloud coding
agent and review the draft PR it opens.

::::::::::::::::::::::::

No project handy? Use this starter and ask for one feature — a stratified 80/20
split, a standardized logistic regression, and a printed majority-class baseline
next to the test accuracy:

```python
import pandas as pd
from sklearn import datasets

cancer = datasets.load_breast_cancer()
```

:::::::::::::::::::::::: solution

## What people typically observe

The "list every choice you did not specify" line is the most valuable one in the
template. Typical answers: a random seed, a default imputation, a metric it added
"for context", a file it created that you didn't ask for, a dependency it installed.
Each is now a decision you own. The ones that surprise you are exactly the ones to
write into the next prompt — or into the context file, so you never specify them
again.

Contrast with what a bare "implement the model" prompt does: something
impressive-looking with choices you never made, and no list.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- A feature is one thing you can check. Work the plan one feature per session, with a small diff and one pull request.
- Underspecified prompts get average-case answers; your data and your research are rarely the average case. The failure mode is plausible-but-wrong.
- Context engineering sets the standing rules (context file, standards, plan); prompt engineering phrases the specific ask. Use both.
- Good prompts give evidence, ask for a diagnosis before a change, and specify inputs, output, "done when", and "do not touch".
- Maintenance tasks — refactors, docstrings, README audits, environment pins, merge summaries — are ideal agent work under the same small-specified-checkable rules.
- Always ask the agent to list the choices you didn't specify.

::::::::::::::::::::::::::::::::::::::::::::::::
