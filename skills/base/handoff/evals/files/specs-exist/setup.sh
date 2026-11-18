#!/bin/sh
# Recreates ./shop: the search feature is specified, nothing is built yet.
set -e
rm -rf shop && mkdir shop && cd shop
git init -q -b main
git config user.name "Dana Lee" && git config user.email dana@example.com
mkdir -p docs/specs shop/core shop/adapters
touch shop/__init__.py shop/core/__init__.py shop/adapters/__init__.py
printf 'from dataclasses import dataclass\n\n\n@dataclass\nclass Product:\n    sku: str\n    title: str\n    price_cents: int\n' > shop/core/catalog.py
printf 'import json\nfrom pathlib import Path\n\nfrom shop.core.catalog import Product\n\n\ndef load_products(path: Path) -> list[Product]:\n    return [Product(**p) for p in json.loads(path.read_text())]\n' > shop/adapters/files.py
cat > docs/ARCHITECTURE.md <<'MD'
# Architecture

- `shop/core/` holds the domain and must not import from `shop/adapters/`; adapters depend on core, never the other way.
- Anything that touches files, the network, or the clock lives in `shop/adapters/`.
- Tests sit beside the code as `test_<module>.py` and run with `python3 -m unittest`.
MD
cat > docs/specs/search.md <<'MD'
# Search

## Background

Shoppers on the mobile site abandon the catalogue after scrolling about forty products, according to the March funnel review. Most of them came looking for one item they could already name, so the fastest win is a search box over titles. We looked at bringing in a search engine and decided against it for now: the catalogue is under two thousand products and fits in memory.

## Design notes

Matching is done in core on a list of products the adapter has already loaded. Titles are compared case-insensitively and accents are ignored, so "creme" finds "Crème brûlée". Results keep catalogue order; no ranking yet.

## Acceptance criteria

1. `search(products, "mug")` returns every product whose title contains "mug", ignoring case.
2. `search(products, "creme")` finds a product titled "Crème brûlée".
3. An empty or whitespace-only query returns an empty list.
4. `python3 -m unittest` passes, with a test for each criterion above.
MD
git add -A && git commit -qm "docs: specify search"
