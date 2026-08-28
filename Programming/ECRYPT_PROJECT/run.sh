#!/bin/bash
#
# Programming/ECRYPT_PROJECT -- see ../../run.sh for the probe contract.
set -euo pipefail

# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../scripts/course_lib.sh
. "$(dirname "$(readlink -f "$0")")/../../scripts/course_lib.sh"

# No --entry on purpose: code/project.py prompts on stdin, so it cannot be run
# headlessly. This course ships a real pytest suite, and that is the check.
course_main --kind python \
    --test-dir "$(dirname "$(readlink -f "$0")")/sieve" \
    -- "$@"
