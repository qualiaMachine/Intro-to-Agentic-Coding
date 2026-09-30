---
site: sandpaper::sandpaper_site
---

AI coding agents are tools that can read a repository, run commands, edit multiple
files, and revise their own output. They are changing how research software is
written. They shorten the time between an idea and a result, and they shorten the time
between a mistake and a misleading result by the same amount.

This lesson covers the working principles behind effective and safe agentic coding for
researchers. It is about principles rather than one product: the practices of limiting
access, planning, specifying, verifying, and managing cost apply unchanged across
Claude Code, GitHub Copilot, Codex, Cursor, OpenCode, and their successors, so the
main text is tool-agnostic. Where the mechanics differ (a command name, a mode
toggle, a settings page), episodes give the equivalents for the two tools researchers
most commonly have access to, Claude Code and GitHub Copilot. Other tools map
one-to-one onto the same concepts.

Three principles run through the lesson:

1. **Stay in the driver's seat.** The agent writes the code. You review it, and you
   decide what is merged to `main`.
2. **Work feature by feature, not project by project.** A feature is one thing you
   can check. An underspecified prompt does not produce random code; it produces the
   statistically typical code for the average project, and research data is rarely
   the average case.
3. **Assume nothing; verify everything.** Rely on test-driven development. Good data science practice
   still applies in full: examine the data, know the distributions, and know what the
   model is responding to. Code that runs without error and scores well can still be
   wrong.

This lesson was piloted at the [ML Marathon](https://ml-marathon.wisc.edu/) at
UW–Madison. Taught in full, with all exercises, it takes about 3.5 to 4 hours; a
two-hour version covers the main points and leaves some exercises as homework. The
[instructor notes](instructors/instructor-notes.md) give both schedules.

::::::::::::::::::::::::::::::::::::::::::  callout

## Citing this lesson

Endemann, C., Reuter, T., and Mann, T. (2026). *Introduction to Agentic Coding*
(alpha). The Carpentries Incubator.
<https://qualiamachine.github.io/Intro-to-Agentic-Coding/>

The [citation page](citation.html) has this in other formats, generated from the
repository's `CITATION.cff`. The lesson is licensed CC-BY 4.0; reuse and adaptation
are welcome with attribution.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::  prereq

## Prerequisites

- Comfort working at a command line and with git basics (clone, branch, commit, push).
- Some experience writing Python and doing basic data analysis (pandas, scikit-learn or
  similar). No local Python installation is needed; the agent's sandbox runs the code.
- Access to at least one agentic coding tool. The [setup page](learners/setup.md)
  lists options, including free tiers.
- Ideally, a small project of your own to point the agent at. The exercises work on
  your repository; a fallback starter is provided where it matters.

::::::::::::::::::::::::::::::::::::::::::::::::
