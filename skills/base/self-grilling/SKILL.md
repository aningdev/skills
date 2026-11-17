---
name: self-grilling
description: Grill yourself about your own decisions under a mission, writing each call out, and bring the user only what's outside it or hard to undo. Use once you've read enough to commit to an approach, whenever you pick between ways, assume what nothing settled, depart from what was agreed, add what nobody asked for, or fail at the same thing twice, and before you hand off.
---

# Self-Grilling

Run `grilling` on yourself, with a **mission** as the yardstick: the role's mission, or else one sentence distilled from the request. Write each call out as you settle it, at three points:

- Once you've read what you need, before you commit to an approach: list the calls this work needs and answer each.
- Whenever you pick between two or more ways, assume something nothing settled, depart from what was agreed or a convention, add something nobody asked for, or fail at the same thing twice.
- Before you hand off: go back over every call, and raise any that's outside your mission or hard to undo instead of letting it pass.

Answer each by how the user has decided before, then by current best practice. A call already settled, by how the user has decided before, a role lesson, or the project's docs, takes one line naming what settled it; don't grill it again. Take to the user only what's outside your mission or hard to undo; with no user to ask, mark it for the user in what you hand off and carry on with what can be undone.

How the user has decided before is in the `observe-result` skill, when it's installed. Hard to undo means things like changing the stack, a public interface, or deleting data. A role embeds the points and the answer rule above word for word, and may add moments of its own.

When you hand off, list every call once, in this exact form so it can be audited later, saying who made it: the role you're acting as, by its skill name, or `no role`. This is the list that gets audited; the calls you write along the way are working notes.

```
Calls I made as <role>:
- <decision> → <choice> (<one-line reason>)
```
