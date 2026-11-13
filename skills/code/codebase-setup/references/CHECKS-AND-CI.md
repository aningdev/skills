# Checks, Hooks, and CI

For adding or changing scripts, tool config, git hooks, or CI. The goal is the standard; the way is a recommendation.

### Entry points

**Goal:** one obvious way to check the project and one to run its scripted acceptance, the same on every machine.

**Why:** an agent landing in any project shouldn't have to read CI YAML to learn how to verify its work. A command written in two places will drift.

**A way that works:** three names in every project, whatever the stack: `check` (format, lint, type check), `fix` (autofix what `check` reports), and `test` (the scripted acceptance walkthroughs, plus any other tests the project keeps). `bun run <name>` for TypeScript, `make <name>` elsewhere; what goes behind them follows the recommended toolchain in [SKILL.md](../SKILL.md). In a workspace, members define their own and the root aggregates.

Worth keeping however you get there:

- **Checking doesn't rewrite.** Whatever verifies the project should only read. A check that fixes as it goes passes in CI while hiding the problem.
- **Verify before handing off.** Run `check` and `test` before calling work done; run autofix only when you mean to review what it rewrote.

### Pre-commit hook

**Goal:** catch the cheap mistakes (formatting, obvious lint) before they reach a commit, without slowing anyone down.

**Why:** a slow or flaky hook gets skipped, and then it catches nothing.

Principles:

- **Staged files only**, so it stays fast however big the repo gets. In TypeScript, `vp staged` does this.
- **Autofix is fine here.** It's the one place fixing runs unattended, and only on what's about to be committed.
- **Leave the full `check` and `test` to CI.** A stack without a cheap hook can skip it.

### CI

**Goal:** every change to `main`, and every PR, is verified by the same entry points a person would run, and the answer comes back fast.

**Why:** CI is the shared, impartial answer to "is this healthy?". If it runs different commands than local, the answer stops meaning anything; if it's slow, people merge around it.

Principles:

- **Call the entry points.** CI sets up the toolchain and runs `check` and `test`; it never keeps its own copy of the commands.
- **Install from the lockfile.** A stale lockfile should fail the build, not get quietly updated.
- **Red means not ready.** A failing check is a reason to stop, not something to call "unrelated".
- **Don't spend time on runs nobody will read.** Cancel superseded runs, cache what installs, skip changes that can't break anything, and bound how long a job may hang.
- **Keep actions current.** Use their latest major versions when you touch a workflow.

### Machine over prose

**Goal:** a convention a tool can enforce is enforced by the tool, and the docs only hold what tools can't judge.

**Why:** prose gets skimmed and forgotten; a failing check doesn't. Names, seams, and where a module belongs need judgement; import boundaries, generated-file rules, and banned APIs don't.

**A way that works:** encode the convention (a lint rule, an ignore pattern, a step behind `check`), break it once to see the check fail, then shrink its line in `docs/ARCHITECTURE.md` to a pointer at the rule, or delete it.
