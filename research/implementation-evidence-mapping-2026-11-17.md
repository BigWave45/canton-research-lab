# Implementation Evidence Mapping: Settlement Accounting Interface

**Audit snapshot:** 17 November 2026  
**Status vocabulary:** PRESENT = evidenced in reviewed public source; PROPOSED = in a CIP or design proposal; PARTIAL = some but not all semantics evidenced; ABSENT IN REVIEWED MATERIAL = not found in inspected public material; UNVERIFIED = insufficient evidence to classify. These labels are not statements about private or unreleased deployments.

## 1. Snapshot correction and source selection

The traffic-report implementation history has two relevant pull requests:

- PR #103 introduced a database-backed interval-report trigger and store.
- PR #111 explicitly replaces #103, carrying its history from before a squash. Its current description specifies an on-demand reader using sequencer counter snapshots and an internal OpenAPI spec.

The mapping below treats PR #111 as the current reviewed report-API proposal, not PR #103's earlier persistent-store design. Do not infer durable archival from the superseded PR.

## 2. Field-by-field evidence matrix

| Interface requirement | Status | Evidence in reviewed material | Gap / interpretation |
|---|---|---|---|
| Ten-minute interval bounds | PRESENT IN PROPOSAL | CIP-0132; PR #111 report endpoint | Exact boundary convention and clock guarantees need confirmation |
| Aggregate traffic quantity | PRESENT IN PROPOSAL | PR #111 sums participant traffic per interval from sequencer counter snapshots | Source completeness and lifecycle semantics remain separate questions |
| Report status | PARTIAL | PR #111 describes OK, UNDETERMINED and CANNOT_PROVIDE | Status meanings and consumer settlement policy need normative specification |
| Stable report ID | ABSENT IN REVIEWED MATERIAL | No report-level immutable identifier described in PR #111 summary | Add stable report ID or deterministic content address |
| Schema version | PARTIAL | Endpoint has an internal OpenAPI specification | Versioned report payload and compatibility policy not established by inspected summary |
| Operator report signature | ABSENT IN REVIEWED MATERIAL | JWT authenticates API caller; no report-level operator signature established in PR #111 summary | Caller authentication is not a signature over report content |
| Durable report archive | ABSENT IN CURRENT PR #111 DESIGN | PR #111 replaces PR #103's stored interval trigger with on-demand sequencer reads | Retention and historical query availability depend on sequencer history and upgrade semantics |
| Measurement-method version | ABSENT IN REVIEWED MATERIAL | No explicit versioned metering-method identifier in reviewed API description | Needed to reproduce changes in counter semantics |
| Agreement ID/version | OFF-LEDGER / NOT IN REPORT API | CIP-0132 says report-to-burn link and discounts are governed off-ledger | Needs authoritative version registry or auditable agreement reference |
| Pricing-rule digest | ABSENT IN REVIEWED MATERIAL | Pricing/discount terms are off-ledger | Need canonical rule representation and effective-time mapping |
| Liability amount and due schedule | ABSENT IN REPORT API | Paymaster automation calculates payment; smoothing/delay may be off-ledger | Needs explicit obligation and tranche record |
| Burn event identity | PRESENT ON LEDGER; LINKAGE OFF-LEDGER | Paymaster purchase/burn path and public ledger events | Mapping each burn to obligation/interval is not established by a common manifest |
| Global allocation uniqueness | ABSENT IN REVIEWED MATERIAL | No shared allocation manifest/index identified | Needed for multi-synchronizer portfolio reconciliation |
| Paid amount compared with report | ABSENT IN LEDGER PURCHASE CHECK | Tracker issue #155 explicitly says nothing checks paid amount against report | Must be performed by paymaster reconciliation and/or additional protocol mechanism |
| Registration/paymaster identity | PRESENT IN PURCHASE PATH | RegisteredSynchronizer registration and paymaster gating in feature work | Does not prove amount paid is sufficient |
| Reward activity hook | PROPOSED / DRAFT IN SNAPSHOT | CIP-0132 proposes activity recording; PR #8449 is draft; issue #163 tracks integration | Do not mark end-to-end reward linkage as implemented |
| Reward rule and epoch linkage | PARTIAL / UNVERIFIED | CIP-0104 activity recording architecture and CIP-0132 Phase 1 proposal | Need evidence of final reward record mapping for this flow |
| Independent source measurement evidence | UNVERIFIED | Sequencer counter API is the reported source | No independent completeness proof established |
| Audit attestation | ABSENT IN REVIEWED MATERIAL | Not part of reviewed CIP/API summary | Proposed interface addition |
| Dispute/correction history | ABSENT IN REVIEWED MATERIAL | Not specified in reviewed public interface | Needs append-only correction and dispute semantics |
| End-to-end acceptance test | NOT DEMONSTRATED IN REVIEWED SNAPSHOT | Issue #159 specifies register, transact, report, pay and activity-record flow as deliverable | A test specification is not a passing CI result |

## 3. Evidence sources and their correct interpretation

### CIP-0132: Dedicated Synchronizer Paymaster Model

Status in the 17 November snapshot: Proposed and entered voting on 16 November. It specifies:
- dedicated synchronizer traffic reporting in ten-minute intervals;
- post-hoc CC burn by a designated paymaster on the Global Synchronizer;
- an off-ledger link between report and burn;
- trust in operator and paymaster to report and burn correctly during Phase 1;
- activity recording intended to support app and validator rewards.

It does not establish that the model is approved, deployed or fully automated.

Source: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md

### Traffic report PR #111

PR #111 describes `GET /v0/traffic-report`, JWT authentication, 100 intervals per page, ten-minute interval totals, and sequencer counter reads at interval start and end. It explicitly replaces PR #103. The endpoint's specification is described as internal (`sync-operator-internal.yaml`).

This is report API evidence, not a signed settlement record. JWT authenticates access to the endpoint; it does not authenticate the returned report as a signed accounting statement.

Source: https://github.com/canton-network/splice-multi-sync/pull/111

### Paymaster purchase and amount checking

Tracker issue #155 describes the registered-synchronizer purchase path and explicitly states that nothing checks the paid amount against the report; the paymaster may pay less than usage. This is a design limitation recorded in the tracker, not evidence that an operator has actually underpaid.

Source: https://github.com/ChainSafe/canton-extending-mainnet/issues/155

### Activity recording and end-to-end test

PR #8449 is titled `DRAFT: Daml for ActivityRecorder`. Tracker issue #163 describes the dependency for recording app and asset activity. Tracker issue #159 specifies the complete register → transact → report → pay → activity-record integration test.

Sources:
- https://github.com/canton-network/splice/pull/8449
- https://github.com/ChainSafe/canton-extending-mainnet/issues/163
- https://github.com/ChainSafe/canton-extending-mainnet/issues/159

## 4. Research implications

The interface is not simply a missing API response field. The missing evidence spans different institutional and technical boundaries:

1. **Report provenance:** the operator needs to bind a report's exact contents to an authorised signing key.
2. **Commercial authority:** the agreement version and its effective dates need a governed reference.
3. **Settlement attribution:** the paymaster needs an auditable mapping from liabilities to public burns, including portfolio-wide uniqueness.
4. **Reward traceability:** the reward record must link to the paid activity and applicable rule.
5. **Measurement completeness:** a signature, report digest or proof does not show that all chargeable source activity was counted.

These requirements should not be collapsed into one cryptographic mechanism.

## 5. Priority order

| Priority | Work | Why |
|---|---|---|
| 1 | Define report semantics, expected intervals and non-OK handling | Prevent missing evidence from being treated as zero |
| 2 | Add signed, versioned report provenance and retention policy | Make report origin and historical evidence reproducible |
| 3 | Define agreement-version, liability and due-schedule records | Make payment calculations independently reproducible |
| 4 | Define burn allocation manifest and global uniqueness | Prevent duplicate credit across synchronizers |
| 5 | Complete and test reward linkage end-to-end | Verify the full economic accounting chain |
| 6 | Audit source measurement completeness | Establish what an OK report can actually guarantee |
| 7 | Add selective public proofs where they reduce disclosure | Avoid proof engineering before predicates and inputs are stable |

## 6. What this audit does not claim

- It does not claim real underpayment, fraud or production financial loss.
- It does not claim private transaction payloads are needed for routine accounting verification.
- It does not claim a zero-knowledge proof is necessary or sufficient.
- It does not claim every absence in the inspected public PR summaries is absent from all private or unreleased implementations.
- It does not treat a proposed CIP or open PR as deployed functionality.

## 7. Next research step

Use the field map to define a minimum viable evidence package and a staged adoption path. The first implementation target should be signed interval reports plus agreement-aware due-schedule reconciliation and a global burn-allocation manifest. Benchmark cryptographic proofs only after the public predicates and canonical input format are stable.
