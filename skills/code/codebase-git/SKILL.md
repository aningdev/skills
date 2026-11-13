---
name: codebase-git
description: Goals and recommended practices for how changes are committed, branched, merged, and described. Use when writing a commit message, naming a branch, opening or merging a PR, or writing a PR description. Not for reviewing a PR (codebase-review).
---

# Codebase Git

History is read by people and agents who weren't there. The goal: from `git log` alone, anyone can tell what changed and where; from a PR alone, what was agreed and whether it was met. The practices below are recommendations that serve that goal. A project can choose otherwise and record why in `docs/ARCHITECTURE.md`.

## Commits

**Goal:** each commit is one change that a reader understands from its subject line.

**A way that works:** [Conventional Commits](https://www.conventionalcommits.org), `type(scope): subject`.

- **Type** says what kind of change: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `ci`, `chore`.
- **Scope** says where: the package or module (`client`, `route`, `auth`). Leave it out when the change spans the repo.
- **Subject** says what the behaviour now is ("require close above EMA9 for hold"), not what you did ("update logic"), in the language the project's history already uses.
- A body earns its place by explaining why, when the subject can't. A breaking change says so (`!` after the scope) and tells callers what to do.

## Branches and merging

**Goal:** `main` stays healthy and its history stays readable, one entry per agreed change.

**A way that works:**

- A short-lived branch per change, named so its scope and topic are obvious (`client/navigator-sections`).
- Squash merge, so `main` gets one commit per PR, titled in commit format with its PR number.
- Merge once CI is green (see the `codebase-setup` skill).

## Worktrees

**Goal:** changes in flight don't step on each other, and the main checkout stays clean.

Principles:

- **One change, one worktree.** Parallel work gets its own directory and branch, sharing one repository.
- **Don't nest.** If you're already in a worktree, work there.
- **Prefer the tool's own worktree support**; otherwise keep worktrees outside the checkout, so nothing lands inside it.
- **Start from a clean baseline**, so a failure later is yours and not inherited.
- **Clean up after merging**: the worktree and its branch.

## PR descriptions

**Goal:** a reviewer who never saw the conversation can check the diff against what was agreed, criterion by criterion.

**A way that works:** the format in [PR-FORMAT.md](references/PR-FORMAT.md), with the acceptance criteria quoted verbatim and each marked with how it's accepted (the Acceptance section of the `codebase-verify` skill).
