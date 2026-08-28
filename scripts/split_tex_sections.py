#!/usr/bin/env python3
r"""Split an over-long LaTeX report into one ``\input{}`` file per section.

The 250-line cap in this repo applies to prose as well as code, and several
submitted reports are far over it -- ``projectA.tex`` is 1,876 lines. The fix
for a report is structural rather than editorial: move each section into
``sections/`` and leave the parent holding the preamble and a list of
``\input`` lines, which is how a long LaTeX document is normally organised
anyway.

Nothing here rewrites the *content*. Every byte between two section headers is
moved verbatim, so the built PDF is unchanged --  check that with
``scripts/tex_fingerprint.sh --save`` before and ``--check`` after.

Usage::

    scripts/split_tex_sections.py report.tex
    scripts/split_tex_sections.py report.tex --level chapter --dry-run
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import unicodedata
from pathlib import Path

# A section header this script is willing to split on. Leading whitespace is
# allowed because several of these reports indent their body one tab.
_HEADER = r"^[ \t]*\\{level}\*?(?:\[[^\]]*\])?\{{"

# \end{document} may likewise be indented, and anything after it belongs to
# the parent file rather than to the last section.
_END_DOCUMENT = re.compile(r"^[ \t]*\\end\{document\}")

_MAX_SLUG_WORDS = 6
# A single section is nothing to split; the parent would just gain a level.
_MIN_SECTIONS = 2

# print() is not available here (ruff T201, no per-file-ignores in this repo),
# so progress goes through logging configured to emit the bare message -- the
# output is identical to a print, and the rule is satisfied rather than muted.
logger = logging.getLogger(__name__)


def _slugify(title: str) -> str:
    """Turn a section title into a short ASCII filename stem.

    Polish diacritics are folded rather than dropped, so ``Rozwiązanie
    efektywne`` becomes ``rozwiazanie-efektywne`` instead of ``rozwi-zanie``.
    """
    # NFKD splits 'ą' into 'a' + a combining ogonek, which the ASCII encode
    # then discards. 'ł' has no decomposition, so it is mapped by hand.
    folded = unicodedata.normalize("NFKD", title.replace("ł", "l").replace("Ł", "L"))
    ascii_only = folded.encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[A-Za-z0-9]+", ascii_only.lower())
    return "-".join(words[:_MAX_SLUG_WORDS]) or "section"


def _brace_span(text: str, open_index: int) -> int:
    r"""Return the index just past the ``{...}`` group starting at *open_index*.

    Counting braces rather than matching ``\{[^}]*\}`` matters: a title may
    contain a nested group, as in ``\section{The \emph{hard} part}``.
    """
    depth = 0
    for i in range(open_index, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
    msg = "unbalanced braces in a section header"
    raise ValueError(msg)


# A title may run onto the following line, as EOPSY lab3 does:
#   \\section{Explanation of types of values in summary results and summary
#   processes files}
# so the brace scan looks at a small window rather than one line.
_TITLE_WINDOW = 6


def _section_title(lines: list[str], index: int) -> str:
    """Extract the title text of the header starting at *index*."""
    window = "".join(lines[index : index + _TITLE_WINDOW])
    open_index = window.index("{")
    title = window[open_index + 1 : _brace_span(window, open_index) - 1]
    return " ".join(title.split())


def find_sections(lines: list[str], level: str) -> list[tuple[int, str]]:
    """Return ``(line_index, title)`` for every header at *level*."""
    header = re.compile(_HEADER.format(level=level))
    return [
        (i, _section_title(lines, i))
        for i, line in enumerate(lines)
        if header.match(line) and "{" in line
    ]


def _document_end(lines: list[str]) -> int:
    r"""Index of the real ``\end{document}``, or the end of the file.

    The LAST match, not the first: ECOTE's two reports quote a whole example
    LaTeX document inside an ``lstlisting`` block, so ``\end{document}``
    appears in the middle of the file. Taking the first one there stranded
    everything after it and silently changed the rendered PDF -- which is
    exactly what ``scripts/tex_fingerprint.sh --check`` caught.
    """
    for i in range(len(lines) - 1, -1, -1):
        if _END_DOCUMENT.match(lines[i]):
            return i
    return len(lines)


def plan(lines: list[str], level: str) -> list[tuple[str, int, int]]:
    """Work out ``(stem, start, stop)`` for each section, as a half-open range."""
    heads = find_sections(lines, level)
    end = _document_end(lines)
    # The 01-, 02- ... prefix is what keeps the names unique: two sections
    # may legitimately share a title, and their slugs would then collide.
    return [
        (
            f"{n + 1:02d}-{_slugify(title)}",
            start,
            heads[n + 1][0] if n + 1 < len(heads) else end,
        )
        for n, (start, title) in enumerate(heads)
    ]


def split(tex: Path, level: str, out: str, prefix: str, *, dry_run: bool) -> int:
    """Split *tex* in place. Returns the number of sections extracted."""
    lines = tex.read_text(encoding="utf-8").splitlines(keepends=True)
    sections = plan(lines, level)
    if len(sections) < _MIN_SECTIONS:
        logger.info("%s: %d \\%s found; nothing to split", tex, len(sections), level)
        return 0

    out_dir = tex.parent / out
    first = sections[0][1]
    tail = lines[sections[-1][2] :]
    body = [f"\t\\input{{{prefix}/{stem}}}\n" for stem, _, _ in sections]

    if dry_run:
        for stem, start, stop in sections:
            logger.info("  %s/%s.tex  <- lines %d-%d", out, stem, start + 1, stop)
        return len(sections)

    out_dir.mkdir(exist_ok=True)
    for stem, start, stop in sections:
        (out_dir / f"{stem}.tex").write_text(
            "".join(lines[start:stop]), encoding="utf-8"
        )
    tex.write_text("".join([*lines[:first], *body, *tail]), encoding="utf-8")
    logger.info("%s: %d sections -> %s/", tex, len(sections), out_dir)
    return len(sections)


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and split each named report."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex", nargs="+", type=Path, help="report(s) to split")
    parser.add_argument(
        "--level",
        default="section",
        choices=("chapter", "section", "subsection"),
        help="header level to split on (default: section)",
    )
    parser.add_argument(
        "--out",
        default="sections",
        help="directory to write the pieces into, beside the .tex (default: sections)",
    )
    parser.add_argument(
        "--input-prefix",
        default=None,
        help="path used inside \\input{}. LaTeX resolves \\input relative to "
        "the MAIN document, not to the including file, so a second-level "
        "split needs e.g. --out 03-results --input-prefix sections/03-results "
        "(default: the value of --out)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the plan without writing anything",
    )
    args = parser.parse_args(argv)
    logging.basicConfig(format="%(message)s", level=logging.INFO, stream=sys.stdout)

    for tex in args.tex:
        if not tex.is_file():
            logger.error("no such file: %s", tex)
            return 1
        split(
            tex,
            args.level,
            args.out,
            args.input_prefix or args.out,
            dry_run=args.dry_run,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
