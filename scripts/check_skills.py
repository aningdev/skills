#!/usr/bin/env python3
# /// script
# requires-python = ">=3.15"
# dependencies = []  # skills-ref comes from the submodule: see `make check`
# ///

"""Validate every skill in skills/: the Agent Skills spec, and the script rules in docs/ARCHITECTURE.md.

Claude Code reads a few frontmatter fields the open spec doesn't list; they're allowed
here so the check fails only on real problems.

Usage:
    make check
"""

import re
import sys
from pathlib import Path

from skills_ref import validate, validator

CLAUDE_CODE_FIELDS = frozenset(
    {"disable-model-invocation", "argument-hint", "model", "when_to_use"}
)
validator.ALLOWED_FIELDS |= CLAUDE_CODE_FIELDS


def script_problems(path: Path) -> list[str]:
    """Return what a bundled script is missing from its required header."""
    text = path.read_text()
    problems = []
    if not text.startswith("#!/usr/bin/env "):
        problems.append("no `#!/usr/bin/env` shebang")
    if not path.stat().st_mode & 0o111:
        problems.append("not executable")
    if path.suffix == ".py":
        if "# /// script" not in text or "requires-python" not in text:
            problems.append("no PEP 723 `# /// script` block with requires-python")
        if not re.search(r'""".*?Usage:.*?"""', text, re.DOTALL):
            problems.append("module docstring has no Usage section")
    if path.suffix == ".sh":
        if "set -euo pipefail" not in text:
            problems.append("no `set -euo pipefail`")
        if not re.search(r"^# Usage:", text, re.MULTILINE):
            problems.append("header has no Usage section")
    return problems


def main() -> int:
    """Validate skills and their scripts, and print a summary."""
    skills = sorted(Path("skills").glob("*/*/SKILL.md"))
    failed = 0
    for skill in skills:
        scripts = [
            s
            for s in sorted(skill.parent.glob("scripts/*"))
            if s.suffix in {".py", ".sh"}
        ]
        script_issues = [
            *(f"{s.name}: {p}" for p in script_problems(s)) for s in scripts
        ]
        problems = [*validate(skill.parent), *script_issues]
        if problems:
            failed += 1
            print(f"✗ {skill.parent}", file=sys.stderr)
            for problem in problems:
                print(f"    {problem}", file=sys.stderr)
    print(f"✓ {len(skills) - failed}/{len(skills)} skills valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
