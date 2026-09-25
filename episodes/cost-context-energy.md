---
title: "Cost, Context, and Energy"
teaching: 10
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- How much energy does an agentic coding session use?
- Why do agentic sessions cost so much more than chat queries?
- Which habits reduce token usage without reducing quality?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Give an order-of-magnitude energy figure for a chat query, a coding session, and a heavy agentic day, and explain why the estimates vary.
- Explain why token use grows faster than linearly over a long agentic session.
- Use `/cost`, `/compact`, model switching, and skills (or their equivalents) to manage context and spending.
- Compare real session cost across models before committing to one.

::::::::::::::::::::::::::::::::::::::::::::::::

## Energy use of AI models

A single LLM chat query now uses roughly 0.3 Wh, about the same as a web search. An
agentic coding session chains hundreds of such calls as the agent reads files,
reasons, writes code, runs commands, and iterates. Estimates for a session vary by an
order of magnitude, and no provider publishes per-query figures, but the range is
well established:

| Activity | Energy | Source |
|----------|--------|--------|
| One chat query or web search | ~0.3 Wh | [Epoch AI](https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use) |
| LED bulb for one hour | ~10 Wh | |
| One median coding session (24 model calls, ~590k tokens) | ~41 Wh, roughly 130 chat queries | [Simon Couch, 2026](https://simonpcouch.com/blog/2026-01-20-cc-impact/) |
| Streaming one hour of video, including the device | ~36–80 Wh | |
| A median session on large analyses with subagents | ~600 Wh | [Zeke Hausfather, 2026](https://www.theclimatebrink.com/p/the-real-energy-use-of-agentic-ai) |
| One heavy agentic day (multiple sessions, parallel agents) | ~1,300 Wh | [Simon Willison, 2026](https://simonwillison.net/tags/ai-energy-usage/) |
| One dishwasher cycle | ~1,300 Wh | |
| A refrigerator for one day | ~1,200–1,500 Wh | |

Couch scaled Epoch AI's per-token estimates by his own Claude Code token counts.
Hausfather ran his own tokens through three published methods and obtained a figure an
order of magnitude higher, because he runs subagents on large analyses. The
defensible statement is an order of magnitude rather than a precise figure: tens of
watt-hours per session, hundreds under heavy agent use, and a heavy day roughly
equal to running a dishwasher.

The aggregate picture:

- The [IEA projects](https://www.iea.org/reports/energy-and-ai) that global data
  center electricity use will roughly double, from about 415 TWh in 2024 to more
  than 945 TWh by 2030, driven largely by AI workloads.
- An estimated 60–90% of AI computing energy goes to inference rather than training.
  Every agentic session and chat query is part of that ongoing cost, which means
  usage patterns are the variable within the user's control.

This is not an argument against the tools; the productivity gains can be substantial,
and the energy per unit of useful output may compare favorably with the alternative.
It is an argument for deliberate use. An agent that loops on a vague prompt spends
energy that a well-scoped prompt would have avoided. Efficient prompting is both
cheaper and lower in energy.

## Why agentic sessions use many tokens

A chat query is one round trip. An agentic session chains hundreds: read files,
reason, write code, run commands, read the output, repeat. A focused task might use
50K–200K tokens; an underspecified session can exceed a million. Two mechanisms
account for this:

- **Agentic loops.** A vague prompt sends the agent into cycles of trying, failing,
  reading more, and trying again. This is the same failure described in the
  feature-based-development episode: vagueness costs quality, money, and energy.
- **Context accumulation.** Every new message resends the accumulated conversation,
  including file contents and command output. The fiftieth message in a session costs
  far more than the first.

## Reducing token use

- **Watch usage.** Knowing what you are spending is also how you detect an agent that
  is retrying in a loop.
- **Match the model to the task.** Not every task requires the most expensive model.
  Use a smaller model by default for mechanical work (renames, formatting, lookups)
  and switch to a larger one when the task requires the reasoning. Providers do not
  route for you; they are optimized for spend rather than efficiency.
- **Keep sessions short.** As a session grows, old context accumulates and every
  subsequent message pays for it again. Start fresh between unrelated tasks; compact a
  long thread rather than letting it grow. Prefer search over reading whole files,
  since context is what you pay for.
- **Use skills.** A skill loads a short pointer instead of a long explanation each
  time. The [caveman](https://github.com/JuliusBrussee/caveman) skill from the
  previous episode reduces output tokens by design.
- **Run long or independent tasks in a background agent** rather than in a foreground
  session you are watching.
- **Compare real session cost across models before committing to one.**
  [OpenRouter's session-cost rankings](https://openrouter.ai/rankings#session-cost)
  report what people spend per session across live agentic-coding traffic, which is a
  useful check against vendor benchmarks.

:::::::::::::::: group-tab

### Claude Code

- `/cost`: what the current session has consumed; `/context`: what is occupying the
  window.
- `/model`: switch models mid-session.
- `/clear`: reset context between unrelated tasks. The cheapest habit to adopt.
- `/compact`: summarize a long conversation, retaining what matters.
- <kbd>Esc</kbd>: interrupt an agent that is heading in the wrong direction.

### GitHub Copilot

- Check credit and premium-request usage on the
  [Copilot settings page](https://github.com/settings/copilot). Model choice changes
  the rate.
- The model picker in the chat panel switches models.
- **New chat** between unrelated tasks is the equivalent of `/clear`.
- For a long thread, carry a short summary of key decisions into a fresh chat.
- The **stop button** interrupts an agent-mode session.

::::::::::::::::::::::::

In any tool, correct course early. An agent heading in the wrong direction generates
output that is then carried in context, at cost, for the rest of the session. A
specific prompt in a clean context is at once higher quality, cheaper, and lower in
energy.

::::::::::::::::::::::::::::::::::::: callout

## Use the model to build tools, not to be the tool

The wasteful pattern is not agentic coding but using a frontier model for every
individual question: pasting data into chat to inspect it, asking it to convert units
or check a threshold, repeatedly. Code generation reverses this. The model's compute
is spent once to produce a script, and the script then runs deterministically at a
negligible fraction of the energy, indefinitely and reproducibly. If you ask an AI the
same kind of question repeatedly, that is a script that has not yet been written.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: What did this session cost? (5 minutes)

1. Check what your session has consumed (`/cost` in Claude Code; the usage dashboard
   for Copilot) and record the figure and the model.
2. Estimate the energy: if a median session is about 41 Wh, scale by the fraction of
   a typical session you have used (tokens are a reasonable proxy). How many chat
   queries is that? What fraction of a dishwasher cycle?
3. Review the session history. Which single interaction consumed the most? Was it a
   vague prompt that produced a loop?

:::::::::::::::::::::::: solution

## Typical findings

Most workshop sessions come to a few watt-hours, a small percentage of a dishwasher
cycle. The informative result is usually the third item: one underspecified prompt
accounts for a disproportionate share of the total. A clearer sentence in that prompt
would have avoided those tokens.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- A chat query is about 0.3 Wh; a median coding session about 41 Wh; a heavy agentic day about a dishwasher cycle. Estimates vary by an order of magnitude, so think in tens to hundreds of watt-hours per session.
- Data center electricity use is projected to roughly double by 2030, and most AI energy now goes to inference rather than training. Usage patterns are the variable you control.
- Agentic sessions chain hundreds of model calls, and context accumulation makes late messages far more expensive than early ones.
- Watch usage, match the model to the task, keep sessions short and compact, use skills, and compare real session cost across models before committing.
- A specific prompt in a clean context is better, cheaper, and lower in energy. One discipline, three benefits.

::::::::::::::::::::::::::::::::::::::::::::::::
