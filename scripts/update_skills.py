#!/usr/bin/env python3
# /// script
# requires-python = ">=3.15"
# dependencies = []
# ///

"""Have magpie fetch this repo's skills from GitHub again, after a push.

Only the skills magpie installed from this repo (its `origin` on GitHub) are updated;
skills from anywhere else are left alone. A skill edited by hand in magpie's library is
kept as it is, and magpie says so.

Usage:
    make push                          # push, wait for GitHub, then update
    uv run scripts/update_skills.py
    uv run scripts/update_skills.py --dry-run
"""

import json
import re
import subprocess
import sys
from pathlib import Path
lazy import argparse

LIBRARY = Path.home() / ".config" / "magpie" / "library.json"


def origin_repo() -> str:
    """This repo's `owner/name` on GitHub, from its origin remote."""
    url = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    found = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    if not found:
        raise SystemExit(f"✗ Error: origin isn't on GitHub: {url}")
    return found.group(1)


def main() -> int:
    """Update every magpie skill whose source is this repo."""
    ap = argparse.ArgumentParser(description="Update this repo's skills in magpie.")
    ap.add_argument(
        "--dry-run", action="store_true", help="list the skills, update nothing"
    )
    args = ap.parse_args()

    repo = origin_repo()
    try:
        library = json.loads(LIBRARY.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"✗ Error: can't read magpie's library {LIBRARY}: {e}", file=sys.stderr)
        return 1
    names = [
        s["name"]
        for s in library.get("skills", [])
        if (s.get("source") or {}).get("repo") == repo
    ]
    if not names:
        print(f"✓ No magpie skills come from {repo}")
        return 0
    if args.dry_run:
        print(f"✓ Would update {len(names)} skills from {repo}: {', '.join(names)}")
        return 0
    failed = [
        name
        for name in names
        if subprocess.run(
            ["magpie", "library", "skill", "update", name], check=False
        ).returncode
    ]
    if failed:
        print(
            f"✗ Error: {len(failed)} skills failed to update: {', '.join(failed)}",
            file=sys.stderr,
        )
        return 1
    print(f"✓ Updated {len(names)} skills from {repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
