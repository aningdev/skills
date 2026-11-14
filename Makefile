.PHONY: check fix push

# Read-only: skills against the spec and script rules, Python lint and format, Markdown/JSON format.
check:
	uv run --quiet --python 3.15 --with ./references/agentskills/skills-ref scripts/check_skills.py
	uvx ruff check --quiet skills scripts
	uvx ruff format --check --quiet skills scripts
	bunx oxfmt --check

# Rewrites files: autofix lint, then format Python and Markdown/JSON.
fix:
	uvx ruff check --fix --quiet skills scripts
	uvx ruff format --quiet skills scripts
	bunx oxfmt

# push, give GitHub a moment, then have magpie fetch this repo's skills again
push:
	git push
	sleep 15
	uv run --quiet scripts/update_skills.py
