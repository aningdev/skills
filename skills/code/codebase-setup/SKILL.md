---
name: codebase-setup
description: Principles and recommended defaults for a project's engineering shell and for setting a repo up, covering toolchain, the check, fix, and test entry points, hooks, CI, moving conventions into tools, the files a project needs, and what AGENTS.md holds, plus an evidence-based check of an existing repo. Use when starting a project, setting up or re-checking a repo, changing its stack, or touching scripts, tool config, hooks, or CI. Not for proving a change does what was agreed (codebase-verify).
---

# Codebase Setup

These are principles with recommended defaults, not a template to stamp out. Follow the principle every time; take the recommendation unless the project has a reason not to, and when it does, record the reason in `docs/ARCHITECTURE.md`.

Project choices come first. A project that already decided keeps its decision.

## Principles

- **Follow the language's own conventions.** Each ecosystem already has a standard layout, package manager, and toolchain. Use it rather than importing another ecosystem's habits.
- **A workspace only when there are several things to ship.** Several apps, or packages shared between them, earn a workspace. A single app or library stays a single package in its language's standard layout.
- **One tool per job, one config home.** One formatter, one linter, one type checker, one test runner, and their config in the project's main manifest or tool config file. No overlapping tools, and no stray per-tool config files when the main file can hold it.
- **Every file is formatted.** Code is formatted by its language's formatter. Docs and config (Markdown, JSON, YAML) are formatted too, by the same tool in every repo.
- **One entry point, three names.** Every project exposes `check`, `fix`, and `test`, whatever runs behind them. Their contract is in [CHECKS-AND-CI.md](references/CHECKS-AND-CI.md).
- **Pin what installs.** One lockfile per repo, committed, and CI installs from it.

## Recommended toolchains

| Language       | Recommended                                      | Worth knowing                                                                                                                                      |
| -------------- | ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TypeScript** | bun + vite-plus (`vp`)                           | `vp` covers format, lint, type check, and test; don't stack tsc, eslint, prettier, or biome on top. Workspaces share versions through the catalog. |
| **Python**     | uv + ruff + ty + pytest                          | Don't turn on fix-on-run in ruff config: it makes `check` rewrite source.                                                                          |
| **Rust**       | cargo + rustfmt + clippy                         | Clippy warnings fail `check`. Set `rust-version`, so the MSRV is a decision.                                                                       |
| Docs & config  | `vp fmt` in TypeScript projects, oxfmt elsewhere | Markdown, JSON, YAML                                                                                                                               |

Entry points are `package.json` scripts in TypeScript and a `Makefile` elsewhere. A project mixing languages takes the toolchain of its main app, and the others join as members with their own conventions intact (Rust crates in a bun workspace stay a Cargo workspace).

## By scenario

Read the file for what you're doing:

- **Setting up a repo**, new or existing, or re-running setup: [SETTING-UP.md](references/SETTING-UP.md). What a project needs, what `AGENTS.md` holds, and the explore, propose, confirm, write flow.
- **Changing scripts, tool config, hooks, or CI**: [CHECKS-AND-CI.md](references/CHECKS-AND-CI.md). The entry points, the pre-commit hook, CI, and moving conventions into tools.
- **Checking an existing repo**: [CHECKING.md](references/CHECKING.md). An evidence-based audit, reported before anything changes.

## Asking the user

Find facts yourself. Bring the user only the decisions that change the outcome, all at once, each with your recommended answer. Never assume silently.
