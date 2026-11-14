# Skills

[中文](README.zh.md)

A personal library of agent skills for Claude Code, pi, and any agent that reads [Agent Skills](https://agentskills.io). Methods live in skills; roles add a stance and judgement on top; an observer learns how you decide and feeds it back.

| Layer            | What's in it                                                                                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skills/base/`   | Methods that produce no deliverable of their own: `grilling`, `self-grilling`, `handoff`, `research`                                                                                                          |
| `skills/code/`   | Conventions for every code repo, usable with no role installed: `codebase-setup`, `codebase-docs`, `codebase-design`, `codebase-lang`, `codebase-verify`, `codebase-debug`, `codebase-git`, `codebase-review` |
| `skills/agents/` | Roles you call by name: `code-feature-definer`, `code-architect`, `code-builder`, `code-reviewer`, and the cross-domain `advisor` and `observer`                                                              |

Terms are in [docs/GLOSSARY.md](docs/GLOSSARY.md); layering and writing rules in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## From request to merge

```
fuzzy request ──► /code-feature-definer ──► Agreement (acceptance criteria + examples)
                    │ touches terms, stack, or layering
                    ▼
               /code-architect ──► conventions, scaffolding, a list to fix
                    │
                    ▼
               /code-builder ──► implementation + walking each criterion as the user + Evidence ──► PR
                                                                                                  │
                                                                                                  ▼
                                                                                   /code-reviewer ──► merge / not yet
```

When something breaks, just describe it: `codebase-debug` loads on its own, finds the cause, then fixes it. Every step also works alone; a missing role leaves the others and the `codebase-*` skills working.

## Which role when

Call a role by name (`/name`) to have the agent take it on, or let the agent pick it up when the work matches; `codebase-*` skills load on their own when the situation calls for them.

| You want to                                                                | Call                    | Conventions it draws on                                       |
| -------------------------------------------------------------------------- | ----------------------- | ------------------------------------------------------------- |
| Talk something through, understand it, and decide, in code or not          | `/advisor`              |                                                               |
| Pin down what to build and what "done" means                               | `/code-feature-definer` | codebase-docs                                                 |
| Start a project, align it with conventions, shape its structure or tooling | `/code-architect`       | codebase-setup, codebase-docs, codebase-design, codebase-git  |
| Build what was agreed                                                      | `/code-builder`         | codebase-lang, codebase-design, codebase-verify, codebase-git |
| Gate a change before it merges                                             | `/code-reviewer`        | codebase-review                                               |
| Audit how agents decide for you, and learn from it                         | `/observer`             |                                                               |

## Teaching agents how you decide

Every question an agent puts to you is a sample: which recommendations you take, which you override, which of its own calls you undo. Grilling rounds open with `🎯 [<role>] <goal>` and self-grilling hands off `Calls I made as <role>:`, so each decision says who made it. Now and then (session logs are kept 30 days by default) call `/observer`. It:

1. Copies new question rounds and your replies from local Claude Code, pi, Codex, grok, and dsh sessions, plus Claude Code's feedback memories and the friction `/insights` found, with `scripts/digest.py`. Only what's new is read.
2. Reads them and distills your principles (rule, why, how to apply, example, sightings) into the `observe-result` skill at `~/.agents/skills/observe-result/`, a regular skill every agent loads read-only, and that you can carry anywhere as one folder.
3. Reports adoption, kept calls, and missed questions, plus proposals that crossed their threshold.

Nothing is written until you confirm the report, and skills change only when you approve each proposal.

## Names that look alike

| Name                         | What it is                                                                                    |
| ---------------------------- | --------------------------------------------------------------------------------------------- |
| `/code-reviewer`             | Role: the independent gate, gives merge / not yet                                             |
| `codebase-review`            | Convention: the two-axis review method, loads on its own                                      |
| `/code-review`               | Claude Code's built-in command, unrelated to this library                                     |
| `advisor` (Claude Code tool) | Claude Code's built-in second-opinion tool; `/advisor` here is the role that helps you decide |

## Install

```bash
git clone --recurse-submodules https://github.com/aningdev/skills.git
ln -s "$PWD/skills/code/codebase-setup" ~/.claude/skills/codebase-setup   # one link per skill, or use your skill manager
make check   # validates every skill against the Agent Skills spec, plus script and Markdown rules
```

## Acknowledgements

This library was built by reading, borrowing from, and internalising these projects. Thank you to their authors.

- [mattpocock/skills](https://github.com/mattpocock/skills) (MIT)
- [obra/superpowers](https://github.com/obra/superpowers) (MIT)
- [tw93/Waza](https://github.com/tw93/Waza) (MIT)
- [agentskills/agentskills](https://github.com/agentskills/agentskills) (Apache-2.0)
- [huacnlee/noop](https://github.com/huacnlee/noop)

## License

[MIT](LICENSE)
