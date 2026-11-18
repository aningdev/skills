#!/bin/sh
# Recreates ./ui-kit: five components, but llms.txt lists only three.
set -e
rm -rf ui-kit && mkdir ui-kit && cd ui-kit
git init -q -b main
git config user.name "Dana Lee" && git config user.email dana@example.com
mkdir -p components
for c in Button Input Dialog Card Tabs; do
  printf 'export function %s(props: Record<string, unknown>) {\n  return null;\n}\n' "$c" > "components/$c.tsx"
done
cat > llms.txt <<'TXT'
# ui-kit

- [Button](components/Button.tsx): triggers an action when clicked.
- [Input](components/Input.tsx): a single-line text field.
- [Dialog](components/Dialog.tsx): a modal window over the page.
TXT
cat > AGENTS.md <<'MD'
# ui-kit

- Every component in components/ has one line in llms.txt: `- [Name](components/Name.tsx): <what it is for, one sentence ending in a period>.`
- Keep llms.txt in the order components were added: Button, Input, Dialog, Card, Tabs.
- `make check` verifies llms.txt against components/.
MD
printf 'check:\n\t@for f in components/*.tsx; do n=$$(basename $$f .tsx); grep -q "^- \\[$$n\\](components/$$n.tsx): .*\\.$$" llms.txt || { echo "missing $$n"; exit 1; }; done; echo ok\n' > Makefile
git add -A && git commit -qm "feat: add Card and Tabs components"
