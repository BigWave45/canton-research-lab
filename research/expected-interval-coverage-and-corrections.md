# Expected Interval Coverage and Corrections

**Status:** Synthetic, implementation-neutral model.  
**Date:** 17 November 2026.

## Purpose

A reconciliation process cannot identify a missing report unless it knows which intervals were expected. This specification defines an expected schedule, a reporting deadline and an append-only correction chain.

## Example

A one-hour window with ten-minute cadence contains six half-open intervals: 12:00-12:10, 12:10-12:20, and so on through 12:50-13:00. With five minutes of reporting grace, each report is due five minutes after its interval ends.

At 13:00, a missing final report is still pending. At 13:06, it is overdue. An UNDETERMINED report is never interpreted as zero activity.

## Correction rule

Reports are immutable versions. Revision zero has no predecessor. Each later revision increments by one and explicitly references the report it supersedes. The evaluator uses the latest valid revision while preserving earlier records. A broken chain or revision gap is invalid.

A report arriving after its deadline remains marked late even if its status is OK. A correction is separately marked, rather than silently rewriting the original report.

## States

- COMPLETE: every expected interval has a valid on-time OK report.
- INCOMPLETE_PENDING: an interval is still within reporting grace and has no report.
- INCOMPLETE_OVERDUE: an expected interval remains missing after its deadline.
- INCOMPLETE_NON_OK: the latest report status is not OK.
- COMPLETE_WITH_LATE_REPORTS: every interval has an OK report, but at least one arrived after its deadline.
- INVALID: unexpected interval, boundary mismatch, duplicate ID, invalid status, naive timestamp, revision gap or broken correction chain.

## Research implications

1. The expected schedule is authoritative input. A verifier needs a committed schedule or another trusted way to know cadence, window boundaries and exceptions.
2. Late data should remain visible. A policy may allow late reports for eventual settlement, but should not erase missed deadlines.
3. Corrections should be append-only and attributable.
4. A correction can change liability and may require a settlement adjustment or new manifest. This model records the chain but does not calculate that adjustment.
5. Coverage establishes presence and structural validity, not truth or completeness of source measurement.

## Files

- analysis/interval_coverage.py
- tests/test_interval_coverage.py

The ten tests are authored. They must be run in a real repository checkout or CI before being reported as passing.

## Limitations

Inputs are synthetic. The module is not integrated into Canton or the existing reconciliation state machine. It does not establish schedule authority, source-measurement completeness, revised liabilities, or legal dispute outcomes.
