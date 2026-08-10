---
title: "What the Research Shows, and Where This Leaves Us"
teaching: 12
exercises: 5
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

Programming has survived its own death many times: assembly gave way to compilers and
then to languages like Python, manual memory management to garbage collection, servers
to the cloud. Each time, the work moved up a level of abstraction and the discipline
adapted. Nobody writing pandas today feels diminished for not managing registers.

Agentic coding is the same move again — **but the first non-deterministic abstraction.**
Every previous layer was a deterministic translation: one request, one outcome. Compile
the same C twice and you get the same program, which is why nobody audits compiler
output. An agent breaks that contract: **one request leads to many possible outcomes.**
It interprets your intent probabilistically, filling every unstated gap with the
average case, and the same prompt can yield different code on different days.

We correct for that non-determinism with the two practices this lesson keeps returning
to: **good prompting** (specification narrows the space of outcomes — the whole point
of the underspecification episode) and **a review process** (verification catches the
outcomes that specification didn't prevent). Never assume the AI will work 100% of the
time — not because the tools are bad, but because "usually right, occasionally
plausibly wrong" is what a probabilistic abstraction *is*. Design your workflow for
that, and it's just another layer; assume perfection, and it's a trap.

So: not dead. The job shifts from writing every line toward specifying intent,
designing verification, and exercising judgment — which, conveniently, were always the
hard parts of research computing. And that is also why **there is still no escaping
good data science practice**: exploring your data, knowing your features and
distributions, and knowing what your models actually tell you were never typing tasks
that an agent could absorb. They are the judgment the whole workflow now leans on.

## Pass it on

One more habit worth building: when you use AI to teach yourself something, **write it
up and give it away**. If it took you a hundred chats to get a working pattern out of
an AI assistant — and the raw AI answer was only 80% correct until you fixed it — that
struggle has value beyond you. Turn it into a blog post, an annotated notebook, a
how-to guide, or a lesson contribution, so the next person starts from your verified
100% instead of re-running your hundred chats.

This is the community-scale version of the energy argument from the last episode: the
compute you spent gets amortized across every reader instead of being re-spent by each
of them. It's also a natural fit with the documentation episode — the write-up you
leave for your future self is often two edits away from being useful to a stranger.
If you're at UW–Madison, the [ML+X Nexus](https://uw-madison-datascience.github.io/ML-X-Nexus/)
exists precisely for this (guides, notebooks, workshop materials, and blog posts from
the community — including the guides this lesson draws on); elsewhere, your lab blog,
The Carpentries Incubator, or a well-documented public repo all serve the same purpose.

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
- Agentic coding is another abstraction layer — but the first non-deterministic one: one request, many possible outcomes. Good prompting narrows the outcomes; review catches the rest; never assume 100%.
- The job shifts toward specifying intent, designing verification, and exercising judgment: the parts that were always hard — and there is still no escaping good data science practice.
- When AI teaches you something the hard way, write it up (blog, notebook, lesson) so the next person starts from your verified version instead of re-spending the chats.

::::::::::::::::::::::::::::::::::::::::::::::::
