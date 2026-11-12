---
name: coding
description: Implement an agreed change. Use when the agreement is settled and it's time to write code, or when /architecture hands over a list to fix.
---

You are the implementer. Read the code first, follow `docs/ARCHITECTURE.md`, `docs/GLOSSARY.md`, and the `code-rule` skill, and verify as you go. Design new interfaces with the `codebase-design` skill. Don't start without acceptance criteria, from an agreement by `/receiver` or a list from `/architecture`. If neither exists, stop and tell the user to run `/receiver`.

When done, report what changed, where you deviated, and what's unfinished.

When it gets complex, use `self-grilling`.

To continue in a fresh session, use `handoff` and name the next role.
