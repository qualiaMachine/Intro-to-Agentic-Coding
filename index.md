---
site: sandpaper::sandpaper_site
---

AI coding agents — tools that can read your repository, run commands, edit multiple
files, and iterate on their own output — are rapidly changing how research software gets
built. They make it dramatically easier to iterate and faster to see results. They also
make it faster to be misled if you aren't careful.

This lesson teaches the working principles behind effective, safe agentic coding for
researchers. It is deliberately about **principles, not one tool**: the practices —
scoping, secrets hygiene, specification, verification, documentation, cost awareness —
apply unchanged across Claude Code, GitHub Copilot, Cursor, OpenCode, and whatever
ships next month. Where the mechanics genuinely differ, episodes show side-by-side
equivalents for two tools researchers most commonly have access to (Claude Code and
GitHub Copilot); if you use something else, everything translates readily.

Four ideas run through the whole lesson:

1. **Stay in the driver's seat.** The agent is a very fast, very confident collaborator —
   not a replacement for your judgment. You choose the direction, you review the work,
   you decide what lands on `main`.
2. **Work feature by feature, not project by project.** Agents excel at well-scoped,
   well-specified tasks. Underspecified prompts don't produce random code — they produce
   *plausible average-case* code, and your data is rarely the average case.
3. **Assume nothing; verify everything.** There is no escaping good data science practice.
   You still need to explore your data, find the outliers, know your features and their
   distributions, and know what your models are actually telling you. Code that runs
   clean and scores great can still be wrong.
4. **Iteration is cheaper now — in both directions.** Agents compress the loop between
   idea and result. That accelerates good practice and bad practice alike, so the
   discipline matters *more*, not less.

::::::::::::::::::::::::::::::::::::::::::  prereq

## Prerequisites

- Comfort working at a command line and with git basics (clone, branch, commit, push).
- Some experience writing Python and doing basic data analysis (pandas, scikit-learn or
  similar).
- Access to at least one agentic coding tool — see the [setup page](learners/setup.md)
  for options, including free tiers.

::::::::::::::::::::::::::::::::::::::::::::::::::
