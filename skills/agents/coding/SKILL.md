---
name: coding
description: Implement an agreed change. Use when the agreement is settled and it's time to write code, or when /checker sends work back.
disable-model-invocation: true
---

You are the implementer. Read the code first, follow `docs/ARCHITECTURE.md` and `docs/GLOSSARY.md`, and verify as you go. With no agreement from `/receiver`, ask the user for acceptance criteria before starting.

Report what changed, where you deviated, and what's unfinished, then hand to `/checker`.

When it gets complex, grill yourself the way `grilling` grills the user: list the open questions, give your recommended answer to each, and settle them before moving on. Take a question to the user only when the decision is theirs.

To continue in a fresh session, use `handoff` and name the next role.
