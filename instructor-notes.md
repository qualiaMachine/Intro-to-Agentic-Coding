---
title: 'Instructor Notes'
---

## Origin and format

This lesson began as a 2-hour evening workshop ("Agentic Coding: (Developing) Best
Practices," ML Marathon 2026, UW–Madison, developed by Chris Endemann, Tracy Reuter,
and Tejvir Mann; Zekai Otles contributed the dev container setup). The first eight
episodes follow the workshop's blocks in order; the ninth, research and outlook, is
the close.

Say at the start that **the slides cover the main points only.** The full lesson is online and stays
online, so nobody needs to take notes on the details.

## Suggested 2-hour schedule

Two hours, five short exercises plus two demos, one break. Everything runs on the
participants' own repositories where possible. The 2026 pilot split blocks among the
presenters (Chris: intro, trust, getting started, close; Tejvir: what agentic coding
is, planning; Tracy: safety, prompting), which is a workable division for any team of
three.

| Time | Min | Block | Episode |
|------|-----|-------|---------|
| 0:00 | 30 | **Intro & getting started (safely).** Before we start (any access requests participants must file now); three principles; what agentic coding is (spectrum, harness, loop); safety: policies, prompt injection, the six limits (network allowlist demo, 2 min), providers, recap; **Exercise: Get your agent running, safely** (8 min) | Episodes 1–2 (3 compressed) |
| 0:30 | 15 | **Planning with agents.** Research on planning; add context; **Exercise: Agree how your team will work together** (10 min); MVP; **Exercise: Plan your MVP with an agent** (15 min) — this block overruns its slot in the pilot agenda; see below | Episode 4 |
| 0:45 | 10 | **Feature-based dev and good prompting.** The agent is not a magic wand; feature by feature; bad/better prompt; underspecified ≠ random | Episode 5 |
| 0:55 | 8 | Break | — |
| 1:03 | 20 | **Exercise: Implement feature (or step) 1** (15 min) then debrief on "choices you did not specify"; maintenance tasks slide as the transition | Episode 5 |
| 1:23 | 20 | **Verification and testing.** Research on checking; look for decisions you did not make; **Exercise 1: Test the feature you just built** (10 min); good data science practice still applies; tests for good data science practice; agents as data scientists | Episode 6 |
| 1:43 | 12 | **MCP tools and skills.** MCP vs API; **Demo: connect an MCP server** (5 min); what a skill is; **Demo: caveman skill** (4–5 min); resources | Episode 7 |
| 1:55 | 5 | **Cost, energy, and wrap-up.** Energy numbers; token techniques with `/cost`, `/model`, `/compact` demos; is programming dead?; feedback survey | Episodes 8, 11 |

The live agenda is tight — the pilot agenda gave planning 15 minutes but its two
exercises alone total 25. Options: run the team-conventions exercise as homework
announced at the start (teams commit `CONTRIBUTING.md` before the next session), cap
the MVP exercise at 10 minutes and make the `prep.md` follow-up homework, shorten the
feature-1 exercise to 10 minutes (stop at "read the diff"), or turn the MCP connect
into a narrated demo from the instructor's screen rather than a hands-on.

## Block-by-block notes

**Before we start.** If participants need access to a campus-hosted model or
compute (the pilot used BadgerBrain, UW–Madison's hosted open-weight models), put
the request link on the first slide: approvals take days, so file tonight to have it
for the next working session. Announce the next working session (time, place, who
will be there) and that participants should bring what they build tonight.

**Intro.** Callback to the mech suit from kickoff: the suit multiplies what the pilot
can do, but the pilot is still steering, which is the driver's-seat principle. Ask
"anyone want to share something impressive their agent did?" as an opener. Point
out the setup page has free routes (Copilot education tier, OpenCode) for anyone
whose credits didn't work.

**Safety.** Prompt injection first (the Nx incident makes it concrete), then signpost the
six limits in order — "injection was the threat; these six cap what it can do" — and
say that an instruction file *asks* while everything else *removes the ability*. The
PocketOS and Cursor CVE incidents illustrate the "instructions vs. permissions" distinction.
The network-allowlist demo is two minutes in the browser: edit a Claude Code cloud
environment and show the four Network access levels (None / Trusted / Full / Custom
with its Allowed domains list), then a repo's Settings → Copilot → Cloud agent →
Internet access. Note that the claude.ai *capabilities* page's network-egress setting
is for chat and Cowork code execution, not Claude Code environments, and that the
Copilot page is visible only to repository admins on a paid plan. The point to make
while clicking is that a blocked request is fixed by adding the host, not by switching
the firewall off. The
1Password CLI slides are worth showing live if your institution provides it; the
JupyterLab detail can be skimmed if time is short. For **Get your agent running,
safely**: helpers circulate; the
failure to watch for is a desktop app in local mode. Copilot's app has an explicit
plan mode, which is clearer to teach; on the Copilot web, planning is done via the
prompt and gives the same approve-or-exit gate with no toggle, so it is acceptable for
anyone who can't install. Team repos: one shared repo, everyone on a branch named for them,
branches not forks; anyone without write access gets added as a collaborator now.
Cloud sandboxes are usage-billed, so have people confirm their account works.

**Trust (Episode 3) has no dedicated slot.** Its headline content — vet the provider
(the Claude/Copilot defaults table), and model weights are code — is the sixth limit
in the safety block. Name two or three incidents (the fake OpenAI repo at #1 trending,
the hallucinated `huggingface-cli` package, Replit) and point to the episode. Its
provider-vetting exercise is a good at-home assignment.

**Planning.** Two exercises. *Agree how your team will work together* comes first:
decide branches or forks, let the agent draft `CONTRIBUTING.md` on a branch named for
the participant, cut it down to rules people will follow, merge it through a
teammate-reviewed pull request (the first use of the rules just written), and post
the link where advisors can see it. Agents open a pull request by default; point that
out when it happens.
Then MVP: acknowledge levels of planning — it's iterative, and a three-line plan is
fine for a three-line task. Have the team MVP plans open (the shared doc from kickoff
if you have one) and frame the MVP as the baseline you A/B new components against.
The deliverable is a committed `plan.md` — no code until the plan is in; teams that
finish early interrogate their pre-modeling steps into `prep.md`. Note the planning
studies measured accuracy, not tokens; the token argument is a mechanism, not a
measured result.

**Feature-based dev.** Open with "the agent is not a magic wand": the frustration
people arrive with comes from whole-project prompts, and the remedy is a domain
expert in the loop driving one feature at a time. The "list every choice you made
that I did not specify" line is the key step of the exercise: ask two or three people
to read theirs out. Participants reliably discover that everyone got *different*
unaccounted decisions.

**Verification.** Open with the research figures and Faros AI's explanation (larger
pull requests, code that reads well but is often wrong), then the pull request as the
final human check: it is where verification happens, and review by eye does not
scale, so the rest of the block supplies the tests and checks. Then the
before-and-after-every-feature routine: ask for assumptions, ask for tests and edge cases, run them,
commit. *Exercise 1: Test the feature you just built* applies it to feature 1 from
before the break; insist on plan mode for the first prompt, and timebox. The CI
workflow and branch protection can be completed after the session. Close the block
with the five test prompts for good data science practice and the agents-as-data-
scientists prompt. The brain-decoding leakage exercise was cut from the live workshop
for time; it remains in the episode as an optional exercise and works well as
homework, or as the example when a team's project has repeated units (subject, camera
burst, page, source document).

**MCP and skills.** Pre-test the MCP server and the caveman install beforehand so
auth and npm aren't what the room watches. Run `claude mcp list` before and after.
For the caveman demo, ask the same question before and after `/caveman`, and `cat`
the state file to prove it's toggled. Note for VS Code extension users: the same two
install commands work; reload the chat panel afterward.

**Cost and energy.** Name the claim people arrive with (a prompt costs gallons of
water) and replace it with a number. State the spread plainly (Couch ~41 Wh,
Hausfather ~600 Wh). Three live demos in order: `/cost`, `/model`, `/compact`; then
pull up the OpenRouter session-cost rankings. Loop back to skills as a cost lever.

**Close.** Put the question to the room first (discuss with a neighbor, then share)
before giving the answer: agentic coding is another abstraction layer, like assembly
to Python, but a non-deterministic one. The craft is making it deterministic enough
through specification and verification without spending more time prompting than
coding would take; at the feature level the gains are substantial, and they scale
with expertise. Agents amplify expertise; they are not a magic wand (a callback to
the feature-based block). The Anthropic skill-formation result (17% lower, biggest
gap in debugging) is the caution to leave people with: use the agent to ask *why*.
Feedback survey and materials link; note the lesson will keep changing through the
fall.

## Logistics that matter

- **Agent access is the #1 failure mode.** Have helpers confirm during arrival that
  every participant can start a cloud session in *some* tool. Provide a fallback
  (cloud credits, OpenCode with free models, or pairing participants).
- **Participants need a repository, with write access.** The exercises assume one
  shared project repo with everyone on their own branch. Have a small starter repo
  ready for anyone without one, and get collaborators added before the session.
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
