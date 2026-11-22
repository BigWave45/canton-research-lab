# Validation and execution record

This record distinguishes successful local test executions, GitHub Actions workflow failures, and the branch on which the tested code exists.

## Successful local test executions

The following results were recorded from local Python execution. The test inputs were synthetic or explicitly constructed; they did not query Canton production systems.

| Date (UTC) | Focused tests | Complete local suite | Additional check | Commit |
|---|---:|---:|---|---|
| 18 Nov 2026 | 63 passed | 243 passed | — | `b6c1bf27eb10c8bf0349f13f76d2053d85623726` |
| 18 Nov 2026 | 20 passed | 257 passed | `git diff --check` passed | `f99bbde5978dad5dd216244da060615d75357447` |
| 18 Nov 2026 | 71 passed | 271 passed | `git diff --check` passed | `68502120cecb8e223c5bfb5c98028aff02389ed4` |

The focused counts refer to correction/integration suites exercised at each milestone. They are not extra tests to add to the complete-suite count. The complete-suite count is the observed result of the full local `unittest` discovery run at that commit.

The final recorded environment was Python 3.14.2. The full-suite command was:

```bash
PYTHONPATH=analysis python -m unittest discover -s tests -v
```

The agreement-signature tests require `cryptography` for Ed25519 operations:

```bash
python -m pip install cryptography
```

## Critical branch scope

Commit `68502120cecb8e223c5bfb5c98028aff02389ed4` is on the `circleci-project-setup` development history. The current `circleci-project-setup` branch is nine commits ahead of that test commit; the comparison shows those later commits changed research/state documentation, not the `analysis/` or `tests/` files. The recorded 271-test result therefore applies to the tested analysis/test snapshot carried by that development branch.

The public cleanup PR, however, was created from `main`. The `main` branch does not contain the same analysis and test code. A direct comparison identifies differences in multiple implementation and test files, including interval coverage, integrated reconciliation, portfolio settlement, protocol settlement, adversarial accounting, comparative assurance and their tests.

Therefore, **271 passing tests must not be represented as a test result for the current `main` branch or the current presentation PR**. The tested development code and the public branch must first be reconciled. The final reconciled tree must then be tested before claiming that the public branch's code passes.

## GitHub Actions distinction

The repository's GitHub Actions workflow runs concluded with failure. These are GitHub Actions failures, not failed local test executions. The inspected latest job record contained no executed steps and no assigned runner; no job log was available from the retrieved API response. This does not establish that the Python tests ran and failed. The exact infrastructure cause remains undetermined.

The cleanup PR currently removes the old GitHub Actions workflow. This record does not claim that the workflow was repaired or that a new Actions run passed.

## What the passing tests establish

They establish that the tested implementation behaved as expected for the supplied test cases at the recorded development-branch commits. The work covers selected interval and report validation, agreement-signature checks, report-to-obligation binding, deterministic liability and reconciliation, burn allocation and correction handling, and bounded reward-budget checks.

They do not establish that:
- source traffic measurements are complete or independently authenticated;
- the prototype is connected to a production synchronizer, paymaster or reward service;
- the complete reward-attribution framework is implemented;
- the proposed accounting path is deployed end to end;
- synthetic scenarios measure real Canton operating behaviour.

The repository's research notes describe the assumptions and limits of individual experiments. A passing unit test must not be presented as a production measurement or deployment result.
