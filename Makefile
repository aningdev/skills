.PHONY: check

check:
	uv run --quiet --project references/agentskills/skills-ref python scripts/check_skills.py
