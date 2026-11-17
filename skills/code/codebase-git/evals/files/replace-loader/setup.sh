#!/bin/sh
# Recreates the user's working copy in ./svc: the app switched to a new TOML loader, but the old one is still there.
set -e
rm -rf svc && mkdir svc && cd svc
git init -q -b main
git config user.name "Sam Ortiz" && git config user.email sam@example.com
export GIT_AUTHOR_DATE=2026-08-01T09:00:00 GIT_COMMITTER_DATE=2026-08-01T09:00:00
mkdir -p svc
cat > svc/config_loader.py <<'PY'
import json


def load(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
PY
printf 'from svc.config_loader import load\n\nconfig = load("config.json")\n' > svc/app.py
printf '{"port": 8080}\n' > config.json
printf '# svc\n\nReads its settings from `config.json`.\n' > README.md
printf '__pycache__/\n' >> .gitignore
git add -A && git commit -qm "feat(config): load settings from config.json"
# Uncommitted: a TOML loader added beside the old one, the app switched over, the JSON file left behind.
cat > svc/config_loader_new.py <<'PY'
import tomllib


def load(path: str) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)
PY
printf 'from svc.config_loader_new import load\n\nconfig = load("config.toml")\n' > svc/app.py
printf 'port = 8080\n' > config.toml
