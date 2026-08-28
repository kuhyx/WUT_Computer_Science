#!/bin/bash
#
# Programming/TRAK -- see ../../run.sh for the probe contract.
set -euo pipefail

# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../scripts/course_lib.sh
. "$(dirname "$(readlink -f "$0")")/../../scripts/course_lib.sh"

# Three main.py files live here (the renderer, plus the two standalone
# experiments under code/), so the harness cannot pick one on its own and
# falls back to syntax-checking. Name the renderer explicitly: a run that
# actually ray-traces cornell_box at 400x300 is a real check, and "every
# module parses" is not.
# --output, because config.ini's default is outputs/output.png and that file
# is a TRACKED deliverable: a plain run silently overwrote what was submitted.
# build/ is gitignored, so a rebuild can never do that again.
mkdir -p "$(dirname "$(readlink -f "$0")")/build"
course_main --kind python \
    --entry "$(dirname "$(readlink -f "$0")")/main.py" \
    --entry-args "--output ../build/render.png" \
    -- "$@"
