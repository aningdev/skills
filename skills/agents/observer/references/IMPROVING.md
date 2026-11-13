# Improving

How decisions become principles, and principles become changes.

## Principles

- **Form** a principle from overrides, missed decisions, confirmed non-obvious choices, and the reasons the user gave.
- **Mind the layer.** The store holds only how the user decides across projects; what belongs to one project stays with that project. Before writing a leaning, ask whether it would still hold in a project that shares nothing with this one:
  - About one product's design, domain, stack, or paths ("separate pages, not drawers" in one app, `bots/<id>/bot.json`): it's the project's. Never write it here; if it keeps coming up, propose it for that project's `AGENTS.md` or docs.
  - Could hold anywhere, but so far seen in one project: a candidate in `.observer/candidates.md`, not a principle. Promote it when a second project shows it.
  - Seen in two or more projects: a principle here. When those sightings were project memories, propose deleting the project copies.

  Something already in the user's instructions or a repo's docs isn't recorded again.

- **Strengthen** it when a later decision goes the same way, adopted recommendations included: add the sighting, update the date and sources, and sharpen its Why or How to apply if the new case adds to them.
- **Weaken** it when a decision goes against it: report the conflict for the user to settle, never overwrite the principle quietly.
- **Retire** it when the user overturns it, or when nothing has touched it in a long while and the user agrees it no longer holds.

Edit one entry at a time; never rewrite the file whole.

## From principles to changes

A principle takes effect as soon as it's written to the `observe-result` skill, since every agent reads it; nothing else has to change for that. Propose a lasting change only when it's earned:

- Seen three or more times, across projects: fold it into the skill or role it belongs to.
- Specific to one project, and seen there again and again: that project's `AGENTS.md` or docs.
- Enforceable by a tool: a check.
- A role overridden on the same kind of call again and again: its mission.

Write proposals to `.observer/proposals.md`. Apply each only when the user approves it, then remove the principle it came from, so it lives in one place.
