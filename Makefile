.PHONY: check eval live fix

# SkillEvaluator Tier 1 (static, no LLM) over every skill; reports go to a temp dir, not the repo.
SKILLEVALUATOR = skillevaluator validate skills --policy skillevaluator-policy.yaml --tiers 1 --no-llm -r json -o $${TMPDIR:-/tmp}/skillevaluator
LIVE_URL ?= http://127.0.0.1:3425/v1
LIVE_MODEL ?= opencode-go/deepseek-v4.1-flash

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
eval:
	-$(SKILLEVALUATOR)

# Live, costs model calls: SkillEvaluator Tier 3 on one skill, with and without it, run by OpenCode on this host
# (--env-mode local, inside macOS Seatbelt). Usage: make live SKILL=skills/code/codebase-git. Cases live in the skill's
# evals/evals.json; with none, a one-case starter is generated there. Needs opencode 1.19.5 under SkillEvaluator's
# runtime dir (see AGENTS.md). SkillEvaluator must be a real install (a uv tool), not `uv run --with`: the verifier's
# sandbox can't read uv's overlay env, so it would fail on `import idna` and leave no reward. Docker mode isn't used: on Kiri,
# `compose cp dir/.` copies the dir itself, so Harbor never finds the reward file. Set SKILL_EVAL_LLM_API_KEY if the
# gateway wants one; loopback needs none.
live:
	@test -n "$(SKILL)" || { echo "usage: make live SKILL=skills/<layer>/<name>"; exit 2; }
	SKILL_EVAL_LLM_PROVIDER=openai-compatible SKILL_EVAL_LLM_BASE_URL=$(LIVE_URL) \
	SKILL_EVAL_LLM_API_KEY=$${SKILL_EVAL_LLM_API_KEY:-local} SKILL_EVAL_LLM_MODEL=$(LIVE_MODEL) \
	SKILL_EVAL_MODEL_CATALOG_ALLOW_HTTP_HOSTS=127.0.0.1 \
	skillevaluator tier3 $(SKILL) --agents opencode --env-mode local \
		--agent-model opencode=openai/$(LIVE_MODEL) --timeout-multiplier 2 $(LIVE_ARGS)

# Rewrites files: autofix lint, then format Python and Markdown/JSON.
fix:
	uvx ruff check --fix --quiet skills scripts
	uvx ruff format --quiet skills scripts
	bunx oxfmt
