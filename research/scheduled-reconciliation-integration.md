# Scheduled Reconciliation Integration

**Status:** Synthetic research model. Not a Canton production component.  
**Date:** 17 November 2026.

## 1. Integration change

The reconciliation state machine previously required callers to supply an already calculated due amount. It now has a second entry point, `reconcile_with_schedules`, which accepts:
- the ordinary report, burn and allocation case;
- one authoritative agreement schedule per obligation;
- optional prior credit per obligation.

For each obligation, it calculates the due amount at the case evaluation time, net of prior credit only when carry-forward is enabled. It then runs the existing report, agreement, allocation and reward checks.

## 2. Payment-state refinement

A valid-record payment shortfall is now classified using the schedule result:
- `WITHIN_GRACE`: amount is contractually due but the unpaid portion has not passed its grace deadline;
- `PAST_GRACE_UNPAID`: an unpaid portion remains after the grace deadline;
- `RECONCILED`: current eligible allocations and authorised prior credit cover the amount due within tolerance.

Higher-priority evidence failures remain unchanged. Missing reports, agreement mismatch and invalid allocations still block or dispute reconciliation rather than being re-labelled as grace states.

## 3. Carry-forward

Prior credit is not automatically accepted. The schedule must explicitly enable carry-forward. Otherwise, supplied prior credit is ignored. This avoids silently treating an overpayment in one period as payment for another period without contractual authority.

## 4. Test coverage

Four integration tests cover:
- due amount within grace;
- unpaid amount after grace;
- missing schedule rejection;
- prior credit ignored unless carry-forward is enabled.

The standalone schedule module has twelve authored tests; the integration has four authored tests. They have not been executed in a repository runtime in this step.

## 5. Remaining limits

The integrated model still assumes that:
- the schedule and agreement version supplied are authoritative;
- reports are complete and truthful if their status is OK;
- burn references represent final public ledger events;
- allocation records are authentic;
- the stated tolerance and FIFO allocation policy match the executed agreement.

This integration makes the due-date arithmetic explicit. It does not establish those underlying facts.
