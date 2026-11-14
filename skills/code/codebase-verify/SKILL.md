---
name: codebase-verify
description: Prove your own change does what was agreed before calling it done. Walk each acceptance criterion as its user would, keep the evidence, script the walkthroughs worth repeating, and never claim done, fixed, or passing without fresh evidence. Use when you're about to call a change, a fix, or a config change done. Not for setting up checks, hooks, or CI (codebase-setup), or judging someone else's change (codebase-review).
---

# Codebase Verify

Verification is the author's own proof, before anyone else looks: the change does what was agreed, seen from where its user stands. The goal is the standard; the way is a recommendation.

## Acceptance

**Goal:** before a change is called done, someone has used it the way its user will, and seen it do what was agreed.

**Why:** a change is done when the user's goal is met, not when tests are green. Tests written for their own sake check the code against itself; acceptance checks it against the agreement, from where the user stands. That's the only check that catches "works as coded, not as asked".

**A way that works**, for each acceptance criterion (where criteria come from and how they're written is in the `codebase-docs` skill):

1. **Do what the user would do.** Run the real thing and walk the criterion's path, with realistic data, including the paths they'd hit when things go wrong.
2. **Look where they'd look.** Judge by what the user sees, not internal state.
3. **Keep the evidence**, before and after. It goes in the PR's `## Evidence`, or the commit body when the branch merges without one.
4. **Script the walkthroughs worth repeating.** When a criterion guards something that could quietly break again, turn its walkthrough into a script that drives the same public surface and runs under `test`, so CI walks it on every change. A one-off check can stay manual, with its evidence.

**Scale it to the change.** A typo fix needs a glance at the result; a new flow needs every criterion walked with evidence. Let the size and risk of the change decide how much walking and evidence it gets.

**Walk it somewhere disposable.** A walkthrough or test never reads or writes the user's real data, home directory, or services; point it at a temporary directory or a sandbox, and check that it did before trusting the result.

**When you can't walk it**, because you lack a browser, credentials, or a running environment, say exactly what's missing, mark the criterion manual, and hand the walk to the user. Never let something else stand in for the evidence.

Where the scripts live, and how many to keep, is a judgement call; one folder per feature in `tests/`, named in the terms of `docs/GLOSSARY.md`, keeps them easy to find. There's no required test layer and no coverage target. The measure is whether you'd trust the criterion to a real user.

### Evidence before claims

Never say done, fixed, or passing without having just run what proves it and read its output. "Should work", an earlier run, or a sub-agent's report of success isn't evidence. Walk the criteria one by one; a green test run doesn't stand in for the checklist.

## Asking the user

Find facts yourself. Bring the user only the decisions that change the outcome, all at once, each with your recommended answer. Never assume silently.
