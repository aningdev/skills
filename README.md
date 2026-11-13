# Skills

个人技能库：`base`（方法论）、`codebase-*`（代码库规范）、`code-*`（角色）。术语见 [docs/GLOSSARY.md](docs/GLOSSARY.md)，分层见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

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

出了问题时直接描述现象，`codebase-debug` 会自动加载，查根因再修复。

每一步都可以单独用；缺了哪个角色，其余角色和 `codebase-*` 照样能工作。

## 什么时候用哪个角色

角色要**手动调用**（敲 `/名字`），`codebase-*` 技能由 AI 按场景**自动加载**，不用手打。

| 你想要                                 | 调用                    | 会自动用到的规范                                              |
| -------------------------------------- | ----------------------- | ------------------------------------------------------------- |
| 把一个想法说清楚，定下做成什么样算完成 | `/code-feature-definer` | codebase-docs                                                 |
| 新建项目、对齐规范、梳理结构、改工具链 | `/code-architect`       | codebase-setup、codebase-docs、codebase-design、codebase-git  |
| 按约定把功能做出来                     | `/code-builder`         | codebase-lang、codebase-design、codebase-verify、codebase-git |
| 合并前把关                             | `/code-reviewer`        | codebase-review                                               |

## 容易混的名字

| 名字              | 是什么                                 |
| ----------------- | -------------------------------------- |
| `/code-reviewer`  | 角色：独立把关人，给出 merge / not yet |
| `codebase-review` | 规范：两轴评审的方法，自动加载         |
| `/code-review`    | Claude Code 内置命令，与本库无关       |
