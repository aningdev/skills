---
name: self-grilling
description: Grill yourself about your own decisions under a mission, writing each round out, and bring the user only what's outside it or hard to undo. Use once you've read enough to commit to an approach, whenever you pick between ways, assume what nothing settled, depart from what was agreed, add what nobody asked for, or fail at the same thing twice, and before you hand off.
---

Run `grilling` on yourself, with a **mission** as the yardstick: the role's mission, or else one sentence distilled from the request.

Grill at three points, and write every round out rather than thinking it silently:

- Once you've read what you need, before you commit to an approach: list the calls the work needs and answer each.
- Whenever you pick between two or more ways, assume something nothing settled, depart from what was agreed or a convention, add something nobody asked for, or fail at the same thing twice.
- Before you hand off: go back over every call, and raise any that's outside the mission or hard to undo instead of letting it pass.

Answer each question yourself with the option that best serves the mission: first by how the user has decided before (the `observe-result` skill, when it's installed), then by current best practice. Take to the user only what's outside the mission or would be hard to undo (changing the stack, a public interface, deleting data).

Write each round's calls in this exact form so they can be audited later, saying who made them: the role you're acting as, by its skill name, or `no role`.

```
Calls I made as <role>:
- <decision> → <choice> (<one-line reason>)
```
