# PR Description Format

A PR description carries the Agreement a reviewer checks the diff against. Write it so someone who never saw the conversation can say, criterion by criterion, whether the diff does what was asked.

## Structure

```md
## Why

{One or two sentences: the problem, in the terms of `docs/GLOSSARY.md`. Link the issue if there is one.}

## Acceptance criteria

- [ ] {Each one answers yes or no} (automated: {the scripted walkthrough})
  - Example: {realistic input} → {what the user sees}
- [ ] {Copied verbatim from the Agreement} (manual: {how a user would walk it})
  - Example: {realistic input} → {what the user sees}

## Out of scope

- {What this PR deliberately doesn't do}

## Summary

{The smallest view that makes the change clear: a diff-sketch, a call tree, a file tree, or a Mermaid diagram.}

## Evidence

- **Before:** {what the user saw: screenshot, output, or response}
- **After:** {what the user sees now, walking the same path}

## Merge danger

**Door:** {one-way or two-way}
**Blast radius:** {who or what could break}
```

## Rules

- **Acceptance criteria are verbatim.** Copy them, with their examples, from wherever the Agreement lives (the request, a handoff, the issue, or a spec), never paraphrase. A criterion that can't be answered yes or no isn't one yet.
- **Each criterion says how it's verified.** _Automated_ names the scripted walkthrough that repeats it in CI; _manual_ says how a reviewer walks it as the user would.
- **Out of scope is never empty.** It tells the reviewer what not to flag as missing, and what to flag as scope creep.
- **Pick the smallest view.** One visual next to the sentence it supports beats several. Keep only the calls, files, and seams the reviewer needs.
- **Evidence over claims.** Show what the user saw before and sees now, walking the same path. Screenshots for visual changes.
- **Name the door.** A two-way door can be rolled back cheaply; a one-way door (data migrations, deletions, public API changes) can't. Say which, and what could break.
- **Use the project's words.** Terms from `docs/GLOSSARY.md`, seams and layers from `docs/ARCHITECTURE.md`. No implementation diary, no "first I tried".
