#!/usr/bin/env python3
# /// script
# requires-python = ">=3.15"
# dependencies = []
# ///

"""Copy every question round from local agent sessions into the observation store.

A round is a block of questions an agent put to the user (a grilling round, an ask tool
such as AskUserQuestion, or a self-grilling `Calls I made:` list) together with the
user's reply, kept as raw text. Nothing is judged here: the observer reads the rounds and
goes back to the session through `ref` when it needs more. Each agent tool has a reader
in READERS; add one to support another tool.

Feedback the agents already distilled during a session, Claude Code's per-project
memory files of type `feedback`, is copied too, as rounds with source `memory`, so the
observer can promote what several projects agree on and skip what one project keeps.

Only what's new is read. Each session file is resumed from the byte offset where the last
run stopped, and skipped when it hasn't grown. New rounds land in `inbox.jsonl`; once the
observer's report is confirmed, `--archive` moves them into `rounds/YYYY-MM.jsonl`, so the
next run reads only rounds it hasn't seen.

Usage:
    uv run digest.py --help
    uv run digest.py              # every session on this machine, whatever the project
    uv run digest.py --dry-run    # print new rounds without writing
    uv run digest.py --archive    # after the report is confirmed
"""

import hashlib
import json
import re
import sys
from collections import Counter
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from pathlib import Path
lazy import argparse

HOME = Path.home()
STORE = HOME / ".agents" / "skills" / "observe-result" / ".observer"
LIMIT = 6000  # characters kept per prompt or reply

MARKERS = frozendict(grilling="❓", **{"self-grilling": "Calls I made:"})
NOISE = (
    "<agent-message",
    "<task-notification",
    "[acp_delegate",
    "<local-command",
    "<command-name>",
    "<command-message>",
    "Caveat:",
    "Base directory for this skill",
)


@dataclass
class Event:
    """One step of a session, in the shape every reader produces."""

    line: int
    kind: str  # "user", "agent" (another agent writing as the user), "assistant", or "ask"
    text: str
    ts: str
    cwd: str
    ref: str


def read_jsonl(path: Path, offset: int) -> Iterator[tuple[int, dict]]:
    """Yield (byte offset, record) for each parseable JSON line from `offset` on."""
    with path.open("rb") as f:
        f.seek(offset)
        while line := f.readline():
            at = f.tell() - len(line)
            try:
                yield at, json.loads(line)
            except json.JSONDecodeError:
                continue


def read_claude(path: Path, offset: int) -> Iterator[Event]:
    """Read a Claude Code session: the user's words, queued messages, AI text, and AskUserQuestion answers."""
    for i, d in read_jsonl(path, offset):
        ts, cwd, ref = d.get("timestamp", ""), d.get("cwd", ""), d.get("uuid", str(i))
        if (
            d.get("type") == "queue-operation"
            and d.get("operation") == "enqueue"
            and d.get("content")
        ):
            if not d["content"].lstrip().startswith(NOISE):
                yield Event(i, "user", d["content"], ts, cwd, ref)
            continue
        if d.get("isSidechain") or d.get("isMeta"):
            continue
        result = d.get("toolUseResult")
        if isinstance(result, dict) and "questions" in result and "answers" in result:
            yield Event(i, "ask", json.dumps(result, ensure_ascii=False), ts, cwd, ref)
            continue
        content = (d.get("message") or {}).get("content")
        if d.get("type") == "user":
            if isinstance(content, list):
                if any(b.get("type") == "tool_result" for b in content):
                    continue
                content = " ".join(
                    b.get("text", "") for b in content if b.get("type") == "text"
                )
            text = re.sub(
                r"<system-reminder>.*?</system-reminder>",
                "",
                content or "",
                flags=re.DOTALL,
            ).strip()
            if text and not text.startswith(NOISE):
                yield Event(i, "user", text, ts, cwd, ref)
        elif d.get("type") == "assistant" and isinstance(content, list):
            for b in content:
                if b.get("type") == "text" and b.get("text"):
                    yield Event(i, "assistant", b["text"], ts, cwd, ref)


def read_pi(path: Path, offset: int) -> Iterator[Event]:
    """Read a pi session. A brief handed over by another agent is marked 'agent', never the user's."""
    header = next(read_jsonl(path, 0), (0, {}))[1]  # the session line carries cwd
    cwd = header.get("cwd", "")
    for i, d in read_jsonl(path, offset):
        if d.get("type") == "session":
            cwd = d.get("cwd", "")
        if d.get("type") != "message":
            continue
        msg = d.get("message") or {}
        content = msg.get("content")
        text = (
            " ".join(b.get("text", "") for b in content if b.get("type") == "text")
            if isinstance(content, list)
            else content or ""
        )
        ts, ref = d.get("timestamp", ""), d.get("id", str(i))
        if msg.get("role") == "user":
            text = text.split("[acp_delegate")[
                0
            ].strip()  # a delegate's report appended after the user's words
        if msg.get("role") == "user" and text:
            yield Event(
                i, "agent" if "<file name=" in text else "user", text, ts, cwd, ref
            )
        elif msg.get("role") == "assistant" and text:
            yield Event(i, "assistant", text, ts, cwd, ref)


READERS: frozendict[str, tuple[Path, Callable[[Path, int], Iterator[Event]]]] = (
    frozendict(
        claude=(HOME / ".claude" / "projects", read_claude),
        pi=(HOME / ".pi" / "agent" / "sessions", read_pi),
    )
)


def extract(tool: str, path: Path, offset: int) -> tuple[list[dict], int, bool]:
    """Read a session from `offset`: its new rounds, where to resume, and whether an agent ran it."""
    events = list(READERS[tool][1](path, offset))
    end = path.stat().st_size
    if any(e.kind == "agent" for e in events):
        # a session run by another agent holds none of the user's words
        return [], end, True
    rounds: list[dict] = []
    open_round: dict | None = None  # a round still collecting the user's reply
    turn: list[Event] = []
    for e in events:
        if e.kind == "assistant":
            open_round = None  # the reply is complete once the agent speaks again
            turn.append(e)
            continue
        base = {
            "ts": e.ts,
            "tool": tool,
            "project": e.cwd,
            "session": path.stem.rsplit("_", 1)[-1][:8],
            "ref": f"{path}#{e.ref}",
        }
        if e.kind == "ask":
            rounds.append(
                {**base, "source": "ask-tool", "prompt": e.text[:LIMIT], "reply": ""}
            )
            continue
        if open_round:
            open_round["reply"] = f"{open_round['reply']}\n{e.text}".strip()[:LIMIT]
            continue
        said = "\n".join(t.text for t in turn)
        for source, marker in MARKERS.items():
            if (at := said.find(marker)) >= 0:
                if source == "grilling" and 0 <= (goal := said.rfind("🎯", 0, at)):
                    at = goal  # keep the round's goal line with its questions
                open_round = {
                    **base,
                    "source": source,
                    "prompt": said[at:][:LIMIT],
                    "reply": e.text[:LIMIT],
                    "ref": f"{path}#{turn[-1].ref}",
                }
                rounds.append(open_round)
                break
        turn = []
    if turn and any(m in "\n".join(t.text for t in turn) for m in MARKERS.values()):
        # the last round is still waiting for its reply: resume at its question
        end = turn[0].line
    return rounds, end, False


def read_memories() -> Iterator[dict]:
    """Yield each Claude Code feedback memory as a round: its name and description, and its body."""
    for path in sorted((HOME / ".claude" / "projects").glob("*/memory/*.md")):
        text = path.read_text()
        head, _, body = text.partition("\n---\n")
        fields = {
            k: v.strip('"')
            for k, v in re.findall(r"^\s*(\w+):\s*(.+?)\s*$", head, re.MULTILINE)
        }
        if path.name == "MEMORY.md" or fields.get("type") != "feedback":
            continue
        yield {
            "ts": fields.get("modified", ""),
            "tool": "claude-memory",
            "project": path.parent.parent.name,
            "session": "",
            "ref": str(path),
            "source": "memory",
            "prompt": f"{fields.get('name', '')}: {fields.get('description', '')}",
            "reply": body.strip()[:LIMIT],
        }


def archive(store: Path) -> int:
    """Move the inbox into the monthly archive once the observer's report is confirmed."""
    inbox = store / "inbox.jsonl"
    if not inbox.exists():
        print("✓ Inbox is empty, nothing to archive")
        return 0
    rounds = [
        json.loads(line) for line in inbox.read_text().splitlines() if line.strip()
    ]
    (store / "rounds").mkdir(parents=True, exist_ok=True)
    for r in rounds:
        with (store / "rounds" / f"{(r['ts'] or 'unknown')[:7]}.jsonl").open("a") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    inbox.unlink()
    print(f"✓ Archived {len(rounds)} rounds to {store / 'rounds'}")
    return 0


def main() -> int:
    """Copy new rounds into the store and report counts."""
    ap = argparse.ArgumentParser(
        description="Copy question rounds from local agent sessions into the store."
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="print rounds, write nothing"
    )
    ap.add_argument(
        "--store", default=str(STORE), help=f"observation store (default: {STORE})"
    )
    ap.add_argument(
        "--archive",
        action="store_true",
        help="move the inbox into rounds/ after the report is confirmed",
    )
    args = ap.parse_args()

    store = Path(args.store)
    if args.archive:
        return archive(store)
    state_file = store / "state.json"
    try:
        state = json.loads(state_file.read_text()) if state_file.exists() else {}
    except json.JSONDecodeError as e:
        print(f"✗ Error: unreadable state file {state_file}: {e}", file=sys.stderr)
        return 1

    known = set(
        state.get("_rounds", [])
    )  # fingerprints of rounds already taken, to drop forked copies
    found: list[dict] = []
    for tool, (root, _) in READERS.items():
        for path in sorted(root.glob("*/*.jsonl")):
            seen = state.get(str(path), {})
            if seen.get("agent") or seen.get("offset", 0) >= path.stat().st_size:
                continue  # run by an agent, or nothing written since last time
            rounds, end, by_agent = extract(tool, path, seen.get("offset", 0))
            for r in rounds:
                key = hashlib.sha1(
                    f"{r['source']}{r['prompt']}{r['reply']}".encode()
                ).hexdigest()[:12]
                if key not in known:
                    known.add(key)
                    found.append(r)
            state[str(path)] = {"offset": end, "agent": by_agent}
    for r in read_memories():  # a memory reappears only when its text changes
        key = hashlib.sha1(
            f"{r['source']}{r['prompt']}{r['reply']}".encode()
        ).hexdigest()[:12]
        if key not in known:
            known.add(key)
            found.append(r)

    if args.dry_run:
        for r in found:
            print(json.dumps(r, ensure_ascii=False))
    else:
        store.mkdir(parents=True, exist_ok=True)
        with (store / "inbox.jsonl").open("a") as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in found)
        state["_rounds"] = sorted(known)
        state_file.write_text(json.dumps(state, indent=1))

    counts = Counter(r["source"] for r in found)
    summary = ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "nothing new"
    where = "" if args.dry_run else f" added to {store / 'inbox.jsonl'}"
    print(f"✓ {len(found)} rounds{where}: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
