---
name: codebase-git
description: Goals and recommended practices for how changes are scoped, committed, branched, merged, and described. Use when scoping a change, writing a commit message, naming a branch, opening or merging a PR, or writing a PR description. Not for reviewing a PR (codebase-review).
---

# Codebase Git

History is read by people and agents who weren't there. The goal: from `git log` alone, anyone can tell what changed and where; from a PR alone, what was agreed and whether it was met. The practices below are recommendations that serve that goal. A project can choose otherwise and record why in `docs/ARCHITECTURE.md`.

## Changes

**Goal:** each step can be read and undone on its own, and each goal is accepted and merged as a whole, without more ceremony than it needs.

Commits are cheap and pull requests aren't, so the fine grain goes into commits:

- **A commit is the smallest step that makes sense alone.** One concern, understandable and revertible by itself. It at least builds, so `git bisect` works; the full `check` has to pass where the branch merges.
- **Delete in the same commit.** The commit that brings in a replacement removes what it replaces: old code, files, flags, and docs. No commented-out code, no `_v2`, `_old`, or `_new` copies, no old and new paths side by side. When a migration really needs both for a while, say when the old one goes.
- **A branch delivers one agreed goal**, as the fewest commits it takes. Split it only when part of it is hard to undo (a schema migration, a public contract, deleting data: merge that part on its own), when the branch would live long enough to drift from `main` (merge it in stages that each work), when the diff grows past what a reviewer, human or agent, can judge accurately, or when several people or agents work on it in parallel. Never split a goal into halves that leave `main` unusable, and don't open a branch for a typo.

## Commits

**Goal:** each commit is one change that a reader understands from its subject line.

**A way that works:** [Conventional Commits](https://www.conventionalcommits.org), `type(scope): subject`.

- **Type** says what kind of change: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `ci`, `chore`.
- **Scope** says where: the package or module (`client`, `route`, `auth`). Leave it out when the change spans the repo.
- **Subject** says what the behaviour now is ("require close above EMA9 for hold"), not what you did ("update logic"), in the language the project's history already uses.
- A body earns its place by explaining why, when the subject can't. A breaking change says so (`!` after the scope) and tells callers what to do.

## Branches and merging

**Goal:** `main` stays healthy, and its history keeps every step readable.

**A way that works:**

- A short-lived branch per goal, named so its scope and topic are obvious (`client/navigator-sections`).
- Rebase merge, so each commit lands on `main` as it was written and the history stays linear. Squash only a branch that is one step anyway.
- Merge once `check` is green, locally or in CI (see the `codebase-setup` skill).
- Open a pull request when it earns one: CI that only runs remotely, collaborators who review, or a record someone will look for. In a repo of your own, a branch whose `check` and review pass can be rebased onto `main` locally and pushed, with the evidence in the commit body.

## Worktrees

**Goal:** changes in flight don't step on each other, and the main checkout stays clean.

Principles:

- **One change, one worktree.** Parallel work gets its own directory and branch, sharing one repository.
- **Don't nest.** If you're already in a worktree, work there.
- **Prefer the tool's own worktree support**; otherwise keep worktrees outside the checkout, so nothing lands inside it.
- **Start from a clean baseline**, so a failure later is yours and not inherited.
- **Clean up after merging**: the worktree and its branch.

## PR descriptions

**Goal:** when there is a pull request, a reviewer who never saw the conversation can check the diff against what was agreed, criterion by criterion.

**A way that works:** the format in [PR-FORMAT.md](references/PR-FORMAT.md), with the acceptance criteria quoted verbatim and each marked with how it's accepted (the Acceptance section of the `codebase-verify` skill).
