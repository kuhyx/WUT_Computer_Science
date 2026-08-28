#!/bin/bash
#
# Programming/PORR -- see ../../run.sh for the probe contract.
set -euo pipefail

# shellcheck source-path=SCRIPTDIR
# shellcheck source=../../scripts/course_lib.sh
. "$(dirname "$(readlink -f "$0")")/../../scripts/course_lib.sh"

# This suite is a BENCHMARK, not a smoke test. Measured on this machine, the
# cost is not where you would guess -- it is not the matrix size:
#
#   ProcessingType.PROCESSES   20.9s at n=2, 32.8s at n=5, 78.2s at n=10.
#                              That is pool setup per test, and it grows.
#   matrix_type poli3          densifies a sparse .mat into a 2.3 GB cache
#                              (nemeth12: 723 MB) -- over the 2G ceiling
#                              `../../run.sh run` imposes, before any solving.
#   n=10000                    the SPD matrix alone is 800 MB and
#                              np.linalg.solve needs a second copy.
#   n=5000                     spd_5000.npz was a Git LFS pointer whose object
#                              404s on the server, so this size regenerates
#                              from scratch: a dense 5000x5000 eigendecomposition.
#
# What is left after removing those is fast and still covers the whole
# Richardson implementation across every size that fits: 18 tests, 28 seconds.
# The full submitted parameter set is one environment variable away, and needs
# headroom the default deliberately does not give it:
#
#   PYTEST_ADDOPTS= RUN_MEMORY_MAX=16G RUN_CPU_QUOTA=800% ./run.sh run Programming/PORR
#
# main.py hardcodes its pytest arguments, so the selection is passed the only
# way that survives that: PYTEST_ADDOPTS, which pytest.main() also honours.
export PYTEST_ADDOPTS="${PYTEST_ADDOPTS--k 'spd and (SEQUENTIAL or THREADS) and not 5000 and not 10000'}"

course_main --kind python \
    --entry "$(dirname "$(readlink -f "$0")")/code/main.py" \
    -- "$@"
