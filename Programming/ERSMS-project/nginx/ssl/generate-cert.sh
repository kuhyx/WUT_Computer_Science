#!/bin/bash

# ============================================================================
# Generate the self-signed localhost certificate nginx uses in docker-compose.
#
# The pair used to be committed. It was a throwaway CN=localhost cert that had
# already expired (notAfter 2025-06-16), so nothing depended on those exact
# bytes -- but a private key does not belong in a public repository, and this
# one is one command to recreate.
#
# NOTE: removing it from HEAD does not unpublish it. The key is still in git
# history, which is deliberately not rewritten. That is acceptable ONLY because
# this is an expired self-signed localhost cert with no trust path. A key that
# ever protected anything real would have to be rotated, not just deleted.
#
# Usage: bash generate-cert.sh
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
readonly DAYS=365

main() {
    if ! command -v openssl > /dev/null 2>&1; then
        echo "error: openssl is required" >&2
        exit 1
    fi

    openssl req -x509 -nodes -newkey rsa:2048 \
        -keyout "${SCRIPT_DIR}/nginx.key" \
        -out "${SCRIPT_DIR}/nginx.crt" \
        -days "$DAYS" \
        -subj "/CN=localhost" 2> /dev/null

    chmod 600 "${SCRIPT_DIR}/nginx.key"
    echo "==> wrote nginx.crt and nginx.key (self-signed, ${DAYS} days)"
}

main "$@"
