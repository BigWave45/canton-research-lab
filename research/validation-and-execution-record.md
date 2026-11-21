# Validation and execution record

This record preserves observed local test executions. It supersedes earlier chronological notes that said the integrated test suite had not yet been run.

## Local test executions

All results below were obtained in local Python execution, not from GitHub Actions. The tests use synthetic or explicitly constructed inputs; they do not query Canton production systems.

| Date (UTC) | Focused tests | Complete test suite | Additional check | Commit |
|---|---:|---:|---|---|
| 18 Nov 2026 | 63 passed | 243 passed | — | `b6c1bf27eb10c8bf0349f13f76d2053d85623726` |
| 18 Nov 2026 | 20 passed | 257 passed | `git diff --check` passed | `f99bbde5978dad5dd216244da060615d75357447` |
| 18 Nov 2026 | 71 passed | 271 passed | `git diff --check` passed | `68502120cecb8e223c5bfb5c98028aff02389ed4` |

The focused counts refer to the correction/integration suites exercised at each milestone. They are not additional tests to add to the complete-suite count. The complete-suite count is the observed result of the full local `unittest` discovery run at that commit.

The final recorded environment was Python 3.14.2. The full-suite command is:

```bash
PYTHONPATH=analysis python -m unittest discover -s tests -v
```

The agreement-signature tests require the `cryptography` package for Ed25519 operations. Install it before running the full suite:

```bash
python -m pip install cryptography
```

## GitHub Actions distinction

The repository also has GitHub Actions workflow runs that concluded with failure. These are not the successful local test executions above.

The inspected Actions run records show a failed job with no recorded steps, no assigned runner ID and no job log available through the retrieved GitHub API response. That does not establish that a Python test failed. It also does not establish the precise infrastructure cause. Do not cite those workflow conclusions as test-suite failures or as evidence that the local tests did not pass.

The cleanup pull request removes the old workflow file. This record does not claim that the workflow has been repaired or that a new Actions run has passed.

## What the passing tests establish

They establish that the tested implementation behaved as expected for the supplied test cases at the recorded commits. The work covers selected interval and report validation, agreement-signature checks, report-to-obligation binding, deterministic liability and reconciliation, burn allocation and correction handling, and bounded reward-budget checks.

They do not establish that:
- source traffic measurements are complete or independently authenticated;
- the prototype is connected to a production synchronizer, paymaster or reward service;
- the complete reward-attribution framework is implemented;
- the proposed accounting path is deployed end to end;
- synthetic scenarios measure real Canton operating behaviour.

The repository's research notes describe the assumptions and limits of individual experiments. A passing unit test must not be presented as a production measurement or deployment result.
