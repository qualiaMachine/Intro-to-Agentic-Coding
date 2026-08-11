---
title: "Verification and Review: No Escaping Good Data Science"
teaching: 20
exercises: 10
---

:::::::::::::::::::::::::::::::::::::: questions

- Why isn't "the code runs and the score is high" enough?
- What does verification look like when an agent wrote the code?
- How much checking is enough, and when can I relax?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Apply established data science verification practices (know your data, compare to a source of truth, ask a colleague) to agent-generated analyses.
- Detect a data leakage bug in code that runs cleanly and scores well.
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

## Worked example: leakage that scores great

Data leakage is the perfect case study because it produces code that runs clean, scores
great, and is wrong. Ask an underspecified agent for "a model with good accuracy on
this dataset" and you may get something like:

```python
import numpy as np
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

X, y = datasets.load_breast_cancer(return_X_y=True)

# Standardize and select the 10 best features
X = StandardScaler().fit_transform(X)          # fit on ALL data
X = SelectKBest(f_classif, k=10).fit_transform(X, y)   # selected using ALL labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=5000).fit(X_train, y_train)
print(f"Test accuracy: {model.score(X_test, y_test):.3f}")
```

No errors. No warnings. A high score. And the evaluation is contaminated: the scaler
and — much worse — the feature selector were fit on the *entire* dataset, labels
included, before the split. The "held-out" test set helped choose the features it is
now being used to evaluate. On this dataset the inflation is modest; with wide data
(genomics, imaging radiomics, any p ≫ n problem) this exact bug can turn noise into a
publishable-looking result.

The fix is structural, not cosmetic: split first, and fit every preprocessing step on
training data only (in scikit-learn, put the scaler and selector in a `Pipeline` so
cross-validation refits them per fold).

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

## Give the agent a way to check itself

The single highest-leverage practice in agentic coding: **make verification executable**.
Agents perform dramatically better when they can check their own output — run tests,
compare against known values, validate properties — instead of relying on you as the
only feedback loop.

- Include test cases in the prompt: "Write `validate_email`. Cases:
  `user@example.com → True`, `invalid → False`, `user@.com → False`. Run the tests."
- Point at symptoms, not just fixes: "The build fails with this error: [paste]. Fix the
  root cause and verify the build succeeds — don't suppress the error."
- For analyses, demand printed evidence: row counts before/after joins, class balance,
  train/test overlap checks, a baseline model's score next to the fancy one.

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
than catching them. That's why Exercise 3 had you write the contract first. The
division of labor that works: **you decide what must be true** (the properties, the
invariants, the known answers); **the agent does the tedious part** (fixtures,
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

## Exercise 3: Test as contract (10 minutes)

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
- Make verification executable — tests, printed checks, baselines — because autonomy is purchased with verification.
- Agents make tests cheap: ask for them with every feature and for your data's properties. You define what must be true; the agent writes the tedious parts; you review tests like implementations.
- Choose your verification tier (throwaway / working / load-bearing) explicitly, before you start.

::::::::::::::::::::::::::::::::::::::::::::::::
