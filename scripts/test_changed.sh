#!/bin/bash

# ============================================================================
# Run only the pytest suites whose directory has changes vs HEAD (staged,
# unstaged and untracked). Quiet: failures plus a one-line summary per suite.
# Changes to shared config (pyproject.toml, this repo's test scripts) run all
# suites; changes outside any suite run nothing.
# ============================================================================

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
readonly ROOT
readonly SUITES=(Programming/ECOTE Programming/ECRYPT_PROJECT/sieve)

changed="$(cd "$ROOT" && { git diff --name-only HEAD 2>/dev/null || true; git ls-files --others --exclude-standard; } | sort -u)"
selected=()
all=0
for s in "${SUITES[@]}"; do
    grep -q "^${s}/" <<<"$changed" && selected+=("$s")
done
grep -Eq '^(pyproject\.toml|scripts/test_suites\.sh|scripts/test_changed\.sh)$' <<<"$changed" && all=1

if [[ $all -eq 1 ]]; then
    echo "shared test config changed: running all suites"
    exec "$ROOT/scripts/test_suites.sh"
fi
if [[ ${#selected[@]} -eq 0 ]]; then
    echo "no changes in a pytest suite: nothing to test"
    exit 0
fi
SUITE_DIRS="${selected[*]}" exec "$ROOT/scripts/test_suites.sh"
