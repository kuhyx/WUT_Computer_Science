# TODO: remaining work on the gate refactor

REMOVE ME AFTER FINISH

What is done, what is not, and the real numbers. Companion to
`TODO-file-length-250.md`, which parks one specific blocking decision.

## Done

| Area | State |
|---|---|
| Vendored manifest | `gates/vendored.txt`, mirrored into `~/utils` (`kuhyx/utils@a4a3e0a`) |
| Build artifacts | 189 untracked, `.gitignore` closed, 0 tracked-but-ignored files |
| no-binaries gate | Path-scoped `.binary-allowlist`; verified blocking AND passing |
| Markdown | 4 namespaces, all under 250 lines, `CLAUDE.md` written |
| pre-commit | 12 hooks, green on all files |
| pre-push | `pre-commit install --hook-type pre-push` via `install.sh` |
| GitHub CI | `pre-commit` + `md-naming`, both green. Actions had been DISABLED at repo level |
| run.sh | Root harness + 44 course runners over one shared library |
| Runnability | 38 runnable / 5 no-code / 1 blocked, recorded in `DOCS-runnability.md` |

## Not done, with honest sizes

### 1. Python linting — 9,281 ruff findings

Measured with the fleet config (`select = ["ALL"]`, the five standard ignores):

| Rule | Count | Nature |
|---|---|---|
| `Q000` bad-quotes | 2050 | auto-fixable |
| `ANN001`/`ANN201` missing annotations | 1671 | **manual** |
| `E501` line-too-long | 628 | mostly manual |
| `T201` print | 316 | needs a decision per script |
| `D1xx` missing docstrings | ~600 | **manual** |
| `W291`/`W293` whitespace | 431 | auto-fixable |
| everything else | ~3600 | mixed |

Roughly 3,000 are auto-fixable and ~6,000 are hand work. The auto-fixable pass
should be its own commit so the manual diff stays reviewable.

**Blocked on:** nothing. Start with `ruff check --fix` on the safe rules, then
add `pyproject.toml` and the ruff/mypy hooks in the same commit as the last fix
(a gate must not land before its subject is clean).

### 2. Coverage — 19 tests for ~28k lines

`gates/coverage.tsv` (per-directory floors, `target` always 100, floors may
only rise) is designed but not written. Nothing exists for the non-Python
languages yet. This is the largest remaining item by a wide margin and is
measured in weeks.

### 3. Dependency freshness

9 `requirements.txt`, 5 `package.json`, 7 `pom.xml`, 1 `.csproj`, none pinned.
**The upgrade and the gate must land in the SAME commit** or the repo is
instantly and permanently red -- see the warning in
`~/utils/scripts/install_dependency_freshness_gate.sh`.

### 4. The 250-line cap

73 files still over. Breakdown: 27 `.txt` (blocked -- see
`TODO-file-length-250.md`), 19 `.tex`, 10 `.py`, 9 `.cpp`, 4 `.c`, 2 `.java`.
The `.tex` splits are `\input{}` per section, and the acceptance test is that
the rebuilt PDF is unchanged. **Do not split the source files before their
tests exist** -- splitting untested code is the highest-risk action here.

### 5. File-rewriting hooks

`trailing-whitespace` and `end-of-file-fixer` are deliberately absent. They
will touch hundreds of submitted coursework files, so they want their own
reviewed commit rather than being buried in a config change.

### 6. Two courses still fail `run`

- `Programming/PORR` -- its pytest suite solves systems up to 10000x10000 and
  runs for many minutes at full CPU. Under the 2G/2-core cap it will be
  OOM-killed rather than finish. It needs either a smaller default parameter
  set for `run`, or to be marked as a deliberately heavy target.
- `Programming/ZPOB` -- latexmk exits 12 from bibtex even though `esej.pdf` is
  produced. Probably a missing/!stale .bib entry; needs a clean-room rebuild
  to see the first real error rather than the cached one.

## Standing rule

A gate lands only once the thing it gates is clean, so
`pre-commit run --all-files` is green at every commit. Every hook still missing
from `.pre-commit-config.yaml` is listed there with what blocks it.
