# Skills

| 路径             | 性质                           | 现状                                                                                                                          |
| ---------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `skills/base/`   | 动词、方法论、自身不产出交付物 | grilling、self-grilling、handoff、research                                                                                    |
| `skills/code/`   | 名词、工程概念                 | codebase-setup、codebase-docs、codebase-design、codebase-lang、codebase-verify、codebase-debug、codebase-git、codebase-review |
| `skills/office/` | 名词、办公产物                 | 待建                                                                                                                          |
| `skills/agents/` | 身份、角色                     | code-feature-definer、code-architect、code-builder、code-reviewer、advisor、observer                                          |

## 命令

- `make check`：用 [skills-ref](references/agentskills/skills-ref/README.md) 按 Agent Skills 规范校验 `skills/` 下每个技能（frontmatter 走严格 YAML，冒号等问题会在这里报出）。首次使用先 `git submodule update --init references/agentskills`。改完技能先跑它。
- `make fix`：自动修 lint，并用 ruff 格式化 Python、用 oxfmt 格式化 Markdown/JSON（会改文件，跑完看一眼 diff）。

## 何时读什么

- 术语（Agreement、Walkthrough、Evidence……）：[docs/GLOSSARY.md](docs/GLOSSARY.md)
- 分层、依赖方向、Skill 与 Role 分工、写法：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 边界

- `references/` 只读。
