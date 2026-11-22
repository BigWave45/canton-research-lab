# Integrated Interval Coverage and Settlement Adjustments

**Status:** Synthetic integration specification.  
**Date:** 17 November 2026.

## Purpose

This layer connects expected interval coverage to the existing reconciliation model. It blocks final reconciliation when expected reports are missing, non-OK, late under the default policy, or structurally invalid.

## Correction accounting

A corrected report does not overwrite a prior settlement. The integration requires an agreement-aware liability calculation for the corrected report and compares it with the liability used by the prior settlement.

For a prior settled liability L_old and corrected liability L_new:

adjustment = L_new - L_old.

A positive adjustment represents additional liability; a negative adjustment is only a credit candidate. The model emits an append-only adjustment keyed deterministically by settlement and corrected report ID. Callers may provide previously processed adjustment IDs to make reprocessing a no-op; durable persistence of that idempotency set is caller-owned.

The prior settlement snapshot may include amount settled, burn IDs, committed allocations and reward IDs. When allocation records are supplied, they are reconciled together with new claims against the original burn amounts; replayed allocation or reward IDs are blocked. If a correction has new allocation claims and prior settled/burn/allocation credit is recorded, the caller must explicitly mark the prior allocation details complete; otherwise reconciliation blocks rather than assuming that unused burn capacity is available. The completeness flag is a caller assertion, not authenticated evidence. A post-correction result preserves links to the old and corrected reports, settlement, agreement version, authority reference, prior burn/allocation IDs, and new allocation/burn references.

For partial settlement the model reports the corrected outstanding amount after prior payment; for full settlement it separates additional liability from a credit candidate. It does not rewrite the original settlement, automatically refund/net/carry forward a credit, or reverse rewards. If prior payment amount or allocation details are absent, related balance claims remain explicitly unknown or incompletely evidenced; new correction allocation claims are blocked when prior credit is known but its complete allocation details are not supplied.

Report revisions must form one explicit chain: each correction names its predecessor, branches and cycles fail, and only the terminal valid revision is priced for an unsettled obligation. Paymaster, synchronizer, interval, obligation, agreement version and authority reference are held constant across a correction chain. The signed binding layer additionally compares the new binding identity with the prior settlement snapshot.

These are prototype rules, not Canton correction requirements. CIP-0132 leaves the report-to-burn link and commercial terms off-ledger and does not specify a correction, reversal, refund, carry-forward or reward-reversal process. A mathematical delta does not prove that the correction was authorised.

## Late-report policy

Late reports block settlement by default. A caller may explicitly allow them, in which case the result retains COMPLETE_WITH_LATE_REPORTS. This is a policy choice, not a claim about current Canton rules.

## Tests

Focused tests cover complete/missing coverage, late-report policy, missing corrected-liability inputs, upward/downward corrections, corrections before settlement, partial/full settlement deltas, deterministic idempotency keys, allocation/reward replay, incomplete prior-allocation-history blocking, burn-cap conservation, identity changes, branching/cycles/missing predecessors, and signed authority continuity.

On 18 November 2026 the focused local correction-related suites passed: 71 tests total across interval coverage (29), correction identity (6), pricing/correction integration (12), multi-interval correction edges (4), and signed protocol settlement interface (20). The complete local suite passed 271 tests; execution details are recorded in `STATE.md`.

## Evidence boundary and current upstream references

CIP-0132 is Proposed and describes ten-minute traffic reporting, trusted paymaster burns, off-ledger report/burn links and app/validator reward creation. It does not define correction authority or post-settlement corrections. The current [splice-multi-sync#111](https://github.com/canton-network/splice-multi-sync/pull/111) report API PR was open when checked on 18 November 2026. Its diff describes final reports for completed intervals and `CannotProvide` when counters are pruned or predate an upgrade; it does not define report revisions or a correction/settlement-adjustment flow. [ChainSafe/canton-extending-mainnet#152](https://github.com/ChainSafe/canton-extending-mainnet/issues/152) remained open and requests persisted totals across pruning/LSU, unfinished-interval handling, and four-node consistency. These are source-status observations, not proof of deployed behavior.

## Limits

The integration is synthetic. It does not prove the expected schedule or correction authority, calculate revised liabilities from traffic quantities unless a separately validated agreement-aware calculation is supplied, establish source measurement completeness, or implement a legal dispute/credit/reward-reversal process. The exact acceptance and retention rules for corrections, settled burns, credits and rewards remain unspecified in the applicable protocol and commercial agreement evidence reviewed here. No production Canton guarantee or live vulnerability is claimed; an authorised end-to-end operator/network test remains outstanding.
