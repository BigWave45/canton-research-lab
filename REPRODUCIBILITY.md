# Reproducibility

This repository contains deterministic research models and unit tests. They evaluate supplied synthetic or explicitly constructed records; they do not query Canton production systems.

## Requirements

- Python 3.10 or later.
- The test suite uses Python's built-in `unittest` framework.
- The repository does not currently provide a pinned dependency lockfile. Do not assume that every optional analysis script has been tested in every Python environment.

## Run the test suite

From the repository root:

```bash
PYTHONPATH=analysis python -m unittest discover -s tests -v
```

The `PYTHONPATH` setting makes the modules in `analysis/` available to the test files.

## Run selected standalone experiments

Examples:

```bash
python analysis/aggregate_linear_leakage.py
python analysis/aggregate_disclosure_experiment.py
```

Not every analysis module is designed as a standalone command-line program. Inspect its module docstring and `run` or entry-point function before executing it.

## Interpretation

A passing test establishes that the checked-in implementation behaved as expected for that test's supplied inputs. It does not establish:

- completeness or authenticity of production traffic measurements;
- production deployment or integration of the proposed accounting path;
- legal authority or institutional independence of signers;
- correctness of production tariffs or reward rules;
- independent operational assurance.

Synthetic experiment outputs must be interpreted under the assumptions stated in the corresponding research note and in the paper. In particular, synthetic privacy experiments do not establish the permissions or query capabilities of a live Canton reporting interface.

## Reproducibility record

For a reproducible report, record the commit SHA, Python version, command, test output and any local modifications. The manuscript's November 2026 snapshot and its source references define the scope of the reported findings.
