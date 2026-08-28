#!/usr/bin/env python3
"""Three checks that catch what ruff and a smoke run both miss.

Every one of these exists because it caught a real regression during the
`select = ["ALL"]` campaign on this archive:

1. **Signatures.** Annotating 110 EARIN functions silently dropped the DEFAULT
   VALUES from 22 of them, so a call relying on a default would have raised
   TypeError. Nothing flagged it: ruff does not look at defaults, and the
   affected paths were not the ones a smoke run exercises.
2. **Logging.** Rewriting ``print()`` as ``logger.info()`` made programs
   silent, because logging's last-resort handler only emits WARNING and above.
   A module that logs and has a ``__main__`` guard must configure logging.
3. **print keywords.** ``print(x, end="")`` builds a line incrementally.
   Dropping ``end=`` turned a rendered chess board into one glyph per line;
   dropping ``file=sys.stderr`` would silently move error output to stdout.

Usage::

    scripts/check_refactor_safety.py --logging --print-keywords <paths>
    scripts/check_refactor_safety.py --signatures <before-tree> <after-tree>

Exit status is 1 if anything is reported.
"""

from __future__ import annotations

import argparse
import ast
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

_MAIN_GUARD = "__name__ == '__main__'"


def _functions(source: str) -> dict[str, tuple[set[str], dict[str, str]]]:
    """Map each function name to its parameter names and their defaults."""
    out: dict[str, tuple[set[str], dict[str, str]]] = {}
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.FunctionDef):
            continue
        args = node.args
        defaults: dict[str, str] = {}
        # defaults cover posonlyargs and args together, tail-aligned.
        ordered = args.posonlyargs + args.args
        positional = ordered[len(ordered) - len(args.defaults) :]
        for arg, value in zip(positional, args.defaults, strict=True):
            defaults[arg.arg] = ast.unparse(value)
        for arg, value in zip(args.kwonlyargs, args.kw_defaults, strict=True):
            if value is not None:
                defaults[arg.arg] = ast.unparse(value)
        names = {a.arg for a in args.posonlyargs + args.args + args.kwonlyargs}
        out[node.name] = (names, defaults)
    return out


def check_signatures(before: Path, after: Path) -> int:
    """Report any parameter or default that changed between two trees."""
    problems = 0
    for old in sorted(before.rglob("*.py")):
        new = after / old.relative_to(before)
        if not new.exists():
            continue
        was = _functions(old.read_text(encoding="utf-8"))
        now = _functions(new.read_text(encoding="utf-8"))
        for name, (names, defaults) in was.items():
            if name not in now:
                logger.error("%s: %s disappeared", new, name)
                problems += 1
                continue
            names_now, defaults_now = now[name]
            missing = sorted(names - names_now)
            if missing:
                logger.error("%s: %s lost parameters %s", new, name, missing)
                problems += 1
            changed = {
                key: (value, defaults_now.get(key))
                for key, value in defaults.items()
                if key in names_now and defaults_now.get(key) != value
            }
            if changed:
                logger.error("%s: %s default(s) changed %s", new, name, changed)
                problems += 1
    return problems


def check_logging(paths: list[Path]) -> int:
    """Report modules that log but never configure logging."""
    problems = 0
    for path in paths:
        source = path.read_text(encoding="utf-8", errors="ignore")
        if "logger.info(" not in source and "logger.debug(" not in source:
            continue
        if "basicConfig" in source:
            continue
        tree = ast.parse(source)
        runnable = any(
            isinstance(node, ast.If) and ast.unparse(node.test) == _MAIN_GUARD
            for node in tree.body
        )
        # Only a module that can be RUN is at fault: configuring logging is
        # the entry point's job, not a library module's.
        if runnable:
            logger.error("%s: logs at INFO but never calls basicConfig", path)
            problems += 1
    return problems


def check_print_keywords(paths: list[Path]) -> int:
    """Report print() calls whose keywords an automated rewrite would lose."""
    problems = 0
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "print"
                and node.keywords
            ):
                continue
            keys = sorted(k.arg or "**" for k in node.keywords)
            logger.error(
                "%s:%d: print() with %s -- convert this one by hand",
                path,
                node.lineno,
                ", ".join(keys),
            )
            problems += 1
    return problems


def _python_files(roots: list[str]) -> list[Path]:
    """Every .py under the given roots, skipping venvs and vendored trees."""
    found: list[Path] = []
    for root in roots:
        base = Path(root)
        candidates = [base] if base.is_file() else sorted(base.rglob("*.py"))
        found.extend(
            p for p in candidates if ".venv" not in p.parts and "sightpy" not in p.parts
        )
    return found


def main(argv: list[str] | None = None) -> int:
    """Run the requested checks and return 1 if any reported something."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="files, directories, or two trees")
    parser.add_argument("--signatures", action="store_true")
    parser.add_argument("--logging", action="store_true")
    parser.add_argument("--print-keywords", action="store_true")
    args = parser.parse_args(argv)
    logging.basicConfig(format="%(message)s", level=logging.INFO, stream=sys.stdout)

    problems = 0
    if args.signatures:
        expected = 2
        if len(args.paths) != expected:
            logger.error("--signatures needs exactly two trees: before after")
            return 1
        problems += check_signatures(Path(args.paths[0]), Path(args.paths[1]))
    if args.logging or args.print_keywords:
        files = _python_files(args.paths)
        if args.logging:
            problems += check_logging(files)
        if args.print_keywords:
            problems += check_print_keywords(files)

    logger.info("problems: %d", problems)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
