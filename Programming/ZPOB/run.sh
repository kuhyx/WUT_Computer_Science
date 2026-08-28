#!/bin/bash
#
# Programming/ZPOB -- see ../../run.sh for the probe contract.
set -euo pipefail

# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../scripts/course_lib.sh
. "$(dirname "$(readlink -f "$0")")/../../scripts/course_lib.sh"

# esej.tex ends with \bibliography{references} but contains no \cite and no
# \bibliographystyle, so bibtex aborts and latexmk reports 12 -- after having
# already written a correct esej.pdf. That is how the essay was handed in:
# the submitted esej.pdf (LuaTeX, 2023-12-12) has no bibliography either.
# Adding \bibliographystyle would print a References section that was never
# part of the deliverable, so the build skips bibtex instead.
course_main --kind tex --no-bibtex \
    -- "$@"
