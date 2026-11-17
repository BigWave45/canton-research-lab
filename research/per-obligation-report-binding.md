# Per-Obligation Traffic Report Binding

**Status:** Synthetic model refinement.  
**Date:** 17 November 2026.

## Why the change matters

A dedicated-synchronizer paymaster arrangement can involve more than one synchronizer and more than one commercial agreement. A comparison of the *set* of report versions with the *set* of obligation versions is not sufficient.

For example, synchronizer A may legitimately use agreement version A-3 while synchronizer B uses B-7. A global set comparison can tell us that both version strings occur, but it cannot establish which report is governed by which agreement. It can therefore miss a crossed or incorrectly assigned report.

## Record binding

The synthetic `Report` record now carries:
- `report_id`: stable identifier for the reporting interval;
- `obligation_id`: the commercial obligation to which the interval belongs;
- `synchronizer_id`: the synchronizer whose traffic is represented;
- `agreement_version`: the agreement version used to interpret the report;
- `status`: `OK`, `UNDETERMINED` or `CANNOT_PROVIDE`.

The `Obligation` record carries its own `obligation_id`, `synchronizer_id` and authoritative agreement version.

## Verification predicates

For each report (r), the model checks:

1. Its obligation exists.
2. Its synchronizer identity equals the synchronizer attached to that obligation.
3. If the report status is `OK`, its agreement version equals that obligation's authoritative agreement version.
4. Every obligation has at least one supplied report in the case; expected report IDs independently enforce the expected interval set.

The first two failures produce `DISPUTED_REPORT_BINDING`. An absent report or non-OK report prevents final reconciliation. An agreement-version mismatch produces `BLOCKED_AGREEMENT_MISMATCH`.

## Cross-synchronizer example

| Record | Synchronizer | Obligation | Agreement version |
|---|---|---|---|
| Report r-A | sync-A | obligation-A | A-3 |
| Obligation A | sync-A | obligation-A | A-3 |
| Report r-B | sync-B | obligation-B | B-7 |
| Obligation B | sync-B | obligation-B | B-7 |

This is valid even though the agreements differ. A report for sync-A labelled with sync-B, or a report for obligation-A labelled B-7, is not valid.

## Tests added

- Distinct agreement versions correctly match their own obligations.
- A report bound to the wrong synchronizer is disputed.
- A report carrying the wrong agreement version is blocked.
- Existing report completeness and scheduled reconciliation fixtures now include explicit synchronizer identity.

## Limits

`report_id` is treated as the stable identifier for an interval in this model. The model does not yet validate interval start/end timestamps, interval overlap, expected cadence, or completeness of the expected-report schedule itself. It also cannot establish that the traffic measurement represented by an `OK` report is true or complete.

Next, formalise expected interval coverage: define the reporting window, cadence, boundaries and treatment of delayed or corrected reports. Then run the exact checked-in tests in a real repository checkout or CI.
