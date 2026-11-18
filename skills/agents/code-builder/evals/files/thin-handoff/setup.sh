#!/bin/sh
# Recreates ./exporter: a report exporter, and a thin handoff left by the previous session.
set -e
rm -rf exporter && mkdir exporter && cd exporter
git init -q -b main
git config user.name "Dana Lee" && git config user.email dana@example.com
mkdir -p exporter
touch exporter/__init__.py
cat > exporter/report.py <<'PY'
import json
from pathlib import Path

Row = dict[str, object]


def export_json(rows: list[Row], path: Path) -> None:
    path.write_text(json.dumps(rows, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    export_json([{"name": "张三", "orders": 3}, {"name": "Li, Wei", "orders": 5}], Path("report.json"))
PY
git add -A && git commit -qm "feat(report): export rows as JSON"
cat > HANDOFF.md <<'MD'
# 交接

上一个会话在做：把导出改成支持 CSV。已经看过 exporter/report.py，还没动代码。接着做。
MD
