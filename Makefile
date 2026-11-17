.PHONY: check eval fix

# SkillEvaluator Tier 1 (static, no LLM) over every skill; reports go to a temp dir, not the repo.
SKILLEVALUATOR = uv run --quiet --python 3.13 --with ./references/skillevaluator skillevaluator validate skills --tiers 1 --no-llm -r json -o $${TMPDIR:-/tmp}/skillevaluator
SKILLSPECTOR_WHEEL = https://github.com/NVIDIA/SkillSpector/releases/download/v2.13.4/skillspector-2.13.4-py3-none-any.whl

# Read-only: skills against the spec and script rules, Python lint and format, Markdown/JSON format.
check:
	uv run --quiet --python 3.15 --with ./references/agentskills/skills-ref scripts/check_skills.py
	uvx ruff check --quiet skills scripts
	uvx ruff format --check --quiet skills scripts
	bunx oxfmt --check
	$(SKILLEVALUATOR) --skip security,code-integrity

# Read-only, advisory: full SkillEvaluator Tier 1, adding the SkillSpector security scan and the Bandit/Gitleaks/
# dead-link checks that check skips. Read the report; failures are expected and don't stop make. Known misses: skills
# naming a target project's files (`docs/ARCHITECTURE.md`) count as missing references, Bandit and SkillSpector can't
# parse observer's Python 3.15 digest.py, and assets/observe-result links to references/ that exist only in the store.
# SkillSpector's yara-python has no wheel for Python 3.14, so it's installed as a 3.13 uv tool first.
eval:
	uv tool install --quiet --python 3.13 "skillspector @ $(SKILLSPECTOR_WHEEL)"
	-$(SKILLEVALUATOR)

# Rewrites files: autofix lint, then format Python and Markdown/JSON.
fix:
	uvx ruff check --fix --quiet skills scripts
	uvx ruff format --quiet skills scripts
	bunx oxfmt
