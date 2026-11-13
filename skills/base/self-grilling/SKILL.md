---
name: self-grilling
description: Grill yourself about your own decisions under a mission, and bring the user only what's outside it or hard to undo. Use when a task gets complex, the path isn't obvious, you're about to build on an assumption, or you are acting under a role's mission and need to settle your own decisions.
---

Run `grilling` on yourself, with a **mission** as the yardstick: the role's mission, or else one sentence distilled from the request.

Answer each question yourself with the option that best serves the mission: first by how the user has decided before (the `observe-result` skill, when it's installed), then by current best practice. Take to the user only what's outside the mission or would be hard to undo (changing the stack, a public interface, deleting data).

When you hand off, list the calls you made yourself, in this exact form so they can be audited later:

```
Calls I made:
- <decision> → <choice> (<one-line reason>)
```
