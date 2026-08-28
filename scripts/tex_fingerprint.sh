#!/bin/bash
#
# Print a content fingerprint of the PDF a .tex file builds to.
#
# Splitting a 1,876-line report into \input{} sections is only safe if the
# document it produces is unchanged, and "unchanged" cannot be checked by
# hashing the PDF: pdflatex stamps /CreationDate and an /ID into every build,
# so two runs of the SAME source already differ. This fingerprints what the
# reader sees instead -- the extracted text and the page count.
#
# Usage:
#   scripts/tex_fingerprint.sh <file.tex>            print the fingerprint
#   scripts/tex_fingerprint.sh --save <file.tex>     write it next to /tmp
#   scripts/tex_fingerprint.sh --check <file.tex>    compare against the saved one
#
# Typical use, per report:
#   scripts/tex_fingerprint.sh --save  report.tex    # before touching it
#   ...split it into sections...
#   scripts/tex_fingerprint.sh --check report.tex    # exits 1 if it moved

set -euo pipefail

readonly SCRIPT_NAME="${0##*/}"
MODE="print"
TEX=""
WORK_DIR=""

cleanup() {
    if [[ -n "$WORK_DIR" && -d "$WORK_DIR" ]]; then
        rm -rf "$WORK_DIR"
    fi
}
trap cleanup EXIT

usage() {
    echo "Usage: $SCRIPT_NAME [--save|--check] <file.tex>"
    exit 0
}

validate_requirements() {
    if [[ -z "$TEX" ]]; then
        echo "Error: a .tex file is required" >&2
        exit 1
    fi
    if [[ ! -f "$TEX" ]]; then
        echo "Error: no such file: $TEX" >&2
        exit 1
    fi
    local tool
    for tool in latexmk pdftotext sha256sum; do
        command -v "$tool" > /dev/null 2>&1 || {
            echo "Error: $tool is not installed" >&2
            exit 1
        }
    done
}

# Where the saved fingerprint for a given .tex lives. Keyed by the absolute
# path so two reports named report.tex cannot overwrite each other.
saved_path() {
    local abs key
    abs="$(readlink -f "$TEX")"
    key="$(printf '%s' "$abs" | sha256sum | cut -c1-16)"
    printf '/tmp/tex_fingerprint_%s' "$key"
}

# Build into a scratch directory so nothing lands beside the source, and a
# stale .aux from an earlier build cannot influence the result.
fingerprint() {
    local dir base
    dir="$(dirname "$TEX")"
    base="$(basename "$TEX")"
    WORK_DIR="$(mktemp -d)"

    # -bibtex- for the same reason Programming/ZPOB passes it: a report that
    # declares a bibliography it never cites makes bibtex exit non-zero, and
    # here we only care whether the rendered text moved.
    ( cd "$dir" && latexmk -pdf -bibtex- -interaction=nonstopmode \
        -outdir="$WORK_DIR" "$base" ) > "$WORK_DIR/build.log" 2>&1 || true

    local pdf="$WORK_DIR/${base%.tex}.pdf"
    if [[ ! -f "$pdf" ]]; then
        echo "Error: no PDF produced; see the tail of the build log:" >&2
        tail -20 "$WORK_DIR/build.log" >&2
        exit 1
    fi

    local pages text_hash
    pages="$(pdftotext "$pdf" - 2> /dev/null | grep -c $'\f' || true)"
    text_hash="$(pdftotext -layout "$pdf" - 2> /dev/null | sha256sum | cut -c1-32)"
    printf 'pages=%s text=%s\n' "$pages" "$text_hash"
}

main() {
    validate_requirements
    local fp saved
    fp="$(fingerprint)"

    case "$MODE" in
        print) printf '%s\n' "$fp" ;;
        save)
            printf '%s\n' "$fp" > "$(saved_path)"
            printf 'saved  %s  %s\n' "$fp" "$TEX"
            ;;
        check)
            saved="$(saved_path)"
            if [[ ! -f "$saved" ]]; then
                echo "Error: nothing saved for $TEX -- run --save first" >&2
                exit 1
            fi
            local before
            before="$(cat "$saved")"
            if [[ "$before" == "$fp" ]]; then
                printf 'unchanged  %s  %s\n' "$fp" "$TEX"
            else
                printf 'CHANGED    %s\n  before: %s\n  after:  %s\n' \
                    "$TEX" "$before" "$fp" >&2
                exit 1
            fi
            ;;
    esac
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --save) MODE="save"; shift ;;
        --check) MODE="check"; shift ;;
        -h | --help) usage ;;
        -*) echo "Unknown option: $1" >&2; exit 1 ;;
        *) TEX="$1"; shift ;;
    esac
done

main "$@"
