#!/bin/sh
# Recreates the user's working copy in ./notes-cli: a history written in Chinese, then one uncommitted fix.
set -e
rm -rf notes-cli && mkdir notes-cli && cd notes-cli
git init -q -b main
git config user.name "Wei Chen" && git config user.email wei@example.com
export GIT_AUTHOR_DATE=2026-09-01T09:00:00 GIT_COMMITTER_DATE=2026-09-01T09:00:00
cat > notes.py <<'PY'
import sys


def main(argv: list[str]) -> int:
    if not argv:
        print("用法: notes add <内容>")
        return 1
    with open("notes.txt", "a") as f:
        f.write(" ".join(argv[1:]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
PY
git add -A && git commit -qm "feat(cli): 支持 notes add 追加一条笔记"
printf '# notes-cli\n\n命令行记笔记的小工具。\n' > README.md
git add -A && git commit -qm "docs: 补充 README 用法说明"
printf '.venv/\n__pycache__/\n' > .gitignore
git add -A && git commit -qm "chore: 忽略虚拟环境和缓存目录"
# Uncommitted: `notes add` with no text used to append an empty line; now it refuses.
cat > notes.py <<'PY'
import sys


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] != "add":
        print("用法: notes add <内容>")
        return 1
    with open("notes.txt", "a") as f:
        f.write(" ".join(argv[1:]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
PY
