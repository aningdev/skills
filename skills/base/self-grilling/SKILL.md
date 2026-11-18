---
name: self-grilling
description: Grill yourself about your own decisions under a mission, writing each call out, and bring the user only what's outside it or hard to undo. Use when you take over work or a handoff, once you've read enough to commit to an approach, whenever you pick between ways, assume what nothing settled, depart from what was agreed, add what nobody asked for, or fail at the same thing twice, and before you hand off.
---

# Self-Grilling

Run `grilling` on yourself, with a **mission** as the yardstick: the role's mission, or else one sentence distilled from the request. Write each call out as you settle it, at three points:

- When you take work over, from the user or a handoff, once you've read what you need and before you commit to an approach: ask whether you have enough to go on (the goal, what counts as done, the constraints, where the result goes back); find out what you can, ask for what you can't; then list the calls this work needs and answer each.
- Whenever you pick between two or more ways, assume something nothing settled, depart from what was agreed or a convention, add something nobody asked for, or fail at the same thing twice.
- Before you hand off, to the user or another agent: check the work against its goal and each thing that counts as done, by evidence, and say plainly what isn't met; check that whoever picks it up can carry on from what you hand over alone; then go back over every call, and raise any that's outside your mission or hard to undo instead of letting it pass.

Answer each by how the user has decided before, then by current best practice. A call already settled, by the brief or agreement, how the user has decided before, a role lesson, or the project's docs, takes one line naming what settled it while you work, and stays out of the list you hand off; don't grill it again. Take to the user, before you act, only what's outside your mission or hard to undo, such as changing the stack, deleting data, or renaming, moving, or removing anything others already use (a URL, a public interface, a file or field name), however easy the commit is to revert. With no user to ask, mark it for the user in what you hand off and carry on with what can be undone, keeping what others use working.

How the user has decided before is in the `observe-result` skill, when it's installed. A role embeds the points and the answer rule above word for word, and may add moments of its own.

When you hand off, list every call you made once, leaving out what was settled for you, in this exact form so it can be audited later, saying who made it: the role you're acting as, by its skill name, or `no role`. This is the list that gets audited; the calls you write along the way are working notes.

```
Calls I made as <role>:
- <decision> → <choice> (<one-line reason>)
```
