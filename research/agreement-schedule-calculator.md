# Agreement Schedule Calculator: Due Dates, Grace and Carry-Forward

**Status:** Synthetic research model, not a Canton production component.  
**Date:** 17 November 2026.

## 1. What this adds

The reconciliation state machine previously accepted an externally calculated `due_cc`. This module calculates that amount from a versioned agreement schedule at a specified evaluation time.

It answers four distinct questions:
- How much has reached its contractual due date?
- How much has passed the grace deadline?
- How much remains unpaid after applying eligible prior credit and current allocated payment?
- Is the remaining shortfall still within grace, beyond grace, or within an explicit tolerance?

## 2. Example

Assume a 10 CC liability split into two tranches:
- 4 CC due on 10 November.
- 6 CC due on 10 December.
- Three-day grace period.
- No carry-forward credit.

At 11 November, 4 CC is contractually due but still within grace. Zero payment is therefore classified `WITHIN_GRACE`, not `PAST_GRACE_UNPAID`.

At 15 November, the 4 CC tranche has passed its grace deadline. Zero payment is `PAST_GRACE_UNPAID`.

At 15 December, the full 10 CC is due. If 4 CC has been allocated, the oldest tranche is covered FIFO and the remaining 6 CC is unpaid. The second tranche is still within its grace window, so the result is `WITHIN_GRACE` rather than an overdue shortfall.

Grace does not rewrite the contractual due date. It changes the late-payment classification. The output therefore reports both `due_cc` and `past_grace_due_cc`.

## 3. Rules and assumptions

- Timestamps must include a UTC offset. Naive timestamps are rejected.
- Agreement effective interval is start-inclusive and end-exclusive.
- Amounts are integer CC smallest units; floating-point arithmetic is not used.
- Tranche identifiers must be unique; amounts and grace/tolerance values cannot be negative.
- Current allocated payments are applied FIFO to the oldest due tranches.
- Prior credit is ignored unless carry-forward is explicitly enabled.
- When enabled, prior credit offsets due tranches first; unused prior credit is reported separately. Current payment in excess of all due tranches is returned as `unapplied_payment_cc`; it is not silently converted into carry-forward credit.
- Tolerance is explicit and does not silently change the underlying due amount.
- The supplied agreement version is assumed authoritative; the calculator cannot establish legal authority.

## 4. Integration contract

For each obligation, the calculator returns:
- `due_cc`: all tranches whose due date has arrived, net of eligible prior credit;
- `past_grace_due_cc`: amount whose grace deadline has passed, net of credit;
- `due_unpaid_cc`: due amount not covered by prior credit or current allocated payment;
- `past_grace_unpaid_cc`: unpaid portion of tranches whose grace deadline has passed;
- `status`: NOT_YET_DUE, RECONCILED, WITHIN_GRACE or PAST_GRACE_UNPAID.

The reconciliation state machine should compare allocations with `due_cc` for accounting coverage and use `past_grace_unpaid_cc` to distinguish an overdue shortfall from a shortfall still within grace. It must not label every unpaid due amount as a late payment.

## 5. Synthetic test coverage

Thirteen tests cover future tranches, due dates, grace expiry, FIFO allocation, partial payment, carry-forward enabled/disabled, excess credit, tolerance, timezone offsets, naive timestamps, agreement effective periods and duplicate tranche IDs, and explicit reporting of payment not applied to currently due tranches.

Tests are authored; execution status must be recorded separately. All data is synthetic.

## 6. Limits and next step

This calculator does not validate traffic measurements, agreement signatures, CC ledger finality, legal interpretation, or whether a payment allocation is genuine. It assumes the agreement terms have already been authenticated and represented faithfully.

Next, integrate its `due_cc` and `past_grace_unpaid_cc` outputs into the reconciliation state machine, then run the complete synthetic test suite and record reproducible results.
