#!/bin/bash

# ============================================================================
# Set this repository up for development.
#
# Usage:
#   ./install.sh            install tools and wire the git hooks
#   ./install.sh --check    verify only; exit 1 if anything is missing
#
# Idempotent: a second run reports what is already present and changes nothing.
#
# It ENDS by verifying, and fails loudly if the gate is not actually runnable.
# A warning here would just recreate the bug it exists to prevent: the hooks
# were absent from this repo entirely, so every "pre-commit passed" claim
# before now was vacuous.
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly UTILS_ROOT="${UTILS_ROOT:-$HOME/utils}"

CHECK_ONLY=0

log() { printf '==> %s\n' "$*"; }
err() { printf 'error: %s\n' "$*" >&2; }

usage() {
    grep -E '^#   \./install\.sh' "${BASH_SOURCE[0]}" | sed 's/^#   //'
    exit 0
}

# The shared gates are not vendored here on purpose -- they live in one repo so
# that every repo enforces the same rule. Without them the hooks cannot run.
check_shared_gates() {
    if [[ ! -d "$UTILS_ROOT" ]]; then
        err "shared gates not found at $UTILS_ROOT"
        err "  git clone https://github.com/kuhyx/utils \"$UTILS_ROOT\""
        err "  (or set UTILS_ROOT to where it lives)"
        return 1
    fi
    log "shared gates: $UTILS_ROOT"
}

install_tools() {
    local missing=()
    command -v shellcheck > /dev/null 2>&1 || missing+=(shellcheck)
    command -v pre-commit > /dev/null 2>&1 || missing+=(pre-commit)

    if [[ ${#missing[@]} -eq 0 ]]; then
        log "tools already present: shellcheck, pre-commit"
        return 0
    fi

    if [[ $CHECK_ONLY -eq 1 ]]; then
        err "missing tools: ${missing[*]}"
        return 1
    fi

    log "installing: ${missing[*]}"
    if command -v pacman > /dev/null 2>&1; then
        sudo pacman -S --needed --noconfirm "${missing[@]}"
    elif command -v apt-get > /dev/null 2>&1; then
        sudo apt-get update -qq && sudo apt-get install -y -qq "${missing[@]}"
    else
        err "no supported package manager; install manually: ${missing[*]}"
        return 1
    fi
}

install_hooks() {
    if [[ $CHECK_ONLY -eq 1 ]]; then
        [[ -f "${SCRIPT_DIR}/.git/hooks/pre-commit" ]] || {
            err "git hooks are not installed"
            return 1
        }
        log "git hooks installed"
        return 0
    fi

    log "wiring git hooks (pre-commit and pre-push)"
    ( cd "$SCRIPT_DIR" \
        && pre-commit install > /dev/null \
        && pre-commit install --hook-type pre-push > /dev/null )
}

# The last word. If the gate cannot actually run, say so and exit non-zero.
verify() {
    log "verifying the gate runs"
    if ! ( cd "$SCRIPT_DIR" && pre-commit run --all-files > /dev/null 2>&1 ); then
        err "pre-commit run --all-files failed -- the repo is not clean"
        err "run it directly to see why:  pre-commit run --all-files"
        return 1
    fi
    log "OK: all hooks pass"
}

main() {
    check_shared_gates
    install_tools
    install_hooks
    verify
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --check) CHECK_ONLY=1; shift ;;
        -h | --help) usage ;;
        *) err "unknown option: $1"; exit 1 ;;
    esac
done

main "$@"
