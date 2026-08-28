# shellcheck shell=bash
# Split out of course_lib.sh, which was over this repo's 250-line cap. Sourced
# by it, never on its own -- the helpers and constants it uses live there.
#
# Answers --probe: can this course run HERE, without running it.

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

