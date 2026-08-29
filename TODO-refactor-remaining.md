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
| pre-commit | 12 hooks, green on all files |
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
| **Now** | **308** |

Courses at zero: `WDWR`, `SPD`, `MOM`, `ECRYPT`, `ECRYPT_PROJECT`, `ECOTE`,
`NLP`, `EARIN`, `PORR`, `TRAK`, `twm_4`, `PBAD`. What is left, by course:

| Course | ruff | Can it be verified by running? |
|---|---|---|
| `ERSMS-project` | 156 | No: docker-compose course |
| `PSD` | 152 | No: `run.sh` predates the harness and installs packages with sudo |

`course_run.sh`'s notebook branch is fixed: it executes to a temp
`--output-dir`, probes jupyter by running it rather than by `command -v`, and
`course_main` now fails if a run changed anything git can see under the course
root. `PBAD` is still blocked on jupyter itself -- the binary on PATH is a
pipx shim whose interpreter is gone, so `--probe` reports "needs jupyter".

**A notebook does not need to be executed to be linted.** ruff reads `.ipynb`
natively and rewrites `source` only, so the check that the deliverable is
intact is a hash of everything EXCEPT `source`:

```python
stripped = {k: v for k, v in nb.items() if k != "cells"}
stripped["cells"] = [{k: v for k, v in c.items() if k != "source"} for c in nb["cells"]]
```

That hash was identical across all four passes on `twm_4` and all of PBAD's
three notebooks. The notebook also
round-trips byte-for-byte through
`json.dumps(nb, indent=1, ensure_ascii=False) + "\n"`, which is what makes
editing cells programmatically safe -- check it first for any new notebook.
Where an edit is mechanical, verify it mechanically too: PBAD's 134 long
Polish column names were re-wrapped by script, and an AST pass proved every
dict key still spells exactly what it did.

## mypy has NOT been run against any of this

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
| `PSD/zin1` | 5 |

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
- `pyproject.toml` now carries a `[[tool.mypy.overrides]]` block with
  `ignore_missing_imports` for `Imath`, `OpenEXR`, `OpenGL` and `matplotlib`.
  Those four ship neither stubs nor `py.typed`; without it mypy cannot import
  them at all and reports nothing else about the file. It is not a suppression
  of our own code -- do not extend it to anything we wrote.

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
