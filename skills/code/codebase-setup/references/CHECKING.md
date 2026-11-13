# Checking a Repo

Audit an existing repo's shape and agent setup, report first, and change nothing until the user confirms.

Compare the repo with the principles and toolchain in [SKILL.md](../SKILL.md), [SETTING-UP.md](SETTING-UP.md), and [CHECKS-AND-CI.md](CHECKS-AND-CI.md). A difference is a finding only when it ties to evidence:

- **Risk**: a path that can lose data, spend money, publish, or leave hard-to-undo state.
- **An unreachable constraint**: something an agent must know, can't recover from the code, and won't reach when it matters.
- **Failure**: user corrections, repeated fix chains, stale generated files, broken references.
- **A verifier gap**: an outcome that matters with no check at the layer where it fails.

Anything else, a missing file, a long doc, many skills, is informational. For each finding, say whether it's **Drift** (nobody chose it: align it) or a **Choice** (the project needs it: keep it, and make sure `docs/ARCHITECTURE.md` says why), and write it as:

```
- <symptom> (file:line)
  Why: <one line>
  Action: <the exact edit or command>
```

Anything you can't tell apart is a decision for the user, not a fix.
