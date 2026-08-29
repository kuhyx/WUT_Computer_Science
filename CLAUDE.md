# WUT_Computer_Science

Archive of university coursework from Warsaw University of Technology.
44 course directories, 12 languages, ~28k lines of authored code plus the
submitted reports, figures and datasets. It is an **archive**: the code is
finished, and the value is that it still builds, runs and is readable.

## Repository Layout

| Path | What it is |
|---|---|
| `Programming/` | 25 course dirs with real code (Python, C/C++, Java, TS/Angular, C#, Unity, MATLAB-adjacent). |
| `NotProgramming/` | 19 course dirs that are mostly LaTeX reports, PDFs and EDA schematics. Exceptions: `ENUME` (MATLAB), `STUP/makieta` (Angular), `EDABA-LAB` (SQL). |
| `gates/` | Machine-readable gate inputs. `vendored.txt` is the source of truth for "not my code". |
| `scripts/` | Repo-local gates. Shims that `exec` into `~/utils` live here too. |

Two structural facts that surprise people:

- **`Programming/PSD/zin3/third/` and `Programming/psd_project/` are the same
  services under different names**, and `WDWR/project/` vs `WDWR/projekt/`,
  `SDM` vs `SDM2`, and `EMISY/componentSchematic/` vs `EMISY/schematic/` are
  likewise near-duplicates. They are **not** de-duplicated: each is a separate
  submitted deliverable, and merging them would rewrite the academic record.
- **`Programming/EOPSY/lab{3,4}/task*/work/` is not student code.** It is the
  extraction target of `make setup` from the tarballs in the sibling `ftp/`.
  Verified byte-identical, 14/14 files. Do not edit or split it.

## Git Workflow

Work directly on `main`; commit and push straight there.

```bash
./install.sh          # deps + pre-commit hooks, then verifies and fails loudly
./run.sh check        # the full local gate
./run.sh status       # probe every course dir, regenerate DOCS-runnability.md
./run.sh run <dir>    # build AND run one course, capped at 2G RAM and 2 cores
./run.sh run <dir> --list      # what targets does this course have?
./run.sh run <dir> 2           # run target 2 (an index, path substring, or "all")
./run.sh run <dir> --batch     # never prompt; stdin /dev/null, 60s per program
```

`run` runs the program, it does not just build it. Twelve courses have more
than one target (EPFU a game and a lab, EOOP six binaries, MOM three reports);
with no target named, an interactive `run` prints a numbered menu and asks.
Not a terminal, or `--batch`, means all targets and no prompt -- a prompt
nobody can answer is how an unattended run hangs. `--probe`/`status` never
execute anything and never enumerate targets, so the sweep stays seconds long.

It is interactive by default on purpose: EPFU's penguins and ECOAR's puzzle
both read stdin, and you typed `run`, so you are at the keyboard.

`run` executes inside a transient systemd scope (`MemoryMax=2G`,
`MemorySwapMax=0`, `CPUQuota=200%`, `nice -n 19`, `ionice -c 3`), so a course
build cannot make an interactive machine stutter. This is not caution, it is a
kernel-enforced ceiling -- PORR's suite solves 10000x10000 systems and will
take every core it is given. Raise it deliberately for a single run with
`RUN_MEMORY_MAX=8G RUN_CPU_QUOTA=800% ./run.sh run <dir>`.

Never `--no-verify`. If a gate fails, fix the cause.

## Development Workflow

- Confirm a change works by **running the thing** and reading its output, not
  by running tests. Tests come after.
- `git rm --cached`, never bare `git rm`, when removing build output — it must
  stay on disk so a mis-classification is recoverable.
- After touching `.gitignore` or `.binary-allowlist`, re-run:
  ```bash
  git ls-files | git check-ignore --stdin --no-index
  ```
  It must print nothing. A file that is both tracked and ignored fails
  **silently** on `git add`: not an error, the edit just never lands. This
  repo had 130 such files.

## Code Conventions

Anything a hook already enforces is omitted here — read
`.pre-commit-config.yaml` for that list. What follows is what a linter cannot
check.

### Everything

- **Every file is at most 250 lines, source and prose alike**, enforced by the
  shared gate in `~/utils`. There is deliberately no baseline and no
  allowlist: split the file. For a LaTeX report that means `\input{}` per
  section; for a markdown report, sibling `DOCS-*.md` files behind an index.
- **Coursework is held to the same bar as the tooling.** It gets the full
  `select = ["ALL"]` treatment -- annotations, docstrings, naming, the lot --
  and there are no per-file-ignores carving the two course trees out. The
  version that was handed in is preserved by git history, which is a better
  archive than a frozen working tree; this repo's job is code that still
  builds, runs and reads well. (This reverses an earlier rule that said not to
  improve coursework beyond what was submitted. kuhy overruled it on
  2026-08-28: "yes fix it if necessary we can always go back to worse version
  by going back in git repo.")
- The one thing that is still off limits is *what was delivered*: do not add
  content to a submitted `.pdf`/report that was never in it, and do not merge
  the near-duplicate submission directories listed above.

### Vendored content

`gates/vendored.txt` is the only place a path becomes exempt from lint,
coverage and the cap. Every entry carries a reason **and how it was
verified** — an unverified entry is a suppression wearing a costume. The list
is mirrored into `~/utils/file_length/_tables.py`, `[tool.ruff] exclude` and
`[tool.coverage.run] omit`; edit the manifest, never a mirror.

### Python

- `ruff` runs with `select = ["ALL"]` and mypy with `strict = true`.
- No `# noqa`, no `# type: ignore`. A pre-commit hook rejects both outright.
- mypy runs **per directory**, never repo-wide: many courses ship a `main.py`
  and mypy stops at `Duplicate module named "main"`. Point it at the course's
  own venv or every import is unresolvable:
  `mypy --strict --python-executable Programming/<course>/.venv/bin/python <dir>`.
- **One deliberate mypy override exists**, in `pyproject.toml`:
  `temperature_anomaly_detector` sets `disallow_subclassing_any = false`
  because it must subclass pyflink's `MapFunction` and `KeyedProcessFunction`,
  which ship no types and are not installed in `Programming/PSD/.venv`. It is
  scoped to that one module. Do not widen it, and do not add a second override
  for our own code without the same kind of reason written beside it.
- **No per-file-ignores either, including for tests.** `pyproject.toml` has no
  `[tool.ruff.lint.per-file-ignores]` table at all, which is stricter than the
  rest of the fleet. So a test asserts by raising:
  `if x != y: msg = ...; raise AssertionError(msg)` -- never a bare `assert`,
  which is `S101`. Test functions carry docstrings and full annotations like
  any other code, `pytest.raises` always takes `match=`, and an expected value
  gets a named constant rather than being a magic number. Decided by kuhy on
  2026-08-28 against the alternative of mirroring testsAndMisc's test block.
- Notebooks: `ruff` reads and formats `.ipynb` natively (cell-aware, so an
  import used two cells later is not reported unused), which is why there is
  no `nbqa` layer. It rewrites `source` only — outputs are left byte-identical.
  Nothing strips outputs on commit yet; the four notebooks here were committed
  with theirs. Real logic belongs in a sibling importable module — a notebook
  cannot be covered.

### LaTeX

Build output is ignored, not committed: `.aux`, `.fls`, `.fdb_latexmk`,
`.xdv`, `-eps-converted-to.pdf` and friends. The submitted `.pdf` **is**
committed, because it is the deliverable.

### Shell

`set -euo pipefail`, quoted expansions, `main "$@"` last. Never embed another
language's logic inline — put it in its own file so that language's tooling
applies.

## Key Files

| Path | Why it matters |
|---|---|
| `gates/vendored.txt` | What is not my code, and how each entry was verified. |
| `gates/coverage.tsv` | Per-directory coverage floors. Floors may only rise. |
| `.binary-allowlist` | Path-scoped: deliverables allowed under the two course trees, compiled output allowed nowhere. |
| `DOCS-runnability.md` | Per-course run status, recorded separately for `local` and `ci`. |
| `TODO-*.md` | Open decisions. Each carries the removal marker and is deleted when the work lands. |
