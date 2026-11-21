# Comparative Assurance Experiment: Initial Three Scenarios

**Status:** Executed synthetic model; not an empirical study of Canton traffic or paymaster behaviour.  
**Model:** `analysis/comparative_assurance_model.py`  
**Tests:** `tests/test_comparative_assurance_model.py`

## Purpose

The first experiment compares four assurance architectures against the same three accounting conditions. The purpose is to test what each architecture can establish from its evidence, not to estimate real-world fraud or error probabilities.

## Explicit assumptions

- One synchronizer, one paymaster and one required accounting interval.
- The expected interval schedule is known to the verifier for the signed-reconciliation and proof architectures. Without a known schedule, an omitted interval may be indistinguishable from an interval that was never expected.
- The independent auditor can inspect complete and sufficiently reliable source records. If source records are incomplete or controlled by the same unverified measurement process, the audit result is weaker.
- The cryptographic proof binds the expected interval set, report commitment, agreement calculation and burn-allocation statement. It proves the encoded statement over submitted inputs, not the truth of the source measurement.
- A payment is considered reconciled when the burn equals the liability calculated from the submitted report and agreement. This is deliberately distinct from whether the report reflects actual activity.
- All activity and CC amounts below are illustrative.

## Scenario inputs

| Scenario | Actual activity | Reported activity | Calculated liability | Allocated burn |
|---|---:|---:|---:|---:|
| Accurate accounting | 100 | 100 | 10 CC | 10 CC |
| Under-reporting | 100 | 90 | 9 CC | 9 CC |
| Missing interval | 100 | No report | Undetermined | 0 CC |

The under-reporting case is intentionally constructed so the paymaster burns exactly what the understated report says is due. This isolates measurement completeness from payment arithmetic.

## Results matrix

| Scenario | Public burn only | Signed reconciliation | Independent confidential audit | Cryptographic proof |
|---|---|---|---|---|
| Accurate accounting | Burn observed; liability and measurement cannot be assessed | Reconciles; measurement remains unverified | Audited and reconciled, assuming complete independent source evidence | Proof valid for submitted inputs; source measurement remains unverified |
| Under-reporting | Cannot detect omission from burn data alone | Passes internal reconciliation; does not detect omitted activity | Detects under-reporting by comparing report with independent source evidence; burn still matches understated liability | Proof passes over submitted inputs; does not detect omitted source activity |
| Missing interval | Cannot know an interval was required | Detects missing interval from expected schedule and signed coverage manifest | Detects missing interval from schedule and source records | Detects inability to prove complete interval coverage, if expected interval set is bound into the statement |

## What the experiment establishes

1. **Payment reconciliation and measurement assurance are separate properties.** In the under-reporting case, the 9 CC burn exactly matches the 9 CC liability calculated from the report. The payment reconciles while the report is wrong relative to the synthetic reference activity.
2. **A signature does not make a measurement complete.** Signed reconciliation provides provenance and reproducible arithmetic, but cannot independently identify activity omitted before signing.
3. **A proof can faithfully prove the wrong input.** A proof that the submitted report was processed correctly does not show that the report includes every chargeable event.
4. **Completeness requires an expected population or interval set.** A missing report is detectable only when the verifier knows that the interval should exist. A cryptographic proof can enforce coverage of that known set, but cannot conjure missing source data.
5. **Independent audit has stronger measurement assurance only under a demanding assumption:** the auditor must obtain complete, reliable source evidence that is independent enough to challenge the reported measurement.

## What this does not establish

- It does not estimate detection probabilities, actual incident rates or expected financial losses.
- It does not establish that any Canton paymaster has under-reported or failed to pay.
- It does not establish that the proposed CIP-0132 reporting interface currently provides a signed coverage manifest or a cryptographic proof.
- It does not show that independent source evidence is currently available to an auditor.
- It does not measure operational cost, privacy leakage or latency. Those dimensions remain for later experiments.

## Model validation

The six unit tests check matrix size, the distinction between report/payment reconciliation and source measurement, detection of under-reporting under the independent-audit assumption, missing-interval detection when the expected schedule is known, the limits of public burn-only evidence, and the limits of proofs over submitted inputs.

Run from the repository root:

```bash
python -m unittest discover -s tests -p 'test_comparative_assurance_model.py' -v
python analysis/comparative_assurance_model.py
```

## Next experiment

Add agreement-version mismatch and smoothing/due-date handling. These test whether an architecture can distinguish a genuine shortfall from a payment that is contractually not yet due. After that, expand to burn misallocation across multiple obligations.
