# Reproducibility

This repository contains deterministic research models, validators and unit tests. They evaluate supplied synthetic or explicitly constructed records; they do not query Canton production systems.

## Requirements

- Python 3.14.2 was used for the recorded successful local full-suite execution.
- The test suite uses Python's built-in `unittest` framework.
- Agreement-signature tests require the `cryptography` package for Ed25519 operations.
- The repository does not currently provide a pinned dependency lockfile.

Install the test dependency:

```bash
python -m pip install cryptography
```

## Run the test suite

From the repository root:

```bash
PYTHONPATH=analysis python -m unittest discover -s tests -v
```

A complete local suite of **271 tests passed** on 18 November 2026 at commit `68502120cecb8e223c5bfb5c98028aff02389ed4`, using Python 3.14.2. That commit is on the `circleci-project-setup` development history. The current `main` branch and the presentation PR do not contain the same analysis/test code, so this result does not certify those branches. See the [validation and execution record](research/validation-and-execution-record.md) for the branch comparison, earlier successful milestones and the distinction from GitHub Actions failures.

## Run selected standalone experiments

Examples:

```bash
python analysis/aggregate_linear_leakage.py
python analysis/aggregate_disclosure_experiment.py
```

Not every analysis module is designed as a standalone command-line program. Inspect its module docstring and `run` or entry-point function before executing it. Each experiment's research note defines its inputs, assumptions, expected invariants and interpretation limits.

## Interpretation

A passing test establishes that the tested implementation behaved as expected for that test's supplied inputs. It does not establish:
- completeness or authenticity of production traffic measurements;
- production deployment or integration of the proposed accounting path;
- legal authority or institutional independence of signers;
- correctness of production tariffs or reward rules;
- independent operational assurance.

Synthetic experiment outputs must be interpreted under the assumptions stated in the corresponding research note and in the paper. In particular, synthetic privacy experiments do not establish the permissions or query capabilities of a live Canton reporting interface.

## Reproducibility record

For a new run, record the commit SHA, branch, Python version, command, test output and any local modifications. Do not conflate a successful local test execution with a GitHub Actions workflow conclusion. Test the final reconciled branch before describing its implementation as passing.
