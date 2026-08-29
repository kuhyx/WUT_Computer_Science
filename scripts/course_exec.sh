# shellcheck shell=bash
# Running what the build produced. Sourced by course_lib.sh, never run.
#
# Building is not running. `./run.sh run EPFU` used to print one `gcc` line and
# stop, leaving you to find `a.out` yourself -- reported by kuhy on 2026-08-29:
# "I run run.sh and I have no idea where the actual program is and how to run
# it". Every kind that produces an executable now executes it and says so.
#
# Interactive by default: you typed `run`, so you are at the keyboard, and
# EPFU's penguins and ECOAR's C both read stdin. Under --batch stdin is
# /dev/null and a timeout applies, so an unattended run cannot wedge. --probe
# never reaches this file at all.

COURSE_EXEC_FAILURES=0
readonly COURSE_TIMEOUT_EXIT=124

_batch_timeout() { printf '%s' "${COURSE_BATCH_TIMEOUT:-60}"; }

_exec_note() {
    local rc="$1" what="$2"
    if [[ "$rc" -eq 0 ]]; then
        return 0
    fi
    COURSE_EXEC_FAILURES=$((COURSE_EXEC_FAILURES + 1))
    if [[ "$rc" -eq "$COURSE_TIMEOUT_EXIT" && -n "${COURSE_BATCH:-}" ]]; then
        # Not a failure of the program: --batch gives stdin as /dev/null, and
        # an interactive one is supposed to sit there. Say which it was.
        printf '    %s: still running after %ss, stopped (batch mode)\n' \
            "$what" "$(_batch_timeout)" >&2
    else
        printf '    %s: exited %s\n' "$what" "$rc" >&2
    fi
}

# Run one built artifact, from its own directory so relative data files resolve.
_exec_built() {
    local exe="$1" label rc=0
    label="$(_target_label "$exe")"
    printf '\n--> running %s\n' "$label"
    if [[ -n "${COURSE_BATCH:-}" ]]; then
        ( cd "$(dirname "$exe")" \
            && timeout "$(_batch_timeout)" "$exe" < /dev/null ) || rc=$?
    else
        ( cd "$(dirname "$exe")" && "$exe" ) || rc=$?
    fi
    _exec_note "$rc" "$label"
}

# Every executable file under a directory, with its mtime, so that "what did
# the build just produce" can be answered by comparing two snapshots. A
# makefile need not say what it writes, and EPFU's does not: `gcc ... main.c`
# with no -o leaves an a.out that nothing mentions.
_executable_snapshot() {
    find "$1" -type f -executable \
        -not -name '*.sh' -not -name '*.py' -not -name '*.pl' \
        -not -path '*/.git/*' -not -path '*/.venv/*' \
        -printf '%p\t%T@\n' 2>/dev/null | sort
}

# Run whatever appeared or changed between two snapshots.
_exec_new_binaries() {
    local before="$1" after="$2" what="$3"
    local new_paths=()
    local line path
    while IFS= read -r line; do
        path="${line%%$'\t'*}"
        new_paths+=("$path")
    done < <(comm -13 <(printf '%s\n' "$before") <(printf '%s\n' "$after"))

    if [[ ${#new_paths[@]} -eq 0 ]]; then
        printf 'nothing new to run after %s (already built, or it produces no binary)\n' \
            "$what"
        return 0
    fi
    local exe
    for exe in "${new_paths[@]}"; do
        _exec_built "$exe"
    done
}

# `make` in one directory, then run what it produced.
_make_and_run() {
    local dir="$1" before after
    before="$(_executable_snapshot "$dir")"
    ( cd "$dir" && make )
    after="$(_executable_snapshot "$dir")"
    _exec_new_binaries "$before" "$after" "make in $(_target_label "$dir")"
}

# A jar is not self-describing either: pick the one maven just wrote, skipping
# the sources/javadoc siblings that are not runnable.
_run_jar() {
    local dir="$1" jar
    jar="$(find "$dir" -path '*/target/*.jar' \
        -not -name '*-sources.jar' -not -name '*-javadoc.jar' -print -quit 2>/dev/null)"
    if [[ -z "$jar" ]]; then
        printf 'built, but no runnable jar under %s/target\n' "$(_target_label "$dir")"
        return 0
    fi
    local rc=0
    printf '\n--> running %s\n' "$(_target_label "$jar")"
    if [[ -n "${COURSE_BATCH:-}" ]]; then
        ( cd "$dir" && timeout "$(_batch_timeout)" java -jar "$jar" < /dev/null ) || rc=$?
    else
        ( cd "$dir" && java -jar "$jar" ) || rc=$?
    fi
    _exec_note "$rc" "$(_target_label "$jar")"
}

# A loose C program with no makefile of its own. Same deal as the cxx kind:
# compile into the gitignored build/, then actually run it.
_compile_and_run_c() {
    local src="$1" cc out
    cc="$(_require_any 'a C compiler' gcc cc clang)"
    mkdir -p "$COURSE_ROOT/build"
    out="$COURSE_ROOT/build/$(basename "${src%.c}")"
    printf 'compiling %s\n' "$(_target_label "$src")"
    "$cc" -O2 -Wall -Wextra -o "$out" "$src"
    _exec_built "$out"
}
