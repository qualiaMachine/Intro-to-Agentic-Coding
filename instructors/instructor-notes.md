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
| 0:15 | 12 | Words of caution: security, secrets, policies, trust | Episodes 2–3 |
| 0:27 | 8 | Exercise 1: first look at a repo (plan mode, read-only) | Episode 4 |
| 0:35 | 8 | Debrief: what it couldn't infer; context files; autonomy comparison | Episode 4 |
| 0:43 | 10 | Underspecification & feature-driven development | Episode 5 |
| 0:53 | 10 | Exercise 2: bad vs. better prompt | Episode 5 |
| 1:03 | 5 | Break | — |
| 1:08 | 20 | Verification and review; leakage worked example | Episode 6 |
| 1:28 | 10 | Exercise 3: test as contract | Episode 6 |
| 1:38 | 8 | What the research shows | Episode 10 |
| 1:46 | 6 | Cost + energy; Exercise 4 (`/cost`, napkin math) | Episode 9 |
| 1:52 | 8 | Close: is programming dead?; three things before the sprint | Episode 10 |

Note the live schedule runs research-findings *before* the cost block; the written
episodes order cost before research/outlook because it reads better asynchronously.
Either order works.

**Episode 7 (Documentation) in the 2-hour format:** like the trust episode, this has
no dedicated live slot — it exists in full for asynchronous study. In the workshop,
land its two headline ideas inside the verification block or the close: (1) agents
make documentation cheap, so ask for docstrings/README updates/narrated notebooks with
every task, and (2) documentation is context the agent reads back later, so it
compounds — and "explain this code" doubles as a verification pass. Its 5-minute
document-and-cross-examine exercise makes a good at-home assignment alongside the
trust episode's provider-vetting exercise.

**Episode 8 (Common Workflows) in the 2-hour format:** async-only material. If time
allows, its highest-value live moment is naming the two review postures (agent commits
freely, PR is the review gate vs. review every change) during the verification block
or close, and noting that the choice should be deliberate and written into the project
context file.

**Episode 3 (Trust) in the 2-hour format:** there is no dedicated slot for the trust
episode in the live schedule — it exists in full for asynchronous study. In the
workshop, compress it into the words-of-caution block: name two or three of the real
incidents (the Replit production-database deletion and the hallucinated
`huggingface-cli` package land especially well), state the two rules that follow
(never auto-approve installs; vet your provider's data policy), and point to the
episode for the rest. Its 5-minute "vet your own tool" exercise also works as an
at-home assignment announced during the close.

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
