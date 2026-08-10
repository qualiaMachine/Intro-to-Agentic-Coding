---
title: "Words of Caution: Safety, Security, and Policy"
teaching: 12
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- What can an agent actually access on my machine, and why does that matter?
- How do I keep credentials and restricted data away from AI tools?
- Which protections are guarantees, and which are just layers?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Keep secrets out of local plaintext files entirely, injecting them at runtime instead.
- Treat permissions and sandboxing as defense-in-depth layers, not guarantees.
- Use git hygiene (clean state, branches, small frequent commits) as your primary recovery mechanism.
- Apply institutional data policies before pointing an agent at any project.

::::::::::::::::::::::::::::::::::::::::::::::::

## An agent runs with *your* permissions

When you launch an agentic tool from your terminal or IDE, it operates with your user
account's full filesystem and shell access. It can read your SSH keys, your `.env`
files, your notes — anything you can. This is not unique to any one tool; it is what
"shell access" means.

Agents also *automatically scan for context*. That is their job: to read your project
and figure out what's relevant. A credentials file sitting in your working directory is,
from the agent's point of view, just more context.

## Secrets never touch disk

The single most effective protection: **a secret that isn't on disk can't be read,
echoed, committed, or exfiltrated** — by an agent, by malware, or by you at 11pm.

- Don't store passwords or API keys in `.env` files, JSON configs, or shell profiles.
- Use a secrets manager (many universities, including UW–Madison, provide 1Password for
  free) or your OS keyring, and inject values at runtime.

Compare these two patterns:

```python
# BAD: secret lives in plaintext on disk; any process (or agent) can read it
API_KEY = open(".env").read().split("=")[1]
```

```python
# GOOD: secret lives in the OS keyring, fetched only at call time
def get_oauth_token() -> str:
    """Obtain OAuth token for UW-Madison API using credentials from keyring."""
    url = "https://api.wisc.edu/oauth/token"
    response = httpx.post(
        url,
        data={
            "client_id": keyring.get_password("UW_API", "UW_API_KEY"),
            "client_secret": keyring.get_password("UW_API", "UW_API_SECRET"),
            "grant_type": "client_credentials",
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]
```

The second version can be read aloud by an agent, pasted into a chat, or committed to a
public repo without leaking anything.

## Layers, not guarantees

Modern agents ship real protections — Claude Code asks permission before writes and
shell commands, supports deny rules for sensitive paths, and has an OS-level sandbox
that restricts filesystem and network access. Configure them. But understand what they
are:

- Deny rules can be subtly mis-written, and an allowed command (like `cat`) can read a
  file that a read-rule covers.
- Instruction files ("never touch `~/.ssh`") are advisory — followed in good faith, not
  enforced by the system.
- Prompt injection is real: a malicious README, issue body, or data file can contain
  hidden instructions that try to hijack the agent.

Think of it as defense in depth: secrets off disk *first*, then sandbox, then deny
rules, then permission prompts. Each layer reduces the odds; none is a vault door.

## Git is your seatbelt

Version control is what makes agent mistakes cheap instead of catastrophic:

- **Start from a clean git state.** If the agent goes sideways, `git diff` shows you
  exactly what it did and `git restore` undoes it. A dirty working tree means agent
  changes and your changes get tangled together.
- **Always work on a branch.** Never let an agent commit directly to `main`.
- **Commit small and often.** Each commit is a save point you can revert to.
- **Review and test before committing** — or, if you let the agent commit freely as it
  works, review the full diff at the PR stage. Either workflow is fine; what's
  non-negotiable is that *someone* (you, a colleague, or CI) reads the code before it
  lands on `main`.

## Institutional data policies apply — fully

AI tools do not get an exemption from your institution's data rules. At UW–Madison
specifically (adapt to your own institution):

- Follow UW–Madison, UW System, and Board of Regents GenAI policies; DoIT maintains an
  overview of policies and vetted tools at [it.wisc.edu/ai](https://it.wisc.edu/ai/).
- UW does not currently have a data agreement with Anthropic, so **restricted data stays
  off**: no student records (FERPA), health data (HIPAA/PHI), unpublished sensitive
  research, CUI, export-controlled data, or anything under a DUA that prohibits
  third-party processing.
- General, non-sensitive research code is fine. When in doubt, ask your IT office
  *before* the session, not after.

Remember: your code and prompts are sent to the model provider's servers for inference.
Don't run an agent on a machine where restricted data is stored — anything in the
workspace can end up in a prompt.

Policies tell you what *you* may send to a provider. The next episode turns the
question around: how much should you trust the provider — and the packages and models
your agent pulls in along the way?

::::::::::::::::::::::::::::::::::::: callout

## On individual/consumer AI plans, check your training settings

Commercial and enterprise API terms typically prohibit training on your data. Consumer
plans (free or personal subscriptions) often make it a *setting* — sometimes defaulted
on. Whatever tool you use, find the data/model-training toggle in your account settings
and make a deliberate choice.

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: keypoints

- Agents run with your permissions and scan your workspace for context — assume anything on disk in plaintext can be read.
- The only secret an agent can't leak is one that isn't there: use a secrets manager or keyring and inject at runtime.
- Permissions, sandboxing, and deny rules are valuable layers, not guarantees; prompt injection is a real attack surface.
- Clean git state, branches, and small frequent commits make agent mistakes cheap to undo.
- Institutional data policies apply unchanged: restricted data stays away from unvetted AI services.

::::::::::::::::::::::::::::::::::::::::::::::::
