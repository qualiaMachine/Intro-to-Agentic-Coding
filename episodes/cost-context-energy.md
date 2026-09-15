---
title: "Cost, Context, and Energy"
teaching: 10
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- How much energy does an agentic coding session actually use?
- Why do agentic sessions cost so much more than chat queries?
- Which habits reduce token usage without reducing quality?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Give an order-of-magnitude energy figure for a chat query, a coding session, and a heavy agentic day — and say why the estimates spread.
- Explain why tokens accumulate super-linearly over a long agentic session.
- Use `/cost`, `/compact`, model switching, and skills (or their equivalents) to manage context and spending.
- Compare real-world session cost across models before committing to one.

::::::::::::::::::::::::::::::::::::::::::::::::

## How much energy do AI models use?

People arrive with a claim — a prompt costs gallons of water — so replace it with a
number. Estimates vary wildly and no provider publishes per-query figures, but the
order of magnitude is well established:

| Activity | Energy | Source |
|----------|--------|--------|
| One chat query | ~0.3 Wh — an LED bulb for about two minutes | Epoch AI per-token estimates |
| One median coding session (24 model calls, ~590k tokens) | ~41 Wh — roughly 130 chat queries | [Simon Couch, 2026](https://simonpcouch.com/blog/2026-01-20-cc-impact/) |
| One heavy agentic day | ~one dishwasher cycle, or a refrigerator running for a day | Simon Willison, 2026 |
| A median session on large analyses with subagents | ~600 Wh | [Zeke Hausfather, 2026](https://www.theclimatebrink.com/p/the-real-energy-use-of-agentic-ai) |

Couch scaled Epoch's per-token estimates against his real Claude Code token counts.
Hausfather ran his own tokens through three published methods and got a number an
order of magnitude higher, because he runs subagents on large analyses. Nobody outside
the labs knows the true per-token energy. So the honest framing is **order of
magnitude, not precision: tens of watt-hours per session, hundreds if you run agents
hard.**

Two macro takeaways survive the uncertainty:

- **The real issue is aggregate demand.** Individual queries are lightweight, but
  massive scaling drives significant overall power consumption. OpenAI's CEO once
  noted that a single California almond takes as much water as tens of thousands of
  ChatGPT queries — meant to downplay per-query impact, it mostly shows how micro-costs
  scale when billions of queries a day are processed.
- **Inference dominates training.** Operational inference, not model training, is
  where most AI energy now goes — which means your usage patterns are the lever.

This is not an argument against the tools; the productivity per unit of energy may
well beat the alternative. It is an argument for **intentionality**. Don't let an
agent spin in loops that a well-scoped prompt would have avoided.

## Why agentic sessions burn tokens

A chat query is one round trip. An agentic session chains hundreds: read files,
reason, write code, run commands, read the output, iterate. A focused task might use
50K–200K tokens; a sprawling underspecified session can burn over a million. Two
dynamics drive this:

- **Agentic loops.** A vague prompt sends the agent into try–fail–read-more–try-again
  cycles. (This is the *same* failure as in the feature-based-development episode —
  vagueness costs quality *and* money *and* energy.)
- **Context accumulation.** Every new message resends the accumulated conversation —
  file contents, command output, all of it. The 50th message in a session costs far
  more than the 1st.

## Techniques to reduce token usage

- **Pay attention to usage.** Look at what you're spending. It's also how you catch
  a runaway agent burning tokens on retries.
- **Police which model you are using and match it to the task's difficulty.** Not
  every task needs your most expensive model. Keep a smaller model as the default
  for mechanical work (renames, formatting, lookups) and switch up deliberately when
  the task needs the reasoning. Providers won't route for you — they optimize for
  spend, not efficiency.
- **Minimize the context in each session.** As a session runs long, old context piles
  up and every future message re-pays for it. Start fresh between unrelated tasks;
  compact a long thread instead of letting it grow. Prefer search over reading whole
  files — context is the thing you're paying for.
- **Use skills** to reduce input and output. A skill loads a short pointer instead of
  a long explanation every time; the [caveman](https://github.com/JuliusBrussee/caveman)
  skill from the previous episode cuts output tokens by design.
- **Push long or independent tasks to a background agent** rather than watching a
  meter run on a foreground session.
- **Compare real-world session cost across models before you commit to one, not just
  benchmark scores.** [OpenRouter's session-cost rankings](https://openrouter.ai/rankings#session-cost)
  track what people actually spend per session across live agentic-coding traffic —
  a gut check against marketing claims.

:::::::::::::::: group-tab

### Claude Code

- `/cost` — what the current session has consumed; `/context` — what's filling the
  window.
- `/model` — switch models mid-session.
- `/clear` — reset context between unrelated tasks. Cheapest single habit.
- `/compact` — summarize a long conversation, keeping what matters.
- <kbd>Esc</kbd> — interrupt an agent that's heading the wrong way.

### GitHub Copilot

- Check credit/premium-request usage on your
  [Copilot settings page](https://github.com/settings/copilot); model choice changes
  the burn rate.
- The model picker in the chat panel switches models.
- **New chat** between unrelated tasks — the `/clear` equivalent.
- For a long thread, carry a short summary of key decisions into a fresh chat.
- The **stop button** interrupts an agent-mode session mid-flight.

::::::::::::::::::::::::

Whichever tool: course-correct early. An agent heading the wrong way generates output
you then pay to carry in context for the rest of the session. **A tight, specific
prompt in a clean context is simultaneously higher-quality, cheaper, and greener.**

::::::::::::::::::::::::::::::::::::: callout

## Use the model to build tools, not to be the tool

The wasteful pattern isn't agentic coding — it's reaching for a frontier model for
*every single question*: pasting data into chat to eyeball it, re-asking it to
convert units or check a threshold, day after day. Code generation inverts that.
Spend the model's compute **once** to produce a good script, and that script then
runs deterministically at a negligible fraction of the energy — forever, and
reproducibly. If you find yourself asking an AI the same kind of question
repeatedly, that's a script asking to be written.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: What did tonight cost? (5 minutes)

1. Check what your session has consumed (`/cost` in Claude Code; the usage dashboard
   for Copilot) and note the number and the model.
2. Back-of-napkin energy: if a median session ≈ 41 Wh, scale by how much of a
   typical session you've used (tokens are a reasonable proxy). How many chat queries
   is that? What fraction of a dishwasher run?
3. Look back at your session history: which single interaction consumed the most? Was
   it a vague prompt that triggered a loop?

:::::::::::::::::::::::: solution

## Typical findings

Most workshop sessions land in the low single-digit Wh — a few percent of a
dishwasher run. The interesting result is usually #3: one underspecified prompt
accounts for a disproportionate share of the total. The cheapest token is the one a
clearer sentence made unnecessary.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- A chat query is ~0.3 Wh; a median coding session ~41 Wh; a heavy agentic day about a dishwasher cycle. Estimates spread by an order of magnitude — think tens to hundreds of Wh per session, not precision.
- The issue is aggregate demand, and inference now dominates; your usage patterns are the lever.
- Agentic sessions chain hundreds of model calls; context accumulation makes late messages far more expensive than early ones.
- Watch usage, match the model to the task, keep sessions short and compact, use skills, and compare real session cost across models before committing.
- Specific prompts in clean context are better, cheaper, and greener — the same discipline pays three times.

::::::::::::::::::::::::::::::::::::::::::::::::
