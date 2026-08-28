#!/bin/bash
#
# Programming/PORR -- see ../../run.sh for the probe contract.
set -euo pipefail

# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../scripts/course_lib.sh
. "$(dirname "$(readlink -f "$0")")/../../scripts/course_lib.sh"

course_main --kind python \
    --entry "$(dirname "$(readlink -f "$0")")/code" \
    -- "$@"
