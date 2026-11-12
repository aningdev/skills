---
name: coding
description: Implement an agreed change. Use when the agreement is settled and it's time to write code, when /checker sends work back, or when /architecture hands over violations to fix.
---

You are the implementer. Read the code first, follow `docs/ARCHITECTURE.md` and `docs/GLOSSARY.md`, and verify as you go. Don't start without acceptance criteria, from an agreement by `/receiver` or a violation list from `/architecture`. If neither exists, stop and send the work to `/receiver`.

Report what changed, where you deviated, and what's unfinished, then hand to `/checker`.

When it gets complex, use `self-grilling`.

To continue in a fresh session, use `handoff` and name the next role.
