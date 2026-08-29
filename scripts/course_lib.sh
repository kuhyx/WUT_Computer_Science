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

# `command -v` is true for a dead pipx shim: the file is there and executable,
# and only running it shows that the interpreter it points at is gone. That is
# what `jupyter` is on this machine, and it turned a clean "blocked: needs
# jupyter" into a confusing exec failure. Probe by running, not by looking.
#
# The timeout is not paranoia: `unityhub --version` on this machine never
# returns, so a probe without one would hang the whole status sweep. Use
# _works only for tools that answer --version; _have is right for the rest.
_works() { _have "$1" && timeout 5 "$1" --version > /dev/null 2>&1; }

# Blocked-with-a-reason for a tool that has to actually run. "needs jupyter"
# and "jupyter is on PATH but does not run" send you to different fixes, and
# the status table is only worth keeping if it says which.
_require_working() {
    local tool="$1"
    _have "$tool" || _blocked "needs $tool"
    _works "$tool" || _blocked "$tool is on PATH but does not run (dead shim)"
}

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

# What the course tree looks like to git. Compared before and after a run,
# because executing coursework has twice silently overwritten a submitted
# deliverable -- TRAK's outputs/output.png and SPD's results_*.png -- and
# neither was noticed until a much later `git status`. Gitignored build output
# does not show up here, which is why every runner writes into build/.
# numstat is included so that re-writing an already-modified file still counts.
_tree_state() {
    git -C "$COURSE_ROOT" status --porcelain -- "$COURSE_ROOT" 2>/dev/null || true
    git -C "$COURSE_ROOT" diff --numstat -- "$COURSE_ROOT" 2>/dev/null || true
}

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

# The .tex that is an actual document, not one of the ~100 \input fragments
# the 2026-08 split created. `_first_file '*.tex'` returns whatever readdir
# hands back first, which for MOM was report_three/sections/02-*.tex; latexmk
# then faithfully tried to typeset a bare \section and failed with "Missing
# \begin{document}".
#
# Deliberately NOT sorted: readdir order is what every other tex course has
# been building all along, and sorting changed ELAC's pick from projectB to
# projectA and AIS's to report/final/ver1 -- both of which fail to build. The
# fragments are the bug; which document a multi-report course picks is a
# separate question, recorded in TODO-refactor-remaining.md.
_first_tex_document() {
    local candidate
    while IFS= read -r candidate; do
        if grep -q '\\documentclass' "$candidate"; then
            printf '%s' "$candidate"
            return 0
        fi
    done < <(find "$COURSE_ROOT" -name '*.tex' -not -path '*/build/*')
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
# shellcheck source-path=SCRIPTDIR
# shellcheck source=course_targets.sh
. "${_COURSE_LIB_DIR}/course_targets.sh"
# shellcheck source-path=SCRIPTDIR
# shellcheck source=course_exec.sh
. "${_COURSE_LIB_DIR}/course_exec.sh"

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

    # Everything after `--` is the user's, not the stub's.
    COURSE_BATCH=""
    COURSE_SELECT=""
    local mode="run"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --probe) mode="probe"; shift ;;
            --list)  mode="list"; shift ;;
            --batch) COURSE_BATCH=1; shift ;;
            -h | --help) mode="help"; shift ;;
            -*) printf 'unknown option: %s\n' "$1" >&2; return 1 ;;
            # A bare word picks a target: an index, a path substring, or "all".
            *) COURSE_SELECT="$1"; shift ;;
        esac
    done

    case "$mode" in
        # --probe must stay cheap and must never execute anything, so it does
        # not even enumerate targets.
        probe) _probe ;;
        help)
            printf 'usage: %s [--probe|--list] [--batch] [<target>]\n' "$(basename "$0")"
            printf '  --probe   report runnable/blocked/no-code without running\n'
            printf '  --list    list this course'"'"'s targets and stop\n'
            printf '  --batch   no prompts, stdin is /dev/null, %ss timeout per run\n' \
                "$(_batch_timeout)"
            printf '  <target>  an index, a path substring, or "all"\n'
            ;;
        list) _collect_targets; _print_menu ;;
        run) _run_selected ;;
    esac
}

# Run every chosen target, with the tree guard around the whole thing.
_run_selected() {
    _collect_targets
    _choose_target || return 1

    local before after target
    before="$(_tree_state)"
    for target in "${COURSE_CHOSEN[@]}"; do
        COURSE_ENTRY="$target"
        _run
    done
    after="$(_tree_state)"
    if [[ "$before" != "$after" ]]; then
        printf 'FAILED: the run changed files under %s\n' "$COURSE_ROOT" >&2
        diff <(printf '%s\n' "$before") <(printf '%s\n' "$after") >&2 || true
        return 1
    fi
    if [[ "$COURSE_EXEC_FAILURES" -gt 0 ]]; then
        printf '\n%s of the programs did not exit cleanly (see above)\n' \
            "$COURSE_EXEC_FAILURES" >&2
        return 1
    fi
}
