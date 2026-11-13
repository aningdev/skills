"""Validate every skill in skills/ against the Agent Skills spec (skills-ref).

Claude Code reads a few frontmatter fields the open spec doesn't list; they're
allowed here so the check fails only on real problems.
"""

import sys
from pathlib import Path

from skills_ref import validate, validator

CLAUDE_CODE_FIELDS = {
    "disable-model-invocation",
    "argument-hint",
    "model",
    "when_to_use",
}
validator.ALLOWED_FIELDS |= CLAUDE_CODE_FIELDS

failed = 0
for skill in sorted(Path("skills").glob("*/*/SKILL.md")):
    problems = validate(skill.parent)
    if problems:
        failed += 1
        print(f"✗ {skill.parent}")
        for problem in problems:
            print(f"    {problem}")

total = len(list(Path("skills").glob("*/*/SKILL.md")))
print(f"{total - failed}/{total} skills valid")
sys.exit(1 if failed else 0)
