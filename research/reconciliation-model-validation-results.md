# Reconciliation Model Validation Results

**Date:** 17 November 2026  
**Scope:** Focused synthetic validation of the schedule calculator and reconciliation state machine.  
**Status:** Local isolated test run passed; full repository suite not executed.

## Execution result

A local isolated Python test harness was assembled from the current source and test logic retrieved from the repository. It exercised 29 focused cases across schedule arithmetic, payment-state integration and base reconciliation.

Result:

- 29 tests executed.
- 29 passed.
- 0 failed.
- Runtime: approximately 0.001 seconds.

The cases covered:
- future and due tranches;
- grace-period boundaries and overdue unpaid balances;
- FIFO payment allocation;
- timezone offsets and rejection of naive timestamps;
- agreement effective-period checks;
- duplicate tranche identifiers;
- carry-forward enabled and disabled;
- tolerance;
- excess payment reporting;
- missing schedules and schedule-version mismatch;
- missing and undetermined reports;
- allocation duplication and burn over-allocation;
- short payment and missing reward records;
- explicit non-claim about source-measurement completeness.

## Important execution qualification

A direct shallow clone of the private repository could not be completed because the execution environment could not resolve `github.com` (DNS/network failure). The 29-test run therefore used an isolated local harness assembled from the retrieved source and test logic. It is evidence that those focused scenarios pass against the locally reconstructed implementation, not evidence that the repository's complete test suite passes unchanged.

No claim is made that all repository tests were discovered or executed. A full checkout-based run remains outstanding.

## Review findings

1. Excess current payment is now exposed as `unapplied_payment_cc`. It is not silently converted into carry-forward credit. Prior credit remains separately governed by the agreement's explicit carry-forward flag.
2. Agreement schedule version is checked against each obligation's authoritative version before reconciliation.
3. Grace-period classification is separate from contractual due amount.
4. Report agreement-version comparison in the base model uses sets of versions. The schedule-integrated path adds a per-obligation version check, but report-to-obligation identity is not yet represented. A later interface revision should bind each report interval explicitly to its synchronizer/obligation and agreement version.
5. The model still cannot prove the truth or completeness of source traffic measurement, agreement legal authority, ledger finality or reward arithmetic.

## Next step

Add explicit synchronizer/obligation identity and interval-to-agreement binding to the input records, then add cross-obligation tests. After that, obtain a real repository checkout and run the exact checked-in test suite in CI or another reproducible Python environment.
