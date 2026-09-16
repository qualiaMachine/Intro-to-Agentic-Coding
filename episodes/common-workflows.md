---
title: "Common Workflows"
teaching: 10
exercises: 6
---

:::::::::::::::::::::::::::::::::::::: questions

- How do experienced users structure day-to-day work with agents?
- Should I review every commit, or review at the pull request?
- How do agent workflows change when I contribute to, or maintain, a shared project?
- What are skills, hooks, and MCP, and when do I need them?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Choose a review posture (per-commit or pull-request-as-gate) deliberately, matched to stakes and safety nets.
- Adapt agent workflows for contributing to projects you do not own and for maintaining projects others contribute to.
- Recognize when to codify a recurring workflow as a skill, a hook, or an MCP integration.
- Write a short workflow contract into your project context file.

::::::::::::::::::::::::::::::::::::::::::::::::

The workshop episodes covered principles. This episode, intended for reading after
the workshop, describes the recurring shapes of day-to-day agentic work. None is the
single correct approach. The aim is to choose a pattern deliberately and record it,
rather than improvise it in each session.

## Two review postures

The non-negotiable rules are that agents work on branches, never on `main`, and that
someone (you, a colleague, or CI) reads the code before it is merged. Within those
rules, two workable postures differ on when the human review happens.

**Posture A: the pull request is the review gate.** The agent commits freely and
often to its feature branch as it works. The commit log becomes verbose; that is
acceptable, because frequent small commits are restore points, and an agent's
granular history is more useful than the usual human sequence of `wip`, `fix`,
`fix again`. Your review happens once, on the full pull-request diff, as it would for
a human collaborator's branch. This posture maintains momentum and concentrates
attention where it is most effective. It depends on safety nets: a real test suite,
CI checks gating the merge, and diffs small enough to read in full (feature-sized, as
described in the feature-based-development episode).

**Posture B: review every change as it happens.** You approve each edit or commit,
staying close to the work in real time. This is slower, and appropriate where posture
A's safety nets are absent: you are new to the tool, the code is sensitive, the tests
are thin, or you are still establishing what the agent does with your codebase.

The choice is a calibration, and it maps onto the verification tiers. Throwaway and
well-tested working code tolerate posture A; load-bearing code with weak tests calls
for posture B, or A with a second reviewer. Many people use both: A for routine
feature work, B when modifying anything expensive to get wrong.

## Contributing to projects you do not own

Agent workflows change when the repository belongs to a community:

- **Read the contribution guidelines first.** The agent can help: "summarize
  CONTRIBUTING.md and any pull-request conventions in this repo" is a good first
  prompt. Then follow them, including commit-message and branch-naming conventions.
- **Work from a fork** when you lack write access. That is the intended flow for most
  community projects, and it means no agent has push access to the canonical
  repository.
- **Disclose AI assistance when the project requires it.** Many projects now have
  explicit policies; The Carpentries has a Generative AI contributions policy, for
  example. Disclosure is inexpensive; a discovered violation is not.
- **Keep pull requests small and self-explanatory.** Maintainers review in their own
  time. An agent makes large diffs easy to produce, and large diffs are a common
  reason contributions are declined. One focused change, well described, with tests.

## Maintaining a project others contribute to

On the receiving side, agents are useful for routine maintenance: summarizing and
triaging issues, drafting release notes and changelogs from the commit history,
dependency-update pull requests, documentation-freshness sweeps, and a first-pass
review of incoming pull requests ("what does this change, and what should a human
examine most closely?"). The human retains the merge decision. An agent's review is
a brief for your judgment, not a substitute for it. As the trust episode noted,
incoming pull requests are untrusted input, and prompt injection through
pull-request content is a documented pattern.

## Codifying workflows: skills, hooks, and MCP

When the same workflow recurs, the tools provide ways to record it once instead of
re-prompting it:

- **Skills** are reusable, on-demand instruction packages: a release checklist, a
  group's analysis conventions, a "new episode" template. They load only when
  relevant, so they do not enlarge every session the way an overgrown context file
  does.
- **Hooks** are deterministic scripts that run at fixed points (after every edit,
  before every commit). Unlike context-file instructions, which are advisory, hooks
  always run. Use them for rules that must never be skipped, such as running the
  linter or blocking writes to `data/raw/`.
- **MCP (Model Context Protocol)** connects the agent to external systems: an issue
  tracker, a database, a lab notebook. Each connection widens what the agent can
  reach, so apply the trust episode's rules before adding one: minimum access, and
  treat what comes back as untrusted input. The [MCP and skills](skills-and-mcp.md)
  episode has hands-on exercises for both.

A reasonable progression: context file first; skills when you notice yourself
repeating instructions; hooks when a rule needs enforcement rather than a reminder;
MCP when the agent needs an external system.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Write your workflow contract (6 minutes)

If your team completed the planning episode's exercise on working together, you
already have a `CONTRIBUTING.md`. This is the individual version, and an opportunity
to add the review-posture decision to it. Add a short "Workflow" section to a project
context file (or draft one in a scratch file): three to five rules that make your
chosen pattern explicit.

:::::::::::::::: group-tab

### Claude Code

The file is `CLAUDE.md` at the repository root. Create it if the project has none.

### GitHub Copilot

The file is `.github/copilot-instructions.md`. The cross-tool convention `AGENTS.md`
also works in tools that support it.

::::::::::::::::::::::::

For example:

```markdown
## Workflow
- Agents work on feature branches (`feat/<name>`); never commit to main
- Commit freely on the branch; review happens at the PR (Posture A)
- Every PR: tests pass locally, diff under ~300 lines, description says how to verify
- Never modify `data/raw/` or `results/`; never force-push
```

Include at least one rule about review (who reads what, and when) and one about what
the agent may never modify.

:::::::::::::::::::::::: solution

## Why record it

Two benefits. The agent reads it, so your posture, branch conventions, and forbidden
paths shape every session without re-prompting. Collaborators read it, so the
group's workflow is documented rather than assumed. If a rule is safety-critical
("never modify `data/raw/`"), it is advisory here; back it with a hook or a deny
rule.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Choose a review posture deliberately: pull-request-as-gate (the agent commits freely; one full review of the diff) when tests and CI support it; per-commit review when they do not. Verbose agent commit logs are useful, since small commits are restore points.
- Contributing: read the project's guidelines (or have the agent summarize them), work from forks, disclose AI use where required, keep pull requests small.
- Maintaining: agents draft triage, changelogs, and first-pass reviews, but incoming pull requests are untrusted input and the human makes the merge decision.
- Codify recurring workflows: context file, then skills (reusable instructions), then hooks (guaranteed enforcement), then MCP (external systems, minimum access).

::::::::::::::::::::::::::::::::::::::::::::::::
