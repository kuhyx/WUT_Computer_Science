#!/bin/bash
#
# Programming/ECRYPT -- see ../../run.sh for the probe contract.
set -euo pipefail

# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../scripts/course_lib.sh
. "$(dirname "$(readlink -f "$0")")/../../scripts/course_lib.sh"

course_main --kind none \
    --note "test1.py is a 0-byte stub; this course produced no submitted code" \
    -- "$@"
