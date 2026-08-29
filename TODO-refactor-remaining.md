# TODO: remaining work on the gate refactor

REMOVE ME AFTER FINISH

What is done, what is not, and the real numbers, re-measured 2026-08-28 after
the lint campaign started. Companion to `TODO-file-length-250.md`, which parks
one specific blocking decision.

## Done

| Area | State |
|---|---|
| Vendored manifest | `gates/vendored.txt`, 8 entries, mirrored into `~/utils` |
| Build artifacts | 189 untracked, `.gitignore` closed, 0 tracked-but-ignored files |
| no-binaries gate | Path-scoped `.binary-allowlist`; verified blocking AND passing |
| Markdown | 4 namespaces, all under 250 lines, `CLAUDE.md` written |
| pre-commit | 15 hooks, green on all files -- `ruff`, `ruff format` and `no-suppressions` landed 2026-08-29 |
| pre-push | `pre-commit install --hook-type pre-push` via `install.sh` |
| GitHub CI | `pre-commit` + `md-naming`, both green |
| run.sh | Root harness + per-course runners over one shared library |
| `pyproject.toml` | `select = ["ALL"]`, mypy strict, coverage config. **No hook wired up yet** |
| LaTeX 250-line cap | 19 reports split, every rebuilt PDF verified identical. 1 left |
| ZPOB | Fixed: builds with `--no-bibtex`, exits 0 |

## The lint campaign

`select = ["ALL"]`, and by kuhy's decision on 2026-08-28 there are **no
per-file-ignores at all** -- not even the `S101` block for tests that ruff's
own docs and the rest of this fleet carry. A test asserts by raising.

| | ruff findings |
|---|---|
| Baseline, before any of this | 9,281 |
| After the format + safe-fix pass and excluding `TRAK/sightpy` | 3,686 |
| **Now** | **0** |

**Every course is at zero.** 9,281 findings to 0.

What that cost, and what it bought, is in the commit messages; the standing
rules for the next pass are below.

## mypy: run per directory; the six deliberate errors are gone

`pyproject.toml` sets `strict = true` and `CLAUDE.md` says the repo runs mypy.
mypy IS installed now (`~/.local/bin/mypy`) -- the earlier note here saying it
was not is out of date. **"Zero findings" in a commit message still means zero
RUFF findings unless it says otherwise**; only `TRAK` has been type-checked.

| Course | mypy --strict errors |
|---|---|
| `WDWR`, `SPD`, `MOM`, `ECRYPT_PROJECT` | 0 |
| `ECOTE` | 14 |
| `NLP` | 29 |
| `EARIN/lab1` alone | 46 |
| `TRAK` | **0** -- cleared 2026-08-29 |
| `twm_4` | **0** -- cleared 2026-08-29 |
| `PBAD` | not run (no venv; notebooks only) |
| `PSD` | **0** -- cleared 2026-08-29 (scoped override; see below) |
| `ERSMS-project` | **0** -- cleared 2026-08-29 (typed DeclarativeBase) |

Two structural notes for whoever runs it next:

- It cannot be pointed at the whole repo. There are many `main.py` files and
  mypy stops at `Duplicate module named "main"`. Run it per directory.
- Most errors are `Returning Any` from untyped third-party calls (openai,
  pandas) and genuinely-wrong unions this pass introduced by hand, e.g.
  `str | bool` returns in `gpt_chunks.reformat`. They are real.
- Point it at the course's own venv or every import is unresolvable:
  `mypy --strict --python-executable Programming/<course>/.venv/bin/python <dir>`.
  Without that, TRAK reported 4 phantom `matplotlib` import errors on top of
  the real ones.
- **`ERSMS-project` is at 0** (was 4), fixed 2026-08-29. The old note here
  claimed a fix "would rewrite both models"; that was wrong. flask-sqlalchemy
  3.1.1 *does* ship `py.typed`. The actual blocker was that `class
  User(db.Model)` is attribute access, which mypy cannot resolve in a
  base-class position. `backend/models.py` now declares a named
  `DeclarativeBase` with SQLAlchemy 2.0 `Mapped[]` columns, and the six
  legacy `Model.query` call sites became `db.session` selects, because the
  `Model` mixin goes away with the base. Verified by driving the real routes
  through Flask's test client with Firebase stubbed: 16 scenarios and both
  `CREATE TABLE` statements byte-identical to the submitted version.
  Two traps worth keeping: `mapped_column(ForeignKey("user.uid"))` silently
  infers VARCHAR from the referenced column, which changed the submitted
  `user_id INTEGER` until an explicit `Integer` was put back; and
  `backend/Dockerfile` copied only `app.py`, so the split needed it too.
- **PSD is at 0** (was 2), by a scoped `[[tool.mypy.overrides]]` for
  `temperature_anomaly_detector` with `disallow_subclassing_any = false`.
  pyflink ships no types AND is not installed in that venv, so a hand-written
  `.pyi` would assert an API nothing here can check. Recorded in `CLAUDE.md`
  as well as here, because this file gets deleted and that one does not.
- Point `MYPYPATH` at `Programming/PSD/zin3/python/code` for that tree: the
  modules import `model.*` via a runtime `sys.path.append`, which mypy
  cannot follow.
- `pyproject.toml` now carries a `[[tool.mypy.overrides]]` block with
  `ignore_missing_imports` for `Imath`, `OpenEXR`, `OpenGL` and `matplotlib`.
  Those (plus `keras`, `tensorflow`, `sklearn`, `seaborn`, `kafka` and
  `pyflink`) ship neither stubs nor `py.typed`; without it mypy cannot import
  them at all and reports nothing else about the file. It is not a suppression
  of our own code -- do not extend it to anything we wrote.

## Found while proving the run guard, not yet fixed

`NotProgramming/MOM` was recorded as runnable and was not: `_first_file
'*.tex'` used `find -print -quit`, which handed back
`report_three/sections/02-model-dwukryterialny.tex`, and latexmk faithfully
tried to typeset a bare `\section`. It picks a file containing
`\documentclass` now, and MOM, ELAC, AIS, SPD, ZPOB, SDM, DPZ and ESOEN all
exit 0.

Two things surfaced on the way and are still true:

- **A multi-report course builds one arbitrary report.** PARTLY FIXED
  2026-08-29: `run.sh run <dir>` now enumerates every document and either asks
  which, or builds all of them when not interactive, so nothing depends on
  readdir order any more. What is still open is that some of those documents
  are broken -- see below. MOM has three, ELAC two, AIS several drafts.
  Sorting looked like the fix until it swapped ELAC to `projectA` and AIS to
  `report/final/ver1`, **both of which fail with latexmk exit 12** -- so those
  documents are broken and sorting merely surfaced it. Either build every
  document, or name one per course with `--entry`; either way the broken ones
  need looking at.
- `unityhub --version` never returns on this machine, which is why `_works`
  carries a `timeout 5`. Use `_works` only for tools that answer `--version`;
  `_have` is still right for the other ten probe call sites.

## Found by actually running the programs, not yet fixed

`run.sh run` executes what it builds as of 2026-08-29, and the first thing that
fell out is a course that had never been run by the harness at all:

- **`EPFU/labs/krudnic3_lab1.c` dies with SIGFPE** (exit 136) on
  `printf("\n%f", i_one / i_two)` -- an integer division by zero. It was
  invisible before because EPFU's stub pins `--entry` to `penguins/src`, so
  the lab was never compiled, let alone run. gcc also warns twice about
  `%d`/`%f` against the wrong argument types on lines 12 and 14. Left alone
  for now: it is a submitted deliverable and fixing it is a separate decision
  from making the runner work.
- **`ECOAR` overwrites a tracked deliverable when it runs.** `C/puzzle.out`
  writes `C/dest.bmp` beside its source, so the before/after tree guard fails
  the run -- correctly. It was invisible before for the same reason as EPFU's
  lab: the runner built `puzzle.out` and never executed it. The fix is to make
  the program write into `build/`, which means touching a submitted `.c`, so
  it is recorded rather than done. `git checkout --` restores the file
  meanwhile; the guard is what makes that recoverable at all.

## Still open

### 1. The 250-line cap: 50 files

| Type | Count | Note |
|---|---|---|
| `.txt` | 27 | Blocked -- see `TODO-file-length-250.md` |
| `.py` | 10 | Several GREW during the lint pass, because docstrings and annotations are lines: `NLP/gpt_chunks.py` 911 -> 973, `EARIN/lab2/main.py` 581 -> 647, `PORR/.../linear_algebra_utils.py` 422 -> 553. Split them AFTER the lint work, not during. TRAK is already clear: its three over-cap files were split in the same pass that linted them, each verified by a byte-identical render. `twm_4/TWM_KerasIntro.py` joined the list at 407 lines and should NOT be split: it is an nbconvert export, and a partial one |
| `.cpp` | 9 | |
| `.c` | 4 | |
| `.java` | 2 | |
| `.tex` | 1 | `ELAC/.../03-building-nfa-...tex`, 418 lines of consecutive tikz figures with no subsection to split on |

### 2. Coverage

`gates/coverage.tsv` is designed but not written, and there are 125 tests for
~28k lines. The largest remaining item by a wide margin.

### 3. Dependency freshness

9 `requirements.txt`, 5 `package.json`, 7 `pom.xml`, 1 `.csproj`, none pinned.
**The upgrade and the gate must land in the SAME commit.**

### 4. File-rewriting hooks

`trailing-whitespace` and `end-of-file-fixer` are deliberately absent; they
want their own reviewed commit.

### 5. Three checks that must be run on every future pass

`scripts/check_refactor_safety.py` exists because ruff and a smoke run BOTH
missed three regressions this campaign introduced. Run it before and after any
automated rewrite:

```bash
cp -r <course> /tmp/before
# ...do the pass...
./scripts/check_refactor_safety.py --signatures /tmp/before <course>
./scripts/check_refactor_safety.py --logging --print-keywords <course>
```

And run mypy per directory afterwards: it found 12 latent TypeErrors in EARIN
that ruff could not see -- call sites still passing positionally to arguments
the pass had made keyword-only.

Prefer a check the program itself settles. TRAK's `ray_tracing0` path has no
RNG at all, so `main.py --algorithm ray_tracing0 --output ../build/x.png`
renders byte-identically every time: refactoring 109 findings out of
`rendering.py` and splitting it in two was verified by one md5 comparison. The
cornell_box path is stochastic and cannot be used that way -- its ray count
drifts by ~20 between runs on its own. Where an RNG is unavoidable, do the
restructure and the `NPY002` swap as SEPARATE steps: the first must be
bit-identical under an external seed, only the second may move the pixels.

### 6. Disk

`Programming/PORR/code/` holds 3.8 GB of generated .npz caches (poli3 alone is
2.3 GB). All gitignored, all regenerable, none of it needed unless the full
benchmark is re-run.

## Standing rule

A gate lands only once the thing it gates is clean, so `pre-commit run
--all-files` is green at every commit. Every hook still missing from
`.pre-commit-config.yaml` is listed there with what blocks it.
