# Design It Twice

When the user wants to explore alternative interfaces for a chosen deepening candidate, design it several ways before settling. Based on "Design It Twice" (Ousterhout): your first idea is unlikely to be the best.

Uses the vocabulary in [SKILL.md](../SKILL.md): **module**, **interface**, **seam**, **adapter**, **leverage**.

## Process

### 1. Frame the problem space

Before designing, write a user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- A rough illustrative code sketch to ground the constraints, not a proposal, just a way to make the constraints concrete

Show this to the user, then go straight on to Step 2.

### 2. Design it several ways

Produce three or more **radically different** interfaces for the deepened module, each pulled by a different constraint: the smallest possible interface, the most flexible one, the one that makes the most common caller trivial, and (where a seam crosses a dependency) one built around ports and adapters.

Keep the designs independent: separate sub-agents with fresh context if you can spawn them, otherwise separate passes of your own that don't look back at earlier designs. Give each the vocabulary of [SKILL.md](../SKILL.md) and `docs/GLOSSARY.md`, and the dependency categories in [DEEPENING.md](DEEPENING.md). Each design should show its interface (including invariants and error modes), how a caller uses it, what it hides, and where its leverage is thin.

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by **depth** (leverage at the interface), **locality** (where change concentrates), and **seam placement**.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated: the user wants a strong read, not a menu.
