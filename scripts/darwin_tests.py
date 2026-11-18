#!/usr/bin/env python3
"""Write a skill's darwin-skill test set from its evals/evals.json, so the cases live in one place.

Only cases marked with `"split": "dev"` or `"split": "holdout"` are taken; negative cases
(`expected_skill: null`) never are, since darwin measures what a skill adds over a bare model.
Assertions become darwin's checks, and fixture paths are given from the skill's directory.

Usage:
    python3 scripts/darwin_tests.py skills/<layer>/<name>   # writes <skill>/test-prompts.json
"""

import json
import sys
from pathlib import Path


def convert(skill: Path) -> list[dict]:
    """The darwin test entries for one skill, dev cases first."""
    evals = json.loads((skill / "evals" / "evals.json").read_text())["evals"]
    tests = [
        {
            "id": e["id"],
            "split": e["split"],
            "source": e.get("source", "doc"),
            "prompt": e["prompt"],
            "files": [f"evals/{f}" for f in e.get("files", [])],
            "checks": e.get("assertions", []),
        }
        for e in evals
        if e.get("split") in ("dev", "holdout") and e.get("expected_skill")
    ]
    return sorted(tests, key=lambda t: t["split"] != "dev")


def main() -> int:
    """Convert the skill named on the command line."""
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    skill = Path(sys.argv[1])
    tests = convert(skill)
    if not tests:
        print(f"✗ No case in {skill}/evals/evals.json has a split", file=sys.stderr)
        return 1
    out = skill / "test-prompts.json"
    out.write_text(json.dumps(tests, ensure_ascii=False, indent=2) + "\n")
    counts = {s: sum(t["split"] == s for t in tests) for s in ("dev", "holdout")}
    print(f"✓ {out}: {counts['dev']} dev, {counts['holdout']} holdout")
    return 0


if __name__ == "__main__":
    sys.exit(main())
