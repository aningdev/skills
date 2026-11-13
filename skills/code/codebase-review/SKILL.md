---
name: codebase-review
description: Review a change along two separate axes, Standards (does it follow the project's conventions and language rules?) and Agreement (does it do what was agreed?). Runs both in fresh parallel sub-agents and reports them side by side. Use when reviewing a PR, a branch, or an area of the codebase, or gating a PR before it merges. Not for finding why something breaks (codebase-debug).
---

Two-axis review of a change:

- **Standards**: does the code follow the project's conventions and the language rules?
- **Agreement**: does the code do what was agreed?

Both axes run as **parallel sub-agents**, each with a fresh context window, so neither inherits the reasoning that wrote the code. This skill then puts their findings side by side. If you can't spawn sub-agents, run the axes one after the other as separate passes, Standards first, and don't let one pass's findings steer the other.

The review doesn't fix anything: it reports, and for a PR it gives a verdict.

## Process

### 1. Check CI

For a PR, check its CI first (`gh pr checks <number>`). Anything red or pending means the verdict is "not yet", whatever the review finds; review anyway, so the author gets everything in one round.

### 2. Pin the diff

Review the PR or branch against its base: `git diff <base>...HEAD` (three-dot, so the comparison is against the merge-base), and `gh pr diff <number>` for a PR. If the user names another fixed point, use that. Confirm the diff is non-empty before going further.

When the caller asks to review an area of the codebase rather than a change, review those files as they stand instead of a diff.

### 3. Collect the Agreement

The acceptance criteria, quoted verbatim, from the PR description's `## Acceptance criteria` (the format in the `codebase-git` skill), any spec in `docs/specs/`, and its linked issues, or wherever the user points. Use the PR's `## Out of scope` to tell scope creep from deliberate omissions.

If there's none, the **Agreement** axis skips and reports "no Agreement available".

### 4. Collect the standards

- `docs/ARCHITECTURE.md` and `docs/GLOSSARY.md`, checked with the list in the `codebase-docs` skill
- The `codebase-lang` skill and the reference for each language in the diff
- The `codebase-setup` skill for entry points, hooks, and CI in the diff, and the `codebase-git` skill for its commits
- A **smell baseline**: Fowler's code smells (_Refactoring_, ch.3), which apply even when the project documents nothing. The project's documented conventions override them, and each one is a labelled judgement call ("possible Feature Envy"), never a hard violation. Skip anything tooling already enforces.

### 5. Run both axes

Each axis gets the diff and only its own inputs, and answers its own question:

- **Standards** gets the standards above. It reports where the diff breaks a documented convention or language rule (citing the rule and `file:line`), any baseline smell, and any structural choice the docs don't cover, as a gap. Breaches are hard findings; smells are judgement calls.
- **Agreement** gets the acceptance criteria verbatim, the author's evidence, and Judging the evidence below. For each criterion it says pass or fail from the user's side, judging the evidence and walking the criterion itself where the evidence is missing or doesn't convince; a criterion marked automated fails without a scripted walkthrough. It also lists behaviour nobody asked for, and criteria that look met but are built wrong.

Keep both reports short and quote what they're judging.

### 6. Report

Present the two reports under `## Standards` and `## Agreement`, lightly cleaned. Do **not** merge or rerank across the axes. End with one line: findings per axis, and the worst issue within each. For a PR, then give the verdict: **merge**, or **not yet** with what stands in the way.

Findings are a report, not a fix: don't change the code. Post them to the PR only when the user asks.

## Judging the evidence

Evidence is convincing when it shows the user's path and the user's view: before and after, same path, the real running thing. When it's missing, shows internals instead, or doesn't match the criterion, walk that criterion yourself. How to walk a criterion as its user would is in the `codebase-verify` skill.

## Why two axes

Code can follow every convention and still build the wrong thing, or build exactly the right thing in a way that breaks the project's shape. Reporting the axes separately stops one from masking the other.
