# Underlying sequencer semantics: traffic journal pruning race

**Audit date:** 17 November 2026  
**Repositories inspected:** `digital-asset/canton` main source and `canton-network/splice-multi-sync` PR #111 head.  
**Evidence class:** direct source-code inspection. No production incident or end-to-end reproduction is claimed.

## 1. The data structure

Canton's `DbTrafficConsumedStore` stores each traffic-consumption update as a new row in `seq_traffic_control_consumed_journal`. The store exposes `lookupLatestBeforeInclusive(timestamp)`, which returns each member's latest journal row at or before the requested timestamp.

Relevant source:
- `community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizing/traffic/store/db/DbTrafficConsumedStore.scala` (actual path: `community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizing/traffic/store/db/DbTrafficConsumedStore.scala`)
- Interface: `community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizing/traffic/store/TrafficConsumedStore.scala`

## 2. What pruning preserves

`DbTrafficConsumedStore.pruneBelowExclusive(upToExclusive)`:
1. Queries the latest journal timestamp at or before the pruning timestamp for each member.
2. Deletes rows for each member with timestamps strictly earlier than that member's selected row.
3. Performs the deletes in parallelised batches with `transactional = false`.

The selected row is deliberately retained because it is the last counter value needed to answer lookups at timestamps at or after the pruning boundary. The interface documentation states the same retention rule.

The sequencer's broader pruning path also uses batched, non-transactional deletes. The traffic-store implementation is therefore not one atomic operation covering every member's journal rows.

## 3. Why the report-reader race is plausible

The PR #111 report reader performs these operations separately:
1. Calls `getSequencerPruningStatus()` and reads the current lower bound.
2. Calculates which requested intervals are still readable.
3. Makes separate historical traffic-state reads for interval boundaries.

The report reader's own source comment warns that the journal is pruned before the lower bound is moved and that a request at the retention edge can race pruning and report a wrong total.

The underlying store semantics explain the mechanism:

- Let a requested boundary be (t).
- At the initial status check, the reported pruning lower bound is (L_0), and (t) is considered readable.
- Pruning begins for a newer boundary (L_1), where (L_1 > t).
- For a member, suppose the last journal row at or before (t) is at time (r), and the last row at or before (L_1) is at time (s), with (r < t < s leq L_1).
- Pruning retains (s) and deletes rows strictly before (s), including (r).
- A subsequent `lookupLatestBeforeInclusive(t)` cannot return (s), because (s > t), and can no longer return (r), because it was deleted.

That member's historical state at (t) is therefore no longer available from the journal. Depending on the caller's handling of an absent member row, this can become a missing state or an incorrect aggregate rather than a clean failure.

The exact report API result under this interleaving has not yet been established. In particular, we have not demonstrated that the full API returns `Ok` with an incorrect number. That needs an integration test using the actual sequencer and report reader.

## 4. Why the pruning boundary update order matters

The source comment in `TrafficReport.scala` explicitly states that Canton prunes the journal before moving the pruning lower bound. This ordering creates a period in which:
- the status endpoint can still expose the old lower bound;
- some rows required for timestamps beyond the old bound may already have been deleted.

This is a classic time-of-check/time-of-use consistency problem. It is not enough for the pruning status to be accurate when read; the status and subsequent historical lookups need a shared consistency guarantee or a safe retention margin.

## 5. What existing tests do and do not establish

The Canton `DbTrafficConsumedStoreTest` exercises the traffic store's ordinary interface and pruning behaviour. The sequencer pruning integration tests exercise sequencer pruning and acknowledgement safety.

The inspected tests do not establish this exact interleaving across:
- the sync-operator status check;
- concurrent sequencer journal pruning;
- historical reads for both boundaries of a traffic-report interval;
- the final `Ok` / `CannotProvide` status returned by the report API.

The PR #111 tests cover interval calculation and logical synchronizer upgrade behaviour, but the reviewed evidence does not show a controlled concurrent-pruning test for the report endpoint.

## 6. Required integration test

A targeted test should use the actual sequencer database and report reader:

1. Create at least one member with multiple traffic-consumption journal entries.
2. Choose a report boundary (t) and ensure the latest row at or before (t) is distinct from the latest row at or before a later pruning timestamp (L_1).
3. Pause the report request immediately after it reads pruning status, while the lower bound still reflects (L_0 < t).
4. Advance pruning to (L_1 > t), and wait for the relevant journal deletion to complete.
5. Resume the report request and allow it to query the historical state at (t).
6. Inspect whether the API returns:
   - the correct value;
   - an explicit unavailable/error response; or
   - `Ok` with a value inconsistent with the pre-pruning reference calculation.
7. Repeat with multiple members and batched deletes to test partial progress, not only the fully-pruned endpoint state.

The test should use deterministic barriers/hooks rather than sleeps. It should assert both the interval status and the numerical result.

## 7. Candidate engineering guarantees

A safe implementation needs at least one of:
- a consistent snapshot spanning pruning-status and historical-state reads;
- a retention rule that prevents deletion of any row needed by in-flight report requests;
- a durable report snapshot created before the underlying journal can be pruned;
- explicit detection of missing boundary states, returning unavailable rather than calculating a number.

A simple time buffer is only sufficient if its bound is derived from maximum request duration, pruning cadence, and storage semantics. An arbitrary margin is not a correctness proof.

## 8. Scope and claims

Established from source:
- traffic consumption is journalled;
- historical lookup is latest-row-at-or-before-timestamp;
- pruning retains the latest row at/before its pruning timestamp and deletes earlier rows;
- those deletes are batched and non-transactional;
- PR #111 reads pruning status separately from historical traffic state;
- PR #111 source explicitly warns of the race and possible wrong totals.

Not established:
- a production misreport;
- an observed financial loss;
- that the current full API necessarily returns `Ok` for the missing-state interleaving;
- that the race is reachable under every deployment's pruning schedule;
- that the relevant PR has been deployed.

## 9. Primary source links

- [DbTrafficConsumedStore.scala](https://github.com/digital-asset/canton/blob/main/community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizing/traffic/store/db/DbTrafficConsumedStore.scala)
- [TrafficConsumedStore.scala](https://github.com/digital-asset/canton/blob/main/community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizing/traffic/store/TrafficConsumedStore.scala)
- [DbSequencerStorePruning.scala](https://github.com/digital-asset/canton/blob/main/community/synchronizer/src/main/scala/com/digitalasset/canton/synchronizer/sequencer/store/DbSequencerStorePruning.scala)
- [TrafficReport.scala at PR #111 head](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReport.scala)
- [TrafficReportReader.scala at PR #111 head](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportReader.scala)
- [PR #111](https://github.com/canton-network/splice-multi-sync/pull/111)
