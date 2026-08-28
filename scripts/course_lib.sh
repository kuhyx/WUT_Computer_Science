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
#   course_main --kind <kind> [--entry <path>] [--note <text>] -- "$@"
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

# --- probes ------------------------------------------------------------------

_probe() {
    case "$COURSE_KIND" in
        none) _no_code "${COURSE_NOTE:-no executable code in this directory}" ;;
        tex)
            _probe_any "a LaTeX toolchain" latexmk pdflatex xelatex
            _runnable "builds ${COURSE_ENTRY:-the report} with latexmk"
            ;;
        python)
            _have python3 || _blocked "needs python3"
            [[ -n "$(_first_file '*.py')" ]] || _no_code "no .py files found"
            _runnable "python3 ${COURSE_ENTRY:-the entry script}"
            ;;
        node)
            _have node || _blocked "needs node"
            _have npm || _blocked "needs npm"
            _runnable "npm install && npm start"
            ;;
        maven)
            _have mvn || _blocked "needs maven"
            _have java || _blocked "needs a JDK"
            _runnable "mvn package"
            ;;
        make)
            _have make || _blocked "needs make"
            _probe_any "a C compiler" gcc cc clang
            _runnable "make"
            ;;
        dotnet)
            _have dotnet || _blocked "needs the .NET SDK"
            _runnable "dotnet build"
            ;;
        unity)
            _have unity-editor || _have unityhub \
                || _blocked "needs the Unity editor (GUI, not installable on a CI runner)"
            _runnable "opens in the Unity editor"
            ;;
        matlab)
            _probe_any "MATLAB or Octave" matlab octave
            _runnable "runs the .m scripts"
            ;;
        cxx)
            _probe_any "a C++ compiler" g++ clang++
            [[ -n "$(_first_file '*.cpp')" ]] || _no_code "no .cpp files found"
            _runnable "compiles each standalone .cpp"
            ;;
        notebook)
            _have jupyter || _blocked "needs jupyter"
            # Being on PATH is not the same as working: this machine has a
            # jupyter shim whose pipx venv interpreter is gone, so it fails
            # with "bad interpreter". Probe by actually invoking it.
            jupyter --version > /dev/null 2>&1 || _blocked "jupyter is on PATH but broken (bad interpreter)"
            _runnable "jupyter nbconvert --execute"
            ;;
        compose)
            _have docker || _blocked "needs docker"
            docker info > /dev/null 2>&1 || _blocked "docker is installed but the daemon is not running"
            _runnable "docker compose up"
            ;;
        *) _blocked "unknown COURSE_KIND '${COURSE_KIND:-unset}'" ;;
    esac
}

# Use the course venv when one exists, otherwise the system interpreter.
_python_bin() {
    if [[ -x "$COURSE_ROOT/.venv/bin/python" ]]; then
        printf '%s' "$COURSE_ROOT/.venv/bin/python"
    else
        printf 'python3'
    fi
}

# Dependencies are the runner's job, not the reader's. Without this, EARIN
# dies on ModuleNotFoundError for gymnasium and the "runnable" status is a lie.
_python_install_requirements() {
    local reqs=()
    while IFS= read -r r; do reqs+=("$r"); done < <(
        find "$COURSE_ROOT" -name 'requirements*.txt' -not -path '*/.venv/*' | sort)
    [[ ${#reqs[@]} -gt 0 ]] || return 0

    if [[ ! -x "$COURSE_ROOT/.venv/bin/python" ]]; then
        printf 'creating .venv\n'
        python3 -m venv "$COURSE_ROOT/.venv"
    fi
    "$COURSE_ROOT/.venv/bin/python" -m pip install --quiet --upgrade pip

    # EVERY requirements file, not just the first: EARIN is six independent
    # labs plus a project, and installing only one of them left the lab it
    # then tried to run missing gymnasium.
    local req
    for req in "${reqs[@]}"; do
        printf 'installing %s\n' "${req#"$COURSE_ROOT"/}"
        "$COURSE_ROOT/.venv/bin/python" -m pip install --quiet -r "$req" || {
            printf 'warning: some requirements in %s failed\n' "${req#"$COURSE_ROOT"/}" >&2
        }
    done
}

# Where a course ships real tests, running them is a stronger check than
# running the program -- and for an interactive program (ECRYPT_PROJECT prompts
# on stdin) it is the ONLY check that works without a person at a keyboard.
_python_run_tests() {
    local suite
    suite="$(find "$COURSE_ROOT" -name 'test_*.py' -not -path '*/.venv/*' -print -quit 2>/dev/null)"
    [[ -n "$suite" ]] || return 0
    local py
    py="$(_python_bin)"
    "$py" -c 'import pytest' 2> /dev/null || {
        printf 'tests present but pytest is not installed; skipping\n'
        return 0
    }
    # Which directory pytest runs FROM is course-specific and cannot be
    # guessed: ECOTE needs program/ so `from translator.main import` resolves,
    # ECRYPT_PROJECT needs sieve/ because its fixtures open P-100000.csv by a
    # relative path. So the stub says, and COURSE_ROOT is only the default.
    local from_dir="${COURSE_TEST_DIR:-$COURSE_ROOT}"
    printf 'running the test suite in %s\n' "${from_dir#"$COURSE_ROOT"/}"
    ( cd "$from_dir" && "$py" -m pytest -q )
}

# --- runners -----------------------------------------------------------------

_run() {
    case "$COURSE_KIND" in
        none) _no_code "${COURSE_NOTE:-nothing to run}" ;;
        tex)
            local tex="${COURSE_ENTRY:-}"
            [[ -n "$tex" ]] || tex="$(_first_file '*.tex')"
            [[ -n "$tex" ]] || _no_code "no .tex found"
            local tool
            tool="$(_require_any 'a LaTeX toolchain' latexmk pdflatex xelatex)"
            # Build into build/, never beside the source. A submitted report.pdf
            # is a tracked deliverable, and a rebuild whose output name happens
            # to match it would silently overwrite what was handed in.
            local dir base
            dir="$(dirname "$tex")"
            base="$(basename "$tex")"
            if [[ $tool == latexmk ]]; then
                ( cd "$dir" && latexmk -pdf -interaction=nonstopmode -outdir=build "$base" )
            else
                ( cd "$dir" && mkdir -p build \
                    && "$tool" -interaction=nonstopmode -output-directory=build "$base" )
            fi
            printf 'output in %s/build\n' "$dir"
            ;;
        python)
            local entry="${COURSE_ENTRY:-}"
            # An entry may be given as a directory; resolve it to the module
            # inside. Passing the directory itself makes python look for
            # __main__.py and fail with a message about the wrong thing.
            if [[ -d "$entry" ]]; then
                local cand
                for cand in main.py project.py __main__.py; do
                    if [[ -f "$entry/$cand" ]]; then
                        entry="$entry/$cand"
                        break
                    fi
                done
            fi
            # Only auto-pick a main.py when there is exactly ONE. A course
            # with six labs has six, and choosing whichever find returns first
            # is not "running the project", it is running an arbitrary lab.
            if [[ ! -f "$entry" ]]; then
                local mains
                mains="$(find "$COURSE_ROOT" -name 'main.py' -not -path '*/.venv/*' | wc -l)"
                [[ "$mains" -eq 1 ]] && entry="$(_first_file 'main.py')"
            fi

            _python_install_requirements

            if [[ -f "$entry" ]]; then
                ( cd "$(dirname "$entry")" && "$(_python_bin)" "$(basename "$entry")" )
            else
                # A pile of one-shot scripts with no entry contract (NLP is
                # the case here). Syntax-check them all rather than picking one
                # arbitrarily and calling that "running the project".
                printf 'no single entry point; syntax-checking every module instead\n'
                find "$COURSE_ROOT" -name '*.py' -not -path '*/.venv/*' -print0 \
                    | xargs -0 -r "$(_python_bin)" -m py_compile
                printf 'all modules compile\n'
            fi
            _python_run_tests
            ;;
        node)    ( cd "${COURSE_ENTRY:-$COURSE_ROOT}" && npm install && npm start ) ;;
        maven)   ( cd "${COURSE_ENTRY:-$COURSE_ROOT}" && mvn -q package ) ;;
        make)    ( cd "${COURSE_ENTRY:-$COURSE_ROOT}" && make ) ;;
        dotnet)  ( cd "${COURSE_ENTRY:-$COURSE_ROOT}" && dotnet build ) ;;
        compose) ( cd "${COURSE_ENTRY:-$COURSE_ROOT}" && docker compose up ) ;;
        unity)   _blocked "open ${COURSE_ROOT} in the Unity editor; there is no headless path" ;;
        cxx)
            # Each .cpp here is a self-contained assignment with its own main(),
            # so they are compiled individually rather than linked together.
            local cxx src rel out
            cxx="$(_require_any 'a C++ compiler' g++ clang++)"
            # Binaries go to build/, which is gitignored -- compiling in place
            # drops untracked executables next to the sources, and an
            # extensionless binary is not something .gitignore catches by name.
            mkdir -p "$COURSE_ROOT/build"
            while IFS= read -r src; do
                rel="${src#"$COURSE_ROOT"/}"
                if _is_known_incomplete "${src#"${COURSE_GATES%/gates}"/}"; then
                    printf 'skipping  %s (see gates/known-incomplete.txt)\n' "$rel"
                    continue
                fi
                out="$COURSE_ROOT/build/$(basename "${rel%.cpp}")"
                # Some files here are exam-answer fragments with no main(), so
                # they cannot be linked. Compile those to an object instead --
                # that still type-checks them, which is the point.
                if grep -qE '\bint[[:space:]]+main[[:space:]]*\(' "$src"; then
                    printf 'compiling %s\n' "$rel"
                    "$cxx" -O2 -o "$out" "$src"
                else
                    printf 'checking  %s (no main; -c only)\n' "$rel"
                    "$cxx" -O2 -c -o "${out}.o" "$src"
                fi
            done < <(find "$COURSE_ROOT" -name '*.cpp' -not -path '*/node_modules/*' -not -path '*/build/*' | sort)
            printf 'binaries in %s/build\n' "$COURSE_ROOT" 
            ;;
        notebook)
            _have jupyter || _blocked "needs jupyter"
            local nb
            while IFS= read -r nb; do
                jupyter nbconvert --to notebook --execute --inplace "$nb"
            done < <(find "$COURSE_ROOT" -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*' | sort)
            ;;
        matlab)
            local tool
            tool="$(_require_any 'MATLAB or Octave' matlab octave)"
            printf 'run the .m files in %s with %s\n' "$COURSE_ROOT" "$tool"
            ;;
        *) printf 'unknown COURSE_KIND: %s\n' "${COURSE_KIND:-unset}" >&2; return 1 ;;
    esac
}

course_main() {
    COURSE_KIND=""
    COURSE_ENTRY=""
    COURSE_NOTE=""
    COURSE_TEST_DIR=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --kind)  COURSE_KIND="$2"; shift 2 ;;
            --entry) COURSE_ENTRY="$2"; shift 2 ;;
            --note)  COURSE_NOTE="$2"; shift 2 ;;
            --test-dir) COURSE_TEST_DIR="$2"; shift 2 ;;
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
