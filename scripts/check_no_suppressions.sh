#!/bin/bash
#
# Reject `# noqa` and `# type: ignore` in this repo's own Python.
#
# CLAUDE.md says a hook rejects both outright. Until now it did not, and the
# only thing stopping them was whoever was reading ruff's output. Vendored
# paths are exempt via gates/vendored.txt, which ruff already excludes.
set -euo pipefail

readonly PATTERN='#[[:space:]]*(noqa|type:[[:space:]]*ignore)'
status=0

for file in "$@"; do
    [[ -f "$file" ]] || continue
    case "$file" in
        */TRAK/sightpy/* | */EOPSY/lab[34]/task[34]/work/*) continue ;;
    esac
    if grep -nEH "$PATTERN" "$file"; then
        status=1
    fi
done

if [[ $status -ne 0 ]]; then
    echo "Fix the underlying finding instead of suppressing it (CLAUDE.md)." >&2
fi

exit "$status"
