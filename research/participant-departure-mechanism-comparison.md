# Participant departure: charging semantics and mechanism comparison

**Research status:** specification ambiguity identified; no defect finding.  
**Implementation snapshot:** proposed traffic-report code in splice-multi-sync PR #111, commit b6a7733d22751636820138ab705db103184e4d18.  
**Protocol reference:** CIP-0132, Proposed, 17 November 2026 snapshot.

## 1. What the sources establish

CIP-0132 says the dedicated synchronizer tracks traffic consumed and exposes ten-minute interval reports. It also says the operator and paymaster are trusted in Phase 1 to report usage and burn the correct amount under their off-ledger agreement. It does not, in the text inspected, define how traffic from a participant that leaves during an interval is treated for billing.

The proposed API contract describes its value as traffic charged to participants. The implementation in TrafficReport.participantsConsumed iterates over participants present in the end-of-interval state. It counts a participant joining during the interval from zero and excludes a participant with no end-state reading because that participant left during the interval. The source comment says this explicitly.

Therefore:
- The implementation behaviour is established for the inspected PR snapshot.
- The commercial chargeability of pre-departure traffic is not established.
- It is not valid to label the behaviour an underpayment defect until the pricing agreement or normative rule is known.
- The report-to-burn link remains off-ledger and trusted in the Phase 1 CIP design.

Sources:
- CIP-0132: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- PR #111: https://github.com/canton-network/splice-multi-sync/pull/111
- Issue #155: https://github.com/ChainSafe/canton-extending-mainnet/issues/155

## 2. Lifecycle accounting identity

For interval i, partition participant membership epochs into:
- C_i: members present at both interval boundaries (continuing).
- J_i: members present at the end but absent at the start (joined).
- L_i: members present at the start but absent at the end (left).

Let c_start(m) and c_end(m) be cumulative traffic counters, and c_exit(m) the final counter captured at departure.

The end-state aggregation is:

R_i = sum(C_i counter deltas) + sum(J_i end counters)

If pre-departure traffic remains chargeable, the economically complete amount is:

E_i = R_i + sum(L_i [c_exit(m) - c_start(m)])

The additional term is computable only if departure snapshots or equivalent durable counter evidence exist. If the intended policy excludes departed members' interval traffic, then R_i may be correct by definition, but the exclusion must be explicit in the pricing rule.

Use membership epochs, not just participant IDs, to prevent a leave/rejoin cycle from being treated as one continuous counter history. Counter resets, sequencer upgrades and unavailable intervals must remain unknown until a defined recovery rule applies.

## 3. Four mechanisms and one policy choice

| Design | Accounting treatment | Privacy implications | Operational/dispute implications |
|---|---|---|---|
| Signed departure snapshot | Capture final counter and bind it to member epoch, interval and departure event | Identity plus exit time/counter may expose lifecycle metadata; signatures do not prove completeness | Clear evidence for disputes if signer and event source are trusted; requires event capture and signature verification |
| Carry-forward counter | Retain the departing member's final counter in durable interval state and include its delta at close | Can keep participant detail internal and publish only aggregate totals; retained state increases linkability risk for operator | Avoids a separate settlement per exit; requires durable state, pruning policy, replay protection and recovery |
| Event-driven boundary settlement | Close and account for a member's usage at departure, then add it to the settlement window | More frequent settlement events can reveal timing and participant-level patterns | Faster attribution, but increases event volume, reconciliation complexity and risk of double counting |
| Explicit exclusion | Define pre-departure interval usage as non-chargeable | Lowest additional disclosure; no new lifecycle evidence | Simple, but intentionally separates consumed traffic from billable traffic; must be disclosed in the agreement |
| Current end-state aggregation without explicit policy | Counts only those present at interval end | Aggregate output minimises participant detail | Operationally simple, but leaves the billing interpretation ambiguous |

A signed snapshot only authenticates the statement by the signer. It does not independently prove that every departure was captured. Carry-forward state has the same completeness dependency unless the membership transition stream itself is complete and authenticated. Event-driven settlement changes timing, not the need for trustworthy source events.

## 4. Synthetic mechanism comparison

The reproducible model uses:
- Continuing member: counter rises from 50 to 150, so 100 units.
- Departing member: counter rises from 20 to 60 before leaving, so 40 units.
- Joining member: end counter is 25, so 25 units from a zero baseline.

The current end-state population rule returns 125 units. If pre-departure traffic is chargeable, a departure snapshot, carry-forward counter or event-driven boundary record yields 165 units. Under explicit exclusion, 125 units is the correct policy-defined billable total.

The 40-unit difference is a synthetic illustration, not a Canton traffic estimate. The three evidence mechanisms yield the same total because they are alternative ways of preserving the same departure delta, not because their security properties are equivalent.

The model treats missing departure evidence as incomplete, never zero. It rejects conflicting duplicate departure-event identifiers and ignores identical replayed events.

## 5. Comparative assessment

### Assurance
- Signed snapshot: authenticates a departure statement if the signer is trusted; needs independent evidence that all exits were captured.
- Carry-forward: preserves a counter across membership removal; needs durable, complete lifecycle state and counter continuity.
- Event-driven settlement: makes the boundary explicit; needs complete departure events and idempotent settlement.
- Exclusion: no measurement proof needed for excluded traffic, because the policy says it is not billed.

None independently proves that the underlying traffic counter measures every economically relevant byte. None removes the Phase 1 trust assumption by itself.

### Privacy
The API currently returns an aggregate total, not participant-level rows. A mechanism can retain participant-level evidence internally and publish only a window total, but an auditor's ability to verify the total depends on access to the evidence or a proof of correct aggregation. Repeated aggregate queries and small participant populations can still leak activity patterns.

### Cost and operations
- Signed snapshots add event signing, verification and retention.
- Carry-forward adds state management and recovery complexity, but can avoid per-departure settlement.
- Event-driven settlement adds transaction/event volume and more complex settlement attribution.
- Explicit exclusion has the lowest technical cost but is only valid if accepted in the commercial policy.

No numeric cost score is assigned because implementation measurements, traffic distributions and privacy requirements are unavailable.

## 6. Decision gate

Before selecting a mechanism, obtain an authoritative answer to:

Does the applicable synchronizer pricing agreement charge traffic consumed by a participant before that participant leaves during a ten-minute reporting interval?

If yes, test carry-forward and signed departure evidence first. They preserve window-level aggregation without requiring a separate burn for each departure. Event-driven settlement remains a comparison point if prompt closure is commercially important.

If no, document the exclusion rule and test whether the API's behaviour matches the policy for join/leave/rejoin and counter-reset cases.

If the rule varies by agreement, make the policy version and effective time part of the accounting input. Never apply one current rule retrospectively to all intervals.

## 7. Reproduction and limits

Run:
- python analysis/participant_lifecycle_mechanisms.py
- python -m unittest discover -s tests -p 'test_participant_lifecycle_mechanisms.py' -v

The tests establish the behaviour of this synthetic model only. They do not establish actual Canton billing policy, production deployment, participant omission in live traffic, or actual financial loss.


## 8. Paymaster automation and the missing normative link

A further source check narrows the implementation boundary.

The tracking issue for DSync Paymaster Support (#87) explicitly says the work enables paymaster automation but does not add the automation itself; each paymaster must implement it. CIP-0132 says the report-to-burn automation is up to the paymaster. The traffic-report PR #111 exposes the report endpoint but does not define a universal paymaster-side consumer or a common report-to-burn reconciliation implementation.

Consequences:
- There is no single upstream paymaster automation path in the inspected work whose member-departure treatment can be traced end to end.
- A paymaster could implement agreement-specific aggregation, smoothing and reconciliation differently from another paymaster.
- The off-ledger agreement and the paymaster's own automation are therefore essential evidence for resolving whether departure usage is billable and how it is included.
- The on-ledger purchase choices enforce registered-paymaster identity and create burns/activity records for the bytes purchased, but issue #155 states that the purchase path does not check the amount paid against the traffic report.

This strengthens the case for making the accounting interface explicit, but it does not establish that any particular paymaster omits departure traffic.

Sources:
- DSync paymaster tracking issue #87: https://github.com/canton-network/splice-multi-sync/issues/87
- Traffic report PR #111: https://github.com/canton-network/splice-multi-sync/pull/111
- CIP-0132: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- Paymaster purchase issue #155: https://github.com/ChainSafe/canton-extending-mainnet/issues/155
