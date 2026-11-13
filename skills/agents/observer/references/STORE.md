# The Store

The store is a skill, `~/.agents/skills/observe-result/`, so what's learned travels as one folder and every agent tool loads it like any other skill. Agents only read it; only the observer writes it.

```
~/.agents/skills/observe-result/
├── SKILL.md                 fixed: the intro and how to read what's here, copied from this role's assets/
├── references/principles.md the principles, learned and kept by the observer
├── references/roles/<role>.md   lessons for one role
└── .observer/               the observer's working data, never read by other agents
    ├── state.json           per session: the byte offset read to, whether an agent ran it; fingerprints of rounds and memories taken
    ├── inbox.jsonl          rounds not yet judged (digest adds them)
    ├── rounds/YYYY-MM.jsonl judged rounds, moved by `digest.py --archive` after a confirmed report
    ├── proposals.md         changes waiting for the user
    └── metrics.md           one row per run
```

A round is `ts · tool · project · session · source · prompt · reply · ref`, the prompt and reply as raw text.

## SKILL.md

Fixed. It says what the store is, that these are leanings rather than instructions, and where the principles and role lessons are. It comes from [assets/observe-result/SKILL.md](../assets/observe-result/SKILL.md): copy it over when setting up the store or when the template changes, and never edit it in place. What's learned goes in the files below.

## references/principles.md

Principles grouped by area, each in five parts:

```md
## Scope

- **Ship the smallest first version; don't pre-build settings, capabilities, or folders.**
  Why: the user kept cutting first versions back ("只需要提供认证凭证", "首版只提供文件读取、编辑与命令执行").
  How to apply: when proposing a first version of a product, module, or skill, leave out what no current flow needs. Not for scope already agreed.
  Example: provider setup asks only for credentials; detailed model parameters wait for custom providers.
  _6 sightings · last 2026-11-13 · AgentChat, dsh-bot, grill-me-runner, skills_
```

Why carries the user's reason, in their words where short. How to apply says when it applies and where it stops: without a boundary, a principle gets applied everywhere. A principle seen once ends its metadata with `(weak)`. One folded into a skill or role is removed, with no tombstone left behind.

## references/roles/<role>.md

The same entry shape, about how one role decides: what the user keeps correcting it on, and what it gets right.

## .observer/proposals.md

```md
- [ ] **Fold "reuse upstream before building" into codebase-design.** Seen 5 times across 3 projects.
      Target: `skills/code/codebase-design/SKILL.md`.
```

Tick an entry once the user approves and it's applied; delete one they decline.

## .observer/metrics.md

```md
| Run        | Rounds | Adoption   | Kept  | Missed | Unjudged |
| ---------- | ------ | ---------- | ----- | ------ | -------- |
| 2026-11-13 | 244    | 72% (est.) | — (0) | 6      | 0        |
```

Keep each file under 200 lines. No long quotes, secrets, or private people's data.
