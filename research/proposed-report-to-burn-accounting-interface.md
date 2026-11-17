# Proposed report-to-burn accounting interface

**Status:** design proposal derived from the research; not a Canton standard, CIP amendment or implemented integration.

## 1. Why an interface is needed

CIP-0132 places the report-to-burn link off-ledger and leaves automation to each paymaster. Tracking issue #87 says upstream work enables automation but does not implement it. Issue #155 states that the on-ledger purchase path does not compare the amount paid with the traffic report.

The evidence chain is split:
- Operator API: aggregate traffic bytes by interval.
- Off-ledger agreement: pricing, discounts, minimums and permitted smoothing.
- Paymaster automation: calculates the amount to purchase and when.
- Public ledger: records CC burns and activity records.

Without a common settlement manifest, a third party cannot reliably determine which report intervals, agreement version and public burn events a particular settlement claims to reconcile.

## 2. Proposed manifest

Each settlement should produce a durable manifest with these logical fields:

| Field | Purpose |
|---|---|
| settlement_id | Stable unique identifier for the settlement obligation |
| synchronizer_id | Dedicated synchronizer covered |
| window_start / window_end | Exact record-time range being settled |
| interval_evidence[] | Every expected interval, its bounds, status, byte total and report digest |
| agreement_version | Effective agreement version for each interval or pricing segment |
| pricing_rule_reference | Versioned identifier/hash for price, discount, minimums, conversion and rounding policy |
| expected_cc | Amount calculated under the referenced agreement and approved smoothing policy |
| burn_events[] | Public ledger event IDs and amounts credited to this settlement |
| tolerance_cc | Contractually authorised reconciliation tolerance |
| operator_attestation | Authenticated statement binding interval evidence to the operator |
| paymaster_attestation | Authenticated statement binding calculation and burn allocation to the paymaster |

This is a logical schema, not a claim that the current API exposes all these fields. PR #111 returns interval bounds, status and aggregate bytes; it does not itself supply a signed report digest, agreement identifier, settlement ID or burn mapping. Those are additional interface requirements.

## 3. Required invariants

**I1. Complete interval coverage.** The settlement window must be partitioned by contiguous, non-overlapping intervals. Every expected interval must be Ok and contain a non-negative traffic amount. Undetermined and CannotProvide make the manifest incomplete; they must not be converted to zero.

**I2. Agreement version correctness.** Every interval must resolve to the agreement version effective for that interval. A change in discount, minimum rate, CC price reference, conversion or rounding rule must create a new effective pricing segment. Retrospective application of a current agreement version is invalid unless the agreement explicitly permits it.

**I3. Deterministic liability calculation.** Expected CC must be reproducible from interval bytes and the referenced agreement policy, including aggregation order, discount, minimums, conversion source/time, smoothing and rounding. The manifest references the rule; it should not invent a universal formula where agreements differ.

**I4. Unique burn attribution.** Every public burn event may be credited to at most one settlement obligation. Event IDs must be stable, and the verifier needs a global uniqueness index, not only per-manifest duplicate detection.

**I5. Due-date-aware window reconciliation.** At the contractual settlement deadline, the sum of uniquely attributed burns must equal expected CC within the agreed tolerance. Permitted delayed or smoothed payment must be represented as an explicit schedule and outstanding balance, not treated as a mismatch before it is due.

**I6. Reward consistency.** Bytes purchased for reward attribution must be traceable to the corresponding burn and applicable activity weights. Reward issuance must not exceed the rule-derived entitlement for the paid bytes. This does not prove traffic input was complete.

**I7. Lifecycle policy explicitness.** The agreement must state whether usage before a participant's departure during an interval remains chargeable. If chargeable, the operator must include a departure delta or mark the interval incomplete where evidence is unavailable. If excluded, the manifest records the exclusion policy version.

**I8. Privacy minimisation.** The ordinary manifest contains synchronizer-level aggregate bytes, not participant identifiers or transaction payloads. Detailed membership evidence remains with authorised parties and is disclosed only for disputes or independent audits. This reduces routine disclosure but does not guarantee anonymity; cohort size and repeated timing queries still matter.

## 4. Attestation and commitment design

A report digest is useful only if report content and digest are bound by an authenticated source. A hash generated by the paymaster after receiving an unsigned response proves only that the paymaster can later identify its own copy; it does not prove what the operator served.

Minimum proposal:
1. Operator signs a canonical encoding of synchronizer ID, interval bounds, status, aggregate bytes and report schema/version.
2. Paymaster signs the settlement manifest, including exact report digests, agreement reference, expected CC calculation and burn-event IDs.
3. Public burn IDs are independently resolvable from ledger data.
4. An auditor verifies signatures, interval coverage, agreement version, calculation, event uniqueness and reconciliation status.

This provides attribution and tamper evidence. It still does not prove that the operator's source counters included every economically chargeable participant or byte. That requires a separately justified metering-completeness mechanism or an explicit operator-trust assumption.

A Merkle tree could batch interval commitments and support selective disclosure, but it does not solve source completeness. Do not introduce it until report volume, audit query pattern and privacy threat model justify it.

## 5. Smoothing and delayed payment

CIP-0132 permits off-ledger discounts and smoothing/delays. Immediate interval equality is therefore the wrong invariant.

For settlement window W:
- calculate agreement-implied liability for the covered interval set;
- calculate the portion due by the current contractual deadline;
- attribute burns to that obligation;
- carry unpaid amounts as outstanding until due;
- reconcile only when the relevant due date arrives.

The manifest should distinguish not-yet-due, reconciled, short-paid, overpaid, incomplete-evidence and disputed. A delayed burn is not automatically a shortfall.

## 6. Reference validator

analysis/settlement_manifest_validator.py implements structural checks:
- complete contiguous interval coverage;
- Ok status and byte values;
- agreement-version and digest presence;
- duplicate/cross-manifest burn claims;
- settlement-window attribution;
- expected-versus-burned amount comparison.

It deliberately does not calculate expected CC from raw bytes because agreement formula, conversion source, discount and smoothing rules are not universal or yet evidenced. It accepts expected CC as an input and therefore cannot verify the pricing calculation itself.

The validator does not verify signatures, public ledger events, source measurement, reward contracts or privacy guarantees.

## 7. Reproduction

- python analysis/settlement_manifest_validator.py
- python -m unittest discover -s tests -p 'test_settlement_manifest_validator.py' -v

The tests validate the reference model only. They are not Canton integration tests.

## 8. Research contribution and open questions

The proposal composes known ideas—signed reports, versioned agreements, event attribution, reconciliation and selective disclosure—into an explicit accounting interface for this private-traffic-to-public-burn pipeline. The contribution is not a claim that any individual primitive is novel.

Open questions:
- Can the operator API safely expose a signed report or stable report version?
- Who is authorised to see the agreement reference and pricing parameters?
- How is a smoothing schedule represented and amended?
- How are public burn IDs allocated to multiple synchronizers when a paymaster settles in aggregate?
- What is the normative participant departure rule?
- Which reward issuance records can be joined to paid-byte attribution?
- What independent evidence can establish traffic-source completeness without revealing private payloads?
