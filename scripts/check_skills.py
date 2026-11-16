#!/usr/bin/env python3
# /// script
# requires-python = ">=3.15"
# dependencies = []  # skills-ref comes from the submodule: see `make check`
# ///

"""Validate every skill in skills/: the Agent Skills spec, and the script and role rules in docs/ARCHITECTURE.md.

Only the spec's frontmatter fields pass, so every skill stays portable across agent tools.

Usage:
    make check
"""

import re
import sys
from pathlib import Path

from skills_ref import validate


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


def grilling_problems(role: Path, moments: list[str]) -> list[str]:
    """Return what a role is missing of the self-grilling points, answer rule, and calls format it must embed."""
    text = role.read_text()
    problems = [
        f"self-grilling text not embedded verbatim: {m[:50]}…"
        for m in moments
        if m not in text
    ]
    if f"Calls I made as {role.parent.name}:" not in text:
        problems.append(f"no `Calls I made as {role.parent.name}:` format")
    return problems


def main() -> int:
    """Validate skills and their scripts, and print a summary."""
    skills = sorted(Path("skills").glob("*/*/SKILL.md"))
    grilling = Path("skills/base/self-grilling/SKILL.md").read_text()
    body = grilling.split("at three points:", 1)[1]
    moments = re.findall(r"^(?:- |Answer each by ).+$", body, re.MULTILINE)
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
        role_issues = (
            grilling_problems(skill, moments) if skill.parts[1] == "agents" else []
        )
        problems = [*validate(skill.parent), *script_issues, *role_issues]
        if problems:
            failed += 1
            print(f"✗ {skill.parent}", file=sys.stderr)
            for problem in problems:
                print(f"    {problem}", file=sys.stderr)
    print(f"✓ {len(skills) - failed}/{len(skills)} skills valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
