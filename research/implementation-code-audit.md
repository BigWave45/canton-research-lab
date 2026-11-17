# Implementation Code Audit: Existing Synchronizer Traffic Accounting

**Date:** 17 November 2026  
**Repository inspected:** https://github.com/canton-network/splice  
**Branch snapshot inspected:** commit 408f7ed9e742707f0d6fe080ca386aedc742d977  
**Status:** Targeted source-code inspection, not a full security review.

## 1. Why inspect implementation

CIP-0129 describes a future universal-burn and reward-attribution framework. Before proposing new verification controls, we need to understand existing Canton/Splice traffic accounting and avoid claiming that a mechanism is absent when related infrastructure already exists.

The current public Splice repository contains a pre-existing decentralized-synchronizer extra-traffic purchase flow. It is relevant background, but it must not be conflated with CIP-0129's proposed universal-burn reporting mechanism.

## 2. Existing code path found

### AmuletRules_BuyMemberTraffic

File: daml/splice-amulet/daml/Splice/AmuletRules.daml

The choice accepts:
- provider party;
- member ID;
- synchronizer ID;
- migration ID;
- traffic amount;
- transfer inputs and context.

It obtains the configured traffic-purchase price and calls the buyMemberTraffic function. The returned result includes the round, transfer summary, Amulet paid, purchased traffic contract, sender change and metadata.

### buyMemberTraffic

The implementation:
1. validates that the synchronizer ID is supported;
2. validates that the purchase meets the configured minimum top-up;
3. burns Amulet through the transfer/burn path;
4. creates a MemberTraffic contract recording the purchase.

The traffic-cost function uses traffic amount in bytes, converts bytes to MB by dividing by 1,000,000, multiplies by the configured USD-per-MB traffic price, and converts USD cost into Amulet using the round's Amulet price.

This is an existing fee/purchase path, not proof that CIP-0129's dedicated-synchronizer universal-burn and party-attribution mechanism is implemented.

### MemberTraffic contract

File: daml/splice-amulet/daml/Splice/DecentralizedSynchronizer.daml

The contract records:
- DSO party;
- sequencer member ID (participant or mediator);
- synchronizer ID;
- migration ID;
- total purchased traffic bytes;
- number of purchases;
- Amulet spent;
- USD spent.

The contract comment describes it as state tracking extra synchronizer traffic purchases for a sequencer member.

### Aggregation automation

File: apps/sv/src/main/scala/org/lfdecentralizedtrust/splice/sv/automation/delegatebased/MergeMemberTrafficContractsTrigger.scala

The automation groups MemberTraffic contracts by member and synchronizer, then merges them by summing purchased bytes, purchase count, Amulet spent and USD spent.

## 3. What this establishes

The public implementation already has an on-ledger mechanism for:
- identifying a sequencer member and synchronizer for an extra-traffic purchase;
- recording the amount of traffic purchased;
- recording associated Amulet and USD costs;
- aggregating those purchase records.

This provides a concrete baseline for studying traffic accounting and auditability.

## 4. What it does not establish

This code path does not, by itself, establish:
- that the full CIP-0129 universal-burn policy is deployed;
- that dedicated synchronizer traffic is reported per application/party under CIP-0129;
- that MemberTraffic purchase records contain the underlying private transactions;
- that the member-level purchased-byte total proves which parties generated the traffic;
- that the CIP-0129 aggregate paid-traffic cap and per-party reward attribution are enforced by this existing contract;
- that the operator-reporting mechanism acknowledged in CIP-0129 has been implemented or cryptographically verified.

The distinction matters: MemberTraffic records a purchase associated with a sequencer member, synchronizer and migration. CIP-0129 describes operator-published aggregate traffic reports attributed per party for reward allocation. Those are different data objects and different accounting questions.

## 5. Research implications

1. Treat the existing MemberTraffic mechanism as the baseline accounting architecture.
2. Map how purchased bytes, paid CC/Amulet, round prices, and member identities are connected.
3. Determine whether and how current contracts expose enough information to independently reconcile purchase totals.
4. Separately inspect the implementation planned for CIP-0129; do not assume the existing MemberTraffic contract is its implementation.
5. Compare member-level traffic accounting with the new per-party reward attribution requirement.
6. If the CIP-0129 report mechanism is not yet implemented, the research should remain an ex-ante design analysis, not an empirical audit of live misreporting.

## 6. Source files

- AmuletRules traffic purchase and cost functions: https://github.com/canton-network/splice/blob/408f7ed9e742707f0d6fe080ca386aedc742d977/daml/splice-amulet/daml/Splice/AmuletRules.daml
- MemberTraffic and synchronizer fee configuration: https://github.com/canton-network/splice/blob/408f7ed9e742707f0d6fe080ca386aedc742d977/daml/splice-amulet/daml/Splice/DecentralizedSynchronizer.daml
- MemberTraffic aggregation automation: https://github.com/canton-network/splice/blob/408f7ed9e742707f0d6fe080ca386aedc742d977/apps/sv/src/main/scala/org/lfdecentralizedtrust/splice/sv/automation/delegatebased/MergeMemberTrafficContractsTrigger.scala
- CIP-0129: https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md
