#!/bin/bash

# ============================================================================
# Fail if any TRACKED file is also matched by a .gitignore rule.
#
# That combination fails silently: `git add` on such a file is not an error,
# the edit simply never lands. This repo had 130 of them -- dist/ swallowing
# the vendored jQuery bundle, and the LaTeX template's man-page patterns
# (*.[1-9]) eating EPFU's date-named doc/21.11/ directory along with its
# report.pdf.
#
# They were fixed by hand once. This is the gate that keeps them fixed, so
# that .binary-allowlist can stop *instructing* the reader to re-run a command
# and just have it enforced instead.
#
# Usage: scripts/check_ignore_consistency.sh
# ============================================================================

set -euo pipefail

main() {
    local offenders
    offenders="$(git ls-files | git check-ignore --stdin --no-index 2>/dev/null || true)"

    if [[ -z "$offenders" ]]; then
        exit 0
    fi

    echo "Tracked files that .gitignore also matches:" >&2
    printf '%s\n' "$offenders" | sed 's/^/  /' >&2
    cat >&2 <<'MSG'

Each of these fails SILENTLY on `git add` -- not an error, the edit just
never lands. Fix by either:
  1. adding a "!" override in .gitignore (if the file belongs in the repo), or
  2. `git rm --cached` it (if it is build output that should never have been
     tracked; --cached keeps it on disk).
MSG
    exit 1
}

main "$@"
