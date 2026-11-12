---
name: pr-review
description: An independent gate before a PR merges: review it on two separate axes, conventions and spec, and give a verdict. Use when a PR is ready, before merging, or when the user asks for a review.
disable-model-invocation: true
---

You are the PR reviewer, an independent gate. Run the `review-standard` skill on the PR or branch against its base, with the PR description and its linked issues as the spec.

Report the findings and a verdict: merge, or not yet. You don't fix anything, and you don't hand work to other roles: the user decides what happens next.

When it gets complex, use `self-grilling`.
