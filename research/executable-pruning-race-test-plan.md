# Executable test implementation plan: reuse the existing traffic-report test path

**Audit date:** 17 November 2026  
**Inspected source:** `canton-network/splice-multi-sync` PR #111, head `b6a7733d22751636820138ab705db103184e4d18`.

## 1. Existing test infrastructure

The PR already contains:
- `apps/syncoperator/src/test/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportReaderTest.scala`
- `apps/syncoperator/src/test/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportTest.scala`
- `apps/app/src/test/scala/org/lfdecentralizedtrust/splice/integration/tests/SequencerPruningIntegrationTest.scala`

The reader unit test mocks `SequencerAdminConnection`. Its helper `mockSequencer` returns a `Map[Member, TrafficState]` for exact timestamps and fails with `NotAtUpgradeTimeOrBeyond` when a timestamp is absent. The reader maps that specific failure to `None`, which causes the current interval and subsequent intervals to be reported as `Undetermined`.

The integration test already configures frequent sequencer pruning (2-second interval, 180-second retention) and observes completed pruning. It is an SV-level integration test, not a traffic-report race test. It does not currently pause the report reader between its pruning-status check and historical reads.

## 2. Important refinement to the test design

The initial specification proposed forcing pruning between the status check and the historical reads. That is still the correct concurrency schedule, but the expected result must be derived from actual store/API semantics.

The DB store's pruning algorithm keeps, per member, the latest journal row at or before the pruning timestamp and deletes older rows. A lookup at an earlier timestamp after pruning may therefore return no row for that member: the retained row is later than the requested timestamp and fails the query predicate.

The report reader's aggregation is asymmetric:
- members present at the end but absent at the start are counted from zero;
- members present at the start but absent at the end are not counted.

Consequently, if a pruning race removes a member's start snapshot while the end snapshot remains available, the reader could count that member's cumulative end value from zero and still construct an `Ok` interval. This is the concrete incorrect-success path the test must investigate. It is not yet demonstrated through the full sequencer API.

There is a second possible outcome: the sequencer RPC may translate a missing state into `NotAtUpgradeTimeOrBeyond`, which the reader maps to `Undetermined`. The test must discover which behaviour the real service produces; it must not hard-code either result.

## 3. Lowest-cost implementation sequence

### Step A — extend the existing reader unit test first

In `TrafficReportReaderTest.scala`, add a controllable mock with promises/barriers:
1. Return an old pruning lower bound from `getSequencerPruningStatus`.
2. Pause the first `getLsuTrafficControlState(start)` call.
3. Simulate the post-prune result for that timestamp, specifically testing both:
   - an empty/missing member state returned successfully;
   - a failed RPC with `NotAtUpgradeTimeOrBeyond`.
4. Return the end snapshot containing the member's cumulative counter.
5. Assert the exact status and traffic amount.

For example, use cumulative counter 100 at the requested start and 150 at the end. The independent expected interval amount is 50. If the start member is omitted but the end member remains, the current aggregation logic may report 150 as `Ok`. If the RPC fails with the recognised error, the interval should be `Undetermined`.

This unit test verifies reader behaviour for the two possible RPC contracts. It does not prove the DB race.

### Step B — add a DB-store concurrency test

Use the existing Canton database-backed sequencer test fixture. Insert at least two cumulative journal entries for one member and one stable member. Pause after the pruning-status read, run the real `pruneBelowExclusive` to completion, then execute the real `lookupLatestBeforeInclusive` at the earlier report boundary.

Assert whether the member is absent from the start snapshot and whether it is present at the end snapshot. Verify both PostgreSQL and H2 if the fixture supports them; the SQL query paths differ.

### Step C — connect the real report endpoint

Only after A and B establish the component behaviours, run the actual traffic-report reader with the real sequencer admin RPC and DB store. Capture the full response. This is the evidence required to classify the issue as incorrect `Ok`, explicit `Undetermined`/error, or safe retry.

## 4. Why not start with the full SV integration test?

The existing `SequencerPruningIntegrationTest` is expensive and orchestrates a multi-SV environment. It is useful for final end-to-end validation, but poor as the first debugging tool. Unit and store-level tests isolate the semantics and make the race deterministic. The SV test should be the final confirmation, not the first step.

## 5. Acceptance criteria

- The test uses barriers/promises, never arbitrary sleeps to establish the race ordering.
- The expected total is captured independently of the reader.
- Missing start member and missing RPC state are tested separately.
- The test records exact pruning bound, journal rows before/after pruning, start/end maps, API status and reported value.
- No claim of a production vulnerability is made unless the real report path returns an incorrect `Ok` under a supported configuration.
- A safe `Undetermined` response is recorded as an availability/retention limitation, not a payment-integrity defect.

## 6. Direct source references

- [TrafficReportReaderTest.scala](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/test/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportReaderTest.scala)
- [TrafficReportReader.scala](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportReader.scala)
- [TrafficReportTest.scala](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/test/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportTest.scala)
- [SequencerPruningIntegrationTest.scala](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/app/src/test/scala/org/lfdecentralizedtrust/splice/integration/tests/SequencerPruningIntegrationTest.scala)
- [DbTrafficConsumedStore.scala](https://github.com/digital-asset/canton/blob/main/community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/store/db/DbTrafficConsumedStore.scala)
- [TrafficConsumedStore.scala](https://github.com/digital-asset/canton/blob/main/community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencing/traffic/store/TrafficConsumedStore.scala)

No upstream code has been changed or test executed in this research step. This is an implementation plan grounded in the actual existing test structure.
