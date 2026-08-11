---
title: "Cost, Context, and Energy"
teaching: 6
exercises: 6
---

:::::::::::::::::::::::::::::::::::::: questions

- Why do agentic sessions cost so much more than chat queries?
- What is context accumulation, and how do I manage it?
- What is the energy footprint of agentic coding?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Explain why tokens accumulate super-linearly over a long agentic session.
- Use `/clear`, `/compact`, and `/cost` (or their equivalents) to manage context and spending.
- Estimate the energy footprint of your own usage with back-of-napkin math.

::::::::::::::::::::::::::::::::::::::::::::::::

## Agentic loops burn tokens

A chat query is one round trip. An agentic session chains hundreds: read files, reason,
write code, run commands, read the output, iterate. A focused task might use 50K–200K
tokens; a sprawling underspecified session can burn over a million. Two dynamics drive
this:

- **Agentic loops.** A vague prompt sends the agent into try–fail–read-more–try-again
  cycles. (Notice this is the *same* failure as in the specification episode — vagueness
  costs quality *and* money.)
- **Context accumulation.** Every new message resends the accumulated conversation —
  file contents, command output, all of it. The 50th message in a session costs far
  more than the 1st.

The levers are the same everywhere; only the names differ:

:::::::::::::::: group-tab

### Claude Code

- `/clear` — reset context between unrelated tasks. Cheapest single habit.
- `/compact` — summarize a long conversation, keeping what matters.
- `/cost` — see what the current session has consumed; `/context` shows what's
  filling the window.
- <kbd>Esc</kbd> — interrupt an agent that's heading the wrong way.

### GitHub Copilot

- **New chat** between unrelated tasks — the `/clear` equivalent; keep each chat
  scoped to one task.
- For a long thread, carry a short summary of key decisions into a fresh chat rather
  than letting the thread grow.
- Check credit/premium-request usage on your
  [Copilot settings page](https://github.com/settings/copilot); model choice changes
  the burn rate.
- The **stop button** interrupts an agent-mode session mid-flight.

::::::::::::::::::::::::

Whichever tool: course-correct early — an agent heading the wrong way generates output
you then pay to carry in context for the rest of the session. The principle is
identical everywhere: **a tight, specific prompt in a clean context is simultaneously
higher-quality, cheaper, and — as we'll see — greener.**

## Energy: the dishwasher comparison

A single LLM chat query costs roughly 0.3 Wh — about a Google search. An agentic coding
session chains so many calls that one careful estimate puts a Claude Code session at
about **41 Wh** — roughly 130 chat queries — and a heavy day of multiple parallel
sessions at ~1,300 Wh:

| Activity | Energy |
|----------|--------|
| One chat query / web search | ~0.3 Wh |
| LED bulb for an hour | ~10 Wh |
| One agentic coding session | ~41 Wh |
| Streaming an hour of video | ~36–80 Wh |
| Heavy day of agentic coding | ~1,300 Wh |
| Running a dishwasher once | ~1,300 Wh |

So a heavy agentic day ≈ one dishwasher run: modest individually, significant in
aggregate — data center electricity demand is projected to roughly double by 2030,
driven largely by AI, and 60–90% of AI compute energy goes to *inference*, not
training. This isn't an argument against the tools (the productivity per unit of
energy may well beat the alternative); it's an argument for intentionality. Don't let
an agent spin in loops that a well-scoped prompt would have avoided.

## Code generation is the green pattern

There's a sharper way to frame this than "use less AI": **compare AI-for-code-generation
against the alternative way people use AI.** The wasteful pattern isn't agentic coding —
it's reaching for a frontier assistant for *every single question*: eyeballing data by
pasting it into chat, re-asking the model to convert units, check a threshold, or
reformat a file, day after day. Every one of those queries is another inference pass
through a model with on the order of a trillion parameters — to do work a for-loop
could do.

Code generation inverts that. Spend the model's compute **once** to produce a good
script, and that script then runs deterministically at a completely negligible fraction
of the energy — forever. Need to validate 10,000 rows every morning? Asking the model
to "look them over" daily burns inference every day and gives you a non-reproducible
answer; asking it once to *write the validation script* gives you a versioned,
reviewable, testable artifact that runs in milliseconds on a CPU. Generate once, run
many: the AI's energy cost amortizes toward zero per use, and you get reproducibility —
the thing chat answers never have — as a free side effect.

The rule of thumb: **use the model to build tools, not to be the tool.** If you find
yourself asking an AI the same kind of question repeatedly, that's a script asking to
be written.

One more thing nobody will do for you: **providers optimize for customer spend, not
for efficiency.** If you've selected a frontier model, the dumbest question you ask
gets routed through that largest model — even though a trivial gating mechanism could
have answered it with a tiny model at a small fraction of the energy (and cost). No
such gate exists on the provider's side, because they have no incentive to build one.
So the routing falls to you: keep a small, cheap model as your default for mechanical
work (renames, formatting, simple lookups) and reach for the frontier model
deliberately, when the task actually needs the reasoning. Same discipline, third
payoff: quality where it matters, money and energy saved where it doesn't.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise 4: What did tonight cost? (6 minutes)

:::::::::::::::: group-tab

### Claude Code

Run `/cost` in your session for tokens consumed and `/context` for what's filling
the window.

### GitHub Copilot

Open your [usage dashboard](https://github.com/settings/copilot) to see
credit/premium-request consumption, and note which models you used today.

::::::::::::::::::::::::

1. Check what your session has consumed (your tool's tab above) and note the number.
2. Back-of-napkin energy estimate: if a full session ≈ 41 Wh, scale by how much of a
   "typical" session you've used (tokens are a reasonable proxy). How many chat queries
   is that? What fraction of a dishwasher run?
3. Look back at your session history: which single interaction consumed the most? Was
   it a vague prompt that triggered a loop?

:::::::::::::::::::::::: solution

## Typical findings

Most workshop sessions land in the low single-digit Wh — a few percent of a dishwasher
run. The interesting result is usually #3: one underspecified prompt (often the "bad
prompt" from Exercise 2!) accounts for a disproportionate share of the total. The
cheapest token is the one a clearer sentence made unnecessary.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Agentic sessions chain hundreds of model calls; context accumulation makes late messages far more expensive than early ones.
- `/clear` between tasks, `/compact` within long ones, `/cost` to stay aware — and interrupt early when the agent drifts.
- One agentic session ≈ 41 Wh; a heavy day ≈ one dishwasher run. Individually modest, collectively significant.
- Specific prompts in clean context are better, cheaper, and greener — the same discipline pays three times.
- Use the model to build tools, not to be the tool: code you generate once runs at negligible energy forever, while asking the assistant the same question daily re-spends inference every time.

::::::::::::::::::::::::::::::::::::::::::::::::
