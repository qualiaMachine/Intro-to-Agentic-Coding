---
title: "Documentation: Notes to Your Future Self (and Your Agent)"
teaching: 8
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- Why is documentation one of the best uses of agentic coding?
- How does documentation feed back into agent performance?
- Can asking an agent to explain code actually help verify it?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use an agent to produce and maintain documentation: docstrings, comments, READMEs, and narrated notebooks.
- Explain how documentation doubles as persistent context that improves future agent (and human) sessions.
- Use "explain this code" as a verification technique, treating doc/code mismatches as bug reports.
- Review generated documentation with the same skepticism as generated code.

::::::::::::::::::::::::::::::::::::::::::::::::

## The chore that stopped being a chore

Research code is famously under-documented, and the reason was never that anyone
doubted documentation's value. It was cost: after the analysis finally works, writing
up docstrings and updating the README is exactly the tedious, low-glamour work that
loses to the next experiment. Agents change that economics completely — documentation
is the task they are *best* suited to, because the source of truth (the code) is right
there in context, and because you can review a paragraph of English far faster than
you can review an implementation.

Make it a habit to ask for documentation as part of every task, or as a cleanup pass:

- **Docstrings**: "Add NumPy-style docstrings to every public function in `src/io.py`,
  including parameter types and the exceptions raised."
- **Comments where they matter**: "Add comments explaining *why* the outlier threshold
  is 3.5 here" — not line-by-line narration of *what* the code does.
- **READMEs for your future self**: "Update the README: how to set up the environment,
  run the pipeline end to end, and where outputs land. Note the raw data is read-only."
- **Narrated notebooks**: "Add a markdown cell before each code cell explaining what it
  does and why, at a level a new lab member could follow."
- **Session notes**: at the end of a work session, "summarize what we changed, what's
  still broken, and where to pick up" — pasted into the README, a `NOTES.md`, or your
  lab notebook. Your future self is a stranger who will thank you.

## Documentation is context — it compounds

Here is what makes this more than good hygiene: **everything you document becomes
context the agent reads back in later sessions.** Remember the planning episode — agents
recover *what* and *how* from code, but not *why*, *for whom*, or *what the data
means*. Documentation is precisely where the "why" gets written down:

- A good README means next month's session starts with the agent already knowing how
  to run your tests, instead of guessing.
- Docstrings carry intent ("assumes input is sorted by timestamp") that stops the
  agent from "fixing" deliberate behavior.
- A data dictionary — column meanings, units, known quirks — is the difference between
  an agent that treats `-999` as a measurement and one that knows it's your missing
  code.

In other words, documentation gives LLMs useful added context that measurably improves
what they produce — the same way it helps a new collaborator. Time spent documenting
is not a tax on this workflow; it's an investment that pays out on every future
session, human or agent.

## Explaining as verification

There's a second, subtler payoff: **asking an agent to explain or document code is a
verification act.** To write an accurate docstring, the model has to actually process
what the code does — and mismatches between the explanation and your intent surface
real problems:

- Ask for a plain-English explanation of a pipeline you just built (or inherited). If
  the explanation *surprises* you — "it then drops rows with missing labels before the
  split" — you may have just found a bug, or at least an undocumented decision.
- Ask the agent to document a function's edge-case behavior. "Returns 0 when the input
  is empty" is either correct and worth writing down, or incorrect and worth fixing —
  both outcomes are wins.
- In a narrated notebook, a markdown cell that mis-describes its code cell is a red
  flag for *you* — and, left uncorrected, a trap for the next reader. Fix one or the
  other; never leave them disagreeing.

This is the rubber-duck effect with a duck that talks back. It doesn't replace the
tests and checks from the previous episode — an explanation can be fluent and wrong —
but it's a cheap extra verification layer, and it produces a durable artifact while
verifying.

::::::::::::::::::::::::::::::::::::: callout

## Review docs like code — stale docs are worse than none

Generated documentation inherits the plausible-but-wrong failure mode: it reads
confident, and it can be confidently mistaken. Read it before committing. And keep it
current — documentation that contradicts the code misleads humans *and* poisons agent
context, because agents trust what they read. When behavior changes, updating the
docs is part of the change, not an optional follow-up. ("Update the docstring and
README to match" is a fine thing to put in the same prompt as the change itself.)

And don't rely on change-by-change discipline alone — **periodically run a full
audit**:

> Go through the README, every docstring, and the comments, and verify each claim
> against what the code actually does. Make no assumptions — read the code. List
> every mismatch you find.

It's a cheap sweep (end of the week, before a release, before sharing the repo) that
catches the drift that slips past you one edit at a time — and every mismatch it
surfaces is either a doc fix or a bug found.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Document and cross-examine (5 minutes)

Pick a function or notebook cell you (or an agent) wrote earlier today — or any
undocumented piece of your own code.

1. Ask the agent: "Write a docstring for this function, including behavior on edge
   cases (empty input, missing values). Then explain in two sentences what this
   function does and why it might exist."
2. Read the result critically. Does the described behavior match your intent? Did it
   claim an edge-case behavior you never decided on?
3. If you find a mismatch, treat it as a bug report: fix the code or fix the doc, and
   say which one you chose and why.

:::::::::::::::::::::::: solution

## What people typically find

Most participants find at least one surprise — usually an edge case the code handles
by accident rather than by decision (what *does* it return for an empty DataFrame?).
That's the point: the docstring forced a decision that writing the code never did.
And whichever way you resolve it, you leave behind both a checked behavior and a
written record of it — verification and documentation in one pass.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Documentation is one of the best uses of agentic coding: the agent has the source of truth in context, and English is faster to review than code.
- Ask for docstrings, why-comments, README updates, narrated notebooks, and end-of-session notes as a routine part of every task.
- Documentation compounds: it becomes the context that makes future agent sessions (and future you) measurably better.
- Explaining is verifying — a doc/code mismatch is a bug report; a surprising explanation is a lead worth chasing.
- Review generated docs like code, and update them with the code: stale documentation misleads humans and poisons agent context. Periodically ask the agent to audit every doc claim against the actual code — no assumptions.

::::::::::::::::::::::::::::::::::::::::::::::::
