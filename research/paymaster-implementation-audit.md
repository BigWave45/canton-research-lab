# Paymaster Implementation and Traffic-Report Audit

**Research snapshot:** 17 November 2026  
**Repositories inspected:** `canton-network/splice-multi-sync`, `canton-network/splice`, and the public ChainSafe implementation tracker `ChainSafe/canton-extending-mainnet`.  
**Scope:** Public proposal, pull-request, issue and source-code evidence. This is not a security audit of a deployed production network.

## 1. Implementation status at the snapshot

| Component | Evidence | Status at 17 Nov 2026 |
|---|---|---|
| Register a dedicated synchronizer with a paymaster | `splice-multi-sync#89` | Merged |
| Paymaster buys traffic through Daml choice | `splice-multi-sync#100` | Merged 11 Nov 2026 |
| Scan and SV app handle paymaster purchases and merge traffic records | `splice-multi-sync#104` | Merged 12 Nov 2026 |
| Grant unlimited traffic to admitted dSync members | `splice-multi-sync#101` | Merged |
| Operator exposes 10-minute traffic report | `splice-multi-sync#111` | Open, non-draft; latest review comments resolved, but not merged |
| Record paymaster app/asset activity through CIP-0104 hook | `ChainSafe/canton-extending-mainnet#163`; upstream `splice#8449` | Follow-up; upstream PR #8449 remains draft |
| End-to-end registration → usage → report → payment → activity test | `ChainSafe/canton-extending-mainnet#159` | Tracked follow-up; acceptance requires green CI |
| Paymaster automation | Epic `ChainSafe/canton-extending-mainnet#147` | Explicitly not included; each paymaster builds its own |

The ChainSafe tracker describes this as a Phase 2 deliverable targeting Splice 0.11.0, with a stated deadline of 2 December 2026. That is a project-tracker target, not evidence that the feature is live on Canton MainNet.

## 2. Payment path: what the merged Daml code enforces

PR #100 extends `AmuletRules_BuyMemberTraffic` with an optional `DSyncTrafficPurchase` argument. When present, the choice fetches the DSO-signed `RegisteredSynchronizer` and validates:

- the provider is the registered paymaster;
- the purchase synchronizer ID matches the registration;
- the synchronizer is not one of the Global Synchronizer's required synchronizers;
- migration ID is 0;
- member ID is empty, because the paymaster pays for the synchronizer as a whole;
- app and asset activity weights are between zero and the registration maxima;
- the traffic purchase meets the minimum top-up amount.

The token-standard transfer path obtains the registration from Scan's choice context. PR #104 adds the Scan lookup/index and SV-side merging of paymaster traffic contracts. A paymaster's `MemberTraffic` record uses an empty `memberId`, and the SV app merges those contracts per synchronizer.

The purchase reuses the existing traffic-cost and CC-burn path. The purchase creates a `ValidatorRewardCoupon`, as it does for ordinary traffic purchases.

These are meaningful controls over **who may buy for which registered synchronizer** and the parameters of the purchase. They do not establish that the amount purchased equals the amount consumed.

## 3. The key accounting gap is explicit in the implementation tracker

The parent issue `ChainSafe/canton-extending-mainnet#155` states:

> Nothing checks the paid amount against the report, and the paymaster may pay for less than was used.

The issue also states that Super Validators can stop a misbehaving paymaster by archiving its registration. This is a governance remedy, not automatic reconciliation of each billing period.

The design therefore separates three events:

1. The synchronizer consumes traffic.
2. The operator reports aggregate consumption.
3. The registered paymaster chooses and submits a CC traffic purchase.

The purchase contract validates registration, payer identity, synchronizer identity, weights and minimum top-up. It does not receive or verify a report interval, a cumulative report total, or a proof that the purchase covers that total.

Consequently, the on-ledger burn proves that CC was burned for a stated traffic amount. It does not independently prove that all consumed dSync traffic was paid for. This is the central measurement-to-payment trust boundary.

## 4. Traffic-report API: measurement method

The report API is proposed in PR `splice-multi-sync#111`, which was still open on 17 November.

- Endpoint: `GET /v0/traffic-report`
- Query range: `[start_record_time, end_record_time)`
- Default interval: ten minutes, aligned to UTC interval boundaries.
- Page size: 100 intervals; the response provides `next_start_record_time` where more pages remain.
- Authentication: JWT bearer authentication; the PR adds an auth configuration and tests rejection of absent or wrong-audience tokens.
- Interval statuses:
  - `Ok`: interval ended and traffic is final;
  - `Undetermined`: interval has not ended or the sequencer has not sequenced past its end;
  - `CannotProvide`: interval is no longer readable due to pruning or predates the current sequencer after an upgrade.

### How the number is calculated

The implementation reads each participant's cumulative `extraTrafficConsumed` counter from the sequencer traffic state at both ends of an interval and sums the differences.

The report code relies on the dedicated synchronizer's base traffic rate being zero. Under that configuration, extra traffic is the traffic charged, so the cumulative counter difference represents interval consumption.

The function iterates participants present at the end reading:
- a participant present only at the end is counted from zero (joined during the interval);
- a participant absent at the end is not counted (left during the interval);
- mediators are excluded because the calculation selects `ParticipantId` entries.

The last two rules matter for completeness. The code's own unit test models a participant who leaves during an interval and excludes that participant's accumulated consumption from the interval total. Whether the sequencer retains a departing member's final counter elsewhere, and whether this is intentional billing policy, should be confirmed with the implementation owners. Until then, the public API total should be described precisely as the sum of participant counters present at the interval end, not assumed to be every byte consumed by every participant who was active at any point in the interval.

### Logical synchronizer upgrades

The reader uses the current sequencer for readings up to the upgrade time and the successor sequencer for later readings. The successor takes over counters but not the predecessor's history. The test added to `SyncOperatorLsuIntegrationTest` checks an interval spanning an upgrade against readings from both sequencers.

### Pruning boundary

The code checks the sequencer's pruning lower bound and marks earlier intervals `CannotProvide`. The `TrafficReport.firstReadableStart` source comment explicitly warns that pruning can race the lower-bound update: the sequencer prunes the journal before moving the bound, so a request at the retention edge can still return a wrong total. This is a documented implementation caveat, not a hypothetical attack.

An earlier PR design stored completed interval totals in the sync operator database to survive sequencer pruning. During review, the implementation changed: because the dedicated synchronizer did not prune its sequencer at that point, the store, trigger and migration were removed, and the endpoint reads the sequencer on demand. This makes the current report dependent on the no-pruning/retention assumption. The report API can return `CannotProvide` for unavailable history; it cannot reconstruct missing counters.

## 5. App rewards are a separate, unfinished path

PR #100 defines `paymasterActivity`: purchased bytes multiplied by the registration's app and asset activity weights, rounded down. It computes the intended activity for the paymaster, not for each application or participant using the dedicated synchronizer.

The PR contains a TODO where the activity should be passed through CIP-0104's `ActivityRecorder` hook. The ChainSafe tracker split this into issue #163 because the hook was not yet on upstream Splice main. Upstream PR #8449, titled "Daml for ActivityRecorder", was still a draft in the snapshot.

The `ValidatorRewardCoupon` remains in place. Maintainer discussion confirms it is for validator rewards; the ActivityRecorder path is for app rewards. They are not substitutes.

The tracker also states that how the paymaster passes app rewards on to applications on its synchronizer is up to the paymaster. The public work inspected does not define a mandatory pass-through mechanism or a participant-level distribution rule.

## 6. What has been tested, and what remains unproven

### Tests described in the PRs

- Daml tests cover direct and token-standard purchases, the registered paymaster restriction, mismatched synchronizer, invalid weights, minimum top-up, archived/forged registration and traffic-record merging.
- The Scan/SV integration test registers a synchronizer, buys traffic through token-standard transfers and checks that the DSO merges the paymaster's records.
- The traffic-report PR adds tests for interval calculation, unfinished intervals, pruning, logical synchronizer upgrades, endpoint authentication and a single sync-operator integration flow.

### Evidence gaps

1. The report API PR was still open on 17 November; it had no merged implementation at the snapshot.
2. The PR #111 diff does not show the four-node acceptance test specified in tracker issue #152 (all four operator apps returning the same totals). Do not claim that cross-node equality has been demonstrated by that PR.
3. The full end-to-end test from actual dSync transactions through report, payment and app activity is separately tracked as #159 and depends on #163.
4. The report-to-burn equality is not enforced by the purchase choice.
5. The paymaster's app reward pass-through to the apps using the dSync is not specified in the inspected implementation.
6. The report's handling of participants who leave within an interval needs policy clarification.
7. The pruning-boundary race is documented in the code and requires either a mitigation or an explicit operational boundary.

## 7. Research question now supported by implementation evidence

**How should a privacy-preserving synchronizer reconcile private traffic consumption with public CC burns and reward entitlements when reporting and payment are controlled by separate parties?**

This is not a claim that the design is defective. It is a study of the properties and trade-offs of an intentionally trusted interim model.

### Quantitative variables

For interval t:

- (Q_t): actual traffic charged to participants;
- (\hat Q_t): operator-reported traffic;
- (P_t): traffic-equivalent bytes purchased by the paymaster;
- (C_t): CC burned;
- (X_t): applicable USD/CC conversion price;
- (p_t): USD list price per MB;
- (w_a,w_s): registered app and asset activity weights.

Candidate measures:

- report error: ((\hat Q_t-Q_t)/Q_t);
- payment coverage: (P_t/Q_t);
- unpaid traffic: (max(0,Q_t-P_t));
- underpayment rate: (max(0,Q_t-P_t)/Q_t);
- effective burn cost per consumed MB: (C_t X_t / (Q_t/10^6));
- app reward activity basis: (lfloor P_t w_a floor);
- asset reward activity basis: (lfloor P_t w_s floor);
- reporting delay and proportion of intervals marked `CannotProvide`.

The code-level report output is a traffic measurement. The purchased amount is a separate on-ledger purchase record. The research can reconcile them only if both records are available for the same synchronizer and time window.

## 8. Research contribution and scope

The strongest contribution is a **traffic-to-burn reconciliation framework** for privacy-preserving synchronizers. It can include:

1. a state-transition map from sequencer counters to operator reports to CC burns to rewards;
2. a formal separation of measurement correctness, payment completeness and reward attribution;
3. a reproducible model of underpayment, overpayment, report delay, unavailable history and CC price changes;
4. an audit protocol that compares operator reports with on-ledger purchases without requiring public disclosure of private transaction payloads;
5. design alternatives such as periodic reconciliation, cumulative purchase commitments, challenge windows, operator attestations and governance-triggered suspension;
6. explicit analysis of the costs and privacy consequences of each alternative.

Do not jump to zero-knowledge proofs. First determine whether the trusted operator report and public purchase records are sufficient for an independent audit, and identify exactly which information remains hidden.

## 9. Primary evidence

- CIP-0132: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- CIP-0104: https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md
- Paymaster purchase Daml PR #100: https://github.com/canton-network/splice-multi-sync/pull/100
- Scan/SV paymaster PR #104: https://github.com/canton-network/splice-multi-sync/pull/104
- Traffic report API PR #111: https://github.com/canton-network/splice-multi-sync/pull/111
- Paymaster implementation tracker #155: https://github.com/ChainSafe/canton-extending-mainnet/issues/155
- Traffic report API requirements #152: https://github.com/ChainSafe/canton-extending-mainnet/issues/152
- Paymaster activity hook follow-up #163: https://github.com/ChainSafe/canton-extending-mainnet/issues/163
- End-to-end test #159: https://github.com/ChainSafe/canton-extending-mainnet/issues/159
- Upstream ActivityRecorder draft PR #8449: https://github.com/canton-network/splice/pull/8449
