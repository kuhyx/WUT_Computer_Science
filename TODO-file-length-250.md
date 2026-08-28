# TODO: the 27 data `.txt` files the 250-line cap cannot classify

REMOVE ME AFTER FINISH

The 250-line cap applies to prose as well as code, and the shared gate treats
`.txt` as prose unless its mean line is under 25 characters (a wordlist). These
27 files are **data** with long lines, so the heuristic reads them as prose and
demands they be split. Splitting any of them corrupts it: in every one, a line
is a record.

Nothing here blocks the refactor. It blocks exactly one step — installing the
`file-length` pre-commit hook and workflow — so it must be settled before that
lands, and not before.

Run `bash ~/utils/scripts/check_file_length.sh --all` to see the current list.

## Why the existing mechanism does not cover them

`VENDORED_SUBPATHS` in `~/utils/file_length/_tables.py` matches **directory
prefixes** (`/{repo}/{sub}/`). That is enough for the 7 entries already in
`gates/vendored.txt`, and it is not enough here:

- `Programming/NLP/test_goldStandard/images/` holds the official SemEval corpus
  **and** kuhy's own GPT outputs, side by side.
- `Programming/WDWR/projekt/R/` holds `scenarios.txt` (data) **and** `model.R`
  (authored, 464 lines, must stay gated and covered).

A directory entry would exempt authored work in both cases. Per-file `# noqa`
style suppression is banned outright. So this needs a decision, not a workaround.

## The four categories

### 1. Official SemEval package — 12 files, genuinely third-party

The `STSint.testinput.{headlines,images,answers-students}.{sent1,sent2}[.chunk].txt`
files. Verified against the package's own manifest in
`Programming/NLP/test_goldStandard/00-README.txt`, which enumerates exactly
these, plus `evalF1.pl` and `wellformed.pl`, as the contents of the
"STS 2016 Task 2 Interpretable Semantic Textual Similarity TEST DATASET"
(authors: Eneko Agirre, Montse Maritxalar et al.).

Unambiguously vendored. The only question is *how* to express it.

### 2. kuhy's GPT outputs living inside the corpus directory — 6 files

```
Programming/NLP/test_goldStandard/headlines/headlines-chunks-gpt-{one,two}.txt
Programming/NLP/test_goldStandard/images/images-chunks-gpt-{one,two}.txt
Programming/NLP/test_goldStandard/student/students-chunks-gpt-{one,two}.txt
```

**Not** in the package manifest — these are output from `gpt_chunks.py`, written
next to the corpus they were derived from. Regenerable in principle, but only by
re-running non-deterministic paid GPT calls, so untracking them destroys the
experimental record rather than saving space.

### 3. NLP pipeline data — 4 files

```
Programming/NLP/alignments_unformatted_headlines.txt   375 lines
Programming/NLP/alignments_unformatted_student.txt     344
Programming/NLP/output.txt                             348
Programming/NLP/reformated.txt                         348
```

Intermediate stage data. `alignments_unformatted_headlines.txt` is read as input
by `create_alignments.py:6` and `format_alignments.py:7`, so relocating these
costs exactly two path constants — the cheapest category to fix.

### 4. WDWR solver data and output — 5 files

```
Programming/WDWR/projekt/old_code/data10000.txt        10000 lines  (numeric matrix, solver input)
Programming/WDWR/projekt/R/scenarios.txt                 999        (generated scenario vectors)
Programming/WDWR/projekt/wdwr/solutions1.txt            3038        (CPLEX MILP solver log)
Programming/WDWR/projekt/wdwr/KRZYSZTOF_.../scenarios.txt  999      (submission copy)
Programming/WDWR/projekt/wdwr/KRZYSZTOF_.../solutions1.txt 3038     (submission copy)
```

Two of these live under `KRZYSZTOF_RUDNICKI_307585_WDWR_PROJEKT/`, the submitted
deliverable. Decision 6 of the approved plan says leave semantic duplicates
alone, so **relocation is not available for those two** — moving a file inside a
submission alters what was submitted.

## Options

**A. Extend the shared manifest to support file paths.** Teach
`~/utils/file_length/exemptions.py:is_vendored` to read `gates/vendored.txt` at
the repo root, supporting exact files as well as directories. This is the design
originally chosen (one root manifest consumed by every gate) and is the only
option that handles all four categories.
Cost: `file_length` currently has **zero tests** and no coverage job in
`.github/workflows/shared-gates-tests.yml`. Adding code to a gate 16 repos
depend on means authoring its test suite first.

**B. Relocate categories 2–4 into `data/` subdirectories** and add `data` to the
manifest per course dir. Cheap for categories 2 and 3. Cannot touch the two
WDWR submission-copy files. Does not address category 1.

**C. Accept a documented residual** — install the file-length gate with these 27
paths listed here, and treat the list as the record. Honest, but it is an
allowlist by another name, which the fleet rules reject.

Recommendation: **A**, taken as its own `~/utils` change with its own tests and
CI job, sequenced before Milestone 2 step 4. B as a fallback for categories 2–3
if A is judged too large, leaving categories 1 and 4 to a narrower version of A.
