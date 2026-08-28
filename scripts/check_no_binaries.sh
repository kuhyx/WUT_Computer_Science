#!/bin/bash
# Pre-commit hook: block binary and image files from being committed.
#
# Copied from ~/testsAndMisc/meta/scripts/check_no_binaries.sh, which is where
# this gate lives today (it is NOT in the shared ~/utils gate set). Keep the two
# in step, and prefer moving it to ~/utils over letting them drift -- a
# hand-copied gate is exactly what produced four forks of the 250-line cap.
#
# Only the remedy text differs: "move it to a sibling _binaries/ dir" is wrong
# advice here, because in a coursework archive the PDFs and figures ARE the
# submitted deliverable (approved decision 3: allowlist in place, no history
# rewrite).
# Allowed exceptions are listed in .binary-allowlist (one glob pattern per line).
set -euo pipefail

ALLOWLIST_FILE=".binary-allowlist"

# Binary/image extensions to block
BLOCKED_EXTENSIONS=(
    # Images
    png jpg jpeg gif webp svg ico bmp tiff tif psd
    # Audio/Video
    mp3 mp4 wav avi mkv flac ogg wma aac m4a mov wmv flv
    # Archives
    zip tar gz tgz bz2 xz 7z rar
    # Documents
    pdf doc docx xls xlsx ppt pptx
    # Fonts
    ttf woff woff2 eot otf
    # Compiled / binary
    o so a exe dll dylib pyc pyo class
    # Data
    apkg bin flat db sqlite sqlite3
)

# Build regex pattern from extensions
pattern=""
for ext in "${BLOCKED_EXTENSIONS[@]}"; do
    if [ -z "$pattern" ]; then
        pattern="\\.(${ext}"
    else
        pattern="${pattern}|${ext}"
    fi
done
pattern="${pattern})$"

# Load allowlist
allowed_patterns=()
if [ -f "$ALLOWLIST_FILE" ]; then
    while IFS= read -r line; do
        # Skip comments and empty lines
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// /}" ]] && continue
        allowed_patterns+=("$line")
    done < "$ALLOWLIST_FILE"
fi

is_allowed() {
    local file="$1"
    for pat in "${allowed_patterns[@]+"${allowed_patterns[@]}"}"; do
        # Use bash pattern matching (glob)
        # shellcheck disable=SC2254
        case "$file" in
            $pat) return 0 ;;
        esac
    done
    return 1
}

found=0
for file in "$@"; do
    # Skip files not tracked by git (deleted from index or untracked)
    git ls-files --error-unmatch "$file" >/dev/null 2>&1 || continue
    # Check if the file matches a blocked extension
    if echo "$file" | grep -qiE "$pattern"; then
        if is_allowed "$file"; then
            continue
        fi
        echo "BLOCKED: $file"
        echo "  Binary/image files should not be committed to the repo."
        echo "  In this coursework archive the submitted reports, figures and"
        echo "  datasets are allowed -- but only under Programming/ or NotProgramming/."
        echo "  To allow this file, add a glob pattern to $ALLOWLIST_FILE"
        found=1
    fi
done

if [ "$found" -eq 1 ]; then
    echo ""
    echo "ERROR: Attempted to commit binary/image files."
    echo "Options:"
    echo "  1. A submitted deliverable? Add a glob to $ALLOWLIST_FILE"
    echo "  2. Build output? Add it to .gitignore instead, never the allowlist"
    exit 1
fi
