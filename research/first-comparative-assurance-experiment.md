# First Comparative Assurance Experiment

**Status:** Executed synthetic experiment; not observed Canton network data.  
**Code:** `analysis/comparative_assurance_matrix.py`  
**Tests:** `tests/test_comparative_assurance_matrix.py`

## 1. Experimental setup

All four assurance architectures are given the same three scenarios. The illustrative agreement price is 0.1 CC per resource unit.

| Scenario | Actual units | Reported units | Burn | Condition |
|---|---:|---:|---:|---|
| Accurate accounting | 100 | 100 | 10 CC | Report and payment agree |
| Under-reporting | 100 | 80 | 8 CC | Report and payment agree with each other, but not actual activity |
| Missing report | 100 | unavailable | unavailable | Required interval has no usable report |

These values are deliberately synthetic. They do not represent Canton prices, activity or transactions.

## 2. Results

| Scenario | Public burn only | Signed report + agreement | Independent confidential audit | Cryptographic proof over submitted inputs |
|---|---|---|---|---|
| Accurate accounting | Burn observed; accounting relationship unverified | Reconciled to submitted report | Source measurement and payment reconcile | Proof verifies submitted-input calculation |
| Under-reporting | Cannot identify measurement error | **Does not detect it:** 80 units × 0.1 CC = 8 CC | Detects discrepancy if reliable independent source evidence shows 100 units | **Does not detect it:** proof can correctly verify 80 units × 0.1 CC = 8 CC |
| Missing report | Cannot establish report completeness | Marks interval incomplete | Marks missing report/source evidence incomplete | Detects absent interval only if a completeness manifest defines which intervals are required |

## 3. Main observation

The under-reporting scenario is the discriminating test.

The signed-report architecture and the cryptographic-proof architecture both accept an internally consistent calculation based on 80 reported units and an 8 CC burn. Neither can infer that actual activity was 100 units from those inputs alone.

The confidential-audit architecture detects the discrepancy only because this synthetic case gives the auditor independent source evidence for the 100-unit reference. If that evidence is unavailable, the audit result becomes inconclusive.

This is not an argument against cryptographic proofs. It defines what they prove. A proof can establish that a calculation follows from committed inputs. It does not establish that the inputs represent all real chargeable activity unless the measurement source is separately authenticated and complete.

## 4. Missing-report nuance

A missing report is detectable only if the verifier knows that a report was required.

For signed reconciliation, this means an expected-interval schedule or equivalent register. For cryptographic proofs, it means a completeness manifest or another authenticated statement of the required interval set. Without that reference, the verifier cannot distinguish an omitted report from an interval that was never expected.

## 5. What this experiment establishes

Within the defined synthetic scenarios:

- Public burn evidence alone does not reconcile private activity to contractual liability.
- Signed reports improve provenance and calculation traceability, but do not independently validate measurement completeness.
- Independent audit can detect source/report disagreement when reliable independent evidence is available.
- Cryptographic proofs can verify calculations over submitted inputs, but source truth and interval completeness require additional mechanisms.

These are logical results of the experiment's assumptions, not empirical estimates of real-world detection rates or Canton incidents.

## 6. Limitations and next experiment

The model currently treats independent source evidence as a binary available/unavailable input. It does not yet model noisy meters, audit sampling, auditor error, proof-system costs, privacy leakage or actual reconciliation latency. It also assumes a simple linear price function solely to keep the first comparison interpretable.

**Next experiment:** introduce imperfect source evidence and audit sampling. Measure how often each architecture detects injected under-reporting at different audit probabilities and source-measurement error rates. Keep the base accounting and proof assumptions fixed so that the next results remain comparable.
