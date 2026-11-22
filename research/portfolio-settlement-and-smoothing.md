# Portfolio settlement: smoothing and multi-synchronizer allocation

**Status:** synthetic design experiment. It refines the proposed manifest; it is not a Canton implementation.

## 1. Why a portfolio model is necessary

CIP-0132 permits a paymaster to settle traffic from multiple synchronizers and permits discounts/smoothing under off-ledger agreements. A single public burn may therefore fund more than one synchronizer obligation. Requiring every burn event to map to exactly one synchronizer would be too restrictive.

The invariant is: total allocations from a burn event across all obligations must never exceed that burn's actual amount. Each allocation identifies its burn event and obligation; the validator checks that those records share a paymaster before crediting the obligation.

## 2. Model

Each obligation contains paymaster identity, synchronizer identity, interval-level traffic and agreement version, expected liability per priced interval, and a schedule of amounts and due times.

Burn events contain a public event identifier, amount and paymaster. Allocation records partition burn amounts across obligations.

The model validates interval continuity, complete report status, agreement version per interval, due schedule against expected liability, paymaster consistency, burn allocation limits, obligation liability limits and due-date-aware payment status. Each allocation has its own unique portfolio-wide allocation ID; a burn event ID is not used as an allocation ID. A burn may be partitioned across obligations, and each obligation may receive credit from multiple burns.

## 3. Synthetic portfolio example

One paymaster has two synchronizer obligations.

| Obligation | Synchronizer | Agreement segments | Expected CC | Due schedule |
|---|---|---|---:|---|
| O-A | dSync-A | v1: 5 CC; v2: 4 CC | 9 CC | 3 CC at t=100; 6 CC at t=200 |
| O-B | dSync-B | v4: 6 CC | 6 CC | 6 CC at t=100 |

The paymaster makes two burns: 9 CC and 6 CC. The first burn allocates 3 CC to O-A and 6 CC to O-B. The second allocates 6 CC to O-A. Total allocated value equals total burn value, 15 CC.

At t=150, O-B is reconciled and O-A has paid its 3 CC tranche; its remaining 6 CC is not yet due. At t=250, both obligations are reconciled. A variant that allocates only 2 CC to O-A is short-paid after the final due date. An allocation of 4 CC plus 6 CC from the first 9 CC burn is rejected because it allocates 10 CC from a 9 CC event.

All values are synthetic and do not represent a real paymaster, agreement or Canton burn.

## 4. Agreement changes

Expected liability is stored at interval granularity with an agreement version. This permits a settlement window to cross an agreement change without retrospectively applying one version to every interval.

The model does not calculate CC from raw bytes. It assumes a pricing engine produces per-interval expected CC under the applicable agreement and stores enough versioned inputs to reproduce it. The pricing function requires a documented agreement schema before it can be implemented faithfully.

## 5. Refined burn attribution invariant

One burn may be partitioned among multiple synchronizer obligations for the same paymaster, provided:
- all allocations reference the same real burn event;
- all allocated obligations belong to the same paymaster;
- allocation sums never exceed the burn amount;
- no allocation is duplicated;
- total credited value is never counted twice;
- each obligation's credited amount remains bounded by its liability.

This replaces the earlier, overly restrictive one-burn-to-one-obligation rule.

## 6. Allocation amendments and arithmetic

The portfolio validator accepts already committed `prior_allocations` separately from new allocations. It rejects allocation-ID reuse across that boundary and counts prior credit together with new claims against both the burn amount and the obligation liability. Thus an amendment can use only a burn's remaining unallocated amount; it cannot replay consumed credit as a fresh claim.

Amounts are compared as finite `Decimal` values with no float conversion and no quantization. No CC precision or rounding rule is specified here, so the model performs exact arithmetic on the supplied values and does not invent a smallest unit or rounding policy.

The local tests cover split burns, multiple burns per obligation, many-to-many portfolios, exact and excessive aggregate claims, duplicate evidence/IDs, missing references, paymaster mismatches, non-positive allocations, fractional values, due-tranche distinctions and amendment replay. These are prototype checks over supplied inputs, not evidence about production Canton behaviour.

## 7. Limits and next questions

The model does not verify ledger event authenticity, signatures, actual paymaster allocation policy, exchange rates, minimums, rounding, burn finality, disputes or reward attribution. It does not establish traffic completeness or privacy.

The model cannot establish that the supplied burn set or obligation set is complete, that an obligation is contractually eligible for a particular burn, or that caller-provided due schedules/amendment history follow an authoritative agreement. It does not define a CC precision policy.

Next: derive a reproducible pricing and amendment policy from a documented agreement, then compare which manifest fields can be public, selectively disclosed or held by an authorised auditor.
