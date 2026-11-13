---
name: codebase-debug
description: Find out why something breaks, then fix the cause, not the symptom. Use for errors, crashes, failing checks, regressions, or performance drops. Not for building new features (codebase-docs for what to build) or reviewing a change (codebase-review).
---

# Codebase Debug

The job is to explain why it breaks, not to make the error go away. A fix without a cause is a guess that happens to pass.

## Principles

- **Reproduce first**, the way the user hit it. If you can't, say so and what you tried; don't fix what you can't see.
- **Narrow it down** until every remaining step of the reproduction matters, and you know where on the path it goes wrong. Read the code there rather than guessing at it.
- **One hypothesis at a time.** Predict what you'll see if it's true, run the one check that tells, and drop it when the check surprises you.
- **Fix the cause, not the symptom.** The smallest change that removes it, following `docs/ARCHITECTURE.md` and the `codebase-lang` skill. Don't widen a catch, add a retry, or bump a timeout to make the error go away, and don't refactor on the way.
- **Walk it again.** See the user's path work, per the `codebase-verify` skill; script it if it could quietly break again.
- **Say what you don't know.** Report the root cause, the fix, and the evidence. If you couldn't find the cause, say so, and what you ruled out.

## When the code is right

Sometimes the behaviour is exactly what was asked for, and the request itself is wrong. Then stop: the bug is in the goal, not the code. Say so, and bring it back to the user as a change to the Agreement (the `codebase-docs` skill), with what you'd recommend.

## Asking the user

Find facts yourself. Bring the user only the decisions that change the outcome, all at once, each with your recommended answer. Never assume silently.
