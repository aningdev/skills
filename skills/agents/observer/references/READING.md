# Reading Rounds

How to turn the raw rounds in `~/.agents/skills/observe-result/.observer/inbox.jsonl` into decisions. The inbox holds only rounds no run has judged yet; the archive in `rounds/` is for going back, not for rereading.

## Kinds of decision

A round is a block of questions put to the user, with the reply that followed. Read each question in it as one decision:

- **Asked** (`grilling` or `ask-tool`): a question with a recommended answer. Did the user adopt it or override it, and what reason did they give? A reply that takes the recommendation and adds a new idea is adopted; one that answers a different question than the one asked is an override.
- **Self-decided** (`self-grilling`): each line under `Calls I made:`. Did the user keep the call, or undo or redirect it in what they said next?
- **Missed**: a correction in a reply about something nobody asked. Rewrite it as the question that should have been asked, with the user's answer.
- **Confirmed**: the user explicitly endorsing a choice that wasn't the obvious default ("yes, separate pages, not drawers"). It counts as a sighting just like an override: knowing what to keep matters as much as knowing what to stop. A plain "all yes" isn't one.
- **Remembered** (`memory`): a feedback memory an agent already wrote during a session, one project at a time. Treat each as a sighting in that project, with its Why as the reason.

Missed decisions only show up here when they surface in a reply to some round. Corrections made elsewhere in a session aren't copied into the store, so this count runs low; say so when you report it.

## What's already recorded elsewhere

Before turning anything into a principle, check whether another layer already holds it: the user's global instructions (`~/.claude/CLAUDE.md` and its includes), a project's `AGENTS.md` or `CLAUDE.md`, or the repo's docs. If it's already there, it's covered; don't record it again.

## Whose words

Only the user's own words count. A message one agent wrote to another, such as a brief handed to pi, is never the user's preference. The digest only takes a marker that opens a line or a sentence, so a message explaining a format isn't copied as a round; if one still slips through, skip it.

## Counting sightings

A sighting is one session in which the user leaned the same way on the same kind of question. Saying it three times in one session is still one sighting; the count grows only across sessions and projects.

## When a round isn't enough

Open the session through the round's `ref` when the reply is ambiguous, refers back to something earlier, or the question only makes sense with what came before. Read just the stretch you need.

## Metrics

Count these while reading, for the rounds in this run:

- **Adoption**: recommendations adopted, out of the asked decisions you could judge.
- **Kept**: self-decided calls the user left alone, out of all self-decided calls.
- **Missed**: corrections of things nobody asked.

Leave out what you couldn't judge, and give the count of it.
