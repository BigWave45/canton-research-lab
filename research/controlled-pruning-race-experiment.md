# Controlled pruning-race experiment: protocol and current result

**Date:** 17 November 2026  
**Evidence level:** conceptual model and test oracle; not an execution against Canton Scala code.

## Question

Can pruning advance after the report reader checks the pruning lower bound but before it reads the historical traffic counters? If so, does the reader return a correct value, fail explicitly, or return an incorrect value marked `Ok`?

## What the source establishes

In PR #111 at commit `b6a7733d22751636820138ab705db103184e4d18`, `TrafficReport.firstReadableStart` explicitly documents a race at the retention boundary: the journal is pruned before the lower bound moves, so a request can race pruning and report a wrong total. `TrafficReportReader.read` obtains pruning status and then performs separate historical reads.

This is a source-documented risk. It is not proof that the race has occurred, that it is reachable under deployed settings, or that the current reader returns a wrong `Ok` value.

## Conceptual outcomes

The model distinguishes four outcomes:

| Condition | Model result | Interpretation |
|---|---|---|
| No pruning race | Correct `Ok` | Expected baseline |
| Pruning moves but requested snapshot remains readable | Correct `Ok` | Race in timing, no accounting failure |
| Required snapshot is unavailable and reader fails closed | `CannotProvide` | Availability loss, not a false number |
| Required snapshot is unavailable but stale data is returned as `Ok` | Stale `Ok` | Hypothetical integrity failure requiring proof in the real implementation |

The final row is deliberately a hypothetical branch in the model. The inspected source does not establish that the implementation falls back to stale data or zero.

## Synthetic accounting impact

If the true amount is 150 bytes, the reported amount is 120 bytes, and the illustrative price is 2 accounting units per byte, the difference is 60 accounting units. This only demonstrates the arithmetic consequence of a wrong report. It is not a Canton price or observed loss.

## Test results

Five dependency-free unit tests cover the four timing/outcome classes and the arithmetic consequence. They test the conceptual model only.

## Required real implementation test

A valid implementation-level test should coordinate two actors with a barrier:

1. Start a report request and pause it immediately after `getSequencerPruningStatus()` returns.
2. Advance pruning so the requested historical boundary is crossed.
3. Resume the report request.
4. Record whether the result is a correct `Ok`, `CannotProvide`, surfaced error, or incorrect `Ok`.
5. Repeat around the exact retention boundary and under realistic pruning cadence.

The test should compare the report against a reference total captured before pruning. It must not manufacture the reference from the same post-prune data path.

If the sequencer API cannot deterministically pause between the check and read, add a test seam around those calls or an integration harness. A synthetic Python test is not a substitute.

## Decision criteria

- **Incorrect `Ok` reproducibly observed:** investigate severity, reachable configurations, settlement exposure and a consistency fix.
- **Explicit failure only:** classify as report availability/retention risk; define retry, archival and settlement exception handling.
- **Correct result despite concurrent pruning:** document the actual consistency guarantee and test its boundary conditions.
- **Inconclusive:** do not claim the race is harmless or exploitable; identify missing instrumentation.

## Source

- [TrafficReport.scala, PR #111 head](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReport.scala)
- [TrafficReportReader.scala, PR #111 head](https://github.com/canton-network/splice-multi-sync/blob/b6a7733d22751636820138ab705db103184e4d18/apps/syncoperator/src/main/scala/org/lfdecentralizedtrust/splice/syncoperator/TrafficReportReader.scala)
- [PR #111](https://github.com/canton-network/splice-multi-sync/pull/111)
