# Rust

- **Toolchain.** Don't raise the MSRV by accident: check `rust-version` and `edition` before using new syntax or APIs.
- **Types.** Enums for mutually exclusive states. Newtypes only where values are easy to mix up or carry an invariant. Implement or derive only the traits callers actually need.
- **Ownership.** Borrow views in parameters: `&str`, `&[T]`, `&Path`. Don't clone to dodge the borrow checker, and don't add lifetimes just to avoid a cheap clone.
- **Errors.** `?` to propagate, with context added at meaningful boundaries. Typed errors in libraries; type-erased errors only at the application edge. `unwrap` and `expect` only in tests or where failure is proven impossible, and the `expect` message says why it's impossible.
- **Concurrency.** Never hold a lock across `.await`, or during I/O or a callback. Blocking work goes through the runtime's blocking pool.
- **Unsafe.** Every `unsafe` block carries a `// SAFETY:` comment stating the preconditions and how they're met. Keep unsafe in small private modules behind a safe API. Never hand-implement `Send` or `Sync` without a proof.

## Default checks

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
```

Add `--all-features` only when the features aren't mutually exclusive.
