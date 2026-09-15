---
title: "Verification and Testing: No Escaping Good Data Science"
teaching: 15
exercises: 15
---

:::::::::::::::::::::::::::::::::::::: questions

- Why isn't "the code runs and the score is high" enough?
- Which cheap checks catch the expensive mistakes?
- How do I review an agent's work when the code runs?
- How can the agent help me reason about results, not just write code?
- How do I make checks run automatically so they never get skipped?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Apply established data science verification practices (know your data, compare to a source of truth, ask a colleague, reproduce) to agent-generated analyses.
- Detect a group-leakage bug in code that runs cleanly and scores well, and write the assertion that catches it.
- Run cheap sanity checks — label shuffling, baselines, overlap and duplicate checks, seed variation — that expose broken evaluations.
- Review an agent's diff by hunting for decisions you didn't make.
- Use an agent to reason over saved results and figures, and leave evidence in the repo for it to read.
- Make verification automatic: tests in CI, a context-file rule, and a protected `main`.

::::::::::::::::::::::::::::::::::::::::::::::::

## What the research shows about checking

In research code, **checking agent output is the bottleneck**, not producing it:

- Agents could not judge scientific validity. In OpenAI's 2026 field report on
  scientists using agents, the humans still had to decide whether a result was
  *right*, not just whether it ran.
- Agents multiply code *written* far more than code *shipped*: **240%** more commits,
  but only **30%** more releases across half a million GitHub developers
  (Demirer, Musolff & Yang, 2026). The human review step is where the gains
  attenuate.
- Pull requests wait about **five times longer** for a human review under heavy AI
  use — and **31% more merge without one** (Faros AI telemetry, 22,000 developers,
  2026).

So the skill this episode teaches is the one that's scarce.

## There is no escaping good data science

Before AI enters the picture, research computing already had an answer to "how do I
know this analysis is right?":

- **Know your data.** Distributions, outliers, units, missingness, class balance.
  Look at actual rows.
- **Compare to a source of truth.** A published baseline, a hand-computed subset, a
  control.
- **Ask a colleague.** "Does this number seem plausible to you?"
- **Know what your model is telling you.** If the top predictor makes no scientific
  sense, that is a finding about your pipeline, not about nature.
- **Reproduce the result.** Rerun it, change the seed, rerun on a fresh split. If it
  does not hold, something you are not controlling is driving it.

None of this changed. **Only code typing moved to the agent.** What changed is speed:
you can now generate a plausible, clean-running, well-scoring analysis in minutes —
which means you can be *misled* faster too. Your skepticism has to keep pace. (Agents
can learn more about your project as you leave evidence in the repo — figures,
metrics, notes — but they see a slice of the project at a time, never all of it.)

## Cheap checks that catch expensive mistakes

You don't need a heavyweight process to catch most broken evaluations. A handful of
checks — each a few lines an agent will happily write for you — expose whole classes
of silent failure:

- **Shuffle the labels and re-run.** A sound pipeline collapses to chance. If it does
  not, something leaks.
- **Print the baseline.** 94% stops being impressive when the majority class is 92%.
- **Assert no sample is in both splits.** Repeated measures and tiles from one image
  belong on one side.
- **Hunt duplicates before splitting.** Leakage with no code bug at all.
- **Vary the seed.** A metric that swings substantially across seeds is a variance
  problem, not a result.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: What is wrong with this? (5 minutes)

```python
# Brain decoding. 20 subjects, 400 trials each,
# one EEG window per trial.
X, y, subject = load_windows()      # X: (8000, ch, t)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

clf = make_pipeline(StandardScaler(), LogisticRegression())
clf.fit(X_train.reshape(len(X_train), -1), y_train)
print("accuracy", clf.score(
    X_test.reshape(len(X_test), -1), y_test))
# accuracy 0.91
```

The code runs. The number is good. Find the bug. Then write the one assertion that
would have caught it.

:::::::::::::::::::::::: solution

## The bug, and the assertion that catches it

**Every subject is in both splits.** The model learned who each person is, not what
they were looking at. On a new subject, the score collapses:

```python
from sklearn.model_selection import GroupShuffleSplit

train_idx, test_idx = next(GroupShuffleSplit(
    test_size=0.2, random_state=42).split(X, y, groups=subject))
assert set(subject[train_idx]).isdisjoint(subject[test_idx])
# accuracy on unseen subjects: 0.58
```

**Split by the unit that repeats, and assert it.** Subject in a brain-decoding study.
Camera burst in a wildlife-camera dataset. Page in a document-transcription task.
Source document in a retrieval pipeline. The assertion runs every time, so it never
gets forgotten — tests you have to remember to run get skipped.

If you didn't spot it: that's the point. Nothing about this code *looks* wrong, no
error fires, and the score rewards you for not looking harder. This is exactly the
*plausible average case* failure from the previous episode: `train_test_split` is
the pattern in a million notebooks, and the agent optimized for "task apparently
completed" — clean run, high score. If your review process is also "does it run? is
the score good?", you and the agent share the same blind spot.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Hunt for decisions you did not explicitly make

When you review agent-written analysis code, you are not proofreading syntax — the
code runs. You are **hunting for decisions.** Check assumptions at every step, and
add a test for each. The high-yield places to look:

- **Silently dropped or altered rows**: a default `dropna()`, an inner join that
  shrinks the table, a type coercion that turns errors into NaNs. Demand row counts
  before and after every join and filter.
- **Defaults treated as decisions**: imputation strategy, class weights,
  regularization strength, "reasonable" thresholds. Every default it accepted is now
  a choice you own.
- **Metric switcheroos**: you asked about accuracy, the report quietly features F1
  because the number looked better.
- **Suppressed problems**: warnings silenced, `try/except: pass`, an error "fixed" by
  deleting the check. An agent told to make it run sometimes does just that.

One prompt that pays for itself, every time:

> Summarize every choice you made that I did not specify, and flag the risky ones.

It surfaces the dropped-rows and default-parameter decisions above more reliably
than reading line by line.

## Agents as data science assistants

Verification isn't only about catching bugs. The agent is also a fast second reader
of your *results* — if you give it something to read.

- **Ask it to reason over results, not only write code.** What stands out, what
  disagrees, what to try next.
- **Leave evidence in the repo.** Metrics files, figures, run logs, a `results.md`.
  What is not written down does not exist to the agent.
- **Point it at the evidence every time.** It does not remember last session and
  will not open a file you did not name.
- **It reads plots.** A saved figure is context, not decoration.
- **You iterate faster.** Get the result and look at it, instead of debugging
  convoluted code past midnight. Vet as you go.
- **It does not replace your eyes.** Check every number it cites against the file.
  It sees a slice of the project, never all of it.

> Read `results/feature1_metrics.json`, `figures/cv_by_fold.png` and `plan.md`.
> What stands out? Which fold or class is driving the average, and does the plot
> agree with the numbers? Propose the one experiment you would run next and say what
> result would change our plan. Do not run anything yet.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Now your repo (10 minutes)

Same question as the brain-decoding example — your repo.

1. **Ask, in plan mode:**

   > Plan mode, do not edit. Read `plan.md` and the code. Where could this pipeline
   > produce a confident wrong result without raising an error? Name the file and
   > line for each. For each one, write the assertion that would catch it. Include
   > the check for our project's repeated unit (subject, image, document, site, …).
   > Do not run anything yet.

2. **Pick one assertion** and have the agent add it, as a test.
3. **Make it automatic.** Three things, each a permission rather than a habit:
   - A workflow runs `pytest` on every push ([GitHub Actions for Python](https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python)).
     Ask the agent to write it.
   - Your context file says: *run `pytest` before opening a PR; never commit failing
     tests.*
   - Protect `main` so a failing check blocks the merge ([about protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)).

:::::::::::::::: group-tab

### Claude Code

Plan mode for step 1 (<kbd>Shift</kbd>+<kbd>Tab</kbd> locally; on the web, the "do
not edit" line does the same job). For steps 2–3 switch to normal mode; Claude will
run `pytest` itself — approve the command — and iterate until it passes.

### GitHub Copilot

**Ask** mode with `@workspace` for step 1; **Agent** mode for steps 2–3. Copilot
proposes the `pytest` run in the terminal and waits for your approval. The Actions
workflow and branch protection are set on GitHub, not in the editor.

::::::::::::::::::::::::

:::::::::::::::::::::::: solution

## Why this works

You've turned an invisible methodological requirement into an executable contract.
The agent now has a feedback loop that fails loudly when it reaches for the
average-case pattern — and you have an artifact that keeps protecting you on every
future change, whether the next edit comes from an agent, a labmate, or you in six
months. With CI and a protected `main`, it is no longer possible to forget.

One trap to avoid: an agent asked to "add tests" for existing code will often write
tests that simply *assert whatever the code currently does* — enshrining bugs rather
than catching them. That is why step 1 asks *where could this be wrong* before asking
for a test. **You decide what must be true; the agent writes the tedious parts;** you
review tests with the same care as implementations.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Autonomy is purchased with verification

The single highest-leverage practice in agentic coding: **make verification
executable.** Agents perform dramatically better when they can check their own
output — running tests, comparing against known values, validating properties —
instead of relying on you as the only feedback loop. Include test cases in the
prompt; point at symptoms, not just fixes ("fix the root cause and verify — don't
suppress the error"); for analyses, demand printed evidence. And tests are cheap now:
ask for them with every feature, ask for data-validation tests on your actual dataset
(expected columns, value ranges, unique IDs, row counts across merges), ask the agent
what inputs would break its own function.

The more trustworthy your checks, the more autonomy you can safely grant. Scale the
checking to the stakes — and choose the tier *explicitly*, before you start:

| Tier | Example | Minimum verification |
|------|---------|----------------------|
| Throwaway | one-off plot, scratch script | Read the diff; eyeball the output |
| Working code | lab-internal pipeline, reusable utils | Tests pass in CI; you review the diff; data-property checks printed |
| Load-bearing | results in a paper, shared package, anything cited | All of the above + comparison to a source of truth + a second human |

::::::::::::::::::::::::::::::::::::: keypoints

- Checking is the bottleneck: agents multiply commits far more than releases, and unreviewed merges rise. The scarce skill is verification.
- Established practice still rules: know your data, compare to a source of truth, ask a colleague, know what your model is telling you, reproduce the result. Only the typing moved.
- Cheap checks catch expensive mistakes: shuffle labels, print the baseline, assert no sample in both splits, hunt duplicates, vary the seed.
- Split by the unit that repeats, and assert it. A confident, clean-running 0.91 can be a 0.58 on unseen subjects.
- Review diffs by hunting for decisions you didn't make, and make the agent list its own assumptions.
- Leave evidence in the repo and point the agent at it; it reads figures and metrics, but only the ones you name — and you check every number it cites.
- Make verification automatic: tests in CI, a context-file rule, a protected `main`. Autonomy is purchased with verification.

::::::::::::::::::::::::::::::::::::::::::::::::
