# TypeScript

- **Types.** `unknown` over `any`. Narrow with type guards instead of asserting with `as`. `as const` for literal values.
- **Idioms.** `const` by default, `let` only when reassigned, never `var`. `?.` and `??` over manual null checks.
- **Async.** Every promise is awaited or explicitly handled; no floating promises. `async`/`await` over `.then` chains.
- **Errors.** Throw `Error` objects, never strings. Don't catch only to rethrow.
- **Modules.** Import specific members; no barrel files that re-export everything.
- **React.** Function components only. Hooks at the top level, with complete dependency arrays. Stable IDs as `key`, not array indices. Never define a component inside another. Derive state during render instead of syncing it with an effect. In React 19+, pass `ref` as a prop instead of `forwardRef`.
- **Accessibility.** Semantic elements (`<button>`, `<nav>`) over `<div>` with roles. Labels on inputs, alt text on images, keyboard handlers alongside mouse handlers.
- **Security.** No `dangerouslySetInnerHTML` on unsanitized content. `rel="noopener"` with `target="_blank"`.
- **Debris.** No `console.log` or `debugger` in committed code.
