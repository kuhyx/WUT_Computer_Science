#!/bin/bash
#
# Programming/EPFU -- see ../../run.sh for the probe contract.
set -euo pipefail

# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../scripts/course_lib.sh
. "$(dirname "$(readlink -f "$0")")/../../scripts/course_lib.sh"

course_main --kind make \
    --entry "$(dirname "$(readlink -f "$0")")/penguins/src" \
    -- "$@"
