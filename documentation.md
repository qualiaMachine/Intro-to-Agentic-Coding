---
title: "Documentation: Notes to Your Future Self (and Your Agent)"
teaching: 8
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- Why is documentation one of the better uses of agentic coding?
- How does documentation feed back into agent performance?
- Can asking an agent to explain code help verify it?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Use an agent to produce and maintain documentation: docstrings, comments, READMEs, and narrated notebooks.
- Explain how documentation serves as persistent context that improves later agent (and human) sessions.
- Use "explain this code" as a verification technique, treating mismatches between documentation and code as bug reports.
- Review generated documentation with the same care as generated code.

::::::::::::::::::::::::::::::::::::::::::::::::

## Why documentation suits agents

The feature-based-development episode listed docstrings, README audits, and
environment pins among the maintenance tasks agents do well. This episode, intended
for reading after the workshop, explains why documentation deserves more attention
than that.

Research code is under-documented, and the reason was never doubt about the value of
documentation. It was cost. Once an analysis works, writing docstrings and updating
the README is the low-priority task that loses to the next experiment. Agents change
this. Documentation is the task they are best suited to, because the source of truth
(the code) is in context, and because a paragraph of prose is faster to review than
an implementation.

Request documentation as part of each task, or as a separate pass:

- **Docstrings**: "Add NumPy-style docstrings to every public function in
  `src/io.py`, including parameter types and the exceptions raised."
- **Comments where they matter**: "Add comments explaining why the outlier threshold
  is 3.5 here." Not line-by-line narration of what the code does.
- **READMEs**: "Update the README: how to set up the environment, run the pipeline
  end to end, and where outputs are written. Note that the raw data is read-only."
- **Narrated notebooks**: "Add a markdown cell before each code cell explaining what
  it does and why, at a level a new group member could follow."
- **Session notes**: at the end of a working session, "summarize what we changed,
  what is still broken, and where to resume," saved to the README, a `NOTES.md`, or
  a lab notebook.

## Documentation is context

Everything you document becomes context the agent reads in later sessions. As the
planning episode explained, agents recover *what* and *how* from code but not *why*,
*for whom*, or *what the data means*. Documentation is where those are recorded:

- A good README means the next session begins with the agent already knowing how to
  run the tests, rather than guessing.
- Docstrings carry intent ("assumes input is sorted by timestamp") that stops the
  agent from "fixing" deliberate behavior.
- A data dictionary (column meanings, units, known quirks) is the difference between
  an agent that treats `-999` as a measurement and one that knows it is the missing
  value code.

Documentation therefore improves what the model produces, in the same way it helps a
new collaborator. Time spent documenting is repaid in every later session, whether
the reader is a person or an agent.

## Explanation as verification

Asking an agent to explain or document code is also a check on the code. To write an
accurate docstring the model has to process what the code does, and mismatches
between its explanation and your intent point to problems:

- Ask for a plain-language explanation of a pipeline you built or inherited. If the
  explanation surprises you ("it then drops rows with missing labels before the
  split"), you may have found a bug or an undocumented decision.
- Ask the agent to document a function's behavior on edge cases. "Returns 0 when the
  input is empty" is either correct and worth recording, or incorrect and worth
  fixing.
- In a narrated notebook, a markdown cell that misdescribes its code cell is a
  warning to you and, if left, a trap for the next reader. Correct one or the other;
  never leave them in disagreement.

This does not replace the tests and checks in the verification episode. An
explanation can be fluent and wrong. But it is an inexpensive additional check that
produces a durable artifact as a by-product.

::::::::::::::::::::::::::::::::::::: callout

## Review documentation as code; stale documentation is worse than none

Generated documentation has the same failure mode as generated code: it reads as
confident and can be confidently wrong. Read it before committing. Keep it current:
documentation that contradicts the code misleads people and corrupts agent context,
because agents trust what they read. When behavior changes, updating the
documentation is part of the change. "Update the docstring and README to match" can
go in the same prompt as the change itself.

Do not rely on change-by-change discipline alone. Periodically run a full audit:

> Go through the README, every docstring, and the comments, and verify each claim
> against what the code does. Make no assumptions — read the code. List every
> mismatch you find.

This is inexpensive (end of week, before a release, before sharing the repository)
and catches the drift that accumulates one edit at a time. Every mismatch it finds
is either a documentation fix or a bug found.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Document and cross-examine (5 minutes)

Choose a function or notebook cell you or an agent wrote today, or any undocumented
piece of your own code.

1. Ask the agent: "Write a docstring for this function, including behavior on edge
   cases (empty input, missing values). Then explain in two sentences what this
   function does and why it might exist."
2. Read the result critically. Does the described behavior match your intent? Did it
   assert an edge-case behavior you never decided on?
3. If you find a mismatch, treat it as a bug report: fix the code or fix the
   documentation, and state which you chose and why.

:::::::::::::::::::::::: solution

## Typical findings

Most participants find at least one surprise, usually an edge case the code handles
by accident rather than by decision (what does it return for an empty DataFrame?).
The docstring forced a decision that writing the code never did. Either way of
resolving it leaves both a checked behavior and a written record of it.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Documentation is one of the better uses of agentic coding: the source of truth is in context, and prose is faster to review than code.
- Ask for docstrings, comments explaining why, README updates, narrated notebooks, and end-of-session notes as part of routine work.
- Documentation compounds: it becomes the context that improves later agent sessions and helps your future self.
- Explaining is verifying. A mismatch between documentation and code is a bug report; a surprising explanation is a lead.
- Review generated documentation as you would code, and update it with the code. Periodically have the agent audit every documented claim against the code.

::::::::::::::::::::::::::::::::::::::::::::::::
