---
name: codebase-docs
description: Build and sharpen a project's docs, the domain model in docs/GLOSSARY.md, the architecture conventions in docs/ARCHITECTURE.md, each feature's goals and acceptance criteria in docs/specs/, and the reasons behind hard-to-undo decisions in docs/decisions/. Use when discussing codebase terminology, tech choices, contexts, directory layout, folder or file naming, layering, or seams, when making a decision that's hard to undo, when pinning down what a feature must achieve before building it, or when writing or editing any of these files. Not for designing one module's interface (codebase-design) or PR descriptions (codebase-git).
---

# Codebase Docs

Actively build and sharpen the project's domain model and architecture as you design. This is the _active_ discipline: challenging terms, inventing edge-case scenarios, policing seams and layers, and writing the glossary and conventions down the moment they crystallise. (Merely _reading_ `docs/GLOSSARY.md` for vocabulary or `docs/ARCHITECTURE.md` for context is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model or the conventions, not just consuming them.)

Four kinds of doc, four jobs:

- `docs/GLOSSARY.md`: what things _are_. The language: terms, contexts, and how they relate.
- `docs/ARCHITECTURE.md`: how the system is _built_. The conventions: stack, layout, layers, seams. Facts only, no history. It references the glossary and never redefines it.
- `docs/specs/YYYY-MM-DD-<feature>.md` (optional): what one feature must _achieve_. Its goal, its bounds, and how its user will see it work. Dated, and never a design or a plan.
- `docs/decisions/NNNN-<decision>.md` (optional): _why_ a hard-to-undo choice was made, so the reason outlives the conversation. `ARCHITECTURE.md` keeps only the resulting fact.

## File structure

```
/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── GLOSSARY.md
│   ├── decisions/
│   │   └── 0001-postgres-over-sqlite.md
│   └── specs/
│       └── 2026-11-13-org-audit-log.md
└── src/
```

Create files lazily: only when you have something to write. If no `docs/GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/ARCHITECTURE.md` exists, create it when the first convention is settled. Create a spec when a feature is big enough that its goal needs agreeing before anyone builds it, and a decision record when a choice would be hard to undo.

## During the session

Be active, not a scribe:

- **Challenge terms** that conflict with `docs/GLOSSARY.md`, and sharpen vague or overloaded ones into a precise canonical term.
- **Stress-test with scenarios.** Invent edge cases that force the boundaries between concepts to be precise.
- **Cross-check the code.** When the user says how something works, check whether the code agrees, and surface any contradiction.
- **Guard the conventions.** When a proposal breaks `docs/ARCHITECTURE.md`, say so at once: change the convention, or change the design.
- **Place new code deliberately.** Decide which context and layer own it, and which seam it sits behind, before writing it.
- **Judge new seams** with the `codebase-design` skill. When the same concern leaks into several places, propose the seam that would contain it.

### Keep the structure readable

The folder tree is the first map anyone reads, human or agent. Keep it one they can trust:

- **Folders and files are named in the glossary's words.** Top-level folders follow the domain (`billing/`, `orders/`), not technical kinds (`controllers/`, `services/`). A file is named after the main concept it holds. When no term fits, settle one in the glossary first.
- **No catch-all folders.** `utils/`, `common/`, `helpers/`, `misc/` gather whatever had no obvious home, and nothing in them is found again. Every folder has a rule in `## Layout` for what belongs there; code that fits no rule means a missing concept, so name it.
- **Paths are guessable.** From a concept you can guess its path, and from a path say what it holds. One kind of thing has one place.

### Update GLOSSARY.md inline

When a term is resolved, update `docs/GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](references/GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else. Structural conventions belong in `docs/ARCHITECTURE.md`.

### Update ARCHITECTURE.md inline

When a stack choice, context, layout rule, layering rule, or seam is settled, update `docs/ARCHITECTURE.md` right there, the same way you update the glossary. Use the format in [ARCHITECTURE-FORMAT.md](references/ARCHITECTURE-FORMAT.md).

`ARCHITECTURE.md` holds today's conventions at module altitude: facts, not history. Do not treat it as a decision log (the why goes in `docs/decisions/`), a changelog, a task list, or a design doc for a single feature. When a convention changes, rewrite it in place.

### Record a decision that's hard to undo

When a choice would be expensive to reverse (a datastore, a framework, a public contract, a layering rule), write `docs/decisions/NNNN-<decision>.md`, numbered in order: the context, the decision, why, and the options turned down. Keep it to a screen. A record isn't rewritten later; when the decision changes, a new one supersedes it and says so. Small or easily reversed choices don't get one.

### Write a spec when the goal needs keeping

A spec is optional. Write one when a feature's goal took real settling and is worth keeping beside the code; the format is in [SPEC-FORMAT.md](references/SPEC-FORMAT.md). The spec holds the _what_ and the _why_, never the _how_: no design, no file list, no tasks. Those belong to whoever builds it.

Acceptance criteria come from wherever the agreement lives: the conversation, a handoff note, the issue, the PR description, or a spec. What matters is that they exist and each answers yes or no; when none do, write them before building, and bring the user the decisions in them (see below).

Once agreed, a spec isn't rewritten to match what got built. If the goal changes, write the change into the spec with the date, so the history of the goal stays readable.

## Checking code against the docs

When asked to check code (a diff or the whole project), walk this list and cite `file:line` for each finding:

- An import that goes against the arrows in `## Layers`
- Code outside the folder `## Layout` assigns it, or a folder `## Layout` doesn't list
- A catch-all folder, or a folder or file name that isn't a glossary term
- A context reaching into another context's internals
- A provider or concern used outside its seam
- A name that doesn't match `docs/GLOSSARY.md`

For each finding, say whether the code is wrong or the doc is stale. Anything the docs don't cover is a gap, not a violation.

## Asking the user

Find facts yourself. Bring the user only the decisions that change the outcome, all at once, each with your recommended answer. Never assume silently.
