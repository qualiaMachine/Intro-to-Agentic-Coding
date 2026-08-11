---
title: "Common Workflows"
teaching: 10
exercises: 6
---

:::::::::::::::::::::::::::::::::::::: questions

- How do experienced users actually structure day-to-day work with agents?
- Should I review every commit, or review at the pull request?
- How do agent workflows change when I'm contributing to (or maintaining) a shared project?
- What are skills, hooks, and MCP, and when do I need them?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Choose a review posture (per-commit vs. PR-as-gate) deliberately, matched to stakes and safety nets.
- Adapt agent workflows for contributing to projects you don't own and for maintaining projects others contribute to.
- Recognize when to codify a recurring workflow as a skill, a hook, or an MCP integration.
- Write a short "workflow contract" into your project context file.

::::::::::::::::::::::::::::::::::::::::::::::::

The earlier episodes gave you principles; this one collects the recurring *shapes* of
day-to-day agentic work. None of them is the one true way — the point is to pick your
pattern deliberately and write it down, rather than improvising it fresh every session.

## Two review postures

Everyone agrees on the non-negotiables: agents work on branches, never on `main`, and
*someone* — you, a colleague, or CI — reads the code before it lands. Within that,
two workable postures differ on **when** the human review happens:

**Posture A: the pull request is the review gate.** Let the agent commit freely (and
often) to its feature branch as it works. The commit log gets verbose — that's fine;
frequent small commits are revert points, and an agent's chatty-but-granular history
is more useful than the classic human `wip`, `fix`, `actually fix` sequence. Your
serious review happens once, on the full PR diff, exactly as you'd review a human
collaborator's branch. This posture keeps momentum high and concentrates your
attention where it's most effective — but it leans on safety nets: a real test suite,
CI checks gating the merge, and PR diffs kept small enough to genuinely read
(feature-sized, per the specification episode).

**Posture B: review every change as it happens.** Approve each edit or commit
yourself, staying close to the work in real time. Slower, but right for the
situations where posture A's safety nets are missing: you're new to the tool, the
code is sensitive, the tests are thin, or you're still building trust in what the
agent does with your codebase.

The choice isn't identity, it's calibration — and it maps directly onto the
verification tiers: throwaway and well-tested working code tolerate posture A;
load-bearing code with weak tests deserves posture B (or A plus a second reviewer).
Many people run both: A for routine feature work, dropping to B when touching
anything that would be expensive to get wrong.

## Contributing to projects you don't own

Agent workflows change when the repository belongs to a community:

- **Read the contribution guidelines first** — and this is a place the agent helps:
  "summarize CONTRIBUTING.md and any PR conventions in this repo" is a great first
  prompt. Then follow them, including commit-message and branch-naming conventions.
- **Work from a fork** when you lack write access; that's the intended flow for most
  community projects, and it means no agent ever has push access to the canonical
  repo.
- **Disclose AI assistance when the project asks for it.** More projects have
  explicit policies now (The Carpentries has a Generative AI contributions policy,
  for example). Honesty here is cheap; discovered violations are not.
- **Keep PRs small and self-explanatory.** Maintainers review on their own time; an
  agent makes it easy to generate large diffs, and large diffs are how goodwill dies.
  One focused change, well described, tests included.

## Maintaining a project others contribute to

On the receiving side, agents are useful for the unglamorous middle of maintenance:
summarizing and triaging issues, drafting release notes and changelogs from the
commit history, dependency-update PRs, doc-freshness sweeps, and a first-pass review
of incoming PRs ("what does this change, and what should a human look hardest at?").
The human still owns the merge button — an agent's review is a *brief* for your
judgment, not a substitute (remember the trust episode: incoming PRs are
untrusted input, and prompt injection via PR content is a real pattern).

## Codifying workflows: skills, hooks, and MCP

When you notice the same workflow recurring, the tools give you ways to write it down
once instead of re-prompting it forever:

- **Skills** — reusable, on-demand instruction packages: a release checklist, your
  lab's analysis conventions, a "new episode" template. They load only when relevant,
  so they don't bloat every session the way an overgrown context file does.
- **Hooks** — deterministic scripts that run at fixed points (after every edit,
  before every commit). Unlike context-file instructions, which are advisory, hooks
  are *guaranteed* to fire — use them for the rules that must never be skipped
  (run the linter, block writes to `data/raw/`).
- **MCP (Model Context Protocol)** — connects the agent to external systems: your
  issue tracker, a database, a lab notebook. Each connection widens what the agent
  can touch, so apply the trust episode's lens before wiring
  one in: minimum access, and treat what flows back through it as untrusted input.

A sensible progression: context file first, skills when you catch yourself repeating
instructions, hooks when a rule needs enforcement rather than encouragement, MCP when
the agent genuinely needs an external system.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Write your workflow contract (6 minutes)

Add a short "Workflow" section to a project context file (or draft one in a scratch
file) — three to five rules that make your chosen pattern explicit. For example:

```markdown
## Workflow
- Agents work on feature branches (`feat/<name>`); never commit to main
- Commit freely on the branch; review happens at the PR (Posture A)
- Every PR: tests pass locally, diff under ~300 lines, description says how to verify
- Never modify `data/raw/` or `results/`; never force-push
```

Make at least one rule about *review* (who reads what, when) and one about what the
agent may never touch.

:::::::::::::::::::::::: solution

## Why write it down?

Two payoffs. The agent reads it — your posture, branch conventions, and forbidden
paths now shape every session without re-prompting. And *collaborators* read it — the
lab's workflow stops being folklore. If a rule is safety-critical ("never touch
`data/raw/`"), remember it's advisory here: back it with a hook or deny rule.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Pick a review posture deliberately: PR-as-gate (agent commits freely, one serious review of the full diff) when tests and CI back you up; per-commit review when they don't. Verbose agent commit logs are a feature — small commits are revert points.
- Contributing: read (or have the agent summarize) the project's guidelines, work from forks, disclose AI use where policy asks, keep PRs small.
- Maintaining: agents draft triage, changelogs, and first-pass reviews — but incoming PRs are untrusted input, and the human owns the merge.
- Codify recurring workflows: context file → skills (reusable instructions) → hooks (guaranteed enforcement) → MCP (external systems, minimum access).

::::::::::::::::::::::::::::::::::::::::::::::::
