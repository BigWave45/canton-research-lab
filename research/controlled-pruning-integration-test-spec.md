# Controlled integration-test specification: pruning versus traffic-report reads

**Date:** 17 November 2026  
**Purpose:** Determine whether the PR #111 traffic-report reader can return a numerically incorrect `Ok` result when pruning advances between its pruning-status check and historical counter reads.

## 1. Question and hypothesis

Question: if a report request passes the initial retention check, but the required per-member historical counter row is pruned before the reader queries it, what does the complete report API return?

H0 (safe handling): the reader returns the correct total, retries against a consistent snapshot, or returns an explicit non-Ok/error result.

H1 (incorrect success): the reader returns a numeric total that differs from an independently captured reference total while marking the interval `Ok`.

The test must be able to falsify H1. It must not assume that a missing row is automatically converted into zero; inspect the actual aggregation and status mapping.

## 2. Relevant implementation path

The test should exercise the real implementation, not only the Python model:

1. PR #111 traffic-report endpoint and reader in `canton-network/splice-multi-sync`.
2. Sequencer pruning status retrieval.
3. `TrafficConsumedStore.lookupLatestBeforeInclusive(timestamp)`.
4. `DbTrafficConsumedStore.pruneBelowExclusive(upToExclusive)`.
5. The final report response and its status.

The database store is a per-member journal. Historical lookup selects the latest stored row at or before the requested timestamp. Pruning first selects each member's latest row at or before the pruning timestamp, then deletes older rows in batched, non-transactional operations.

## 3. Deterministic test fixture

Use a database-backed sequencer test fixture. Do not rely on sleeps or wall-clock timing.

Create one member with at least three traffic-consumption journal entries:
- row A at timestamp t0, cumulative counter 100;
- row B at timestamp t1, cumulative counter 150;
- row C at timestamp t2, cumulative counter 190.

Choose report boundaries so the requested start snapshot is at t1 and the end snapshot is at t2. The independently calculated expected interval delta is 40.

The fixture must also include a second member with stable counters, so aggregation across members is exercised and one missing historical row cannot be hidden by an empty overall result.

Capture the expected per-member snapshots and expected aggregate before starting the race. This reference must not be read from the report reader under test.

## 4. Required synchronization barriers

Add test-only hooks or injectable collaborators at these exact boundaries:

- **B1:** immediately after the report reader obtains and evaluates the pruning status/lower bound;
- **B2:** immediately before the historical counter lookup for the requested start boundary;
- **B3:** after pruning has completed its database deletion and before the report reader continues.

Test sequence:
1. Start the report request and block it at B1 or B2 after the old pruning boundary has been observed.
2. Advance pruning beyond t1.
3. Await completion of the actual pruning operation, including its batched deletes.
4. Release the report request to perform its historical lookup.
5. Await the complete API response.

The barriers must establish ordering directly. Do not use arbitrary delays as evidence that pruning happened first.

If production classes cannot be instrumented without invasive changes, introduce the narrowest package-private test seam around the status provider and historical-read call. Document that the seam exists only for deterministic testing.

## 5. Assertions and outcome classification

For each run, record:
- requested interval;
- pruning lower bound observed at B1;
- pruning timestamp and completion at B3;
- rows present before and after pruning;
- actual historical lookup result for each member;
- expected aggregate from the independent fixture;
- API numeric value, status and error.

Classify the outcome:

| Outcome | Required assertion | Interpretation |
|---|---|---|
| Correct `Ok` | value equals independent reference | Correct result despite interleaving |
| Explicit unavailable | status is non-Ok or documented error | Safe refusal; availability loss |
| Retry to correct result | final value equals reference and retry is observable | Safe recovery |
| Incorrect `Ok` | status is `Ok` and value differs from reference | Confirmed correctness defect in tested configuration |

The test must fail if the API returns `Ok` with a value other than the independently calculated expected aggregate.

Do not assert that `CannotProvide` is the only safe response unless the API contract explicitly requires that status for this case. An explicit error or safe retry may also satisfy H0.

## 6. Control runs

Run at least these controls:

A. No pruning during the request: report must equal the independent reference.

B. Pruning completes before the request starts: the reader should reject an interval outside its retention guarantee, or otherwise follow the documented API contract. It must not return a fabricated zero.

C. Pruning starts after all historical reads complete: report must equal the reference.

D. Race interleaving described above: classify the actual response.

E. Repeat with multiple members and with a requested interval exactly at, immediately before, and immediately after the retention boundary.

F. Repeat against each supported storage backend if the report feature supports them. A database-only result must be labelled as such.

## 7. Additional correctness checks

- Verify whether the pruning status lower bound is inclusive or exclusive and align test timestamps accordingly.
- Verify that pruning completion means all batched deletes have completed, not merely that pruning was scheduled.
- Check whether the traffic-report reader performs one historical read per member or a single aggregate query.
- Check whether a missing start snapshot is omitted, treated as zero, or mapped to an error.
- Check whether the end snapshot can be read from a different sequencer generation after a logical synchronizer upgrade.
- Preserve the raw response and relevant logs as test artifacts.
- Ensure the test is deterministic across repeated runs.

## 8. Interpretation boundaries

A failing deterministic integration test showing incorrect `Ok` establishes a code-level correctness defect in the tested revision and configuration. It does not by itself establish:
- that the affected code is deployed on Canton mainnet;
- that a production report has been wrong;
- that an operator underpaid;
- the frequency or financial magnitude of any impact.

A passing test establishes only that the tested interleaving was handled safely. It does not prove all concurrency schedules safe. Follow-up testing should cover other orderings and storage backends.

## 9. Minimum deliverable

The implementation task is complete when:
1. the deterministic test runs against the real Scala path;
2. control runs pass;
3. the race run has a recorded, reproducible classification;
4. the exact tested commit, storage backend and configuration are recorded;
5. the result is reflected in the research paper as either a demonstrated defect, a safe refusal/availability trade-off, or an unresolved risk.

No cryptographic prototype is required for this test.
