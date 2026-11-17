#!/bin/sh
# Recreates the user's working copy in ./invoicer: two committed releases, then uncommitted work.
set -e
rm -rf invoicer && mkdir invoicer && cd invoicer
git init -q -b main
git config user.name "Dana Lee" && git config user.email dana@example.com
export GIT_AUTHOR_DATE=2026-10-01T09:00:00 GIT_COMMITTER_DATE=2026-10-01T09:00:00
mkdir -p invoicer tests
cat > invoicer/money.py <<'PY'
def round_cents(amount: float) -> float:
    return int(amount * 100) / 100
PY
cat > invoicer/invoice.py <<'PY'
from invoicer.money import round_cents


def total(lines: list[tuple[float, int]]) -> float:
    return round_cents(sum(price * qty for price, qty in lines))
PY
cat > tests/test_invoice.py <<'PY'
from invoicer.invoice import total


def test_total():
    assert total([(2.5, 2), (1.0, 1)]) == 6.0
PY
printf '# Invoicer\n\nComputes invoice totlas for small shops.\n' > README.md
printf '__pycache__/\n' >> .gitignore
git add -A && git commit -qm "feat(invoice): compute totals from priced lines"
printf 'def test_placeholder():\n    pass\n' > tests/test_money.py
git add -A && git commit -qm "test(money): add money test module"
# Uncommitted: a discount feature, an unrelated rounding fix, and a README typo fix.
cat > invoicer/invoice.py <<'PY'
from invoicer.money import round_cents


def total(lines: list[tuple[float, int]], discount: float = 0.0) -> float:
    """Sum priced lines, then apply a fractional discount (0.1 = 10% off)."""
    if not 0.0 <= discount < 1.0:
        raise ValueError("discount must be in [0, 1)")
    return round_cents(sum(price * qty for price, qty in lines) * (1 - discount))
PY
cat >> tests/test_invoice.py <<'PY'


def test_total_with_discount():
    assert total([(10.0, 2)], discount=0.25) == 15.0
PY
cat > invoicer/money.py <<'PY'
from decimal import ROUND_HALF_UP, Decimal


def round_cents(amount: float) -> float:
    # Round half up instead of truncating, so 0.105 becomes 0.11.
    return float(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
PY
printf 'def test_rounds_half_up():\n    from invoicer.money import round_cents\n    assert round_cents(0.105) == 0.11\n' > tests/test_money.py
printf '# Invoicer\n\nComputes invoice totals for small shops.\n' > README.md
