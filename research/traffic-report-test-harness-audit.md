# Traffic report test harness audit

**Date:** 17 November 2026  
**Inspected revision:** `canton-network/splice-multi-sync` PR #111 head `b6a7733d22751636820138ab705db103184e4d18`.

## Existing tests that can be reused

### 1. TrafficReportReaderTest.scala

Path:
`apps/syncoperator/src/test/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportReaderTest.scala`

This test already covers:
- completed intervals returning `Ok`;
- intervals beyond the sequencer's current sequencing point returning `Undetermined`;
- intervals below the mocked pruning lower bound returning `CannotProvide`;
- intervals spanning a logical synchronizer upgrade by reading from predecessor and successor sequencers;
- intervals becoming `CannotProvide` when the successor is current and lacks predecessor history.

Important limitation: `mockSequencer` mocks `SequencerAdminConnection`. Its pruning status and historical traffic-state reads are scripted from maps. It cannot demonstrate a database pruning race.

### 2. TrafficReportTest.scala

Path:
`apps/syncoperator/src/test/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportTest.scala`

It covers interval alignment, pagination and participant aggregation. The participant aggregation test explicitly excludes a participant present at the start but absent at the end, and counts a participant present only at the end from zero. This is relevant to the separate lifecycle-accounting question, not the pruning race.

### 3. SequencerPruningIntegrationTest.scala

Path:
`apps/app/src/test/scala/org/lfdecentralizedtrust/splice/integration/tests/SequencerPruningIntegrationTest.scala`

This is an existing real-environment integration test that configures short pruning and retention periods, pauses/resumes the pruning trigger, and checks that pruning completes even when a participant is unavailable.

Limitation: it does not issue a traffic-report request during the pruning operation and does not assert report values against an independent reference.

## Important correction to the race hypothesis

The database store's pruning algorithm deliberately retains, for each member, the latest traffic-consumption row at or before the pruning timestamp. The historical lookup selects the latest row at or before the requested timestamp.

This means the simple claim "pruning deletes the row the reader needs" is incomplete. For a requested timestamp at or after the effective pruning timestamp, the retained boundary row may still be sufficient to answer the lookup correctly.

The potentially problematic case is a stale pruning-status observation: the report reader may accept a requested timestamp based on an older lower bound while pruning has advanced far enough that the retained row is later than that requested timestamp. The exact interaction depends on when the pruning lower bound becomes visible relative to journal deletion and on the sequencer's historical-read response.

The report reader recovers only the specific `NotAtUpgradeTimeOrBeyond` status as an absent/not-yet-sequenced state. Other status runtime exceptions propagate. Therefore an unavailable historical read may fail the request rather than become an incorrect `Ok`. The end-to-end response must be observed; do not assume a missing row is converted to zero.

## Revised implementation plan

1. Keep the existing mocked reader tests as fast unit tests.
2. Add a database-store test that proves the retained boundary row answers timestamps at and above the pruning boundary, and does not fabricate an answer below it.
3. Extend or add a sequencer integration test using the existing short-retention configuration.
4. Add a test-only barrier around the boundary between pruning-status retrieval and historical traffic-state reads, or use a deterministic test hook in the real sequencer service.
5. During the barrier, advance pruning and wait until the database operation has completed.
6. Resume the report request and capture both the low-level historical-read outcome and the complete API response.
7. Compare with an independent counter reference.

## Required classifications

- Correct `Ok`: numeric report equals the independent reference.
- Explicit unavailable/error: request fails or returns a non-Ok result rather than inventing a value.
- Incorrect `Ok`: response is `Ok` but numeric value differs from the independent reference.
- Safe retry: the implementation retries and returns the correct value.

Only the third outcome demonstrates the suspected report-integrity defect in the tested revision. A propagated error would instead demonstrate an availability/robustness issue.

## Current evidence boundary

The inspected code confirms that the report reader checks pruning status separately from subsequent historical reads, and that the database store prunes journal rows in batches while preserving a per-member boundary row. Existing tests do not cover their concurrent interaction.

No deterministic database concurrency test has been implemented or run here. No incorrect `Ok` response, production incident, underpayment or financial loss has been demonstrated.
