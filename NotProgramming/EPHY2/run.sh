#!/bin/bash
#
# NotProgramming/EPHY2 -- see ../../run.sh for the probe contract.
set -euo pipefail

# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../scripts/course_lib.sh
. "$(dirname "$(readlink -f "$0")")/../../scripts/course_lib.sh"

course_main --kind none \
    --note "submitted lab reports as PDFs only; no source was produced" \
    -- "$@"
