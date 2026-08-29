# shellcheck shell=bash
# Split out of course_lib.sh, which was over this repo's 250-line cap. Sourced
# by it, never on its own -- the helpers and constants it uses live there.
#
# Answers a bare invocation: actually build or run the course.


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
            [[ -n "$tex" ]] || tex="$(_first_tex_document)"
            [[ -n "$tex" ]] || _no_code "no .tex found"
            local tool
            tool="$(_require_any 'a LaTeX toolchain' latexmk pdflatex xelatex)"
            # Build into build/, never beside the source. A submitted report.pdf
            # is a tracked deliverable, and a rebuild whose output name happens
            # to match it would silently overwrite what was handed in.
            local dir base
            dir="$(dirname "$tex")"
            base="$(basename "$tex")"
            # A document that declares \bibliography but never cites anything
            # makes bibtex exit 2 ("I found no \citation commands"), and
            # latexmk turns that into exit 12 even though the PDF is fine.
            # --no-bibtex says "this one was handed in without a bibliography",
            # which is a fact about the deliverable, not a suppression.
            # An `x && y=1` one-liner would be a set -e landmine here: when x
            # is false the list returns 1 and the whole runner exits.
            local bibflag=()
            if [[ -n "${COURSE_TEX_NO_BIBTEX:-}" ]]; then
                bibflag=(-bibtex-)
            fi
            if [[ $tool == latexmk ]]; then
                ( cd "$dir" && latexmk -pdf "${bibflag[@]}" \
                    -interaction=nonstopmode -outdir=build "$base" )
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
                # Word-split on purpose: --entry-args is a fixed string the
                # course stub writes, never user input, and it has to become
                # several argv entries. read -a keeps that explicit.
                local entry_args=()
                if [[ -n "${COURSE_ENTRY_ARGS:-}" ]]; then
                    read -r -a entry_args <<< "$COURSE_ENTRY_ARGS"
                fi
                ( cd "$(dirname "$entry")" \
                    && "$(_python_bin)" "$(basename "$entry")" "${entry_args[@]}" )
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
        maven)
            ( cd "${COURSE_ENTRY:-$COURSE_ROOT}" && mvn -q package )
            _run_jar "${COURSE_ENTRY:-$COURSE_ROOT}"
            ;;
        make)
            # A target is either a directory with a makefile, or a standalone
            # .c program that no makefile covers.
            local mtarget="${COURSE_ENTRY:-$COURSE_ROOT}"
            if [[ -f "$mtarget" ]]; then
                _compile_and_run_c "$mtarget"
            else
                _make_and_run "$mtarget"
            fi
            ;;
        dotnet)
            # `dotnet run` builds too, so this is one step, not two.
            # EGUI is a web app: running it starts Kestrel and stays
            # up, which is what running it means. --batch caps that.
            local dir rc=0
            dir="${COURSE_ENTRY:-$COURSE_ROOT}"
            if [[ -n "${COURSE_BATCH:-}" ]]; then
                ( cd "$dir" && timeout "$(_batch_timeout)" \
                    dotnet run < /dev/null ) || rc=$?
            else
                ( cd "$dir" && dotnet run ) || rc=$?
            fi
            _exec_note "$rc" "$(_target_label "$dir")"
            ;;
        compose) ( cd "${COURSE_ENTRY:-$COURSE_ROOT}" && docker compose up ) ;;
        unity)   _blocked "open ${COURSE_ROOT} in the Unity editor; there is no headless path" ;;
        cxx)
            # One .cpp per invocation: each is a self-contained assignment with
            # its own main(), and the target list already enumerated them, so
            # picking one is the caller's job rather than this loop's.
            local cxx src rel out
            cxx="$(_require_any 'a C++ compiler' g++ clang++)"
            src="${COURSE_ENTRY:-}"
            [[ -f "$src" ]] || _no_code "no .cpp entry to compile"
            rel="${src#"$COURSE_ROOT"/}"
            # Binaries go to build/, which is gitignored -- compiling in place
            # drops untracked executables next to the sources, and an
            # extensionless binary is not something .gitignore catches by name.
            mkdir -p "$COURSE_ROOT/build"
            if _is_known_incomplete "${src#"${COURSE_GATES%/gates}"/}"; then
                printf 'skipping  %s (see gates/known-incomplete.txt)\n' "$rel"
                return 0
            fi
            out="$COURSE_ROOT/build/$(basename "${rel%.cpp}")"
            # Some files here are exam-answer fragments with no main(), so they
            # cannot be linked. Compile those to an object instead -- that
            # still type-checks them, which is the point, but there is then
            # nothing to run.
            if grep -qE '\bint[[:space:]]+main[[:space:]]*\(' "$src"; then
                printf 'compiling %s\n' "$rel"
                "$cxx" -O2 -o "$out" "$src"
                _exec_built "$out"
            else
                printf 'checking  %s (no main; -c only)\n' "$rel"
                "$cxx" -O2 -c -o "${out}.o" "$src"
            fi
            ;;
        notebook)
            _require_working jupyter
            # NOT --inplace: all four notebooks in this repo are tracked WITH
            # their outputs, so executing in place rewrites a deliverable.
            # --output-dir sends the executed copy to a temp dir instead.
            # It does NOT redirect what the notebook's own code writes -- the
            # kernel's cwd is still the notebook's directory -- so the
            # before/after tree check in course_main is what actually catches
            # a notebook that saves a figure beside itself.
            local nb nbtmp
            nbtmp="$(mktemp -d)"
            while IFS= read -r nb; do
                jupyter nbconvert --to notebook --execute --output-dir "$nbtmp" "$nb"
            done < <(find "$COURSE_ROOT" -name '*.ipynb' -not -path '*/.ipynb_checkpoints/*' | sort)
            rm -rf "$nbtmp"
            ;;
        matlab)
            local tool
            tool="$(_require_any 'MATLAB or Octave' matlab octave)"
            printf 'run the .m files in %s with %s\n' "$COURSE_ROOT" "$tool"
            ;;
        *) printf 'unknown COURSE_KIND: %s\n' "${COURSE_KIND:-unset}" >&2; return 1 ;;
    esac
}

