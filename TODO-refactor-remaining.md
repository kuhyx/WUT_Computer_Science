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
| **Now** | **1,183** |

Courses at zero: `WDWR`, `SPD`, `MOM`, `ECRYPT`, `ECRYPT_PROJECT`, `ECOTE`,
`NLP`, `EARIN`, `PORR`. What is left, by course:

| Course | ruff | Can it be verified by running? |
|---|---|---|
| `TRAK` | 531 | **Yes** -- `run` ray-traces cornell_box in 37s. `sightpy/` is vendored and excluded; this is kuhy's own code |
| `twm_4` | 228 | No: `jupyter` on PATH is a dead pipx shim. `pip install jupyter` in a venv would fix that |
| `ERSMS-project` | 156 | No: docker-compose course |
| `PSD` | 152 | No: `run.sh` predates the harness and installs packages with sudo |
| `PBAD` | 115 | No: same dead jupyter shim |

**Before running the notebook courses, fix `scripts/course_run.sh` first.**
Its notebook branch is `jupyter nbconvert --execute --inplace`, and all four
notebooks are tracked WITH their outputs -- that would overwrite a committed
deliverable. This exact bug has already been found twice (TRAK's
`outputs/output.png`, SPD's `results_*.png`); execute to a temp path instead.

## mypy has NOT been run against any of this

`pyproject.toml` sets `strict = true` and `CLAUDE.md` says the repo runs mypy,
but mypy is not installed on this machine (pip is externally managed; use a
venv) and no commit so far has type-checked. **"Zero findings" in the commit
messages means zero RUFF findings.** Measured after installing it:

| Course | mypy --strict errors |
|---|---|
| `WDWR`, `SPD`, `MOM`, `ECRYPT_PROJECT` | 0 |
| `ECOTE` | 14 |
| `NLP` | 29 |
| `EARIN/lab1` alone | 46 |
| `TRAK` | 1 |
| `PSD/zin1` | 5 |

Two structural notes for whoever runs it next:

- It cannot be pointed at the whole repo. There are many `main.py` files and
  mypy stops at `Duplicate module named "main"`. Run it per directory.
- Most errors are `Returning Any` from untyped third-party calls (openai,
  pandas) and genuinely-wrong unions this pass introduced by hand, e.g.
  `str | bool` returns in `gpt_chunks.reformat`. They are real.

## Still open

### 1. The 250-line cap: 51 files

| Type | Count | Note |
|---|---|---|
| `.txt` | 27 | Blocked -- see `TODO-file-length-250.md` |
| `.py` | 11 | Several GREW during the lint pass, because docstrings and annotations are lines: `NLP/gpt_chunks.py` 911 -> 973, `EARIN/lab2/main.py` 581 -> 647, `PORR/.../linear_algebra_utils.py` 422 -> 553. Split them AFTER the lint work, not during |
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

### 6. Disk

`Programming/PORR/code/` holds 3.8 GB of generated .npz caches (poli3 alone is
2.3 GB). All gitignored, all regenerable, none of it needed unless the full
benchmark is re-run.

## Standing rule

A gate lands only once the thing it gates is clean, so `pre-commit run
--all-files` is green at every commit. Every hook still missing from
`.pre-commit-config.yaml` is listed there with what blocks it.
