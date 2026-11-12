---
name: code-review
description: "Review a change along two separate axes: Standards (does it follow the project's conventions and language rules?) and Spec (does it do what was agreed?). Runs both in fresh parallel sub-agents and reports them side by side. Use when a change is done and before handing it off, or when the user asks for a review."
---

Two-axis review of a change:

- **Standards**: does the code follow the project's conventions and the language rules?
- **Spec**: does the code do what was agreed?

Both axes run as **parallel sub-agents**, each with a fresh context window, so neither inherits the reasoning that wrote the code. This skill then puts their findings side by side.

## Process

### 1. Pin the diff

Review the uncommitted changes plus any commits made for this work. If the starting point isn't obvious, use the commit the work started from. Confirm the diff is non-empty before going further.

### 2. Collect the spec

The acceptance criteria, quoted verbatim, from whichever source the work came from:

1. An agreement from `/receiver`
2. A violation list from `/architecture`
3. The reproduction from `hunt`: it must now pass, and nothing else may break

If there's none, the **Spec** sub-agent skips and reports "no spec available".

### 3. Collect the standards

- `docs/ARCHITECTURE.md` and `docs/GLOSSARY.md`, checked with the list in the `docs-spec` skill
- The `code-rule` skill and the reference for each language in the diff
- The **smell baseline** below

The smell baseline is a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when the project documents nothing. Two rules bind it:

- **The project overrides.** A documented convention always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*:

- **Mysterious Name**: a name that doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape in more than one hunk or file. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move it onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together. → bundle them into one type.
- **Primitive Obsession**: a primitive standing in for a domain concept. → give the concept its own small type.
- **Repeated Switches**: the same `switch` or `if`-cascade on the same type recurs. → replace with polymorphism, or one shared map.
- **Shotgun Surgery**: one logical change forces scattered edits across many files. → gather what changes together into one module.
- **Divergent Change**: one module is edited for several unrelated reasons. → split so each changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks the spec doesn't need. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation. → hide the walk behind one method on the first object.
- **Middle Man**: a module that mostly delegates onward. → cut it, call the real target directly.
- **Refused Bequest**: a subclass that ignores most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn both sub-agents in parallel

Issue both calls together and wait for both reports.

**Standards sub-agent** gets the diff, the standards from step 3 (the smell baseline pasted in full), and this brief: "Report, per file or hunk, (a) every place the diff breaks a documented convention or language rule: cite the rule and `file:line`; (b) any baseline smell: name it and quote the hunk; (c) any structural choice the docs don't cover: list it as a gap. Convention breaches are hard; smells are judgement calls. Under 400 words."

**Spec sub-agent** gets the diff, the acceptance criteria verbatim, and this brief: "For each criterion, say pass or fail with evidence. Then list (a) behaviour in the diff nobody asked for, and (b) criteria that look met but where the implementation looks wrong. Quote the criterion for each finding. Under 400 words."

### 5. Report

Present the two reports under `## Standards` and `## Spec`, lightly cleaned. Do **not** merge or rerank across the axes. End with one line: findings per axis, and the worst issue within each.

## After the review

- **Hard findings** go back to whoever wrote the code: fix them and review again.
- **Gaps** and conventions that look stale go to the user: tell them to run `/architecture`.
- If the same finding survives two rounds, stop fixing. The problem is in the agreement or the conventions: tell the user to run `/receiver` or `/architecture`.

## Why two axes

Code can follow every convention and still build the wrong thing, or build exactly the right thing in a way that breaks the project's shape. Reporting the axes separately stops one from masking the other.
