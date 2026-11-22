# Traffic report reader: consistency and retention semantics

**Audit date:** 17 November 2026  
**Source snapshot:** `canton-network/splice-multi-sync` PR #111, head `b6a7733d22751636820138ab705db103184e4d18`.  
**Status:** source-level analysis of an open pull request, not evidence of production deployment.

## 1. What the reader actually does

For each requested interval, the reader needs two cumulative traffic-counter snapshots:
- one at the interval start;
- one at the interval end.

It subtracts the start counters from the end counters and sums participant values. The default interval is ten minutes. Requests are aligned to interval boundaries and paginated at 100 intervals.

The report is calculated on demand from sequencer state. In the PR review thread, the author removed the proposed database store and periodic trigger because the dedicated synchronizer sequencer was not being pruned at that time. Therefore the API does not create a durable independent archive of historical reports.

## 2. Three statuses, in plain language

- `Ok`: both readings were available and the interval had completed.
- `Undetermined`: the sequencer had not yet sequenced past the interval end.
- `CannotProvide`: the required historical counter state was considered unavailable, including pruning and some logical synchronizer upgrade cases.

These statuses are materially different. A consumer must not coerce either non-Ok status to zero traffic or silently omit it from a settlement window.

## 3. A source-documented time-of-check/time-of-use race

The reader first calls `getSequencerPruningStatus()`, calculates the first interval it considers readable, and then performs separate historical counter reads.

The source comment in `TrafficReport.firstReadableStart` explicitly says the sequencer prunes the journal before moving its pruning lower bound. It warns that a request at the retention boundary can race a prune and report a wrong total.

This creates a candidate time-of-check/time-of-use condition, but it is not enough to conclude that a wrong report can occur. A separate test-harness audit inspected the pruning implementation and found that it retains, for each member, the latest traffic-consumption row at or before the pruning timestamp. For timestamps at or after the effective pruning boundary, that retained row may be sufficient to answer the historical lookup correctly.

The potentially problematic case is narrower: the report reader observes a stale pruning lower bound, pruning advances between that check and the counter read, and the historical read then resolves to a retained row later than the requested timestamp or otherwise returns an invalid result. Whether this produces an incorrect `Ok`, a propagated error, or an explicit unavailable status depends on the exact sequencing and store semantics. The reader recovers only the specific not-yet-sequenced status; other status runtime exceptions propagate.

No deterministic concurrency test has been implemented or run here. No incorrect `Ok` response, production incident, underpayment or financial loss has been demonstrated. Treat this as an unresolved implementation hypothesis, not a confirmed defect.

## 4. Logical synchronizer upgrade handling

The reader determines the upgrade times from synchronizer upgrade announcements. It uses the current sequencer for readings up to the upgrade time and the successor for later readings.

The successor inherits current counters but not historical counter history. It therefore reports zero for members before its own start. Reading an interval that spans an upgrade requires the start snapshot from the predecessor and the end snapshot from the successor.

The PR adds a test that queries across an upgrade and compares the interval results with direct reads from both sequencers. Once the predecessor's required history is no longer available, some spanning intervals can become `CannotProvide`.

This is a different failure mode from the pruning-boundary hypothesis. Upgrade handling is explicitly implemented and tested in the PR; the stale-pruning-status case still needs a deterministic concurrency test or a stronger read guarantee.

## 5. What an `Ok` report does and does not mean

An `Ok` status means the reader produced a value from the two counter snapshots it obtained. It does not mean:
- the report is digitally signed by the operator;
- the report is independently archived;
- a third party can verify the source counters;
- the traffic meter has been independently proven complete;
- the report has been reconciled against the off-ledger agreement;
- the amount has been burned or rewards correctly attributed.

The JWT protects access to the API. It authenticates the caller, not the truth or provenance of a particular report response.

The API is defined in `sync-operator-internal.yaml`, not a public third-party API specification in this patch.

## 6. Researchable mitigations

These are candidate design responses, not existing features:
1. **Retention safety margin:** refuse to report intervals too close to the pruning boundary. Simple, but sacrifices availability and does not eliminate every race unless the margin is tied to a hard bound.
2. **Atomic or snapshot-consistent reads:** obtain the pruning boundary and all required counter states under a consistent sequencer snapshot, if the underlying API can support it.
3. **Prune-aware failure handling:** if a read detects that the requested state was pruned or invalidated, return an explicit unavailable status rather than a numeric result.
4. **Durable interval snapshots:** persist completed reports before the source journal can be pruned, with idempotent writes and explicit provenance. This was removed from the current PR patch, not implemented there.
5. **Independent boundary validation:** compare adjacent interval totals or re-read boundary snapshots where feasible. This can detect some discontinuities but cannot, by itself, prove source completeness.

The most useful next test is a controlled concurrency test: advance pruning between the pruning-status check and the historical counter reads, then determine whether the API returns a wrong `Ok` value, a clear unavailable status, or a surfaced error.

## 7. Evidence and limits

Primary source:
- [TrafficReport.scala at PR #111 head](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReport.scala)
- [TrafficReportReader.scala at PR #111 head](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportReader.scala)
- [PR #111 and review discussion](https://github.com/canton-network/splice-multi-sync/pull/111)

The inspected PR was open on the audit date. This document does not claim that the code was merged, deployed, or that the race has occurred in production.
