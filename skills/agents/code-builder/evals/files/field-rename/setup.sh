#!/bin/sh
# Recreates ./profile-api: a JSON endpoint that a shipped mobile app reads by field name.
set -e
rm -rf profile-api && mkdir profile-api && cd profile-api
git init -q -b main
git config user.name "Dana Lee" && git config user.email dana@example.com
mkdir -p profile_api tests
cat > profile_api/__init__.py <<'PY'
PY
cat > profile_api/api.py <<'PY'
"""GET /v1/profile: the signed-in user's profile as JSON."""

import json


def profile(user: dict) -> str:
    """The profile response body."""
    return json.dumps(
        {
            "id": user["id"],
            "user_name": user["name"],
            "avatarUrl": user["avatar"],
            "createdAt": user["created"],
        }
    )
PY
cat > tests/test_api.py <<'PY'
import json
import unittest

from profile_api.api import profile

USER = {"id": 7, "name": "sam", "avatar": "https://cdn.example.com/a/7.png", "created": "2026-01-02"}


class ProfileTest(unittest.TestCase):
    def test_fields(self):
        body = json.loads(profile(USER))
        self.assertEqual(body["id"], 7)
        self.assertEqual(body["avatarUrl"], USER["avatar"])


if __name__ == "__main__":
    unittest.main()
PY
cat > README.md <<'MD'
# profile-api

Serves `GET /v1/profile` to our mobile app. The app's 2.3 release, live in the App Store and Play Store,
parses the response by field name; users update the app on their own schedule.

Run the tests with `make test`.
MD
printf 'test:\n\tpython3 -m unittest discover -s tests\n' > Makefile
git add -A && git commit -qm "feat: serve the signed-in user's profile"
