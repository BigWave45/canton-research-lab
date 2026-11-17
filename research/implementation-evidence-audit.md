# Implementation evidence audit: dedicated synchronizer paymaster chain

**Audit date:** 17 November 2026  
**Status:** public source-code and issue-tracker review. This is not a deployment audit and does not establish live-network behaviour.

## 1. Finding

The implementation is not yet an end-to-end verified accounting system. The public code contains meaningful components:
- traffic reporting is under active development in open PR #111;
- a registered paymaster can buy traffic and burn CC;
- Scan and SV components can process the registration and resulting traffic contracts.

But the connection from measured traffic to a correctly sized payment and then to reward attribution is not yet complete in the inspected work. The full end-to-end test remains open, and the ActivityRecorder integration is still a draft/open dependency.

## 2. Status by component

| Component | Evidence | Status on 17 Nov 2026 | What it establishes | What it does not establish |
|---|---|---|---|---|
| Traffic interval calculation | PR #111, TrafficReport.scala, TrafficReportReader.scala | PR open | Computes participant traffic deltas across ten-minute intervals from sequencer cumulative counters; its integration tests cover a completed interval and an interval spanning an LSU | Does not independently establish that the source meter captured every chargeable event or satisfy the four-node equality acceptance criterion in tracker #152 |
| Traffic report API | PR #111, sync-operator-internal.yaml, HttpSyncOperatorHandler.scala | PR open | Authenticated endpoint, aligned time ranges, pagination and explicit interval statuses | Does not provide a public API or signed report for third-party verification |
| Historical report retention | PR #111 review thread and TrafficReportReader.scala | No report database/trigger in current patch | The author states on 17 Nov that no dSync sequencer pruning exists today, so the store/trigger/migration were dropped and the handler reads the sequencer per request | If pruning is introduced, historical intervals may become CannotProvide; this is an operational dependency, not durable archival |
| Logical synchronizer upgrade | PR #111, TrafficReportReader.scala, SyncOperatorLsuIntegrationTest.scala | Test added in open PR | Reads pre-upgrade and post-upgrade counter states from predecessor and successor sequencers | An interval spanning an upgrade may be unavailable if it was not read before predecessor history is lost |
| Paymaster purchase | PR #100 | Merged 11 Nov 2026 | Registered paymaster can burn CC for its synchronizer, with payer, synchronizer, migration and weight checks | Does not automatically check purchase amount against reported usage |
| Scan/SV registration handling | PR #104 | Merged 12 Nov 2026 | Scan can find registrations for token-standard transfers; SV can ingest and merge paymaster traffic contracts | Does not complete traffic-to-burn reconciliation |
| Paymaster reward activity | PR #8449 and tracker #163 | PR #8449 draft/open; #163 open | Proposed ActivityRecorder hook and migration contract exist in draft; purchase-side activity calculation exists | Inspected merged purchase path does not yet record activity through the hook |
| Full end-to-end flow | Tracker #159 | Open | Defines test: register, transact, report, pay, verify activity records | No passing end-to-end evidence in inspected tracker state |

## 3. How traffic reporting works

The proposed endpoint returns one record per aligned interval. The default interval is ten minutes. Each interval has one of three statuses:
- Ok: the interval is complete and the traffic value is final.
- Undetermined: the interval has not ended, or the sequencer has not sequenced beyond its end.
- CannotProvide: the required counter history is no longer available, including certain logical synchronizer upgrade cases.

The implementation reads cumulative sequencer traffic counters at the start and end of an interval, subtracts the start value from the end value, and sums participant counters.

The PR #111 diff includes a single-operator integration test for a completed interval and a logical-synchronizer-upgrade test that reads an interval spanning predecessor and successor sequencers. This is test coverage in an open PR, not a merged or deployed test result. Tracker #152 additionally asks for all four operator apps on a four-node synchronizer to return identical totals; that acceptance criterion is not established by the PR's visible test additions.

The code includes lifecycle behaviour:
- a participant present at the end but absent at the start counts from zero;
- a participant present at the start but absent at the end is not counted.

The test explicitly encodes the second rule as a participant who left during the interval and is not counted. The implementation's `participantsConsumed` function iterates over members present at the end reading; a participant present only at the start contributes no delta. This is a concrete metering-boundary question: does a participant that leaves partway through an interval owe for traffic consumed before departure, and if so, where is that usage retained and included? The current test proves the implementation's chosen behaviour, not that the billing policy is economically correct or consistent with every operator/paymaster agreement.

### Pruning-boundary race noted in the implementation

The PR #111 `TrafficReport.firstReadableStart` source comment states that the sequencer prunes its journal before moving the pruning lower bound, and that a request at the edge of the retention period can race a prune and report a wrong total. The reader obtains pruning status and then performs counter reads, so the source itself identifies a possible time-of-check/time-of-use boundary condition. The reviewed tests cover alignment, paging, participant joins/leaves and LSU reads; they do not demonstrate a test for this concurrent pruning race.

This is a source-level risk observation, not evidence that a wrong report has occurred in production. It should be treated as an unresolved implementation assurance question: can the report reader distinguish a complete interval from a counter snapshot affected by concurrent pruning, and what retry/locking/version mechanism, if any, prevents an incorrect `Ok` result?

## 4. Report storage was removed from the current PR

Tracker issue #152 originally required durable totals in the sync operator app database across sequencer pruning and logical synchronizer upgrades. PR #103 implemented a storage/trigger approach but was closed unmerged and explicitly superseded by PR #111.

In PR #111's 17 November review thread, the author explains that no dedicated-synchronizer sequencer pruning exists at present, so the store, trigger and migration were dropped; the handler reads the sequencer on each request. This is an explicit operational assumption, not durable archival.

The distinction matters:
- while sequencer counter history remains available, on-demand reads may suffice;
- if pruning is introduced, old intervals may become CannotProvide;
- during an LSU, the PR adds a test querying an interval across predecessor and successor sequencers;
- tracker #152 remains open, and the public evidence reviewed here does not establish that its four-node equality acceptance criterion has passed.

The research must not state that reports are durably archived. The current PR patch does not implement that.

## 5. API authentication is not report attestation

PR #111 adds JWT-based authentication to the sync operator API. This answers: “Is the caller authorised to request this report?”

It does not answer:
- Can a third party verify that this exact report was signed by the operator?
- Can the paymaster prove which report version it used?
- Can an auditor independently establish report completeness?
- Can the public verify that the report was not changed after delivery?

The API specification is named sync-operator-internal.yaml. The PR discussion itself asks whether it should be external because paymasters need to build automation against it.

No report-level digital signature or public report commitment is established by the inspected PR.

## 6. What the merged payment change does

PR #100 adds direct and token-standard purchase paths for a registered dedicated synchronizer. The purchase checks include:
- payer is the registered paymaster;
- purchased synchronizer matches the registration;
- synchronizer is not a required/global synchronizer;
- migration ID is zero;
- member ID is empty for a paymaster-level purchase;
- app and asset activity weights are within the registration's maximum.

PR #104 adds Scan and SV handling needed for registrations and paymaster traffic contracts.

These changes establish that the registered paymaster can make a valid purchase and that the resulting contract can be processed by the relevant Splice applications.

They do not establish that the amount burned equals the amount owed under the operator/paymaster agreement. Tracker issue #155 explicitly identifies that no check compares the paid amount with the traffic report and that a paymaster may pay less than usage. This is a documented design/implementation gap, not evidence that a real paymaster has underpaid.

## 7. Reward attribution remains incomplete

PR #100 calculates potential app and asset activity from purchased bytes multiplied by configured weights. Its description says recording the activity through the hook is a follow-up.

The proposed ActivityRecorder contract appears in upstream PR #8449, which remained draft/open in the inspected state. Tracker issue #163 describes the work to connect paymaster purchases to this hook and test resulting activity records.

The full flow test in issue #159 remains open and depends on the report API, purchase/reward work and related tasks.

Do not write that the complete paymaster traffic-to-reward pipeline is implemented or end-to-end tested.

## 8. Evidence classification

**Verified in reviewed source / merged changes**
- Daml purchase constraints and registered-paymaster purchase paths in merged PR #100.
- Scan/SV registration and contract handling in merged PR #104.
- Proposed traffic report calculation, status model, JWT-protected handler and single-operator/LSU tests in open PR #111. These remain proposed until merged and deployed.
- Source-level edge cases in the same PR: participants present at interval start but absent at interval end are excluded from the computed interval delta; the source comment also acknowledges a possible race between pruning and reading the pruning lower bound. Neither is evidence of actual production misbilling, but both require explicit treatment in the accounting assurance analysis.
- Specific participant join/leave calculation behaviour in TrafficReport.scala and its tests.

**Open or draft**
- Traffic report API PR #111.
- ActivityRecorder integration PR #8449.
- Tracker issues #152, #159 and #163.

**Not established by inspected evidence**
- Durable historical report retention.
- Signed operator report or public report commitment.
- Automated reconciliation of burn against contractual liability.
- End-to-end reward attribution from actual dedicated synchronizer traffic.
- Four-operator equality acceptance across all synchronizer operator apps.
- Production deployment of the complete flow.

## 9. Research implications

The proposed auditor-and-commitment architecture should be split into two requirements.

**Immediate, lower-complexity requirement**
- Make the traffic report contractually available to the paymaster and authorised auditor.
- Specify interval coverage, CannotProvide handling, participant lifecycle treatment and retention period.
- Preserve the exact report version and agreement version used for each payment.
- Reconcile due amounts against burn events over the contractual settlement window.
- Define a dispute and correction path for missing or contested intervals.

**Additional assurance, only after the basics exist**
- Add an operator signature or another source-authentication mechanism over canonical report content.
- Add a manifest commitment if parties need tamper-evidence after report delivery.
- Consider public proofs only if there is a specific public verification claim that the auditor model cannot satisfy.

A hash or proof cannot repair missing source data. If an interval is CannotProvide, cryptographic processing of an empty or reconstructed report does not recreate the missing measurement.

## 10. Primary evidence

- PR #100, paymaster traffic purchase: https://github.com/canton-network/splice-multi-sync/pull/100
- PR #104, Scan and SV handling: https://github.com/canton-network/splice-multi-sync/pull/104
- PR #111, traffic report API: https://github.com/canton-network/splice-multi-sync/pull/111
- TrafficReport.scala: https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReport.scala
- TrafficReportReader.scala: https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportReader.scala
- API specification: https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/openapi/sync-operator-internal.yaml
- Tracker #152, traffic report API: https://github.com/ChainSafe/canton-extending-mainnet/issues/152
- Tracker #155, payment/report comparison gap: https://github.com/ChainSafe/canton-extending-mainnet/issues/155
- Tracker #159, end-to-end paymaster test: https://github.com/ChainSafe/canton-extending-mainnet/issues/159
- Tracker #163, ActivityRecorder integration: https://github.com/ChainSafe/canton-extending-mainnet/issues/163
- Upstream PR #8449, ActivityRecorder: https://github.com/canton-network/splice/pull/8449
