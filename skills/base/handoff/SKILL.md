---
name: handoff
description: Compact the current conversation or task into a handoff document for another agent to pick up.
---

# Handoff

Write a handoff document summarising the current conversation or task so a fresh agent can continue the work. Shape it around what the next session will be used for; if the user hasn't said, ask, and with no one to ask, state at the top what you assumed it's for, marked for the user to confirm. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Carry acceptance criteria verbatim, even when another artifact already holds them: never summarise them. Everything else already captured in other artifacts (docs, plans, issues, commits, diffs), don't duplicate; reference it by path or URL instead, written so it resolves from where the receiver starts work, or absolute.

Whoever picks it up, a delegate, a peer, or a later you, should be able to work without coming back to ask:

- **Say what done looks like, and what proves it.** The criteria, and the evidence that would show each is met, without assuming who checks.
- **Write out the rules that matter.** Your context doesn't travel with the document. Name skills if they help, but spell out the few rules this work must follow; a list of names alone gets skipped.
- **Say where the result goes back.** A file, a branch, or who to reply to. Handing the result back is a handoff too. Ask for the `Calls I made as <role>:` list in it, so whoever reads the result sees the calls made without them; when you're the one handing back, put that list in it, and when you pass a result on, pass its list on word for word, as plain top-level text, naming the agent that ran it in the heading: `Calls I made as <role> (via <agent>):`.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
