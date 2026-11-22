# Traffic-report implementation audit: interval and participant semantics

**Snapshot date:** 17 November 2026  
**Primary source:** canton-network/splice-multi-sync#111, open pull request at the snapshot.  
**Related source:** canton-network/splice#8449, draft pull request at the snapshot.

This is a source-code audit of proposed implementation work. The pull requests were not merged at the inspected snapshot. Findings below must not be represented as deployed MainNet behaviour.

## 1. Report API contract

PR #111 adds an authenticated sync-operator endpoint, GET /v0/traffic-report, with aligned start/end record-time bounds.

The OpenAPI contract states:
- Reports cover intervals of the synchronizer operated by that sync-operator app.
- Default interval length is ten minutes, aligned to UTC multiples since Unix epoch.
- Responses contain at most 100 intervals and provide a continuation start time when more remain.
- Each interval has start time, end time and one of three statuses.
- Ok means the interval is over and traffic_consumed is final.
- Undetermined means the interval is not over or the sequencer has not sequenced past its end.
- CannotProvide means the sequencer cannot provide the interval because it was pruned or predates the current sequencer upgrade.
- traffic_consumed is an aggregate byte count and is only set for Ok intervals.
- The endpoint is JWT-authenticated. The PR adds authentication configuration and an integration test rejecting missing or wrong-audience tokens.

The response schema does not expose participant-level rows. It returns an aggregate total for each interval.

## 2. How the aggregate is calculated

The PR's TrafficReportReader reads cumulative traffic-control state at both ends of an interval. Its comments state that the dedicated-synchronizer base rate is kept at zero, so extra traffic is the charged traffic and the difference between counter readings is the interval amount.

The TrafficReport.participantsConsumed implementation iterates participants present in the end-of-interval state map. It subtracts their start counter, defaulting to zero for participants who joined during the interval.

The same implementation explicitly excludes participants who have no end-of-interval reading because they left during the interval. The unit test makes this explicit: a participant with 500 bytes at the start but absent at the end is not counted; a participant who joined during the interval is counted from zero. The test's total is 37 bytes.

This is a concrete implementation semantic in PR #111, not a synthetic assumption. Whether it is an accounting defect depends on the intended charging rule for participants that leave mid-interval. The CIP/report contract needs to specify whether their pre-departure consumption remains chargeable and, if so, how it is carried into the aggregate.

## 3. Upgrade and pruning boundaries

The PR handles logical synchronizer upgrades by reading pre-upgrade state from the current sequencer and post-upgrade state from the successor. The successor inherits counters but not historical journal state, so the reader chooses the sequencer based on the upgrade time.

If the interval spanning an upgrade was not persisted before the old sequencer's history became unavailable, the report can return CannotProvide. The PR includes an LSU integration test for a report interval spanning the upgrade.

The source comment warns that a request at the retention boundary can race pruning and report a wrong total. However, the separate test-harness audit found that the database retains the latest traffic-consumption row at or before the pruning timestamp, which may preserve correct lookups at or after the effective boundary. The remaining hypothesis is a stale pruning-status observation combined with pruning advancing before the historical read. The possible outcomes include a correct value, an explicit error/unavailable response, a retry or an incorrect `Ok`; no incorrect `Ok` has been demonstrated.

These are evidence-availability and boundary semantics. They should be represented explicitly in any accounting protocol and experiment, not converted into zero traffic.

## 4. What this source does not establish

- It does not expose participant-level report rows to the paymaster through this API.
- It does not establish independent completeness of the participants included in the aggregate.
- It does not itself reconcile report totals with CC burns.
- It does not establish that an off-ledger agreement was applied correctly.
- It does not prove that the aggregate report equals every economically chargeable byte under every participant join/leave lifecycle.
- It does not prove production deployment. PR #111 was open at the snapshot.

## 5. Reward path status

The inspected ActivityRecorder PR #8449 is draft at the snapshot. It adds a DSO-controlled activity-recording choice and contract-state migration to create the ActivityRecorder. The PR's Daml changes describe recording app and asset activity in bytes, but the PR being draft means the full integrated reward path cannot be treated as merged or deployed based on this evidence.

The tracker issue #155, closed on 12 November, describes the registered paymaster purchase path and explicitly states that nothing checks the paid amount against the traffic report; the paymaster may pay less than usage. It describes SV archiving of a misbehaving registration as governance enforcement. This is a documented design/control limitation in the issue's acceptance context, not evidence that a paymaster has underpaid in production.

## 6. Research consequences

1. The report is an aggregate byte total, not an externally auditable participant ledger.
2. Participant departure semantics are a concrete question: the current PR implementation excludes a participant absent from the end-state map, even if present at interval start.
3. A complete report window can still be incomplete relative to the intended economic population if lifecycle semantics omit chargeable activity.
4. The report-to-burn reconciliation model needs an explicit population/completeness parameter. A window may be technically Ok while the economic measurement population is incomplete under the chosen charging policy.
5. A future mechanism should specify how departure events are accounted for without disclosing private transaction payloads. Options to compare include carry-forward counters, signed departure snapshots, lifecycle-boundary settlement, and an explicitly accepted exclusion rule. No option is selected yet.

## Source references

- Traffic-report PR #111: https://github.com/canton-network/splice-multi-sync/pull/111
- ActivityRecorder PR #8449: https://github.com/canton-network/splice/pull/8449
- Paymaster purchase tracker issue #155: https://github.com/ChainSafe/canton-extending-mainnet/issues/155
- CIP-0132: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- CIP-0104: https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md
