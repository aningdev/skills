# Reading Rounds

How to turn the raw rounds in `~/.agents/observe-result/.observer/inbox.jsonl` into decisions. The inbox holds only rounds no run has judged yet; the archive in `rounds/` is for going back, not for rereading.

## Three kinds of decision

A round is a block of questions put to the user, with the reply that followed. Read each question in it as one decision:

- **Asked** (`grilling` or `ask-tool`): a question with a recommended answer. Did the user adopt it or override it, and what reason did they give? A reply that takes the recommendation and adds a new idea is adopted; one that answers a different question than the one asked is an override.
- **Self-decided** (`self-grilling`): each line under `Calls I made:`. Did the user keep the call, or undo or redirect it in what they said next?
- **Missed**: a correction in a reply about something nobody asked. Rewrite it as the question that should have been asked, with the user's answer.

Missed decisions only show up here when they surface in a reply to some round. Corrections made elsewhere in a session aren't copied into the store, so this count runs low; say so when you report it.

## Whose words

Only the user's own words count. A message one agent wrote to another, such as a brief handed to pi, is never the user's preference. A round that quotes a format rather than using it, such as a message explaining what `Calls I made:` looks like, isn't a decision; skip it.

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
