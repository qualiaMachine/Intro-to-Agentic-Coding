---
title: 'Instructor Notes'
---

## Origin and format

This lesson began as a 2-hour evening workshop ("Agentic Coding Best Practices," ML
Marathon 2026, UW–Madison, developed by Tracy Reuter, Tejvir Mann, Chris Endemann, and
Zain Waseem). The episodes expand the workshop blocks so participants can study the
material asynchronously; the workshop schedule below maps blocks to episodes.

## Suggested 2-hour schedule

| Time | Min | Block | Episode |
|------|-----|-------|---------|
| 0:00 | 10 | Arrival/food; helpers confirm everyone's agent access works | — |
| 0:10 | 5 | What "agentic" means; tooling landscape | Episode 1 |
| 0:15 | 12 | Words of caution: security, secrets, policies | Episode 2 |
| 0:27 | 8 | Exercise 1: recon (plan mode, read-only) | Episode 3 |
| 0:35 | 8 | Debrief: what it couldn't infer; context files; autonomy comparison | Episode 3 |
| 0:43 | 10 | Underspecification & feature-driven development | Episode 4 |
| 0:53 | 10 | Exercise 2: bad vs. better prompt | Episode 4 |
| 1:03 | 5 | Break | — |
| 1:08 | 20 | Verification and review; leakage worked example | Episode 5 |
| 1:28 | 10 | Exercise 3: test as contract | Episode 5 |
| 1:38 | 8 | What the research shows | Episode 7 |
| 1:46 | 6 | Cost + energy; Exercise 4 (`/cost`, napkin math) | Episode 6 |
| 1:52 | 8 | Close: is programming dead?; three things before the sprint | Episode 7 |

Note the live schedule runs research-findings *before* the cost block; the written
episodes order cost before research/outlook because it reads better asynchronously.
Either order works.

## Logistics that matter

- **Agent access is the #1 failure mode.** Have helpers confirm during arrival that
  every participant can start a session in *some* tool. Provide a fallback (e.g., cloud
  credits, OpenCode with free models, or pairing participants).
- **Exercise 1 needs an unfamiliar repo.** Pick one practice repository in advance so
  the debrief has common ground — ideally a small research project with some
  undocumented quirks the agent will confidently gloss over.
- **Exercise 2 works best with a visible contrast.** Ask 2–3 participants to share what
  their bad prompt produced; the room reliably discovers that everyone got *different*
  unaccountable pipelines.
- **The leakage example is the emotional core of the lesson.** Don't rush it. Let the
  clean run and high score land first, then ask "so are we done?" before revealing the
  bug.
- **Timebox Exercise 3 firmly** — writing a test from scratch can sprawl. Offer the
  provided leakage test as a starting point for anyone stalled at the 4-minute mark.

## Teaching tips

- Keep the emphasis on principles over tools. When a participant uses a different tool,
  translate rather than troubleshoot ("what's the plan-mode equivalent in yours?").
- Recurring motifs worth calling back to explicitly: *stay in the driver's seat*,
  *plausible-but-wrong beats broken as the dangerous failure mode*, *autonomy is
  purchased with verification*, and *vague prompts cost quality, money, and energy —
  the same discipline pays three times*.
- Participants who are experienced ML practitioners sometimes bristle at the "no
  escaping good data science" framing as obvious. Agree with them — then point out the
  METR result: experienced developers *felt* faster while being slower. Obvious
  discipline is exactly what erodes under speed.
