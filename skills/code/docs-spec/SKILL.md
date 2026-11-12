---
name: docs-spec
description: Build and sharpen a project's domain model and architecture conventions. Use when discussing codebase terminology, tech choices, context boundaries, directory layout, layering, or key abstractions, or when writing or editing a GLOSSARY.md or ARCHITECTURE.md.
---

# Domain Modeling

Actively build and sharpen the project's domain model and architecture as you design. This is the _active_ discipline: challenging terms, inventing edge-case scenarios, policing boundaries, and writing the glossary and conventions down the moment they crystallise. (Merely _reading_ `docs/GLOSSARY.md` for vocabulary or `docs/ARCHITECTURE.md` for context is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model or the conventions, not just consuming them.)

Two files, two jobs:

- `docs/GLOSSARY.md`: what things _are_. The language: terms, contexts, and how they relate.
- `docs/ARCHITECTURE.md`: how the system is _built_. The conventions: stack, layout, layers, abstractions. Facts only, no history. It references the glossary and never redefines it.

## File structure

```
/
├── docs/
│   ├── ARCHITECTURE.md
│   └── GLOSSARY.md
└── src/
```

Create files lazily: only when you have something to write. If no `docs/GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/ARCHITECTURE.md` exists, create it when the first convention is settled.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `docs/GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Challenge against ARCHITECTURE.md

When a proposal breaks a convention in `docs/ARCHITECTURE.md`, call it out immediately: a layer importing the wrong way, code landing in the wrong folder, a context reaching into another's internals, a provider SDK used outside its abstraction. "ARCHITECTURE.md says Ordering and Billing talk via events, but this adds a direct call. Change the convention, or change the design?"

### Place new code deliberately

When new code doesn't obviously fit, decide where it goes before writing it: which context owns it, which layer, and whether it sits behind an existing abstraction or needs a new one. "Is this refund logic Billing's or Ordering's? Who owns the money once it's paid?" If the answer is a new convention, it goes in ARCHITECTURE.md.

### Probe abstractions

When a new abstraction is proposed, ask what it hides and how many implementations it really has. One implementation and nothing hidden is indirection, not abstraction. When the same provider or concern leaks into several places, propose the seam that would contain it.

### Update GLOSSARY.md inline

When a term is resolved, update `docs/GLOSSARY.md` right there. Don't batch these up: capture them as they happen. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else. Structural conventions belong in `docs/ARCHITECTURE.md`.

### Update ARCHITECTURE.md inline

When a stack choice, boundary, layout rule, layering rule, or abstraction is settled, update `docs/ARCHITECTURE.md` right there, the same way you update the glossary. Use the format in [ARCHITECTURE-FORMAT.md](./ARCHITECTURE-FORMAT.md).

`ARCHITECTURE.md` holds today's conventions at module altitude: facts, not history. Do not treat it as a decision log, a changelog, a task list, or a design doc for a single feature. When a convention changes, rewrite it in place.

## Checking code against the docs

When asked to check code (a diff or the whole project), walk this list and cite `file:line` for each finding:

- An import that goes against the arrows in `## Layers`
- Code outside the folder `## Layout` assigns it
- A context reaching into another context's internals
- A provider or concern used outside its abstraction
- A name that doesn't match `docs/GLOSSARY.md`

For each finding, say whether the code is wrong or the doc is stale. Anything the docs don't cover is a gap, not a violation.
