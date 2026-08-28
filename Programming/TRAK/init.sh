#!/bin/bash
#
# Create the project virtualenv. Source this file rather than running it if you
# want the activation to persist in your shell: `source init.sh`.
set -euo pipefail

pyenv local 3.11
python -m venv ./venv
# shellcheck source=/dev/null
source ./venv/bin/activate
