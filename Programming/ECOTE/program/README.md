# ECOTE translator

Translates LaTeX `tabular` environments into HTML tables.

| Path | What it is |
|---|---|
| `translator/` | The implementation. Entry point `translator/main.py`. |
| `translator/functional_tests/` | End-to-end fixtures. |
| `unit_tests/test_code/` | 17 pytest modules. |

## Run the tests

```bash
python -m pytest unit_tests
```

> The package used to be called `code/`, which shadows Python's standard
> library `code` module. That is not cosmetic: pytest's debugging plugin
> imports `pdb`, `pdb` imports `code`, and it got this directory instead, so
> the whole suite died with an INTERNALERROR before collecting a single test.
> Renaming it is what makes these tests runnable at all.
