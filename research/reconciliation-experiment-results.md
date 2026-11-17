# Synthetic reconciliation experiment: results and limits

**Status:** deterministic model and unit tests; not a Canton protocol implementation and not empirical network measurement.

## Tested cases

| Case | Expected payable | Burn counted | Result |
|---|---:|---:|---|
| Four intervals, 10 units each, 10% discount, one smoothed burn | 36.00 CC | 36.00 CC | Reconciled |
| Same usage, 4 CC withheld | 36.00 CC | 32.00 CC | 4.00 CC residual |
| One interval unavailable | Not computable | Not evaluated | Incomplete |
| Same burn event delivered twice | 36.00 CC | 36.00 CC | Reconciled; duplicate ignored |
| Agreement changes from 10% to 20% discount | 17.00 CC | 17.00 CC | Reconciled |

A conflicting duplicate event ID with a different amount is rejected. A burn assigned to another settlement window is not counted.

## Rounding sensitivity

For three charges of 0.005 CC, rounding each interval to 0.01 CC produces 0.03 CC. Summing first and rounding once produces 0.02 CC. The one-cent difference is a consequence of the rounding rule, not measurement error. The model currently applies per-interval rounding; the actual contractual rule must be obtained before treating this as the correct Canton calculation.

## Interpretation

1. Agreement-aware window reconciliation avoids the false alarm created by demanding an immediate burn for each ten-minute report when settlement is delayed or smoothed.
2. A known 4 CC shortfall is detectable in the synthetic case once the settlement window is complete and the report, agreement and burn mapping are all available.
3. Missing, undetermined or unavailable intervals must produce an incomplete result. Treating them as zero usage would make the accounting unsound.
4. Duplicate ingestion can be made idempotent only when burn events have stable identifiers and conflicting records are rejected.
5. Agreement versioning must be explicit. A single current price/discount applied retrospectively can misstate historical liabilities.

## Model boundaries

- Inputs are synthetic. No operator traffic report or real CC burn was used.
- The simulator assumes the caller supplies exactly the intervals belonging to a settlement window. It does not infer contractual window membership.
- It assumes each report's agreement version is known and that the burn event can be assigned to the relevant settlement window.
- It does not prove that reported traffic equals actual traffic.
- It does not establish that the public burn is correctly linked to the private report.
- It does not model CC/USD conversion, collateral, paymaster automation, reward coupon issuance, or dispute resolution.
- A counter reset or logical synchronizer upgrade is represented as unavailable evidence (`cannot_provide`); the model does not reconstruct missing counters.
- It does not yet test split views across synchronizer nodes, participant join/leave semantics, report tampering, or reward issuance bounds.

## Reproduction

```bash
python analysis/paymaster_reconciliation_experiment.py
python -m unittest discover -s tests -v
```

The test suite contains ten deterministic tests. These establish behaviour of this model only, not production correctness.
