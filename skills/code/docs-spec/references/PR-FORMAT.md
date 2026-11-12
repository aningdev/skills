# PR Description Format

A PR description is the spec a reviewer checks the diff against. Write it so someone who never saw the conversation can say, criterion by criterion, whether the diff does what was asked.

## Structure

```md
## Why

{One or two sentences: the problem, in the terms of `docs/GLOSSARY.md`. Link the issue if there is one.}

## Acceptance criteria

- [ ] {Each one answers yes or no}
- [ ] {Copied verbatim from the agreement or the issue}

## Out of scope

- {What this PR deliberately doesn't do}

## Summary

{The smallest view that makes the change clear: a diff-sketch, a call tree, a file tree, or a Mermaid diagram.}

## Evidence

- **Before:** {failing test, output, or screenshot}
- **After:** {passing test, output, or screenshot}

## Merge danger

**Door:** {one-way or two-way}
**Blast radius:** {who or what could break}
```

## Rules

- **Acceptance criteria are verbatim.** Copy them from the agreement or the issue, never paraphrase. A criterion that can't be answered yes or no isn't one yet.
- **Out of scope is never empty.** It tells the reviewer what not to flag as missing, and what to flag as scope creep.
- **Pick the smallest view.** One visual next to the sentence it supports beats several. Keep only the calls, files, and seams the reviewer needs.
- **Evidence over claims.** Show the check that failed before and passes now. Screenshots for visual changes.
- **Name the door.** A two-way door can be rolled back cheaply; a one-way door (data migrations, deletions, public API changes) can't. Say which, and what could break.
- **Use the project's words.** Terms from `docs/GLOSSARY.md`, seams and layers from `docs/ARCHITECTURE.md`. No implementation diary, no "first I tried".
