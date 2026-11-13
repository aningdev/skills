# Setting Up a Repo

For a new repo, or re-running setup on an existing one.

### Setting up a repo

The same flow for a new repo and an existing one, and safe to re-run:

1. **Explore.** Read what's there: manifests, lockfiles, `AGENTS.md` and `CLAUDE.md`, `docs/`, the git remote, CI. Don't assume.
2. **Propose.** Summarise what you found and what's missing, with a recommended answer for each open decision. Skip what exploration already settled.
3. **Confirm.** Wait for the user before writing.
4. **Write.** Build on what exists rather than starting over. For a new project, start from the language's own scaffolding. Record any departure from these recommendations in `docs/ARCHITECTURE.md`.

**Done when:** the needs below are met as far as the project calls for, `check` and `test` are green, and `AGENTS.md` answers what a fresh session would otherwise have to ask. Setup never edits a skill file.

### What a project needs

Each need has a recommended file. None is required for its own sake: a missing one matters only when its absence causes a real problem (see Checking a repo).

| Need                                           | Recommended                                                                                                |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| People understand what it is and how to run it | `README.md`                                                                                                |
| Agents know how to work here                   | `AGENTS.md`, with `CLAUDE.md` as one line: `@AGENTS.md`                                                    |
| Terms and structure are written down           | `docs/GLOSSARY.md` and `docs/ARCHITECTURE.md`, once there's something to write (the `codebase-docs` skill) |
| Installs reproduce                             | A committed lockfile                                                                                       |
| It checks itself                               | The `check`, `fix`, and `test` entry points ([CHECKS-AND-CI.md](CHECKS-AND-CI.md))                         |
| Every change is verified the same way          | One CI workflow that calls the entry points                                                                |
| Acceptance worth repeating stays repeatable    | Scripted walkthroughs, e.g. in `tests/`                                                                    |

### AGENTS.md

`AGENTS.md` holds what every session needs and the code can't tell you. How the code is built belongs in `docs/ARCHITECTURE.md`; `AGENTS.md` points there and never restates it.

- **What this is**: one sentence.
- **Commands**: the entry points (`check`, `fix`, `test`, plus `dev` or `run`), one line each on what they do. Never the tool commands behind them.
- **Working here**: the facts that vary by repo: where issues live, where Agreements are kept, which language replies, commits, and docs use. When one of these grows past a few lines, move it to its own file and leave a one-line pointer.
- **Constraints**: what an agent can't recover from the code and mustn't get wrong, each routed to when it matters ("When touching `apps/client/`, read its `AGENTS.md` first"). Once a tool can enforce one, move it into `check` and delete the line.
- **Where to read**: `docs/GLOSSARY.md`, `docs/ARCHITECTURE.md`, then one pointer per area with its own `AGENTS.md` or README.

**Make sure it's read.** `AGENTS.md` is the one source; `CLAUDE.md` only points to it. Check that every agent tool in use actually loads it, nested files included: a root `CLAUDE.md` with its own content can stop a tool from reading `AGENTS.md` below it.
