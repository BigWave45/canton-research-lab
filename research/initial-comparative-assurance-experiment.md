# Comparative Assurance Experiment: Initial and Extended Scenarios

**Status:** Synthetic model and experiment. The original three-scenario baseline was executed, and the user confirmed that the CircleCI research-test pipeline eventually passed after the earlier eight failures. The exact CircleCI run URL and tested commit SHA are not recorded here, so this note does not assert that the run tested the current branch head. This is not an empirical study of Canton traffic or paymaster behaviour.  
**Model:** `analysis/comparative_assurance_model.py`  
**Tests:** `tests/test_comparative_assurance_model.py`

## Purpose

The experiment began with three accounting conditions and was subsequently extended to six. The current executable model compares four assurance architectures against all six conditions (24 scenario/architecture combinations). The purpose is to test what each architecture can establish from its evidence, not to estimate real-world fraud or error probabilities.

## Explicit assumptions

- One synchronizer, one paymaster and one required accounting interval.
- The expected interval schedule is known to the verifier for the signed-reconciliation and proof architectures. Without a known schedule, an omitted interval may be indistinguishable from an interval that was never expected.
- The independent auditor can inspect complete and sufficiently reliable source records. If source records are incomplete or controlled by the same unverified measurement process, the audit result is weaker.
- The signed-reconciliation and cryptographic-proof architectures are abstract capability assumptions in this comparison. The model does not verify a signed traffic report or implement a proof circuit. The current agreement-signature prototype verifies pricing-agreement terms only; it does not attest the report-to-obligation binding. The proof architecture is assumed to bind the expected interval set, report commitment, agreement calculation and burn-allocation statement. Even then, it proves the encoded statement over submitted inputs, not the truth of the source measurement.
- A payment is considered reconciled when the burn equals the liability calculated from the submitted report and agreement. This is deliberately distinct from whether the report reflects actual activity.
- All activity and CC amounts below are illustrative.

## Scenario inputs

| Scenario | Actual activity | Reported activity | Calculated liability | Allocated burn |
|---|---:|---:|---:|---:|
| Accurate accounting | 100 | 100 | 10 CC | 10 CC |
| Under-reporting | 100 | 90 | 9 CC | 9 CC |
| Missing interval | 100 | No report | Undetermined | 0 CC |
| Agreement-version mismatch | 100 | 100 | 8 CC under stale v1 | 8 CC |
| Smoothing not yet due | 100 | 100 | 10 CC total; 4 CC due now | 4 CC |
| Overdue smoothing shortfall | 100 | 100 | 10 CC total; 10 CC due now | 4 CC |

The under-reporting case is intentionally constructed so the paymaster burns exactly what the understated report says is due. This isolates measurement completeness from payment arithmetic. The agreement-version case tests an authoritative v2 reference against use of v1. The two smoothing cases hold total liability and burn constant but vary the amount due at evaluation time, so a not-yet-due balance is not confused with an overdue shortfall.

## Results matrix

| Scenario | Public burn only | Signed reconciliation | Independent confidential audit | Cryptographic proof |
|---|---|---|---|---|
| Accurate accounting | Burn observed; liability and measurement cannot be assessed | Reconciles; measurement remains unverified | Audited and reconciled, assuming complete independent source evidence | Proof valid for submitted inputs; source measurement remains unverified |
| Under-reporting | Cannot detect omission from burn data alone | Passes internal reconciliation; does not detect omitted activity | Detects under-reporting by comparing report with independent source evidence; burn still matches understated liability | Proof passes over submitted inputs; does not detect omitted source activity |
| Missing interval | Cannot know an interval was required | Detects missing interval from expected schedule and signed coverage manifest | Detects missing interval from schedule and source records | Detects inability to prove complete interval coverage, if expected interval set is bound into the statement |

### Extended scenarios now in the executable model

| Scenario | Public burn only | Signed reconciliation | Independent confidential audit | Cryptographic proof |
|---|---|---|---|---|
| Agreement-version mismatch | Cannot identify the applicable agreement from burn data | Detects mismatch against authoritative version reference | Detects mismatch and can separately inspect source evidence | Detects mismatch if authoritative version reference is bound into the proof statement |
| Smoothing not yet due | Cannot infer liability or due schedule | Treats 4 CC paid against 4 CC due as current | Same payment result, with measurement assurance only under the source-evidence assumption | Treats the due-schedule predicate as satisfied if the schedule is correctly committed |
| Overdue smoothing shortfall | Cannot infer liability or due schedule | Detects 6 CC overdue against 10 CC due | Detects overdue shortfall; source measurement assurance still depends on independent records | Detects the encoded due-amount shortfall if the schedule and inputs are correctly bound |

The extended rows describe the current model's classifications. They are not additional empirical observations, and the model does not yet quantify the different privacy, latency or implementation-cost properties of signed reconciliation versus cryptographic proof.

## What the experiment establishes

1. **Payment reconciliation and measurement assurance are separate properties.** In the under-reporting case, the 9 CC burn exactly matches the 9 CC liability calculated from the report. The payment reconciles while the report is wrong relative to the synthetic reference activity.
2. **A signature does not make a measurement complete.** Signed reconciliation provides provenance and reproducible arithmetic, but cannot independently identify activity omitted before signing.
3. **A proof can faithfully prove the wrong input.** A proof that the submitted report was processed correctly does not show that the report includes every chargeable event.
4. **Completeness requires an expected population or interval set.** A missing report is detectable only when the verifier knows that the interval should exist. A cryptographic proof can enforce coverage of that known set, but cannot conjure missing source data.
5. **Independent audit has stronger measurement assurance only under a demanding assumption:** the auditor must obtain complete, reliable source evidence that is independent enough to challenge the reported measurement.
6. **Agreement version and due schedule are independent accounting controls.** The model detects a mismatch against the authoritative agreement version and distinguishes 4 CC currently due from a 10 CC total liability.
7. **The extended model contains six scenarios and four architectures.** Its 24 outputs are logical model classifications, not 24 empirical observations. Signed reconciliation and cryptographic proof currently share several detection outcomes because this model does not yet quantify their different privacy, cost, latency or verifier-trust properties.

## What this does not establish

- It does not estimate detection probabilities, actual incident rates or expected financial losses.
- It does not establish that any Canton paymaster has under-reported or failed to pay.
- It does not establish that the proposed CIP-0132 reporting interface currently provides a signed coverage manifest or a cryptographic proof.
- It does not show that independent source evidence is currently available to an auditor.
- It does not measure operational cost, privacy leakage or latency. Those dimensions remain for later experiments.

## Model validation

The checked-in test file currently contains ten test methods. They check the 24-row matrix, report/payment reconciliation versus source measurement, under-reporting under the independent-audit assumption, missing-interval detection, public burn-only limits, proof/input limits, agreement-version mismatch, and the distinction between smoothing not yet due and an overdue shortfall. The user-confirmed CircleCI pass is the current reported suite status. Because the run URL and tested commit SHA were not captured, do not attribute that pass to a specific branch head or claim independent verification of this test file's inclusion without checking the CircleCI run details.

Run from the repository root:

```bash
python -m unittest discover -s tests -p 'test_comparative_assurance_model.py' -v
python analysis/comparative_assurance_model.py
```

## Next experiment

The model already includes agreement-version mismatch and smoothing/due-date handling. The next research task is to audit whether these abstractions faithfully represent CIP-0132's permitted commercial arrangements, then extend the experimental design only where a measurable research question remains. Portfolio allocation is already modelled elsewhere in the repository and should be integrated into the evidence map rather than reimplemented.
