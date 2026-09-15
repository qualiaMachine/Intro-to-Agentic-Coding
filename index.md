---
site: sandpaper::sandpaper_site
---

AI coding agents — tools that can read your repository, run commands, edit multiple
files, and iterate on their own output — are rapidly changing how research software gets
built. They make it dramatically easier to iterate and faster to see results. They also
make it faster to be misled if you aren't careful.

This lesson teaches the working principles behind effective, safe agentic coding for
researchers. It is deliberately about **principles, not one tool**: the practices —
limiting access, planning, specifying, verifying, managing cost — apply unchanged
across Claude Code, GitHub Copilot, Codex, Cursor, OpenCode, and whatever ships next
month. Where the mechanics genuinely differ, episodes show side-by-side equivalents for
two tools researchers most commonly have access to (Claude Code and GitHub Copilot); if
you use something else, everything translates readily.

Three core principles run through the whole lesson:

1. **Stay in the driver's seat.** The agent types; you review, and you decide what
   lands on `main`. The suit multiplies what the pilot can do, but the pilot is still
   the one steering.
2. **Work feature by feature, not project by project.** A feature is one thing you
   can check. Underspecified prompts don't produce random code — they produce
   *plausible average-case* code, and your data is rarely the average case.
3. **Assume nothing; verify everything.** Lean on tests. There is no escaping good
   data science practice: explore your data, know your distributions, know what your
   models are actually telling you. Code that runs clean and scores great can still be
   wrong — and iteration is cheaper now in *both* directions, so the discipline
   matters more, not less.

The lesson grew out of a two-hour workshop and keeps that shape: the live workshop
is the highlights reel, and the full episodes here are the reference that stays
online. The [instructor notes](instructors/instructor-notes.md) map the workshop
blocks onto episodes.

::::::::::::::::::::::::::::::::::::::::::  prereq

## Prerequisites

- Comfort working at a command line and with git basics (clone, branch, commit, push).
- Some experience writing Python and doing basic data analysis (pandas, scikit-learn or
  similar).
- Access to at least one agentic coding tool — see the [setup page](learners/setup.md)
  for options, including free tiers.
- Ideally, a small project of your own to point the agent at. The exercises work on
  your repository; a fallback starter is provided where it matters.

::::::::::::::::::::::::::::::::::::::::::::::::
