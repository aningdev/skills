# The Store

The store is a skill, `~/.agents/observe-result/`, so what's learned travels as one folder and every agent tool loads it like any other skill. Agents only read it; only the observer writes it.

```
~/.agents/observe-result/
├── SKILL.md                 the principles: what every agent reads before recommending or deciding
├── references/roles/<role>.md   lessons for one role
└── .observer/               the observer's working data, never read by other agents
    ├── state.json           per session: the byte offset read to, whether an agent ran it; fingerprints of rounds taken
    ├── inbox.jsonl          rounds not yet judged (digest adds them)
    ├── rounds/YYYY-MM.jsonl judged rounds, moved by `digest.py --archive` after a confirmed report
    ├── proposals.md         changes waiting for the user
    └── metrics.md           one row per run
```

A round is `ts · tool · project · session · source · prompt · reply · ref`, the prompt and reply as raw text.

## SKILL.md

Keep the frontmatter valid: `name: observe-result`, and a description with no `: ` in it, saying it's how the user decides and to read it before recommending or deciding on their behalf. After writing, check it with `skills-ref validate`.

The body is one short intro, then principles grouped by area, short enough to scan before every recommendation:

```md
### Scope

- **Ship the smallest first version; don't pre-build settings, capabilities, or folders.**
  Example: provider setup asks only for credentials; detailed model parameters wait for custom providers.
  _6 sightings · last 2026-11-13 · AgentChat, dsh-bot, grill-me-runner, skills_
```

A principle seen once ends its metadata with `(weak)`. One folded into a skill or role is removed, with no tombstone left behind.

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
