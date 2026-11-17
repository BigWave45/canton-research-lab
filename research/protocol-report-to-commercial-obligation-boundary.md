# Protocol report and commercial obligation boundary

**Evidence snapshot:** 17 November 2026.  
**Purpose:** Separate the Canton traffic-report contract from synthetic commercial-accounting assumptions.

## 1. What the proposed protocol reports

CIP-0132 describes traffic reporting for a dedicated synchronizer in ten-minute intervals. The traffic report is for the whole synchronizer. The inspected implementation proposal in `canton-network/splice-multi-sync#111` exposes an authenticated `GET /v0/traffic-report` endpoint. Its interval response contains:
- interval start and end record times;
- a status: `Ok`, `Undetermined` or `CannotProvide`;
- an aggregate `trafficConsumed` byte count when status is `Ok`.

The reader obtains cumulative traffic-control state at interval boundaries, calculates participant consumption and sums it into one synchronizer-level interval total. The public response does not expose participant-level rows.

The endpoint does not expose a commercial obligation ID, an agreement version, an invoice ID, or a paymaster burn ID.

## 2. What CIP-0132 says about payment

The link between the traffic report and the paymaster's CC burn is off-ledger in Phase 1. Discounts are handled by an off-ledger agreement between Super Validators and the dedicated-synchronizer operator. The paymaster is responsible for building automation that consumes traffic reports and performs the burn.

Therefore, the protocol does not establish a native one-report-to-one-obligation relationship. The contract may aggregate multiple reports into a billing period, apply a discount, smooth payment over time, or otherwise define settlement terms. The precise mapping depends on the off-ledger agreement and must not be inferred from the report API.

## 3. What the research model currently assumes

The synthetic model currently attaches the following metadata to each interval report:
- synchronizer identity;
- commercial obligation identity;
- agreement version.

These are model-side linkage fields. They are not fields in the inspected traffic-report API response. They represent an explicit mapping supplied by the off-ledger accounting layer.

The model permits multiple interval reports to accumulate into one obligation. It currently represents each interval as mapped to exactly one obligation. This is a simplifying assumption, not a Canton protocol guarantee. It excludes split allocation of one interval across multiple obligations because no primary evidence reviewed here establishes that such splitting is required.

## 4. Correction identity rule

The model rejects a correction that changes synchronizer, obligation or agreement-version binding. This is a conservative accounting invariant: a quantity correction must not silently redirect previously recorded activity to a different commercial counterparty or tariff.

It is not asserted as a Canton protocol rule. Legitimate agreement amendments, novations, synchronizer migrations or billing-period reassignment require an explicit, separately authorised mapping event. They should not be smuggled into an ordinary measurement correction.

## 5. Required interface separation

Before the comparative experiments are treated as final, the model interface should separate:

1. **Protocol report:** interval, status, aggregate bytes, revision/lineage if the reporting system provides it.
2. **Off-ledger settlement binding:** synchronizer, agreement version, billing period, obligation or invoice mapping, and authority for that mapping.
3. **Public payment evidence:** CC burn transaction and any reward records attributable to it.

This separation prevents the model from implying that commercial terms are embedded in the protocol report. It also makes the trust question visible: who supplied and authorised the mapping, how changes are recorded, and what independent evidence can verify it?

## 6. Primary evidence and status

- CIP-0132: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- Traffic-report PR #111 (open at snapshot): https://github.com/canton-network/splice-multi-sync/pull/111
- Traffic-report source, PR head: `TrafficReport.scala`, `TrafficReportReader.scala`, and their Scala tests.
- Paymaster purchase PR #100 (merged 11 November 2026): https://github.com/canton-network/splice-multi-sync/pull/100
- Scan/SV paymaster purchase handling PR #104 (merged 12 November 2026): https://github.com/canton-network/splice-multi-sync/pull/104

The implementation status of PRs #100 and #104 does not imply that the separate traffic-report endpoint PR #111 was merged or deployed. At the snapshot, #111 remained open.

## Research implication

The next model revision should move commercial mapping metadata out of the protocol report object and into a separately versioned settlement-binding object. The four assurance architectures can then be compared on the actual research question: how well each mechanism authenticates, validates and reconciles the off-ledger mapping from private synchronizer activity to public CC burn and rewards.
