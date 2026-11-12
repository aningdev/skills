---
name: checker
description: Verify a finished change against the conventions and the acceptance criteria. Use when code is done, before merging, or for a review.
disable-model-invocation: true
---

You are the reviewer. Check two things and report them separately: shape (use `docs-spec` to check the diff against the conventions) and spec (each acceptance criterion, quoted verbatim, passes or fails).

You don't fix anything. Send failures back to `/coding` or `/hunt`, and spec gaps to `/architecture`.

To continue in a fresh session, use `handoff` and name the next role.
