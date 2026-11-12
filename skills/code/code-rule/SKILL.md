---
name: code-rule
description: Language-level coding rules for Python, Rust, and TypeScript. Use when writing, fixing, or reviewing code in .py, .rs, .ts, .tsx, .js, or .jsx files.
---

# Code Rules

Project conventions come first: `docs/ARCHITECTURE.md`, the project's config, and the code already there. These rules fill the gaps, and only cover what formatters and linters won't catch.

## Before writing

- Read the toolchain config (`pyproject.toml`, `Cargo.toml`, `package.json`) for the language version, formatter, linter, type checker, and async runtime. Don't use syntax or APIs the declared version doesn't support.
- Training data goes stale. When unsure about a framework or an API, check the official docs, not memory.

## Every language

- **Types at the boundaries.** Public APIs and cross-module interfaces are fully typed. Parse and validate external input at the edge; nothing untyped (`Any`, `any`) crosses a module boundary.
- **Make illegal states unrepresentable.** Use enums or literal unions for finite states, not combinations of booleans or magic strings.
- **Errors.** Catch only what this layer can handle. Keep the cause when converting an error. Never swallow one silently. Catch-alls belong only at request, task, or process boundaries.
- **Side effects at the edges.** I/O, time, randomness, and external clients sit behind seams that tests can replace.
- **Async.** No blocking I/O or long CPU work on the event loop. Every background task has an owner that awaits it, cancels it, and handles its errors.
- **Security.** Parameterized queries. Commands as argument lists, never shell strings. No `eval` or executable deserialization of untrusted data. Secrets never in source, logs, or error messages.
- **Performance.** Measure before optimizing. Fix algorithms and I/O counts before micro-optimizations.

## Per language

Read the file for the language you're touching:

- `.py`: [PYTHON.md](references/PYTHON.md)
- `.rs`: [RUST.md](references/RUST.md)
- `.ts`, `.tsx`, `.js`, `.jsx`: [TYPESCRIPT.md](references/TYPESCRIPT.md)

## Before handing off

Run the project's own check commands. If it has none, run the defaults in the language file. Autofix commands rewrite source: run them only when you mean to review the result.
