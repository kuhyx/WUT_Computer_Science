#!/bin/bash

# ============================================================================
# Run the pytest suites that exist in this archive, each from its own directory
# (ECRYPT sieve reads its reference CSVs by relative path, so a repo-root
# `pytest` cannot collect it). Extra args are passed to every pytest run.
# Usage: scripts/test_suites.sh [pytest args]
#        COVERAGE=1 scripts/test_suites.sh   # writes coverage.xml at repo root
# ============================================================================

set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
readonly ROOT
readonly SUITES=(Programming/ECOTE Programming/ECRYPT_PROJECT/sieve)

run_suites() {
    local -a suites=("$@") extra=()
    [[ ${#suites[@]} -eq 0 ]] && suites=("${SUITES[@]}")
    if [[ "${COVERAGE:-0}" == 1 ]]; then
        export COVERAGE_FILE="$ROOT/.coverage"
        rm -f "$COVERAGE_FILE" "$ROOT/coverage.xml"
    fi
    local rc=0 s
    for s in "${suites[@]}"; do
        if [[ "${COVERAGE:-0}" == 1 ]]; then
            extra=(--cov="$ROOT/$s" --cov-branch --cov-append --cov-config="$ROOT/pyproject.toml")
        fi
        (cd "$ROOT/$s" && python3 -m pytest -q --tb=short "${extra[@]}" "${PYTEST_ARGS[@]}") || rc=$?
    done
    if [[ "${COVERAGE:-0}" == 1 ]]; then
        (cd "$ROOT" && python3 -m coverage xml -o coverage.xml --rcfile=pyproject.toml >/dev/null)
    fi
    return "$rc"
}

PYTEST_ARGS=("$@")
[[ -n "${SUITE_DIRS:-}" ]] && read -r -a SELECTED <<<"$SUITE_DIRS" || SELECTED=()
run_suites "${SELECTED[@]}"
exit $?
