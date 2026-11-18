# Skills

| 路径             | 性质                           | 现状                                                                                                                          |
| ---------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `skills/base/`   | 动词、方法论、自身不产出交付物 | grilling、self-grilling、handoff、research                                                                                    |
| `skills/code/`   | 名词、工程概念                 | codebase-setup、codebase-docs、codebase-design、codebase-lang、codebase-verify、codebase-debug、codebase-git、codebase-review |
| `skills/office/` | 名词、办公产物                 | 待建                                                                                                                          |
| `skills/agents/` | 身份、角色                     | code-feature-definer、code-architect、code-builder、code-reviewer、advisor、observer                                          |

## 命令

- `make check`：用 [skills-ref](references/agentskills/skills-ref/README.md) 按 Agent Skills 规范校验 `skills/` 下每个技能（frontmatter 走严格 YAML，冒号等问题会在这里报出）。首次使用先 `git submodule update --init references/agentskills references/skillevaluator`，并装好 SkillEvaluator 和 SkillSpector：`uv tool install --python 3.13 'skillevaluator[tier3]==0.9.0'`、`uv tool install --python 3.13 'skillspector @ https://github.com/NVIDIA/SkillSpector/releases/download/v2.13.4/skillspector-2.13.4-py3-none-any.whl'`（`[tier3]` 是 `make live` 要的）。改完技能先跑它。
- `make eval`：跑 [SkillEvaluator](references/skillevaluator/README.md) 完整 Tier 1（含 SkillSpector 安全扫描，约 1 分钟），只出报告不拦截；`make check` 已含它的轻量部分（跳过 security、code-integrity）。已知误报写在 Makefile 注释里。
- `make live SKILL=skills/<layer>/<name>`：跑 SkillEvaluator Tier 3，让 OpenCode 在本机沙箱里分别带技能、不带技能做 `evals/evals.json` 的用例，用 `LIVE_MODEL`（默认 magpie `127.0.0.1:3425` 上的 `opencode-go/deepseek-v4.1-flash`）作答和评分。会调用模型、花钱，每个用例约 3 分钟。首次使用先装好固定版本的 OpenCode：`/opt/homebrew/bin/npm install -g --prefix ~/.local/share/skillevaluator/runtimes/opencode opencode-ai@1.19.5`（shell 里的 `npm` 是 bun 别名，会忽略 `--prefix`）。额外参数用 `LIVE_ARGS` 传，比如 `LIVE_ARGS="--n-attempts 3"`。结果写进技能的 `evals/results/`，这个目录不入库。
- `python3 scripts/darwin_tests.py skills/<layer>/<name>`：给 darwin-skill（`.agents/skills/darwin-skill`，第三方，只读）生成测试集 `test-prompts.json`，取 `evals/evals.json` 里标了 `"split": "dev"` 或 `"holdout"` 的正例，用例只维护在 `evals.json` 一处；生成的文件不入库。
- `make fix`：自动修 lint，并用 ruff 格式化 Python、用 oxfmt 格式化 Markdown/JSON（会改文件，跑完看一眼 diff）。

## 何时读什么

- 术语（Agreement、Walkthrough、Evidence……）：[docs/GLOSSARY.md](docs/GLOSSARY.md)
- 分层、依赖方向、Skill 与 Role 分工、写法：[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 边界

- `references/` 只读。
