# Spec Format

A spec is an Agreement written to a file: what one feature must achieve, so that someone who never saw the conversation can build it and tell, criterion by criterion, whether it's done. It stops at the goal: how to build it is left to the builder.

## Structure

```md
# {Feature}

{Date agreed.} {Link to the issue, if there is one.}

## Why

{One or two sentences: the problem, and who has it, in the terms of `docs/GLOSSARY.md`.}

## Goal

{What's true once this ships, from the user's side. One short paragraph.}

## Out of scope

- {What this feature deliberately doesn't do}

## Acceptance criteria

- [ ] **{Who}** {does what, step by step from where they'd start}, and **sees** {the result that tells them it worked}. _(automated | manual)_
  - Example: {realistic input} → {what they see}
- [ ] {Include what they'd see when it should refuse or fail}
  - Example: an org admin removes the last owner → "An organization needs at least one owner"

## Open questions

- {Anything still unsettled that changes what gets built. Empty before building starts.}
```

## Rules

- **Goal, not design.** No architecture, file names, APIs, or task lists. If a constraint really is part of the goal ("works offline", "no new dependency"), it goes in Goal.
- **Every criterion is a user walking a path.** Name who, what they do, and what they see. A criterion that can't be answered yes or no isn't one yet.
- **Every criterion carries an example.** At least one concrete input, shaped like real data, and what the user sees. It settles ambiguity the prose leaves open, and it's the walkthrough's first input.
- **Mark how it's accepted.** _Automated_ when the walkthrough is worth scripting so CI repeats it; _manual_ otherwise.
- **Out of scope is never empty.** It's what stops the builder adding, and the reviewer flagging, what nobody asked for.
- **Open questions block building.** A spec with open questions is a draft.
- **Use the project's words.** Terms from `docs/GLOSSARY.md`. A new term gets settled there first.
