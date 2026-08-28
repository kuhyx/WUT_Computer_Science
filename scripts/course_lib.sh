# shellcheck shell=bash
# Shared behaviour for every per-course run.sh. Sourced, never executed.
#
# A course run.sh is a stub: it declares what kind of project it is, then calls
# course_main. The logic lives here once, because 44 hand-copied runners is
# precisely how gates and scripts in this fleet have drifted apart before.
#
# Contract (see ../../run.sh):
#   --probe   report whether this could run HERE, without running it
#             exit 0 runnable | 78 blocked | 79 nothing to run
#   (no args) actually run it
#
# A stub calls:
#   course_main --kind <kind> [--entry <path>] [--entry-args <str>]
#               [--note <text>] [--test-dir <path>] [--no-bibtex] -- "$@"
# Values are passed as arguments rather than set as globals so that a stub has
# no assignments a linter has to be told to ignore.

readonly COURSE_EXIT_BLOCKED=78
readonly COURSE_EXIT_NO_CODE=79

COURSE_ROOT="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[1]}")")" && pwd)"
readonly COURSE_ROOT
# Repo root is two levels up: every course dir is <repo>/<area>/<course>.
COURSE_GATES="$(cd "${COURSE_ROOT}/../.." && pwd)/gates"
readonly COURSE_GATES

# --- helpers -----------------------------------------------------------------

_have() { command -v "$1" > /dev/null 2>&1; }

# Report "blocked" with the reason, which is the whole point of the status
# table: "needs X" is useful, "failed" is not.
_blocked() {
    printf '%s\n' "$1"
    exit "$COURSE_EXIT_BLOCKED"
}

_no_code() {
    printf '%s\n' "$1"
    exit "$COURSE_EXIT_NO_CODE"
}

_runnable() { printf '%s\n' "$1"; exit 0; }

# First tool present wins; otherwise blocked naming all the candidates.
_require_any() {
    local label="$1"; shift
    local tool
    for tool in "$@"; do
        if _have "$tool"; then
            printf '%s' "$tool"
            return 0
        fi
    done
    _blocked "needs $label (none of: $*)"
}

# Probe-side variant. _require_any prints the tool it found, so probes have to
# redirect its stdout -- which also swallowed the failure REASON and turned
# every blocked probe into "unknown". This one returns a status and prints
# only on failure.
_probe_any() {
    local label="$1"; shift
    local tool
    for tool in "$@"; do
        _have "$tool" && return 0
    done
    _blocked "needs $label (none of: $*)"
}

# True if the path is recorded in gates/known-incomplete.txt.
_is_known_incomplete() {
    local manifest="${COURSE_GATES:-}/known-incomplete.txt"
    [[ -f "$manifest" ]] || return 1
    local rel="$1"
    grep -vE '^\s*#|^\s*$' "$manifest" | grep -qxF "$rel"
}

_first_file() {
    find "$COURSE_ROOT" -name "$1" -not -path '*/node_modules/*' -print -quit 2>/dev/null
}


# The probe and the runner are one case statement each and together are most of
# this file's length, so they live beside it rather than in it. SCRIPTDIR is
# resolved from BASH_SOURCE[0] -- BASH_SOURCE[1] is the *caller*, which is a
# per-course run.sh two directories away.
_COURSE_LIB_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
# shellcheck source-path=SCRIPTDIR
# shellcheck source=course_probe.sh
. "${_COURSE_LIB_DIR}/course_probe.sh"
# shellcheck source-path=SCRIPTDIR
# shellcheck source=course_run.sh
. "${_COURSE_LIB_DIR}/course_run.sh"

course_main() {
    COURSE_KIND=""
    COURSE_ENTRY=""
    COURSE_NOTE=""
    COURSE_TEST_DIR=""
    COURSE_TEX_NO_BIBTEX=""
    COURSE_ENTRY_ARGS=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --kind)  COURSE_KIND="$2"; shift 2 ;;
            --entry) COURSE_ENTRY="$2"; shift 2 ;;
            --note)  COURSE_NOTE="$2"; shift 2 ;;
            --test-dir) COURSE_TEST_DIR="$2"; shift 2 ;;
            --no-bibtex) COURSE_TEX_NO_BIBTEX=1; shift ;;
            --entry-args) COURSE_ENTRY_ARGS="$2"; shift 2 ;;
            --) shift; break ;;
            *) break ;;
        esac
    done

    case "${1:-}" in
        --probe) _probe ;;
        -h | --help)
            printf 'usage: %s [--probe]\n' "$(basename "$0")"
            printf '  --probe  report runnable/blocked/no-code without running\n'
            ;;
        "") _run ;;
        *) printf 'unknown option: %s\n' "$1" >&2; return 1 ;;
    esac
}
