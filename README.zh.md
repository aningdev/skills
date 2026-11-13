# Skills

[English](README.md)

个人 Agent 技能库，适用于 Claude Code、pi，以及任何读取 [Agent Skills](https://agentskills.io) 的 Agent。方法放在技能里；角色在此之上加上立场与判断；观察者学习你怎么做决定，再反馈回去。

| 层               | 内容                                                                                                                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `skills/base/`   | 方法论，自身不产出交付物：`grilling`、`self-grilling`、`handoff`、`research`                                                                                                          |
| `skills/code/`   | 每个代码仓库的规范，不装角色也能独立用：`codebase-setup`、`codebase-docs`、`codebase-design`、`codebase-lang`、`codebase-verify`、`codebase-debug`、`codebase-git`、`codebase-review` |
| `skills/agents/` | 按名字调用的角色：`code-feature-definer`、`code-architect`、`code-builder`、`code-reviewer`，以及跨领域的 `observer`                                                                  |

术语见 [docs/GLOSSARY.md](docs/GLOSSARY.md)，分层与写法见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 从需求到合并

```
模糊的需求 ──► /code-feature-definer ──► Agreement（验收标准 + 例子）
                    │ 涉及术语、栈、分层
                    ▼
               /code-architect ──► 约定、骨架、要修的清单
                    │
                    ▼
               /code-builder ──► 实现 + 按用户路径走查 + Evidence ──► PR
                                                                     │
                                                                     ▼
                                                              /code-reviewer ──► merge / not yet
```

出了问题时直接描述现象，`codebase-debug` 会自动加载，查根因再修复。每一步都可以单独用；缺了哪个角色，其余角色和 `codebase-*` 照样能工作。

## 什么时候用哪个角色

角色要**手动调用**（敲 `/名字`），`codebase-*` 技能由 AI 按场景**自动加载**。

| 你想要                                  | 调用                    | 会用到的规范                                                  |
| --------------------------------------- | ----------------------- | ------------------------------------------------------------- |
| 把一个想法说清楚，定下做成什么样算完成  | `/code-feature-definer` | codebase-docs                                                 |
| 新建项目、对齐规范、梳理结构、改工具链  | `/code-architect`       | codebase-setup、codebase-docs、codebase-design、codebase-git  |
| 按约定把功能做出来                      | `/code-builder`         | codebase-lang、codebase-design、codebase-verify、codebase-git |
| 合并前把关                              | `/code-reviewer`        | codebase-review                                               |
| 审计 Agent 替你做决定的情况，并从中学习 | `/observer`             |                                                               |

## 让 Agent 更懂你

Agent 问你的每一道题都是样本：你采纳了哪些推荐、推翻了哪些、它自己拍板的哪些被你改回来。grilling 每轮以 `🎯 [<角色>] <目标>` 开头，self-grilling 交付时写 `Calls I made as <角色>:`，所以每个决定都标明了是谁做的。隔一段时间（会话记录默认只留 30 天）调用 `/observer`，它会：

1. 用 `scripts/digest.py` 把本机 Claude Code 和 pi 会话里的每一轮提问连同你的回复、以及 Claude Code 的 feedback 记忆和 `/insights` 总结的摩擦拷出来，只读新增的部分。
2. 读这些内容，把你的判断原则（规则、Why、How to apply、例子、出现次数）提炼进技能 `observe-result`（`~/.agents/skills/observe-result/`）。它是普通技能，各 Agent 只读加载，也可以整个文件夹带走。
3. 报告采纳率、自决保留率、漏问数，以及达到门槛的改进提议。

都先出报告，你确认后才写入；改技能要你逐条批准。

## 容易混的名字

| 名字              | 是什么                                 |
| ----------------- | -------------------------------------- |
| `/code-reviewer`  | 角色：独立把关人，给出 merge / not yet |
| `codebase-review` | 规范：两轴评审的方法，自动加载         |
| `/code-review`    | Claude Code 内置命令，与本库无关       |

## 安装

```bash
git clone --recurse-submodules <本仓库>
ln -s "$PWD/skills/code/codebase-setup" ~/.claude/skills/codebase-setup   # 每个技能一个链接，或用你的技能管理工具
make check   # 按 Agent Skills 规范校验每个技能，并检查脚本与 Markdown 规则
```

## 参考与致谢

本库在阅读、借鉴、内化以下项目的基础上写成，感谢各位作者。

- [mattpocock/skills](https://github.com/mattpocock/skills)（MIT）
- [obra/superpowers](https://github.com/obra/superpowers)（MIT）
- [tw93/Waza](https://github.com/tw93/Waza)（MIT）
- [agentskills/agentskills](https://github.com/agentskills/agentskills)（Apache-2.0）
- [huacnlee/noop](https://github.com/huacnlee/noop)

## 许可证

[MIT](LICENSE)
