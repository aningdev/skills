#!/usr/bin/env python3
# /// script
# requires-python = ">=3.15"
# dependencies = []
# ///

"""Copy every question round from local agent sessions into the observation store.

A round is a block of questions an agent put to the user (a grilling round, an ask tool
such as AskUserQuestion, or a self-grilling `Calls I made as <role>:` list) together with the
user's reply, kept as raw text. A turn in which the agent changed files is a round too, with
source `delivery`: the agent's closing words and whatever the user said next, since that's
where corrections of delivered work show up. Nothing is judged here: the observer reads the rounds and
goes back to the session through `ref` when it needs more. Each agent tool has a reader
in READERS (Claude Code, pi, Codex, grok, dsh); add one to support another tool.

Feedback the agents already distilled during a session, Claude Code's per-project
memory files of type `feedback`, is copied too, as rounds with source `memory`, so the
observer can promote what several projects agree on and skip what one project keeps.
So is the friction Claude Code's `/insights` already summarised per session (the cached
facets in `~/.claude/usage-data/`), as rounds with source `friction`: corrections the user
made after seeing a result, which no question round shows.

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
import io
import json
import re
import sys
from collections import Counter
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
lazy import argparse
lazy from compression import zstd

HOME = Path.home()
STORE = HOME / ".agents" / "skills" / "observe-result" / ".observer"
LIMIT = 6000  # characters kept per prompt or reply
CLOSING = 300  # characters kept of an agent's closing words on a delivery
# a reply that is a pasted log or an injected skill, not the user's words
PASTED = re.compile(r"^\s*(?:[<{]|\d{4}-\d\d-\d\dT\d|\S+\s*\|\s*\d{4}-\d\d-\d\d)")

# A round starts only where its marker opens a line (after any list, quote, heading, or table
# markup) or a new sentence; a marker quoted mid-sentence isn't one. A grilling round keeps
# its goal line.
MARKERS = frozendict(
    grilling=re.compile(
        r"(?:^[ \t>*#|-]*|(?<=[。！？.!?] ))(?:🎯\s*(?:\[([^\]\n]+)\])?.*\n+[ \t>*#|-]*)?❓",
        re.MULTILINE,
    ),
    **{"self-grilling": re.compile(r"^Calls I made(?: as ([^:\n]+))?:", re.MULTILINE)},
)
EDITS = frozenset(
    {
        "Edit",
        "Write",
        "MultiEdit",
        "NotebookEdit",
        "edit",
        "write",
        "search_replace",
        "apply_patch",
    }
)
INJECTED = ("# AGENTS.md instructions", "<environment_context", "<user_instructions")
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
    kind: str  # "user", "agent" (another agent writing as the user), "assistant", "ask", or "edit"
    text: str
    ts: str
    cwd: str
    ref: str


def open_log(path: Path) -> io.BufferedIOBase:
    """Open a session log as bytes, decompressing a zstd one (dsh) whole."""
    if path.suffix == ".zstd":
        return io.BytesIO(zstd.decompress(path.read_bytes()))
    return path.open("rb")


def log_size(path: Path) -> int:
    """The length of a session log's content, where reading resumes once it's all read."""
    with open_log(path) as f:
        return f.seek(0, io.SEEK_END)


def session_id(path: Path) -> str:
    """The short id of the session a log belongs to, from the last uuid in its path."""
    ids = re.findall(r"[0-9a-f]{8}-[0-9a-f]{4}-", str(path))
    return ids[-1][:8] if ids else path.stem[:8]


def text_of(content: object, *kinds: str) -> str:
    """Join the text blocks of a message's content, or return it when it's a string."""
    if isinstance(content, str):
        return content
    return " ".join(
        b.get("text", "") for b in content or [] if b.get("type") in kinds
    ).strip()


def read_jsonl(path: Path, offset: int) -> Iterator[tuple[int, dict]]:
    """Yield (byte offset, record) for each parseable JSON line from `offset` on."""
    with open_log(path) as f:
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
                elif b.get("type") == "tool_use" and b.get("name") in EDITS:
                    yield Event(i, "edit", b["name"], ts, cwd, ref)


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
        elif msg.get("role") == "assistant":
            if text:
                yield Event(i, "assistant", text, ts, cwd, ref)
            if any(
                b.get("type") == "toolCall" and b.get("name") in EDITS
                for b in content or []
                if isinstance(content, list)
            ):
                yield Event(i, "edit", "", ts, cwd, ref)


def read_codex(path: Path, offset: int) -> Iterator[Event]:
    """Read a Codex session: the user's words without injected context, AI text, patches, and request_user_input answers."""
    cwd = (next(read_jsonl(path, 0), (0, {}))[1].get("payload") or {}).get("cwd", "")
    asks: dict[str, str] = {}
    for i, d in read_jsonl(path, offset):
        p = d.get("payload") or {}
        if d.get("type") != "response_item":
            continue
        ts, ref, kind = d.get("timestamp", ""), p.get("id") or str(i), p.get("type")
        if kind == "message" and p.get("role") == "user":
            text = text_of(p.get("content"), "input_text")
            if text and not text.startswith(INJECTED):
                yield Event(i, "user", text, ts, cwd, ref)
        elif kind == "message" and p.get("role") == "assistant":
            if text := text_of(p.get("content"), "output_text"):
                yield Event(i, "assistant", text, ts, cwd, ref)
        elif kind in ("function_call", "custom_tool_call"):
            args = p.get("arguments") or p.get("input") or ""
            if p.get("name") in EDITS or "*** Begin Patch" in args:
                yield Event(i, "edit", "", ts, cwd, ref)
            elif p.get("name", "").startswith("request_user_input"):
                asks[p.get("call_id", "")] = args
        elif p.get("call_id") in asks:  # the answer to a request_user_input call
            answer = {"questions": asks.pop(p["call_id"]), "answers": p.get("output")}
            yield Event(i, "ask", json.dumps(answer, ensure_ascii=False), ts, cwd, ref)


def read_grok(path: Path, offset: int) -> Iterator[Event]:
    """Read a grok session: the <user_query> the user typed, AI text, edits, and ask_user_question answers. A session with no human operator is marked 'agent'."""
    try:
        summary = json.loads(path.with_name("summary.json").read_text())
    except OSError, json.JSONDecodeError:
        summary = {}
    cwd, ts = (summary.get("info") or {}).get("cwd", ""), summary.get("created_at", "")
    asks: dict[str, str] = {}
    for i, d in read_jsonl(path, offset):
        kind, text = d.get("type"), text_of(d.get("content"), "text")
        if kind == "system" and "no human operator" in text:
            yield Event(i, "agent", "", ts, cwd, str(i))
            return
        if kind == "user" and (
            asked := re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.DOTALL)
        ):
            yield Event(i, "user", asked.group(1), ts, cwd, str(i))
        elif kind == "assistant":
            if text.strip():
                yield Event(i, "assistant", text, ts, cwd, str(i))
            for call in d.get("tool_calls") or []:
                if call.get("name") in EDITS:
                    yield Event(i, "edit", "", ts, cwd, str(i))
                elif call.get("name") == "ask_user_question":
                    asks[call.get("id", "")] = call.get("arguments", "")
        elif kind == "tool_result" and d.get("tool_call_id") in asks:
            answer = {"questions": asks.pop(d["tool_call_id"]), "answers": text}
            yield Event(
                i, "ask", json.dumps(answer, ensure_ascii=False), ts, cwd, str(i)
            )


def read_dsh(path: Path, offset: int) -> Iterator[Event]:
    """Read a dsh session: the user's messages, AI text, edits, and ask_user_question answers. A delegated session is marked 'agent'."""
    header = next(read_jsonl(path, 0), (0, {}))[1]  # the session line carries cwd
    cwd = header.get("cwd", "")
    if header.get("delegationDepth"):
        yield Event(0, "agent", "", "", cwd, "")
        return
    asks: dict[str, str] = {}
    for i, d in read_jsonl(path, offset):
        kind, data = d.get("type"), d.get("data") or {}
        ts = datetime.fromtimestamp(d.get("time", 0) / 1000, UTC).isoformat()
        ref = str(d.get("seq", i))
        if kind == "user/message" and (data.get("source") or {}).get("kind") == "user":
            if text := text_of(data.get("content"), "text"):
                yield Event(i, "user", text, ts, cwd, ref)
        elif kind == "assistant/message":
            if text := text_of((data.get("message") or {}).get("content"), "text"):
                yield Event(i, "assistant", text, ts, cwd, ref)
        elif kind == "tool/call" and data.get("name") in EDITS:
            yield Event(i, "edit", "", ts, cwd, ref)
        elif kind == "tool/call" and data.get("name") == "ask_user_question":
            asks[data.get("callId", "")] = data.get("arguments", "")
        elif kind == "tool/result":
            message = data.get("message") or {}
            call = (message.get("source") or {}).get("callId")
            if call in asks:
                answer = {
                    "questions": asks.pop(call),
                    "answers": message.get("content"),
                }
                yield Event(
                    i, "ask", json.dumps(answer, ensure_ascii=False), ts, cwd, ref
                )


type Reader = Callable[[Path, int], Iterator[Event]]
# per tool: where its sessions live, which files are session logs, and how to read one
READERS: frozendict[str, tuple[Path, str, Reader]] = frozendict(
    claude=(HOME / ".claude" / "projects", "*/*.jsonl", read_claude),
    pi=(HOME / ".pi" / "agent" / "sessions", "*/*.jsonl", read_pi),
    codex=(HOME / ".codex" / "sessions", "**/*.jsonl", read_codex),
    grok=(HOME / ".grok" / "sessions", "*/*/chat_history.jsonl", read_grok),
    dsh=(HOME / ".dsh" / "sessions", "*/*/session.v3.jsonl.zstd", read_dsh),
)


def extract(tool: str, path: Path, offset: int) -> tuple[list[dict], int, bool]:
    """Read a session from `offset`: its new rounds, where to resume, and whether an agent ran it."""
    events = list(READERS[tool][2](path, offset))
    end = log_size(path)
    if any(e.kind == "agent" for e in events):
        # a session run by another agent holds none of the user's words
        return [], end, True
    rounds: list[dict] = []
    open_round: dict | None = None  # a round still collecting the user's reply
    turn: list[Event] = []
    for e in events:
        if e.kind in ("assistant", "edit"):
            open_round = None  # the reply is complete once the agent speaks again
            turn.append(e)
            continue
        base = {
            "ts": e.ts,
            "tool": tool,
            "project": e.cwd,
            "session": session_id(path),
            "role": "",
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
        said = "\n".join(t.text for t in turn if t.kind == "assistant")
        for source, marker in MARKERS.items():
            if found := find_marker(marker, said):
                at = found.start()
                open_round = {
                    **base,
                    "source": source,
                    "role": (found.group(1) or "").strip(),  # who asked, or who decided
                    "prompt": said[at:][:LIMIT],
                    "reply": e.text[:LIMIT],
                    "ref": f"{path}#{turn[-1].ref}",
                }
                rounds.append(open_round)
                break
        else:
            if any(t.kind == "edit" for t in turn) and not PASTED.match(e.text):
                open_round = {
                    **base,
                    "source": "delivery",
                    "prompt": said[
                        -CLOSING:
                    ],  # the agent's closing words on what it did
                    "reply": e.text[:LIMIT],
                    "ref": f"{path}#{turn[-1].ref}",
                }
                rounds.append(open_round)
        turn = []
    said = "\n".join(t.text for t in turn if t.kind == "assistant")
    if turn and (
        any(t.kind == "edit" for t in turn)
        or any(find_marker(m, said) for m in MARKERS.values())
    ):
        # the last round is still waiting for its reply: resume at its question
        end = turn[0].line
    return rounds, end, False


def find_marker(marker: re.Pattern[str], text: str) -> re.Match[str] | None:
    """The first marker outside a fenced code block: one inside a fence is an example, not a round."""
    for found in marker.finditer(text):
        if text.count("```", 0, found.start()) % 2 == 0:
            return found
    return None


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
            "role": "",
            "ref": str(path),
            "source": "memory",
            "prompt": f"{fields.get('name', '')}: {fields.get('description', '')}",
            "reply": body.strip()[:LIMIT],
        }


def read_facets() -> Iterator[dict]:
    """Yield each session `/insights` found friction in: what the user wanted, and what went wrong."""
    usage = HOME / ".claude" / "usage-data"
    for path in sorted((usage / "facets").glob("*.json")):
        try:
            facet = json.loads(path.read_text())
            meta_file = usage / "session-meta" / path.name
            meta = json.loads(meta_file.read_text()) if meta_file.exists() else {}
        except json.JSONDecodeError:
            continue
        if not facet.get("friction_detail"):
            continue
        kinds = ", ".join(facet.get("friction_counts", {}))
        yield {
            "ts": meta.get("start_time", ""),
            "tool": "claude-insights",
            "project": meta.get("project_path", ""),
            "session": facet.get("session_id", path.stem)[:8],
            "role": "",
            "ref": str(path),
            "source": "friction",
            "prompt": f"{facet.get('underlying_goal', '')} [{kinds}]",
            "reply": facet["friction_detail"][:LIMIT],
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
    for tool, (root, pattern, _) in READERS.items():
        for path in sorted(root.glob(pattern)):
            seen, size = state.get(str(path), {}), path.stat().st_size
            if seen.get("agent") or seen.get("size", seen.get("offset", 0)) >= size:
                continue  # run by an agent, or nothing written since last time
            rounds, end, by_agent = extract(tool, path, seen.get("offset", 0))
            for r in rounds:
                key = hashlib.sha1(
                    f"{r['source']}{r['prompt']}{r['reply']}".encode()
                ).hexdigest()[:12]
                if key not in known:
                    known.add(key)
                    found.append(r)
            state[str(path)] = {"offset": end, "size": size, "agent": by_agent}
    for r in (
        *read_memories(),
        *read_facets(),
    ):  # each reappears only when its text changes
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
