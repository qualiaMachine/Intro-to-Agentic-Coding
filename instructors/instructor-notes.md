---
title: 'Instructor Notes'
---

## Origin and format

This lesson began as a 2-hour evening workshop ("Agentic Coding: (Developing) Best
Practices," ML Marathon 2026, UW–Madison, developed by Tracy Reuter, Tejvir Mann,
Chris Endemann, and Zain Waseem). The first eight episodes follow the workshop's
blocks in order; the last three (documentation, common workflows, research and
outlook) are asynchronous reading, with the outlook's headline landing in the close.

Say up front: **the deck is the highlights reel.** The full lesson is online and stays
online, so nobody needs to take notes on the details.

## Suggested 2-hour schedule

Two hours, four short exercises plus two demos, one break. Everything runs on the
participants' own repositories where possible.

| Time | Min | Block | Episode |
|------|-----|-------|---------|
| 0:00 | 30 | **Intro & getting started (safely).** Three principles; what agentic coding is (spectrum, harness, loop); live demo at three autonomy levels; safety: policies, the six limits, prompt injection, version control, providers; **Exercise: Get your agent running** (8 min) | Episodes 1–2 (3 compressed) |
| 0:30 | 15 | **Planning with agents.** Research on planning; add context; MVP; **Exercise: Plan your MVP with an agent** (10 min) | Episode 4 |
| 0:45 | 10 | **Feature-based dev and good prompting.** Feature by feature; bad/better prompt; underspecified ≠ random; maintenance tasks | Episode 5 |
| 0:55 | 8 | Break | — |
| 1:03 | 20 | **Exercise: Implement feature 1** (15 min) then debrief on "choices you did not specify" — or run it before the break if the room is fast | Episode 5 |
| 1:23 | 20 | **Verification and testing.** Research on checking; no escaping good data science; cheap checks; **Exercise: What is wrong with this?** (5 min); hunt for decisions; agents as data science assistants; **Exercise: Now your repo** (10 min) | Episode 6 |
| 1:43 | 12 | **MCP tools and skills.** MCP vs API; **Demo: connect an MCP server** (5 min); what a skill is; **Demo: caveman skill** (4–5 min); resources | Episode 7 |
| 1:55 | 5 | **Cost, energy, and wrap-up.** Energy numbers; token techniques with `/cost`, `/model`, `/compact` demos; is programming dead?; feedback survey | Episodes 8, 11 |

The live agenda is tight. If you are running behind, the feature-1 exercise can be
shortened to 10 minutes (stop at "read the diff"), and the MCP connect can become a
narrated demo from the instructor's screen rather than a hands-on.

## Block-by-block notes

**Intro.** Callback to the mech suit from kickoff: the suit multiplies what the pilot
can do, but the pilot is still steering — that's the driver's-seat principle. Ask
"anyone want to share something impressive their agent did?" to warm the room. For
the demo, use Claude Code in VS Code (or OpenCode) on the project the rest of the
workshop returns to: a tightly directed task, a plan-then-implement task, and an
*explained but not run* multi-agent workflow. Point out the setup page has free
routes (Copilot education tier, OpenCode) for anyone whose credits didn't work.

**Safety.** Signpost the six limits, in order, and say that an instruction file
*asks* while everything else *removes the ability*. The PocketOS and Cursor CVE
stories land the "instructions vs. permissions" distinction; the Nx incident lands
prompt injection. The 1Password CLI slides are worth showing live if your institution
provides it. For **Get your agent running**: helpers circulate; the failure to watch
for is a desktop app in local mode. Team repos: primary owner makes a
`<username>-main` branch, everyone else forks.

**Trust (Episode 3) has no dedicated slot.** Its headline content — vet the provider
(the Claude/Copilot defaults table), and model weights are code — is the sixth limit
in the safety block. Name two or three incidents (the fake OpenAI repo at #1 trending,
the hallucinated `huggingface-cli` package, Replit) and point to the episode. Its
provider-vetting exercise is a good at-home assignment.

**Planning.** Acknowledge levels of planning: it's iterative, and a three-line plan is
fine for a three-line task. Have the team MVP plans open (the shared doc from kickoff
if you have one). The deliverable is a committed `plan.md` — no code until the plan
is in. Note the planning studies measured accuracy, not tokens; the token argument is
a mechanism, not a measured result.

**Feature-based dev.** The "list every choice you made that I did not specify" line
is the hook — ask two or three people to read theirs out. The room reliably discovers
that everyone got *different* unaccounted decisions.

**Verification.** The brain-decoding leak is the emotional core of the lesson. Let
the clean run and 0.91 land first, then ask "so are we done?" before revealing the
bug, then show the 0.58 on unseen subjects. Translate "the unit that repeats" to each
team's project (subject, camera burst, page, source document). For **Now your repo**,
insist on plan mode for step 1 and timebox firmly; the CI workflow and branch
protection can be finished after the session.

**MCP and skills.** Pre-test the MCP server and the caveman install beforehand so
auth and npm aren't what the room watches. Run `claude mcp list` before and after.
For the caveman demo, ask the same question before and after `/caveman`, and `cat`
the state file to prove it's toggled. Note for VS Code extension users: the same two
install commands work; reload the chat panel afterward.

**Cost and energy.** Name the claim people arrive with (a prompt costs gallons of
water) and replace it with a number. Be honest about the spread (Couch ~41 Wh,
Hausfather ~600 Wh). Three live demos in order: `/cost`, `/model`, `/compact`; then
pull up the OpenRouter session-cost rankings. Loop back to skills as a cost lever.

**Close.** Is programming dead? The evidence says no — coding speed is one bottleneck,
and the Anthropic skill-formation result (17% lower, biggest gap in debugging) is the
one to leave people with: use the agent to ask *why*. Feedback survey, materials link,
and ask people to send resources they find useful.

## Logistics that matter

- **Agent access is the #1 failure mode.** Have helpers confirm during arrival that
  every participant can start a cloud session in *some* tool. Provide a fallback
  (cloud credits, OpenCode with free models, or pairing participants).
- **Participants need a repository.** The exercises assume a project repo (or fork).
  Have a small starter repo ready for anyone without one.
- **Pre-run every demo** — the MCP connection, the caveman install, `/compact` on a
  long session — on the same network you'll present from.
- **Keys off disk.** If any exercise calls a hosted model API, show the `op read`
  pattern rather than handing out a `.env`.

## Teaching tips

- Keep the emphasis on principles over tools. When a participant uses a different tool,
  translate rather than troubleshoot ("what's the plan-mode equivalent in yours?").
- Recurring motifs worth calling back to explicitly: *stay in the driver's seat*,
  *instructions shape behavior, permissions constrain it*, *a feature is one thing you
  can check*, *plausible-but-wrong beats broken as the dangerous failure mode*,
  *autonomy is purchased with verification*, and *vague prompts cost quality, money,
  and energy — the same discipline pays three times*.
- Participants who are experienced ML practitioners sometimes bristle at the "no
  escaping good data science" framing as obvious. Agree with them — then point out the
  METR result: experienced developers *felt* faster while being slower. Obvious
  discipline is exactly what erodes under speed.
