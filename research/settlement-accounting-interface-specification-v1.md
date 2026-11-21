# Settlement Accounting Interface Specification v1

**Date:** 17 November 2026  
**Status:** Research specification. Not a CIP, production API schema, or claim of existing implementation.  
**Case study:** CIP-0132 Dedicated Synchronizer Paymaster Model.

## 1. Purpose and boundary

Define the minimum evidence needed to reconcile dedicated-synchronizer activity, the off-ledger commercial agreement, public CC burns, allocation across synchronizers, and reward attribution.

The interface must make five distinct claims independently checkable:

1. The reported activity covers the expected measurement intervals.
2. The correct agreement and pricing rules were applied.
3. burns cover the amount due at the evaluation time.
4. Each burn amount is allocated at most once and within its public amount.
5. reward attribution follows the applicable reward rule and paid-activity inputs.

It does not require private transaction payloads as ordinary accounting evidence. It does require a separately justified source-measurement completeness mechanism.

## 2. Record types

The design uses six linked records rather than one oversized report:

- **IntervalReport:** operator-originated evidence for one synchronizer and interval.
- **AgreementReference:** version and effective-time reference for the commercial rules.
- **SettlementObligation:** calculated liability and due schedule for a covered interval set.
- **BurnAllocation:** portion of a public burn credited to an obligation.
- **RewardAttribution:** mapping from eligible paid activity to the applicable reward calculation.
- **AuditAttestation:** auditor's scoped opinion, evidence range and exceptions.

This separation allows one burn to be allocated across multiple synchronizer obligations and one obligation to be settled by multiple burns.

## 3. Canonical logical schema

The following is illustrative JSON-like pseudocode. Field names and types are proposed for research; they are not copied from the current endpoint.

```json
{
  "schema_version": "1",
  "interval_report": {
    "report_id": "opaque-unique-id",
    "synchronizer_id": "ledger-synchronizer-identifier",
    "interval_start": "UTC timestamp",
    "interval_end": "UTC timestamp",
    "status": "OK | UNDETERMINED | CANNOT_PROVIDE",
    "aggregate_bytes": 123456,
    "measurement_method_version": "opaque-version",
    "sequence_number": 42,
    "issued_at": "UTC timestamp",
    "operator_key_id": "key-reference",
    "operator_signature": "signature-over-canonical-fields"
  },
  "settlement_obligation": {
    "obligation_id": "opaque-unique-id",
    "synchronizer_id": "ledger-synchronizer-identifier",
    "window_start": "UTC timestamp",
    "window_end": "UTC timestamp",
    "interval_report_digests": ["digest-1", "digest-2"],
    "agreement_id": "opaque-agreement-reference",
    "agreement_version": "version-reference",
    "pricing_rule_digest": "digest",
    "liability_cc": "integer-or-fixed-point",
    "due_schedule": [
      {"due_at": "UTC timestamp", "amount_cc": "integer-or-fixed-point"}
    ],
    "calculation_version": "version-reference",
    "paymaster_party": "party-identifier",
    "paymaster_signature": "signature-over-canonical-fields"
  },
  "burn_allocation": {
    "allocation_id": "globally-unique-id",
    "burn_event_id": "public-ledger-event-id",
    "burn_amount_cc": "integer-or-fixed-point",
    "obligation_id": "opaque-unique-id",
    "allocated_amount_cc": "integer-or-fixed-point",
    "ledger_domain": "global-synchronizer-identifier",
    "ledger_effective_time": "UTC timestamp",
    "allocation_sequence": 1
  },
  "reward_attribution": {
    "reward_record_id": "opaque-unique-id",
    "burn_event_id": "public-ledger-event-id",
    "obligation_id": "opaque-unique-id",
    "eligible_activity_quantity": "integer-or-fixed-point",
    "app_weight": "integer-or-fixed-point",
    "asset_weight": "integer-or-fixed-point",
    "reward_rule_version": "version-reference",
    "reward_epoch": "epoch-identifier",
    "recipient": "party-identifier",
    "reward_record_reference": "ledger-event-or-contract-reference"
  },
  "audit_attestation": {
    "attestation_id": "opaque-unique-id",
    "auditor_identity": "auditor-identifier",
    "scope_digest": "digest",
    "period_start": "UTC timestamp",
    "period_end": "UTC timestamp",
    "opinion": "UNQUALIFIED | QUALIFIED | ADVERSE | DISCLAIMER",
    "exceptions_digest": "digest",
    "issued_at": "UTC timestamp",
    "auditor_signature": "signature-over-canonical-fields"
  }
}
```

The schema deliberately separates report status from numeric bytes. A non-OK report must not carry a value that a consumer silently treats as a zero measurement. An implementation may omit `aggregate_bytes` unless status is `OK`.

## 4. Required field semantics

| Field group | Required semantics | Primary verifier |
|---|---|---|
| Schema and report IDs | Versioned, unique, canonical encoding | All parties |
| Synchronizer and interval | Stable synchronizer identity; UTC, half-open interval [start,end); no overlap or gaps in a complete window | Paymaster and auditor |
| Report status | OK, UNDETERMINED, CANNOT_PROVIDE remain distinct; only OK is billable as a measured quantity | Paymaster and auditor |
| Aggregate bytes | Non-negative integer with defined counter/reset/upgrade semantics | Auditor |
| Report signature | Operator key signs canonical fields; key validity and revocation history retained | Auditor; public verifier checks signature if public |
| Agreement version | Effective-time mapping; amendments and authority are auditable | Auditor |
| Pricing rule digest | Binds pricing, discounts, conversion source/time, aggregation, rounding and smoothing rules | Auditor; optional proof verifier |
| Liability and due schedule | Deterministic result with explicit due tranches; no immediate shortfall for not-yet-due amounts | Paymaster and auditor |
| Burn event | Publicly resolvable ledger event with amount, domain and finality semantics | Public verifier |
| Allocation | Globally unique allocation ID; correct burn reference; aggregate allocated amount bounded by burn amount | Public verifier with proof/manifest; auditor directly |
| Reward attribution | Binds eligible activity, weights, reward rule, epoch and ledger record | Auditor; public verifier for exposed predicates |
| Audit attestation | Defines scope, evidence coverage, exceptions and opinion; does not overstate assurance | All parties |

All timestamps must have one canonical time basis and defined boundary convention. The recommended interval convention is UTC and half-open: start inclusive, end exclusive. The implementation must document how sequencer timestamps, interval completion and clock uncertainty map to this convention.

## 5. Normative accounting predicates for the research model

For each settlement window, let E be the expected interval set and R the submitted reports.

**P1 — interval coverage**

Every expected interval appears exactly once. Intervals are contiguous and non-overlapping. Every interval must be OK before a liability is treated as fully measured. Missing, UNDETERMINED or CANNOT_PROVIDE intervals produce an incomplete-evidence state, not zero.

**P2 — report provenance**

The operator signature verifies over the canonical report fields, and the signing key was authorised for the synchronizer and valid at issuance time. This proves provenance, not measurement truth or completeness.

**P3 — agreement authority and calculation**

Each interval maps to the agreement version effective at that time. Liability is reproducible from the referenced pricing rule. The agreement authority, amendment history, rounding and conversion inputs must be retained. A digest alone does not prove that a contract was legally authoritative.

**P4 — due-aware payment**

At evaluation time t, compare attributed burns with D(t), the amount contractually due by t, not the full lifetime liability. Outstanding not-yet-due tranches are not shortfalls.

**P5 — allocation conservation**

For each public burn b:

`sum(allocated_amount for b) <= public_burn_amount(b)`

For each obligation o:

`sum(allocations credited to o by t) >= due_amount(o,t)`

Allocation IDs are globally unique. The same burn event cannot be counted twice across manifests.

**P6 — reward consistency**

Reward attribution must reference eligible paid activity and the applicable rule version. A correct reward calculation does not prove that the underlying traffic report was complete.

**P7 — exception preservation**

The interface must represent at least: INCOMPLETE_EVIDENCE, NOT_YET_DUE, RECONCILED, SHORT_PAID, OVER_ALLOCATED, DUPLICATE_ALLOCATION, AGREEMENT_MISMATCH, REWARD_MISMATCH, DISPUTED and CORRECTED. Corrections append a new version and preserve the prior record; they do not silently overwrite it.

## 6. Disclosure profile

**Public:** public burn event and amount; opaque obligation/manifest commitment; proof or attestation of allocation uniqueness and aggregate bounds; proof verification result; public status and exception category where disclosure is authorised.

**Auditor-restricted:** exact interval reports, agreement text and effective dates, exact liabilities and allocations, source counter evidence, key authorisation history, reward inputs and exception workpapers.

**Operator/paymaster-confidential:** operational telemetry, internal participant-level metering needed to derive aggregates, automation state and non-public commercial details not required for the public proof.

**Excluded from ordinary accounting audit:** private transaction payloads and unrelated party-level ledger data. Access requires a separately documented necessity.

A public commitment or proof may still leak information through timing, repeated releases, cohort sizes or public metadata. The disclosure review must consider the entire release history, not one record in isolation.

## 7. Trust assumptions and limits

- Operator-controlled counters may be incomplete or misconfigured. A signature does not cure this.
- A hash binds a record after commitment; it does not prove the record was complete when created.
- A ZK proof establishes a predicate over committed inputs; it does not establish that omitted events were included.
- An auditor can test source evidence only to the extent the evidence is retained, complete and within scope.
- Agreement authority is legal/governance evidence, not a property of a hash.
- Burn finality and event identity depend on the relevant ledger semantics.
- Reward-record correctness is separate from measurement completeness.
- A multi-synchronizer paymaster requires a global allocation index or equivalent proof of cross-manifest uniqueness.

## 8. Current implementation fit

The public material reviewed as of 17 November 2026 supports only part of this schema:

- CIP-0132 proposes ten-minute interval reporting, a designated paymaster, post-hoc CC burn, off-ledger report-to-burn linkage and Phase 1 reward recording. It is in the voting process, not treated here as approved or deployed.
- The traffic-report PR #111 describes a JWT-protected endpoint returning 100 ten-minute intervals per page, with interval statuses and aggregate traffic derived from sequencer counter snapshots. It replaces earlier PR #103 history. It does not establish a signed report object, agreement version, durable report digest or burn allocation manifest.
- Paymaster purchase work in PRs #100 and #104 and tracker issue #155 establishes the purchase path and registration checks. Issue #155 explicitly says the ledger path does not compare the amount paid with the traffic report.
- The ActivityRecorder integration PR #8449 is a draft in the reviewed snapshot; tracker issue #163 records the dependency.
- Tracker issue #159 specifies the end-to-end register → transact → report → pay → activity-record test, indicating the whole flow was not yet demonstrated by that acceptance test in the reviewed snapshot.

See `research/implementation-evidence-mapping-2026-11-17.md` for field-by-field classification.

## 9. Acceptance criteria for a future implementation

A conforming implementation for this research model should demonstrate:

1. Canonical signed interval reports with key-authorisation history.
2. Explicit expected-interval schedule and non-OK status handling.
3. Reproducible agreement-version and due-schedule calculation.
4. Publicly resolvable burn references and global allocation uniqueness.
5. Portfolio-level reconciliation across multiple synchronizers.
6. Reward-rule and reward-record linkage.
7. Append-only corrections, dispute evidence and audit attestations.
8. A public verification interface that does not disclose exact restricted liabilities by default.
9. An end-to-end test that creates traffic, obtains reports, settles due amounts, attributes burns, records activity and reconciles the final state.
10. An independent source-completeness assessment that does not assume a signature or proof is sufficient.

## 10. Scope boundary

This specification is a research artefact for evaluating the proposed model. It is not a demand that Canton adopt every field, nor a claim that current systems are defective. The contribution is the explicit composition of accounting evidence and assurance claims across a privacy-preserving infrastructure payment flow.
