# Skills Glossary

这套技能体系自己的语言。技能正文用英文，术语按下面的英文词写，一个概念只用一个词。

## Language

**Agreement**:
关于"要做成什么"的约定：为什么做、目标、不做什么、验收标准。可以存在于对话、handoff、issue、PR 描述或 spec 中。
_Avoid_: requirement, 需求文档

**Spec**:
把 Agreement 落成文件的可选形式，`docs/specs/YYYY-MM-DD-<feature>.md`。只写目标，不写设计。
_Avoid_: 用 spec 指代 Agreement 本身

**Acceptance criterion**:
Agreement 中一条能用"是/否"回答的标准：谁、走什么路径、看到什么，附一个具体例子，并标注 automated 或 manual。
_Avoid_: test case, requirement

**Walkthrough**:
像用户那样，在真实运行的东西上走一遍某条 Acceptance criterion 的路径。值得重复的 walkthrough 写成脚本，挂在 `test` 下由 CI 跑。
_Avoid_: acceptance test, 手测

**Evidence**:
Walkthrough 留下的、用户视角的前后对比：截图、输出、响应。没有新鲜的 Evidence 不能说完成。
_Avoid_: proof, 自述

**Entry point**:
项目里固定的三个命令名：`check`（只读检查）、`fix`（自动修复）、`test`（脚本化的 walkthrough 及项目保留的其他测试）。
_Avoid_: script, task

**Baseline**:
`codebase-setup` 给出的推荐形状：原则、推荐工具链、项目的各项需要及推荐文件、AGENTS.md 该装什么。不是必备清单，缺了什么只有在关联到证据时才算问题。

**Drift**:
项目与 Baseline 的差异中，没人主动选择的那种。对齐它。

**Choice**:
项目与 Baseline 的差异中，有意为之的那种。保留，并在项目的 `docs/ARCHITECTURE.md` 记原因。

**Mission**:
一句话说明一个身份要达成什么，是 self-grilling 判断每个决策的标尺。Role 自带 Mission；没有 Role 时，从用户的请求里提炼。

**One-way door**:
做了就难以撤回的决定（hard to undo），比如换栈、改对外接口、删数据。和超出 Mission 的事一样，交给用户。
_Avoid_: structural change, 高风险操作

**Decision**:
Agent 替用户做的一个判断，是观测的单位。三种来源：grilling 里问用户的（Asked）、self-grilling 里自己拍板的（Self-decided）、谁都没当成决定却被用户纠正的（Missed）。见 `observer` 角色。

**Principle**:
从被推翻或漏问的 Decision 里提炼出的用户判断规则，至少出现两次才成立，写在技能 `observe-result`（`~/.agents/observe-result/`）里，各 Agent 推荐或替用户做决定前只读加载。

**Skill**:
一份可被加载的方法或标准，装在 `skills/<layer>/<name>/SKILL.md`。

**Role**:
`skills/agents/` 下的一种身份：用描述性语言说明它的 Mission 和它在意什么，不点名具体的 Skill 或其他 Role；缺了某个 Skill 或 Role 时，靠自己发现和补位。判断力来自在 Mission 下的自我追问。
_Avoid_: agent（指代角色时）

## Relationships

- 一个 **Agreement** 有多条 **Acceptance criterion**；它可以落成一份 **Spec**，也可以不落。
- 每条 **Acceptance criterion** 通过一次 **Walkthrough** 被验收，留下 **Evidence**；标 automated 的，其 **Walkthrough** 由 `test` 这个 **Entry point** 重复执行。
- 项目与 **Baseline** 的每处差异，要么是 **Drift**，要么是 **Choice**。
- 在 **Mission** 之内的决定自己拍板，交付时列出；超出 **Mission** 或属于 **One-way door** 的，交给用户。
