---
title: "Verification and Review: No Escaping Good Data Science"
teaching: 20
exercises: 20
---

:::::::::::::::::::::::::::::::::::::: questions

- Why isn't "the code runs and the score is high" enough?
- What does verification look like when an agent wrote the code?
- Which cheap checks catch the expensive mistakes?
- How much checking is enough, and when can I relax?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Apply established data science verification practices (know your data, compare to a source of truth, ask a colleague) to agent-generated analyses.
- Detect a data leakage bug in code that runs cleanly and scores well.
- Run cheap sanity checks — label shuffling, baselines, overlap and duplicate checks — that expose broken evaluations.
- Review an agent's diff by hunting for decisions you didn't make.
- Give an agent an executable way to check its own work, including tests that encode data properties.
- Choose a verification tier proportional to the stakes of the result.

::::::::::::::::::::::::::::::::::::::::::::::::

## Established practice comes first

Before AI enters the picture, research computing already had an answer to "how do I know
this analysis is right?":

- **Know your data.** Explore it before modeling it. Plot distributions. Find the
  outliers and decide what they are. Know your features — units, ranges, missingness,
  how they were collected. Check class balance. Look at actual rows.
- **Compare to a source of truth.** A published baseline, a hand-computed subset, a
  simpler method you trust, a positive and negative control.
- **Ask a colleague.** Code review and "does this number seem plausible to you?" catch
  what self-review misses.
- **Know what your models are telling you.** Inspect coefficients or feature
  importances; if the strongest predictor makes no scientific sense, that's a finding
  about your pipeline, not about nature.

None of this changed. **There is no escaping good data science practice** — the agent
didn't absorb these responsibilities when it took over the typing. What changed is
speed: you can now generate a plausible, clean-running, well-scoring analysis in
minutes. Iteration is easier and results come faster — which also means you can be
*misled* faster. Your skepticism has to keep up with the pace.

## Worked example: it runs clean and scores great

Ask an underspecified agent for "a model with good accuracy on this dataset" and you
may get something like the code below. Before reading on, try the exercise.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Spot the flaw (5 minutes)

This code runs without errors or warnings and reports high accuracy. What, if
anything, is wrong with the evaluation?

```python
import numpy as np
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X, y = datasets.load_breast_cancer(return_X_y=True)

# Standardize and select the 10 best features
X = StandardScaler().fit_transform(X)
X = SelectKBest(f_classif, k=10).fit_transform(X, y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=5000).fit(X_train, y_train)
print(f"Test accuracy: {model.score(X_test, y_test):.3f}")
```

:::::::::::::::::::::::: solution

## The leak

The evaluation is contaminated by **data leakage**: the scaler and — much worse — the
feature selector were fit on the *entire* dataset, labels included, *before* the
split. The "held-out" test set helped choose the very features it is now being used
to evaluate.

On this dataset the inflation is modest; with wide data (genomics, imaging radiomics,
any p ≫ n problem) this exact bug can turn pure noise into a publishable-looking
result. The fix is structural, not cosmetic: split first, and fit every preprocessing
step on training data only — in scikit-learn, put the scaler and selector inside a
`Pipeline` so cross-validation refits them per fold.

If you didn't spot it: that's the point. Nothing about this code *looks* wrong, no
error fires, and the score rewards you for not looking harder.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: callout

## Why agents are prone to this — and why you might not catch it

Leakage-style bugs are exactly the *plausible average case* failure from the previous
episode: the code pattern appears all over training data (and all over real notebooks),
and nothing about it looks wrong. The agent optimizes for "task apparently completed" —
clean run, high score — and both boxes are checked. If your review process is also
"does it run? is the score good?", you and the agent share the same blind spot.

Assume nothing; verify everything. A surprisingly *good* result deserves the
same suspicion as a surprisingly bad one — arguably more, because you're motivated to
believe it.

::::::::::::::::::::::::::::::::::::::::::::::::

## Cheap sanity checks that catch expensive mistakes

You don't need a heavyweight process to catch most broken evaluations. A handful of
checks, each a few lines an agent will happily write for you, expose whole classes of
silent failure:

- **Shuffle the labels and re-run.** With `y` randomly permuted, a sound pipeline
  should collapse to chance-level performance. If it still scores well, information is
  leaking somewhere — through preprocessing, duplicated rows, or an evaluation bug.
  This is the single highest-value five-minute check in applied ML.
- **Beat a dumb baseline, on purpose.** Always report the majority-class (or mean
  predictor) score next to your model's. A 94% accuracy stops being impressive when
  the majority class is 92% of the data.
- **Check train/test overlap.** Assert that no sample identifier appears in both
  sets — and think about what "same sample" means for your data: repeated measures of
  one patient, tiles from one image, or sequences from one organism belong on the
  *same* side of the split (group-wise splitting), or you've built a subtler leak.
- **Hunt duplicates before splitting.** Duplicated or near-duplicated rows straddling
  the split are leakage without any code bug at all.
- **Vary the seed.** If the headline metric swings wildly across a few random seeds,
  you have a variance problem, not a result.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Break your own evaluation (5 minutes)

Take the modeling pipeline from the specification episode's exercise (or the leaky
code above, fixed or not) and ask your agent:

> Add a sanity check: rerun the exact same pipeline with the labels randomly shuffled
> (use a fixed seed) and report both scores side by side. Also print the
> majority-class baseline.

1. Did the shuffled-label score collapse to roughly chance? If not, work with the
   agent to find the leak.
2. How does your real score look next to the majority-class baseline?

:::::::::::::::::::::::: solution

## What you should see

For the (fixed) breast-cancer pipeline: real accuracy well above the ~63%
majority-class baseline, and shuffled-label accuracy near 50–63% (chance-ish, given
class imbalance). If shuffled labels still score high, the usual suspects in order:
preprocessing fit before the split, duplicate rows, or evaluation on training data.
Note what just happened: the *agent* wrote the check in seconds, but *you* knew which
check mattered and what the result should look like. That division of labor is the
whole lesson in miniature.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

## Reviewing the diff: hunt for decisions you didn't make

When you review agent-written analysis code, you're not proofreading syntax — the
code runs. You're hunting for **decisions you didn't make**. The high-yield places to
look:

- **Silently dropped or altered rows**: default `dropna()`, inner joins that shrink
  the table, type coercions that turn errors into NaNs. Demand row counts before and
  after every join and filter.
- **Defaults treated as decisions**: imputation strategy, class weights,
  regularization strength, "reasonable" thresholds. Each default the agent accepted
  is a choice you now own — make sure you'd defend it.
- **Metric switcheroos**: you asked about accuracy, the report quietly features F1
  (or vice versa) because the numbers looked better. Check the metric matches the
  question.
- **Suppressed problems**: warnings silenced, `try/except: pass`, errors "fixed" by
  deleting the check. An agent told to "make it run" sometimes does exactly that.

A useful habit that costs one prompt: ask the agent to **list its own assumptions** —
"summarize every choice you made that I didn't specify, and flag the risky ones."
It's the documentation episode's explain-as-verification move, applied to the diff —
and it often surfaces exactly the dropped-rows and default-parameter decisions above.

## Give the agent a way to check itself

The single highest-leverage practice in agentic coding: **make verification executable**.
Agents perform dramatically better when they can check their own output — running tests,
comparing against known values, validating properties — instead of relying on you as the
only feedback loop.

- Include test cases in the prompt: "Write `validate_email`. Cases:
  `user@example.com → True`, `invalid → False`, `user@.com → False`. Run the tests."
- Point at symptoms, not just fixes: "The build fails with this error: [paste]. Fix the
  root cause and verify the build succeeds — don't suppress the error."
- For analyses, demand printed evidence: row counts before/after joins, class balance,
  train/test overlap checks, a baseline model's score next to the fancy one.

And make it the *default*, not a per-session request: put your testing requirements
into the project context file from the planning episode —

```markdown
## Testing requirements
- Run the full test suite (`pytest tests/`) after making changes
- If tests fail, fix them before moving on; never commit failing tests
```

One instruction, written once, means the agent verifies even on the days you forget
to ask. (It's advisory, as always — CI on the pull request is the guaranteed
backstop.)

The more trustworthy your test suite and checks, the more autonomy you can safely grant.
This is the exchange rate at the center of agentic coding: **autonomy is purchased with
verification.**

## Tests are cheap now — write more of them

Here's the flip side, and it's good news: the same tool that makes it easy to generate
questionable analyses makes it *dramatically* cheaper to build the verification that
catches them. Test suites used to be rationed because writing them was tedious; that
constraint is gone. Use the agent to validate, validate, validate:

- **Ask for tests alongside every feature** — edge cases, failure modes, the inputs
  you know are weird ("write tests covering empty input, all-NaN columns, and a
  single-row DataFrame").
- **Ask for data-validation tests** on your actual dataset: expected columns and
  dtypes, value ranges, uniqueness of IDs, row counts across merges — the executable
  version of "know your data."
- **Ask it to probe its own work**: "what inputs would break this function? Write
  tests for them."

One trap to avoid: an agent asked to "add tests" for existing code will often write
tests that simply *assert whatever the code currently does* — enshrining bugs rather
than catching them. That's why the exercise below has you write the contract first.
The division of labor that works: **you decide what must be true** (the properties,
the invariants, the known answers); **the agent does the tedious part** (fixtures,
parametrization, the fifteen edge-case variants). Review tests with the same care as
implementations — they are the specification everything else gets checked against.

## How much verification is enough?

Scale it to the stakes:

| Tier | Example | Minimum verification |
|------|---------|----------------------|
| Throwaway | one-off plot, scratch script | Read the diff; eyeball the output |
| Working code | lab-internal pipeline, reusable utils | Tests pass; you review the diff; data-property checks printed |
| Load-bearing | results in a paper, shared package, anything cited | All of the above + comparison to a source of truth + a second human |

The mistake isn't choosing a low tier — it's choosing it *implicitly*. Decide what
tier a task is before you start, and you'll know when you're done checking.

::::::::::::::::::::::::::::::::::::: challenge

## Exercise: Test as contract (10 minutes)

Instead of hoping the agent avoids leakage, encode the requirement as a test it must
satisfy. Write **one pytest test that encodes a property your data or pipeline must
satisfy**, then ask the agent to make it pass. For example:

```python
def test_no_leakage_in_pipeline():
    """Preprocessing must be fit on training data only."""
    from analysis import build_pipeline, load_data
    X, y = load_data()
    # A leakage-free pipeline's CV score should be computable end-to-end:
    # the pipeline object must contain ALL preprocessing steps.
    from sklearn.model_selection import cross_val_score
    pipe = build_pipeline()
    step_names = [name for name, _ in pipe.steps]
    assert "scaler" in step_names and "select" in step_names, \
        "preprocessing must live inside the pipeline, not outside it"
    scores = cross_val_score(pipe, X, y, cv=5)
    assert scores.mean() > 0.9
```

Then prompt: *"Create `analysis.py` with `load_data()` and `build_pipeline()` so that
`pytest test_analysis.py` passes. Run the tests to confirm."*

Other properties worth encoding, depending on your data: no identifier appears in both
train and test; feature X is always non-negative; row count survives the merge; the
model beats a majority-class baseline.

:::::::::::::::::::::::: solution

## Why this works

You've turned an invisible methodological requirement into an executable contract. The
agent now has a feedback loop that fails loudly when it reaches for the average-case
(leaky) pattern — and you have an artifact that keeps protecting you on every future
change, whether the next edit comes from an agent, a labmate, or you in six months.

Note what you did *not* have to do: trust the agent, or read its mind. The test is the
specification.

:::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Established practice still rules: explore your data, know your features and distributions, compare to a source of truth, know what your model is telling you.
- Faster iteration means faster results *and* faster misleading — clean runs and great scores are not evidence of correctness.
- Leakage is the canonical agentic failure: plausible, silent, and flattering. Split first; fit preprocessing on training data only; be suspicious of good news.
- Cheap checks catch expensive mistakes: shuffle labels, print the dumb baseline, assert no train/test overlap, hunt duplicates, vary the seed.
- Review diffs by hunting for decisions you didn't make — dropped rows, accepted defaults, switched metrics, suppressed errors — and make the agent list its own assumptions.
- Make verification executable — tests, printed checks, baselines — because autonomy is purchased with verification.
- Agents make tests cheap: ask for them with every feature and for your data's properties. You define what must be true; the agent writes the tedious parts; you review tests like implementations.
- Choose your verification tier (throwaway / working / load-bearing) explicitly, before you start.

::::::::::::::::::::::::::::::::::::::::::::::::
