---
title: "What the Research Shows, and Where This Leaves Us"
teaching: 12
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- Who benefits from these tools, and on which kinds of work?
- Is programming dead?
- What should I do differently starting tomorrow?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Summarize what early research says about productivity effects and who gains most.
- Explain why agentic coding is another abstraction layer, and the first non-deterministic one.
- Commit to three concrete practices for your next project.

::::::::::::::::::::::::::::::::::::::::::::::::

## What the research shows so far

The evidence base is young, but several findings recur:

- **Coding speed is only one bottleneck.** Agents multiply commits (+240%) far more
  than releases (+30%), and pull requests wait about five times longer for human
  review under heavy AI use (the verification episode's figures). Analyses still
  require expert review and verification, and that step does not accelerate.
- **Perceived and measured speed can diverge.** In a 2025 randomized trial (METR),
  experienced open-source developers believed they were about 20% faster with AI
  tools on their own mature repositories while measuring about 19% slower. The rule
  applied to model scores applies to one's own productivity: measure it.
- **Learning with AI can cost understanding.** In Anthropic's 2026 study, developers
  who learned an unfamiliar library with AI assistance scored 17% lower on a quiz
  covering concepts they had used minutes earlier, with the largest gap on debugging
  questions. The participants who retained understanding used the assistant to ask
  why, not only to produce code
  ([Anthropic, 2026](https://www.anthropic.com/research/AI-assistance-coding-skills)).
- **Gains are uneven.** Experienced practitioners, who can specify precisely, review
  effectively, and recognize plausible-but-wrong output, obtain more value; novices
  are more likely to accept flawed results. Verification skill, not typing speed, is
  the limiting factor.

The evidence supports the conclusion that these tools amplify expertise more than
they replace it. The practices in this lesson (scoping, specifying, verifying) are
the expertise being amplified. The question of skill formation remains open: if
agents do the routine work, where do junior researchers develop the debugging
judgment that supervising an agent requires? Deliberate practice may need to be
scheduled where it previously occurred as a by-product.

::::::::::::::::::::::::::::::::::::: discussion

## Is programming dead?

Before reading on, discuss with a neighbor. What in your own work became faster this
session, and what did not?

::::::::::::::::::::::::::::::::::::::::::::::::

## Is programming dead? The evidence says no

Programming has been declared obsolete before. Assembly gave way to compilers and
then to languages such as Python; manual memory management gave way to garbage
collection; servers gave way to the cloud. Each time, the work moved up a level of
abstraction and the discipline adapted.

Agentic coding is the same transition with one difference: it is the first
non-deterministic abstraction. Every previous layer was a deterministic translation,
one request producing one outcome. Compiling the same C source twice yields the same
program, which is why compiler output is not audited. An agent breaks that contract.
One request leads to many possible outcomes. It interprets intent probabilistically,
fills each unstated gap with the average case, and can produce different code from
the same prompt on different days.

Two practices compensate for the non-determinism, and the lesson has returned to them
repeatedly: good prompting (specification narrows the space of outcomes, the subject
of the feature-based-development episode) and a review process (verification catches
the outcomes that specification did not prevent). Do not assume the agent will be
correct every time. "Usually right, occasionally plausibly wrong" is what a
probabilistic abstraction is. A workflow designed for that treats the agent as one
more layer; a workflow that assumes perfection will eventually fail.

Programming is therefore not dead. The work shifts from writing every line toward
specifying intent, designing verification, and exercising judgment, which were
always the difficult parts of research computing. This is also why good data science
practice still applies in full. Examining the data, knowing the features and their
distributions, and understanding what the model responds to were never typing tasks.
They are the judgment the workflow now depends on.

## Pass it on

When you use AI to teach yourself something, write it up and share it. If it took
many attempts to obtain a working pattern from an assistant, and the raw answer was
only mostly correct until you fixed it, that effort has value beyond you. A blog
post, an annotated notebook, a how-to guide, or a lesson contribution lets the next
person start from your verified version rather than repeating the attempts.

This is the community-scale version of the energy argument in the previous episode:
the compute is amortized across every reader instead of being spent again by each.
It also follows from the documentation episode: the notes you leave for your future
self are usually a short edit away from being useful to a stranger. At UW–Madison, the
[ML+X Nexus](https://uw-madison-datascience.github.io/ML-X-Nexus/) exists for this
purpose (guides, notebooks, workshop materials, and posts from the community,
including the guides this lesson draws on). Elsewhere, a lab blog, The Carpentries
Incubator, or a well-documented public repository serves the same function.

::::::::::::::::::::::::::::::::::::: challenge

## Three things before your next sprint

Before your next project session, commit to:

1. **Set up the guardrails once.** Secrets in a keyring or secrets manager (nothing in
   plaintext on disk), a project context file (`CLAUDE.md`, `AGENTS.md`, or
   `copilot-instructions.md`) under 100 lines, and a branch-only workflow.
2. **Write the contract first.** For the next feature you delegate, write one test or
   printed check that encodes what "correct" means for your data, before you prompt.
3. **Review one full diff as a skeptical referee.** Take one agent-produced change and
   review it as if a stranger had submitted it to your paper's supplementary code:
   examine the data it touches, check a number against a source of truth, and
   determine what the model is responding to.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Agentic tools amplify expertise. Verification skill, not typing speed, is the limiting factor, and perceived speedups can be illusory, so measure.
- Learning with AI can cost understanding (17% lower quiz scores, largest gap in debugging). Use the agent to ask why, not only to produce code.
- How novices build supervisory expertise in an agentic setting is an open and serious question.
- Agentic coding is another abstraction layer, and the first non-deterministic one: one request, many possible outcomes. Good prompting narrows the outcomes; review catches the rest; never assume the agent is always correct.
- The work shifts toward specifying intent, designing verification, and exercising judgment, and good data science practice still applies in full.
- When AI teaches you something at some cost, write it up (blog, notebook, lesson) so the next person starts from the verified version.

::::::::::::::::::::::::::::::::::::::::::::::::
