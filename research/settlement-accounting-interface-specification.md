# Settlement Accounting Interface Specification

**Version:** 0.1  
**Date:** 18 November 2026  
**Status:** Research specification. Not a Canton CIP, deployed API contract or production implementation.

## 1. Purpose and boundary

This specification defines the minimum records needed to reconcile dedicated-synchronizer activity with a paymaster's CC burns and resulting reward attribution. It is implementation-neutral: it does not prescribe a database, signature scheme, proof system or API transport.

It separates source measurement and report completeness; contractual pricing and amount due; public burn evidence; allocation of aggregate burns to synchronizer obligations; reward attribution; and audit/public disclosure.

A report marked unavailable or undetermined is not a zero-activity report.

## 2. Record model

The interface has five linked record types. Identifiers are immutable and unique within their issuing namespace.

### A. IntervalReport

| Field | Type / constraint | Purpose | Disclosure |
|---|---|---|---|
| report_id | Opaque unique ID | Stable report identity | Auditor; public commitment |
| synchronizer_id | Canonical synchronizer ID | Identifies measured system | Restricted or policy-defined |
| interval_start, interval_end | Record-time timestamps; start < end | Exact measurement window | Auditor |
| interval_sequence | Monotonic integer per synchronizer | Detects gaps/reordering | Auditor |
| schema_version | Version string | Defines encoding and semantics | Public |
| status | OK, UNDETERMINED, CANNOT_PROVIDE | Explicit availability state | Public status may be coarsened |
| consumed_bytes | Non-negative integer, required only for OK | Aggregate measured consumption | Auditor; public only if approved |
| measurement_source | Meter/source version identifier | Identifies counter implementation | Auditor |
| generated_at | Timestamp | Report creation time | Auditor |
| operator_key_id | Signing key reference | Key attribution | Public |
| signature | Signature over canonical report | Provenance and tamper evidence | Public verification |
| report_digest | Hash of canonical signed report | Commitment/reference | Public |

UNDETERMINED and CANNOT_PROVIDE must not carry a billable consumed_bytes value. An explicit zero is valid only in an OK report. Reports must use a documented canonical encoding before signing and hashing.

### B. AgreementVersion

| Field | Type / constraint | Purpose | Disclosure |
|---|---|---|---|
| agreement_id | Stable opaque ID | Commercial agreement identity | Auditor |
| version_id | Immutable version ID | Binds calculations to a version | Public reference |
| effective_from, effective_until | Timestamps / nullable end | Determines applicable version | Auditor |
| pricing_rule_digest | Hash of canonical pricing rules | Binds exact rules | Public commitment |
| pricing_parameters | Price, discounts, minimums, conversion source, rounding | Reproducible liability | Auditor |
| smoothing_schedule | Due tranches and permitted delays | Determines amount due at time t | Auditor |
| authorised_parties | Identities/roles and approval evidence | Establishes authority | Auditor |
| authority_attestation | Signed approval or governed registry reference | Establishes version authority | Public reference + auditor evidence |

A version identifier alone does not prove legal or governance authority. The interface requires approval evidence or a governed authoritative registry.

The research prototype uses separate fields for the agreement signer and settlement-binding signer, and checks the corresponding `agreement` and `settlement_binding` roles. The schema does not, by itself, guarantee that these keys belong to different legal principals. If separation of duties is required, the authoritative signer registry must prohibit key/principal overlap for the two roles and define key-rotation, revocation and delegation rules.

### C. SettlementManifest

| Field | Type / constraint | Purpose | Disclosure |
|---|---|---|---|
| settlement_id | Unique ID | Settlement-window identity | Public opaque ID |
| synchronizer_obligations[] | One entry per synchronizer/agreement segment | Allows volume discounts across several synchronizers | Auditor |
| covered_window | Start/end timestamps | Defines included report intervals | Auditor |
| expected_interval_set | Explicit expected interval IDs | Detects missing intervals | Auditor |
| report_digests[] | Ordered references to IntervalReports | Binds source reports | Public commitment |
| agreement_version_refs[] | Version IDs and digests | Binds pricing basis | Public reference |
| gross_liability_cc | Non-negative amount | Agreement-derived liability before payment | Auditor |
| due_by_evaluation_time_cc | Non-negative amount | Amount contractually due at evaluation time | Auditor; proof input |
| calculation_version | Deterministic calculator version | Reproducibility | Public |
| calculation_digest | Commitment to calculation inputs/output | Tamper evidence | Public |
| manifest_root | Commitment to canonical manifest | Binds full record | Public |
| binding_authority_reference | Governed reference identifying who approved the report-to-obligation mapping | Establishes mapping authority basis | Auditor; public reference |
| binding_signer_key_id | Key reference for the actor authorised to attest the mapping | Attribution | Auditor/public verification |
| report_set_digest | SHA-256 digest over canonical, deterministically ordered report records for the interval, including revisions | Binds the exact report set used | Public commitment |
| binding_attestation | Separate Ed25519 signature over binding ID, report-set digest, interval, synchronizer, obligation, agreement ID/version, authority reference and binding signer key ID | Authenticates the mapping and exact report set, not source measurement truth | Auditor/public verification |
| operator_attestation | Signature over report set and measurement claims | Attribution | Auditor/public verification |
| paymaster_attestation | Signature over liability and payment claims | Attribution | Auditor/public verification |
| status | INCOMPLETE, READY, DISPUTED, RECONCILED, SHORT_PAID, OVERPAID | Explicit lifecycle | Public status |

For a multi-synchronizer commercial agreement, the manifest retains each obligation separately even when pricing or payment is aggregated. Aggregate discounts must follow the governing agreement, not an assumed linear sum of per-synchronizer prices.

### D. BurnAllocation

| Field | Type / constraint | Purpose | Disclosure |
|---|---|---|---|
| allocation_id | Globally unique ID | Prevents duplicate claims | Public opaque ID |
| settlement_id | Manifest reference | Identifies obligation set | Public |
| synchronizer_obligation_id | Manifest obligation reference | Identifies credited obligation | Auditor |
| burn_event_id | Canonical public ledger event reference | Links allocation to actual burn | Public |
| burn_amount_cc | Non-negative amount | Public burn value | Public |
| allocated_amount_cc | Amount credited to this obligation | Reconciles many-to-many allocation | Auditor; proof input |
| allocation_sequence | Unique sequence/version | Supports amendments without overwriting history | Public |
| paymaster_signature | Signature over allocation | Attribution | Public verification |

A burn may be allocated across multiple obligations. The same allocation record may not be claimed twice. Across all valid allocations for a burn:

Σ allocation(burn, synchronizer) ≤ public burn amount.

For each obligation s, by evaluation time t:

Σ eligible allocations(s) ≥ amount due D_s(t).

Excess burn remains unallocated or is carried forward only under an explicit contractual rule.

### E. RewardAttribution

| Field | Type / constraint | Purpose | Disclosure |
|---|---|---|---|
| reward_record_id | Unique ID | Identifies attribution result | Public opaque ID |
| settlement_id | Manifest reference | Links reward result to settlement | Public |
| burn_event_id | Public burn reference | Links to burn/coupon | Public |
| activity_rule_version | Rule identifier | Defines reward mapping | Public |
| app_weight, asset_weight | Non-negative configured values within authorised maxima | Reproduces activity weighting | Auditor/public as allowed |
| eligible_bytes | Purchased traffic used for reward calculation | Reproduces activity record | Auditor |
| activity_record_refs[] | On-ledger activity record references | Evidence of recorded activity | Public |
| reward_epoch | Epoch identifier | Reward period | Public |
| paymaster_reward_recipient | Party reference | Initial reward recipient | Public/policy-defined |
| downstream_distribution_ref | Optional evidence of pass-through to apps | Distinguishes paymaster reward from app distribution | Auditor |
| reward_status | NOT_RECORDED, RECORDED, ISSUED, DISTRIBUTED, DISPUTED | Lifecycle | Public status |

The interface distinguishes the paymaster's on-ledger reward entitlement from any off-ledger or subsequent distribution to applications. They are not interchangeable claims.

## 3. Status semantics

| Status | Meaning | Settlement treatment |
|---|---|---|
| OK | Measurement returned for a completed interval | May enter calculation |
| UNDETERMINED | Interval result not yet determinable | Window remains incomplete |
| CANNOT_PROVIDE | Required historical measurement unavailable | Window remains incomplete or disputed |
| INCOMPLETE | Expected evidence missing or non-OK | No final reconciliation |
| READY | Inputs complete and calculation reproducible | May enter due-date evaluation |
| NOT_YET_DUE | Liability exists but payment deadline has not arrived | Not a shortfall |
| RECONCILED | Due amount covered within contractual tolerance | Close or carry forward per agreement |
| SHORT_PAID | Due amount exceeds eligible allocated burns beyond tolerance | Exception |
| OVERPAID | Allocated burns exceed amount due beyond permitted carry-forward | Exception or credit |
| DISPUTED | A party challenged source, agreement or allocation evidence | Freeze final status pending resolution |

Do not collapse missing, undetermined, zero, not-yet-due and disputed into one numeric field.

## 4. Required invariants

1. **Interval coverage:** expected intervals form a complete, contiguous, non-overlapping partition of the settlement window.
2. **Status correctness:** only OK reports contribute measured bytes; non-OK reports block final reconciliation.
3. **Report provenance:** the operator signature binds canonical report content, status, interval and synchronizer.
4. **Agreement authority and binding authority:** every priced interval resolves to an authorised agreement version effective at that time, and the report-to-obligation mapping is separately attested by an actor authorised for that synchronizer and obligation. The binding attestation commits to the canonical report-set digest as well as the mapping metadata. An agreement signature alone does not authenticate the mapping.
5. **Deterministic calculation:** an independent implementation can reproduce liability from report data and versioned pricing rules.
6. **Due-date correctness:** payment is compared to the amount due at evaluation time, not automatically to gross liability.
7. **Burn uniqueness:** burn event references and allocation IDs are globally deduplicated.
8. **Allocation bound:** total allocations credited against a burn do not exceed that burn.
9. **Obligation coverage:** each obligation's eligible allocations cover the amount due, subject to explicit tolerance and carry-forward rules.
10. **Reward traceability:** reward activity records resolve to eligible paid traffic and applicable weight/rule version.
11. **Correction history:** amendments append a new version and preserve prior signed records.
12. **Privacy minimisation:** public verification receives only required identifiers, commitments, predicates and statuses; detailed commercial and measurement inputs remain restricted unless disclosure is justified.

## 5. Public proof predicates

A proof system, if later selected, should be evaluated against explicit predicates:
- allocation IDs in the committed manifest are unique;
- every allocation references a valid burn event in the committed burn set;
- total allocations against each burn do not exceed its public amount;
- the applied agreement version matches the authorised version reference;
- due amount is calculated by the specified deterministic rule over committed inputs;
- allocations credited to each obligation cover its amount due at evaluation time;
- reward activity is calculated from eligible purchased bytes and authorised weights.

A proof over committed inputs does not establish that all source events were included, that the agreement was legally authorised, or that a meter was truthful. Those require separately anchored evidence.

## 6. Minimum audit package

For each audit period, retain all expected interval IDs and statuses; canonical signed reports and digests; source counter provenance, retention/availability metadata and correction history; executed agreement versions, approvals and effective-time history; separately attested report-to-obligation mappings and signer-authority evidence; calculator version, inputs, outputs and reproduction instructions; settlement manifests and every allocation version; public ledger references for burns and activity records; reward rule version, epochs and reward issuance/distribution evidence; and dispute notices, auditor workpapers, resolutions and appeal records.

## 7. Non-goals

This interface does not prescribe a zero-knowledge system, guarantee anonymity, require public disclosure of exact synchronizer usage, inspect private transaction payloads, or assert that any field is currently implemented. It is a target for mapping against Canton source and governance evidence.
