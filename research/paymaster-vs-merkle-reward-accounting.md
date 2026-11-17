# Comparing Two Dedicated-Synchronizer Accounting Designs

**Date:** 17 November 2026  
**Purpose:** Compare the Phase 2 paymaster payment path with the earlier Phase 3 Merkle-root reward-reporting proof of concept.  
**Status:** Design and code-history comparison; not a claim that either complete design is deployed on MainNet.

## 1. Why this comparison matters

The paymaster implementation and the earlier extension-reward proof of concept solve different parts of the accounting problem.

- The **Phase 2 paymaster model** gives participants unlimited traffic on a permissioned dedicated synchronizer. The operator exposes aggregate consumption reports; one registered paymaster buys traffic on the Global Synchronizer by burning CC. The current implementation tracker explicitly says the paid amount is not checked against the report.
- The **earlier Phase 3 reward-reporting proof of concept** commits to per-round activity using a Merkle root and total. The SV-side governance step attests the synchronizer's purchased-traffic total. The reward expansion mechanism constrains minted rewards to the committed tree's weight budget, reported total and purchased traffic.

The earlier proof of concept therefore contains an explicit on-ledger reward-budget invariant that the Phase 2 paymaster purchase flow does not implement. However, it was a Daml proof of concept, without Scala automation or end-to-end wiring, and was parked as future Phase 3 input. It is not evidence of a production feature.

## 2. Phase 2 paymaster model

### Data flow

1. The dedicated synchronizer consumes traffic.
2. The sync operator app reports participant traffic per 10-minute interval.
3. The paymaster reads the report and decides what to buy.
4. The paymaster burns CC through the existing traffic-purchase choice on the Global Synchronizer.
5. The purchase records a `MemberTraffic` contract and issues a `ValidatorRewardCoupon`.
6. The paymaster's app and asset activity are intended to be recorded through the CIP-0104 ActivityRecorder hook.

### Trust and control

- DSO governance registers a paymaster for a synchronizer.
- Only the registered paymaster may buy traffic for that synchronizer.
- SVs can archive the registration to stop a misbehaving paymaster.
- The report-to-purchase amount is not checked by the purchase choice.
- Paymaster automation is external to the Splice feature; each paymaster builds its own.
- The report endpoint is being added in PR #111; it was still open at the research snapshot.
- App reward activity recording is a separate follow-up; upstream ActivityRecorder PR #8449 was still draft.

### What is verifiable

The ledger can establish:
- which registered paymaster submitted the purchase;
- which synchronizer registration the purchase references;
- how many bytes the purchase says it bought;
- the CC burn and traffic-purchase accounting record;
- the configured activity weights and resulting activity once the hook is wired.

It does not, in the current Phase 2 purchase design, independently establish:
- that the purchased bytes equal the operator-reported bytes;
- that the report equals all traffic actually consumed;
- that every reporting interval was paid;
- that app rewards are passed through to the applications that generated activity.

## 3. Earlier Phase 3 Merkle-root reward-reporting proof of concept

Tracker issue `ChainSafe/canton-extending-mainnet#47` describes a Daml proof of concept:

1. The dedicated synchronizer operator reports per-round activity on the Global Synchronizer as a Merkle root hash plus total activity.
2. A per-synchronizer reporting state enforces monotonically increasing rounds and tracks cumulative reported activity.
3. A DSO governance vote starts processing the report and creates a `ProcessRewardsV2` tree with a reward issuance rate, expander and weight budget.
4. The operator expands the committed tree, and leaves mint reward coupons according to activity weight multiplied by the issuance rate.

A review found an important flaw in the first draft: the reported total and the committed Merkle tree were connected only by operator honesty. An operator could report a small total to obtain a favourable issuance rate while committing a tree whose leaves summed to much more.

The follow-up design added:
- a governance vote attesting the synchronizer's purchased-traffic total;
- a requirement that reported activity not exceed purchased traffic;
- weighted internal nodes in the Merkle reward tree;
- an expansion budget threaded through the tree so expansion order or tree shape cannot mint beyond the committed weight.

The resulting stated invariant chain is:

`minted rewards <= committed tree weights <= reported total activity <= purchased traffic`

Four adversarial tests were added for over-reporting relative to purchases, over-declared internal nodes, over-minting leaves and unweighted-batch smuggling.

This is a meaningful design result: it constrains the amount of reward issuance on-ledger even though the activity details remain committed rather than fully public.

### Critical limitations

The tracker says this was a Daml/Daml Script proof of concept only:
- no Scala automation;
- no end-to-end wiring;
- SV-side tranche split, weight, timeout and reported-versus-purchased checks were separate work;
- operator automation and durable tree expansion were out of scope.

The tracker later says rewards were out of Phase 2 and the machinery was parked as input to Phase 3. It must not be represented as a deployed production control.

## 4. Side-by-side comparison

| Dimension | Phase 2 paymaster | Earlier Phase 3 PoC |
|---|---|---|
| Primary purpose | Pay for aggregate dSync traffic with CC | Attribute app rewards to committed activity |
| Measurement input | Operator's 10-minute aggregate traffic report | Operator's per-round activity records |
| On-ledger representation | Traffic purchase / burn record | Merkle root, total activity, reward tree |
| Who submits | Registered paymaster | dSync operator reports; SV governance authorises processing |
| Amount bound to purchased traffic | No report-to-purchase equality check in Phase 2 purchase choice | Proposed invariant requires reported activity <= purchased traffic |
| Reward budget | CC burn yields validator reward; app activity hook intended | Weight budget constrains reward-tree expansion and coupon issuance |
| Granularity | Aggregate paymaster attribution | Per-app / per-activity leaf attribution |
| Privacy | Aggregate report; private transaction payloads remain off-ledger | Merkle commitment can hide activity details while supporting committed expansion |
| Automation | Paymaster builds its own automation | Operator and SV automation were explicitly outside the PoC |
| Status in snapshot | Purchase PRs merged; report API PR open; ActivityRecorder upstream draft | Daml PoC merged on fork, parked as Phase 3 input; not wired end-to-end |

## 5. Research implication

The strongest research problem is now broader and more interesting than simply asking whether paymasters can underpay.

**How should a privacy-preserving financial network allocate verification responsibilities across measurement, payment and reward issuance as it moves from an aggregate trusted-paymaster model to granular committed activity reporting?**

This question supports three separate properties:

1. **Measurement integrity:** does the operator's reported traffic accurately represent sequencer consumption?
2. **Payment completeness:** do cumulative CC burns cover the reportable consumption under the agreed pricing rules?
3. **Reward integrity:** are app and validator rewards bounded by verified burns and committed activity weights?

These properties should not be collapsed into a single statement that the system is "trustless" or "verified." Different controls address different stages.

## 6. Candidate contribution

A hybrid quantitative/interdisciplinary paper could produce:

- a formal state-transition model of both architectures;
- a trust-boundary map identifying who controls each input and who can verify it;
- a reconciliation model for traffic, reports, purchases, CC burns and rewards;
- a formal proof or executable property tests for reward-budget invariants;
- a comparative assessment of aggregate paymaster reporting versus committed per-activity reporting;
- an implementation roadmap identifying the minimum controls needed to move between phases without disclosing private transaction payloads.

The quantitative core can measure:
- report error and coverage;
- unpaid and overpaid traffic;
- report-to-burn lag;
- reward issuance per CC burned;
- committed activity per purchased byte;
- maximum reward-budget overrun under adversarial tree expansion;
- operator/paymaster incentives under alternative pricing and reward arrangements.

## 7. Sources

- Phase 2 paymaster implementation tracker: https://github.com/ChainSafe/canton-extending-mainnet/issues/155
- Phase 2 traffic report requirements: https://github.com/ChainSafe/canton-extending-mainnet/issues/152
- Phase 2 paymaster Daml implementation: https://github.com/canton-network/splice-multi-sync/pull/100
- Phase 2 Scan/SV implementation: https://github.com/canton-network/splice-multi-sync/pull/104
- Phase 2 traffic-report API: https://github.com/canton-network/splice-multi-sync/pull/111
- Earlier Merkle-root reward-reporting PoC: https://github.com/ChainSafe/canton-extending-mainnet/issues/47
- Earlier PoC implementation: https://github.com/canton-network/splice-multi-sync/pull/8
- CIP-0104 ActivityRecorder draft: https://github.com/canton-network/splice/pull/8449
- CIP-0132: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
