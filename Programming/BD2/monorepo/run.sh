#!/bin/bash
#
# Generate the Prisma client, then serve frontend and backend together.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR

# A subshell keeps the cd local, so a failure cannot leave the caller in
# apps/backend and run the next command in the wrong directory.
(cd "${SCRIPT_DIR}/apps/backend" && npx prisma generate)

cd "$SCRIPT_DIR"
nx run-many --target=serve --projects=frontend,backend --parallel
