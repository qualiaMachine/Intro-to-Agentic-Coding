---
title: "What the Research Shows, and Where This Leaves Us"
teaching: 12
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- Who actually benefits from these tools, and on which kinds of work?
- Is programming dead?
- What should I do differently starting tomorrow?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Summarize what early research says about productivity effects and who gains most.
- Articulate why agentic coding is "another abstraction — but the first non-deterministic one."
- Commit to three concrete practices for your next project.

::::::::::::::::::::::::::::::::::::::::::::::::

## What the research shows (so far)

The evidence base is young and shifting, but a few findings recur:

- **Gains are real but uneven.** Early studies of AI *assistants* (autocomplete-style)
  found the largest gains for junior developers on routine tasks. For *agentic* work,
  the pattern appears to flip: experienced developers — who can specify precisely,
  review effectively, and catch plausible-but-wrong output — extract more value, while
  novices are more likely to accept flawed results. Verification skill, not typing
  speed, is the bottleneck.
- **Perceived speed and measured speed can diverge.** In one widely discussed 2025
  randomized trial (METR), experienced open-source developers *felt* about 20% faster
  with AI tools on their own mature repositories while actually being ~19% *slower*.
  Measure, don't vibe — the same rule we apply to model scores applies to our own
  productivity.
- **The skill-formation question is open.** If agents do the routine work, where do
  juniors build the architectural intuition seniors rely on to supervise agents? This
  worry appears across the literature and industry commentary, and it is a real concern
  for how we train researchers — deliberate practice may need to be scheduled where it
  used to happen for free.

The honest summary: these tools amplify expertise more than they replace it. Everything
in this lesson — scoping, specifying, verifying — is precisely the expertise being
amplified.

## Is programming dead?

Programming has survived its own death many times: assembly gave way to compilers,
manual memory management to garbage collection, servers to the cloud. Each time, the
work moved up a level of abstraction and the discipline adapted.

Agentic coding is another abstraction — **but the first non-deterministic one.** A
compiler translates your intent the same way every time; you never audit its output. An
agent interprets your intent probabilistically, filling gaps with the average case. The
same prompt can yield different code on different days. That is *why* this lesson's
discipline differs from what came before: you don't review a compiler's output, but you
absolutely review an agent's — because the abstraction itself can be plausibly,
silently wrong.

So: not dead. But the job shifts from writing every line toward specifying intent,
designing verification, and exercising judgment — which, conveniently, were always the
hard parts of research computing.

## Where this goes next

Two extension points worth knowing exist, even if you don't touch them this week:
**skills** (reusable, on-demand workflow instructions for the agent — a `/deploy`
checklist, your lab's analysis conventions) and **MCP servers** (connecting agents to
external systems: databases, lab notebooks, project trackers). The same principles
govern them: minimum access, maximum clarity, human judgment on what matters.

::::::::::::::::::::::::::::::::::::: challenge

## Three things before your next sprint

Before your next project work session, commit to:

1. **Set up the guardrails once.** Secrets into a keyring/secrets manager (nothing in
   plaintext on disk), a project context file (`CLAUDE.md` / `AGENTS.md` /
   `copilot-instructions.md`) under 100 lines, and a branch-only workflow.
2. **Write the contract first.** For the next feature you delegate, write one test or
   printed check that encodes what "correct" means for *your* data — before you prompt.
3. **Review one full diff like a paranoid person.** Take one agent-produced change and
   review it as if a stranger submitted it to your paper's supplementary code:
   explore the data it touches, check a number against a source of truth, and see what
   the model is really telling you.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Agentic tools amplify expertise; verification skill, not typing speed, is the bottleneck — and perceived speedups can be illusory, so measure.
- How novices build supervisory expertise in an agentic world is an open and serious question.
- Agentic coding is another abstraction layer — the first non-deterministic one, which is exactly why review is non-negotiable.
- The job shifts toward specifying intent, designing verification, and exercising judgment: the parts that were always hard.

::::::::::::::::::::::::::::::::::::::::::::::::
