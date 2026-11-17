# Research Progress — 17 November 2026

## Comparative assurance experiment 1

Added:
- `research/comparative-assurance-model-specification.md`
- `analysis/comparative_assurance_matrix.py`
- `tests/test_comparative_assurance_matrix.py`
- `research/first-comparative-assurance-experiment.md`

The first experiment compares four assurance architectures across three synthetic scenarios: accurate accounting, internally consistent under-reporting, and a missing report.

### Main result from the defined scenarios

The under-reporting case is the key discriminator. Actual activity is 100 units, reported activity is 80 units, and the burn is 8 CC under an illustrative rate of 0.1 CC per unit.

- Public burn evidence shows that 8 CC was burned but cannot establish the correct private liability.
- Signed-report reconciliation accepts the submitted report and matches 8 CC. It does not detect that the source activity was 100 units.
- A confidential audit detects the discrepancy only when it has reliable independent source evidence. Without that evidence, the result is inconclusive.
- A cryptographic proof over submitted inputs can verify the arithmetic 80 × 0.1 = 8. It cannot infer that the source input omitted 20 units.

For the missing-report case, absence is detectable only against a known schedule or completeness manifest that establishes the interval was required.

### Interpretation and limitations

These are logical outcomes of a synthetic model, not measurements of Canton network behaviour, fraud frequency, detection probability, or deployed implementation performance.

The experiment currently abstracts away cryptographic signature verification, proof-system construction, auditor error, noisy measurement, audit sampling, privacy leakage and real operational cost. The architecture labels describe evidence capabilities, not implementations of those cryptographic or audit systems.

The next experiment should introduce imperfect source evidence and probabilistic audit sampling, while keeping the scenario definitions and accounting rules fixed.
