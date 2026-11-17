# Minimum Viable Reconciliation State Machine

**Status:** Synthetic research model, not a Canton production component.  
**Date:** 17 November 2026.

## 1. Purpose

The model tests whether a submitted set of interval reports, agreement references, obligations, public burns and allocation records can be reconciled at a specified evaluation time.

It does not determine whether the synchronizer meter observed every chargeable event. That is a separate measurement-assurance question.

## 2. Four independent checks

The state machine deliberately separates:

1. **Report completeness:** were all expected intervals supplied, and are all statuses billable `OK`?
2. **Agreement consistency:** do report and obligation records reference the authoritative agreement version supplied to the model?
3. **Payment/allocation:** are burn references valid, allocation IDs unique, burn amounts not over-allocated, and each obligation covered for the amount due?
4. **Reward record presence:** does the expected reward record exist?

This separation prevents a reward-record omission from being confused with a payment shortfall, and prevents a missing interval from being treated as zero activity.

## 3. State precedence

| Condition | Payment state | Reason |
|---|---|---|
| Missing, undetermined or cannot-provide interval | BLOCKED_INCOMPLETE_REPORTS | Liability cannot be finalised from incomplete measurement inputs |
| Report/obligation agreement versions differ | BLOCKED_AGREEMENT_MISMATCH | The price basis is not consistent |
| Duplicate allocation ID, unknown burn/obligation, negative amount or burn over-allocation | DISPUTED_ALLOCATION | Allocation evidence violates structural constraints |
| Valid records but allocated amount below amount due | SHORT_PAID | A due liability remains uncovered |
| Complete, version-matched, valid and sufficiently allocated | RECONCILED | Submitted records satisfy the model's reconciliation predicates |

Reward state is reported separately: NOT_REQUIRED, MISSING or RECORDED. If payment is reconciled but a required reward record is missing, the overall state is REWARD_PENDING.

## 4. Smoothing and due dates

The model takes `due_cc` as an input for each obligation at `evaluation_time`. It does not calculate the contract's instalment schedule.

That boundary is intentional. Smoothing terms are off-ledger and agreement-specific. A later schedule module must calculate the authoritative amount due from the executed agreement, its effective version, due tranches and evaluation timestamp.

Example:
- Gross liability: 10 CC.
- Amount due at the current evaluation time: 4 CC.
- Eligible allocated burn: 4 CC.
- Result: RECONCILED, not short-paid.

At a later evaluation time when all 10 CC is due, the same 4 CC allocation yields SHORT_PAID with a 6 CC shortfall.

## 5. Portfolio allocation

A public burn may fund more than one synchronizer obligation. The model therefore checks both:
- sum of allocations against each burn is no greater than that burn's public amount;
- allocations credited to each obligation are at least its amount due.

A valid 10 CC burn can be split 6 CC + 4 CC across two obligations. A 7 CC + 4 CC allocation against the same burn is invalid even if the obligations together are owed 11 CC. Payment claims cannot create more burn value than the public burn event contains.

## 6. Synthetic test coverage

Ten tests cover:
- complete and fully allocated settlement;
- missing interval;
- undetermined interval;
- agreement-version mismatch;
- a not-yet-due smoothed tranche;
- an overdue shortfall;
- duplicate allocation ID;
- burn over-allocation;
- missing reward record;
- explicit non-claim about source measurement completeness.

The tests are authored but have not been run against a repository checkout in this step.

## 7. Limits and next extension

The current model assumes:
- expected interval IDs are known to the verifier;
- agreement authority and the authoritative version are supplied correctly;
- due amounts are calculated correctly upstream;
- burn identifiers refer to genuine public ledger events;
- reward record presence is enough for this stage; reward amount and downstream distribution are not yet verified.

It cannot prove meter truth, source completeness, legal agreement authority, public ledger finality or correctness of reward arithmetic.

Next step: implement the agreement schedule calculator as a separate pure function and test effective dates, tranche deadlines, timezone handling, grace periods, tolerances and carry-forward rules. Then integrate its calculated due amounts into this state machine.
