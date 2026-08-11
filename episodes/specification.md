---
title: "Underspecification and Feature-Driven Development"
teaching: 10
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- What actually happens when I give an agent a vague request?
- Why should I work feature by feature instead of asking for whole projects?
- What does a good prompt look like for research code?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Predict how an agent fills gaps in an underspecified request.
- Decompose project-sized goals into feature-sized, verifiable tasks.
- Write prompts that specify intent, constraints, and how to check the result.

::::::::::::::::::::::::::::::::::::::::::::::::

## Not a mind reader — but not a dice roll either

When your request is ambiguous, the agent doesn't fail and it doesn't guess randomly.
It does something more subtle and more dangerous: **it produces a good guess about the
average case**. It fills every gap in your specification with the most statistically
typical choice from its training data — the most common file layout, the default
hyperparameters, the standard preprocessing for data that looks like yours.

That's why underspecified requests so often produce code that *runs* and *looks
reasonable*: average-case answers usually do. The problem is that your research is
rarely the average case. Your data has that one weird instrument artifact. Your field
has a convention the average GitHub repo doesn't follow. Your "duplicate rows" are
actually repeated measures. Every unstated assumption gets resolved in favor of
someone else's typical project — silently.

Two consequences:

1. **Precision in, precision out.** The specification work you'd have to do for a
   colleague doesn't disappear; it moves into the prompt.
2. **The failure mode is plausible-but-wrong**, not obviously-broken. Which is why the
   next episode, on verification, is the heart of this lesson.

## Think in features, not projects

Agents work best on clear, well-scoped requests. "Build me a dashboard for my
experiment" forces the agent to invent dozens of decisions you never made. Instead,
work the way good software teams already do — **one feature at a time**:

- "Add a function `load_trials()` in `src/io.py` that reads every CSV in `data/raw/`,
  concatenates them, and raises `ValueError` if expected columns are missing."
- "Write a pytest fixture that builds a 20-row synthetic version of our trial data."
- "Refactor `process_data` in `pipeline.py` to handle input with missing columns."

Each is a single, verifiable step. Small scope also means small diffs — which means you
can actually review them, keeping you in the driver's seat. A vague project-sized
prompt doesn't just produce worse code; it produces a diff too large to meaningfully
review, at which point you've silently handed over the wheel.

## Anatomy of a better prompt

From the workshop slides — the same request at two levels of specification:

**Bad prompt:**

> Fix this spaghetti code.

**Better prompt:**

> Update this SQL to use CTEs and window functions to improve performance and
> legibility. Retain all existing in-line comments. Add comments to explain
> functionality for each step.

The better prompt names the *technique* (CTEs, window functions), the *goals*
(performance, legibility), and a *constraint* the agent could not have inferred (keep
the existing comments). Notice what "fix" would have left to the average case: the
agent would have to invent what "fixed" means.

A useful checklist for research-code prompts — specify:

- **Where**: which files/functions to touch (and, implicitly, which to leave alone).
- **What**: the behavior you want, including edge cases you know about.
- **Constraints**: conventions, dependencies allowed, things to preserve.
- **Verification**: how the agent should check its own work — "run the tests," "confirm
  the row count is unchanged," "print the class balance before and after."

That last item is the bridge to the next episode: a prompt that includes its own check
is worth two that don't.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise 2: Prompt engineering (10 minutes)

Start from this snippet in a fresh script or notebook:

```python
# 1. Import modules and dataset
import pandas as pd
from sklearn import datasets

cancer = datasets.load_breast_cancer()
```

1. Give your agent a deliberately **bad** prompt, e.g. "analyze this data" or "build a
   model."
2. In a fresh session (`/clear` in Claude Code, a new chat in Copilot — you'll see why
   in the cost episode), give a **better** prompt. Specify the target and features, the split, the model family, the
   metric, and at least one verification step, e.g.:

   > Using the already-loaded `cancer` dataset, build a train/test split (80/20,
   > stratified, random_state=42), fit a logistic regression on standardized features,
   > and report test-set accuracy and a confusion matrix. Before modeling, print class
   > balance and check for missing values. Don't add other models or plots.

3. Compare: What decisions did the bad-prompt run make for you without telling you?
   Did it hold out a test set at all? Did it look at the data before modeling?

:::::::::::::::::::::::: solution

## What people typically observe

The bad prompt usually yields *something impressive-looking* — often a full modeling
pipeline with choices you never made: an arbitrary model, no stratification, maybe no
held-out evaluation, rarely any actual data exploration. It's not wrong so much as
*unaccountable*: you can't defend any of its decisions because you didn't make them.

The better prompt yields less code doing exactly what you asked, plus the printed
checks that let you believe it. The difference isn't intelligence — it's that you did
the thinking that can't be delegated.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Underspecified prompts get average-case answers; your data and your research are rarely the average case.
- The failure mode is plausible-but-wrong code, which is far more dangerous than broken code.
- Work feature by feature: small, well-specified tasks produce reviewable diffs and keep you in the driver's seat.
- Good prompts specify where, what, constraints, and — most importantly — how to verify the result.

::::::::::::::::::::::::::::::::::::::::::::::::
