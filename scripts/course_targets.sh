# shellcheck shell=bash
# Enumerating and choosing what to run. Sourced by course_lib.sh, never run.
#
# A course directory is not always one program. EPFU ships a game AND a lab
# exercise, EOOP six standalone .cpp files, MOM three reports -- twelve courses
# have more than one target. The runner used to build whichever one `find`
# handed back first and say nothing about it, which is how you end up staring
# at a single gcc line with no idea what it just did.
#
# Enumeration scans COURSE_ROOT rather than only COURSE_ENTRY on purpose: EPFU
# pins --entry to penguins/src, and that pin is exactly why its labs/ was
# invisible. --entry still decides the DEFAULT, it no longer decides the only.

COURSE_TARGETS=()
COURSE_CHOSEN=()

# Fill COURSE_TARGETS for this kind. One entry means there is no choice to make.
_collect_targets() {
    COURSE_TARGETS=()
    local f
    case "$COURSE_KIND" in
        tex)
            while IFS= read -r f; do
                if grep -q '\\documentclass' "$f"; then COURSE_TARGETS+=("$f"); fi
            done < <(find "$COURSE_ROOT" -name '*.tex' -not -path '*/build/*' | sort)
            ;;
        python)
            while IFS= read -r f; do
                COURSE_TARGETS+=("$f")
            done < <(find "$COURSE_ROOT" -name 'main.py' -not -path '*/.venv/*' | sort)
            ;;
        make)
            local mkdirs=()
            while IFS= read -r f; do
                mkdirs+=("$(dirname "$f")")
                COURSE_TARGETS+=("$(dirname "$f")")
            done < <(find "$COURSE_ROOT" \( -name Makefile -o -name makefile \) \
                -not -path '*/build/*' -not -path '*/node_modules/*' | sort)
            # A loose .c with its own main() and no makefile above it is still
            # a program. EPFU's labs/krudnic3_lab1.c is the case that started
            # this: --entry pinned the runner to penguins/, so the lab was
            # invisible and nothing ever compiled it.
            while IFS= read -r f; do
                if grep -qE '\bint[[:space:]]+main[[:space:]]*\(' "$f" \
                    && ! _under_any "$f" ${mkdirs[@]+"${mkdirs[@]}"}; then
                    COURSE_TARGETS+=("$f")
                fi
            done < <(find "$COURSE_ROOT" -name '*.c' -not -path '*/build/*' \
                -not -path '*/node_modules/*' | sort)
            ;;
        cxx)
            while IFS= read -r f; do
                if grep -qE '\bint[[:space:]]+main[[:space:]]*\(' "$f"; then
                    COURSE_TARGETS+=("$f")
                fi
            done < <(find "$COURSE_ROOT" -name '*.cpp' -not -path '*/build/*' \
                -not -path '*/node_modules/*' | sort)
            ;;
    esac
    # Kinds with no natural list -- and any course whose scan found nothing --
    # keep the single implicit target the stub already declares.
    if [[ ${#COURSE_TARGETS[@]} -eq 0 ]]; then
        COURSE_TARGETS=("${COURSE_ENTRY:-$COURSE_ROOT}")
    fi
}

_target_label() { printf '%s' "${1#"$COURSE_ROOT"/}"; }

# Is this path inside any of the given directories? Used to keep a source file
# that some makefile already builds out of the target list.
_under_any() {
    local path="$1"; shift
    local dir
    for dir in "$@"; do
        if [[ "$path" == "$dir"/* ]]; then return 0; fi
    done
    return 1
}

# Resolve an explicit selection: an index, or a substring of a target's path.
# Prints the chosen indices, one per line; empty output means "no match".
_match_selection() {
    local want="$1" i=1 t
    if [[ "$want" == "all" ]]; then
        for ((i = 1; i <= ${#COURSE_TARGETS[@]}; i++)); do printf '%s\n' "$i"; done
        return 0
    fi
    if [[ "$want" =~ ^[0-9]+$ ]]; then
        if [[ "$want" -ge 1 && "$want" -le ${#COURSE_TARGETS[@]} ]]; then
            printf '%s\n' "$want"
        fi
        return 0
    fi
    for t in "${COURSE_TARGETS[@]}"; do
        if [[ "$(_target_label "$t")" == *"$want"* ]]; then printf '%s\n' "$i"; fi
        i=$((i + 1))
    done
}

_print_menu() {
    printf '\n%s has %d targets:\n\n' "${COURSE_ROOT##*/}" "${#COURSE_TARGETS[@]}"
    local i=1 t marker
    for t in "${COURSE_TARGETS[@]}"; do
        marker=""
        if [[ -n "${COURSE_ENTRY:-}" && "$t" == "$COURSE_ENTRY"* ]]; then
            marker="   <- the stub's default"
        fi
        printf '  %2d) %s%s\n' "$i" "$(_target_label "$t")" "$marker"
        i=$((i + 1))
    done
    printf '   a) all of them\n\n'
}

# Decide what to run, into COURSE_CHOSEN.
_choose_target() {
    COURSE_CHOSEN=()
    local idx

    if [[ ${#COURSE_TARGETS[@]} -eq 1 ]]; then
        COURSE_CHOSEN=("${COURSE_TARGETS[@]}")
        return 0
    fi

    # An explicit choice on the command line skips the prompt entirely, which
    # is what makes the menu scriptable as well as answerable.
    if [[ -n "${COURSE_SELECT:-}" ]]; then
        while IFS= read -r idx; do
            COURSE_CHOSEN+=("${COURSE_TARGETS[$((idx - 1))]}")
        done < <(_match_selection "$COURSE_SELECT")
        if [[ ${#COURSE_CHOSEN[@]} -eq 0 ]]; then
            printf 'no target matches "%s"\n' "$COURSE_SELECT" >&2
            _print_menu >&2
            return 1
        fi
        return 0
    fi

    # A prompt nobody can answer is how an unattended run hangs forever, so
    # --batch and a non-terminal stdin both mean "all of them" instead.
    if [[ -n "${COURSE_BATCH:-}" || ! -t 0 ]]; then
        COURSE_CHOSEN=("${COURSE_TARGETS[@]}")
        printf 'not interactive: running all %d targets\n' "${#COURSE_TARGETS[@]}"
        return 0
    fi

    _print_menu
    local reply
    read -r -p "which? [1-${#COURSE_TARGETS[@]} or a, default 1] " reply || reply=""
    reply="${reply:-1}"
    while IFS= read -r idx; do
        COURSE_CHOSEN+=("${COURSE_TARGETS[$((idx - 1))]}")
    done < <(_match_selection "$reply")
    if [[ ${#COURSE_CHOSEN[@]} -eq 0 ]]; then
        printf 'not a valid choice: %s\n' "$reply" >&2
        return 1
    fi
}
