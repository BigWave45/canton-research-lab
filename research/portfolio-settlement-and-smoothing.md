# Portfolio settlement: smoothing and multi-synchronizer allocation

**Status:** synthetic design experiment. It refines the proposed manifest; it is not a Canton implementation.

## 1. Why a portfolio model is necessary

CIP-0132 permits a paymaster to settle traffic from multiple synchronizers and permits discounts/smoothing under off-ledger agreements. A single public burn may therefore fund more than one synchronizer obligation. Requiring every burn event to map to exactly one synchronizer would be too restrictive.

The correct invariant is not one burn to one obligation. It is:

**The total amount allocated from a burn event across all settlement obligations must never exceed that burn's actual amount.**

Each allocation must identify the paymaster, burn event, obligation and amount. The full allocation ledger must be globally consistent.

## 2. Model

Each obligation contains:
- paymaster identity;
- synchronizer identity;
- interval-level traffic and agreement version;
- expected liability per priced interval;
- a schedule of amounts and due times.

Burn events contain a public event identifier, amount and paymaster. Allocation records partition burn amounts across obligations.

The model validates:
- interval continuity and complete report status;
- agreement version per interval;
- due schedule sums to the interval-derived expected liability;
- burn event identity and paymaster consistency;
- allocation amount does not exceed the burn;
- allocation to an obligation does not exceed its liability;
- a due amount not yet payable is not prematurely labelled short-paid.

## 3. Synthetic portfolio example

One paymaster has two synchronizer obligations.

| Obligation | Synchronizer | Agreement segments | Expected CC | Due schedule |
|---|---|---|---:|---|
| O-A | dSync-A | v1: 5 CC; v2: 4 CC | 9 CC | 3 CC at t=100; 6 CC at t=200 |
| O-B | dSync-B | v4: 6 CC | 6 CC | 6 CC at t=100 |

One public burn event is 15 CC. The allocation ledger assigns 9 CC to O-A and 6 CC to O-B. The sum of allocations equals the burn amount.

At t=150, O-B is reconciled and O-A is not yet due for its final 6 CC tranche. At t=250, both obligations are reconciled. This demonstrates why smoothing schedules must be represented explicitly.

A variant allocating 10 CC to O-A and 6 CC to O-B is rejected because 16 CC is allocated from a 15 CC burn. A variant allocating only 8 CC to O-A is short-paid after the final due date.

All values are synthetic. They do not represent a real paymaster, agreement or Canton burn.

## 4. Agreement changes

Expected liability is stored at interval granularity with an agreement version. This allows a settlement window to cross an agreement change without retrospectively applying one version to every interval.

The current reference model does not calculate CC from raw bytes. It assumes an upstream pricing engine produces the per-interval expected CC under the applicable agreement and stores enough versioned inputs to reproduce it. The next implementation stage should test that pricing function once an actual agreement schema is available.

## 5. Refinement to burn attribution invariant

The earlier simple manifest model treated a burn as belonging to one settlement. That is safe for a one-obligation-per-burn design but too restrictive for portfolio-level smoothing.

The refined rule permits a burn to be partitioned among multiple obligations, provided:
- all allocations reference the same real burn event;
- all allocated obligations belong to the same paymaster;
- allocation sums never exceed the burn amount;
- an allocation cannot be duplicated;
- total credited value is never counted twice;
- every obligation's credited amount remains bounded by its liability.

This refinement preserves the economic conservation rule while allowing aggregate burns.

## 6. Limits and next questions

- The model does not verify ledger event authenticity or signatures.
- It does not define how partial burns are allocated by a real paymaster.
- It does not define how exchange rates, minimums, rounding or volume discounts are calculated.
- It does not model disputes, reversals or burn finality.
- It does not establish reward attribution correctness.
- It does not prove traffic completeness or privacy.

Next: derive a reproducible pricing function from a documented agreement, then compare which manifest fields can be public, selectively disclosed or held by an authorised auditor.
