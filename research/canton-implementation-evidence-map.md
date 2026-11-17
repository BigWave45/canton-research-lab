# Canton Implementation Evidence Map for the Settlement Accounting Interface

**Audit snapshot:** 17 November 2026  
**Status vocabulary:** Present in reviewed source; Proposed in a CIP or open work item; Absent from reviewed implementation; Unverified from public evidence. Present means code or specification evidence exists, not that it is deployed on a live network.

## 1. Status findings that materially affect the design

The traffic-report implementation history has two relevant pull requests. **PR #103** was closed on 13 November 2026 without being merged. It was explicitly superseded by **PR #111**, which remains open in the 17 November 2026 snapshot. PR #111 says it replaces #103 and carries forward the report API work after a squash. The related ChainSafe tracker issue #152 remains open.

The distinction matters: PR #103's earlier design included a durable interval-report table and trigger. The current PR #111 design removes that storage/trigger approach and reads sequencer traffic counters on demand at interval boundaries. It uses JWT authentication and an internal OpenAPI specification. Therefore, do not attribute durable report retention to the current PR. Historical availability depends on the sequencer retaining the required counter history; certain intervals can become unavailable across logical synchronizer upgrades. Issue #152 still contains broader acceptance requirements, including retention across pruning/LSU and consistency across four operator apps.

PRs #100 and #104 are merged code changes for paymaster purchase handling and Scan/SV integration. They establish registered-paymaster purchase paths and traffic contracts. They do not themselves reconcile the amount burned with the traffic report. Issue #155 explicitly states that nothing checks paid amount against report. Its closure records completion of the purchase-choice deliverable, not resolution of that accounting gap.

The ActivityRecorder integration remains incomplete in the reviewed snapshot: upstream Splice PR #8449 is a draft/open PR, and tracker issue #163 is open. The CIP-0132 proposal describes the intended activity-recording hook, but that intended behaviour must not be represented as an end-to-end deployed path.

## 2. Field and control mapping

| Interface requirement | Evidence | Status | What can safely be claimed |
|---|---|---|---|
| Dedicated synchronizer registration and paymaster identity | CIP-0132; merged splice-multi-sync PRs #100/#104; tracker #155 | Present in reviewed code; deployment unverified | Purchase choices can be parameterised by an on-ledger registered synchronizer/paymaster. |
| Synchronizer ID on purchase | PR #100 and #104 | Present in reviewed code | Purchase is checked against registered synchronizer context. |
| Public CC burn event | CIP-0132 and purchase path | Present as underlying traffic-purchase mechanism; deployment unverified | A purchase/burn can be recorded on the Global Synchronizer. |
| Burn event linked to private settlement ID | No common settlement-manifest field identified in reviewed PRs | Absent from reviewed implementation | Report-to-burn mapping remains an off-ledger paymaster responsibility. |
| 10-minute interval report concept | CIP-0132; tracker #152; open PR #111 (supersedes closed-unmerged #103) | Proposed / in review | Endpoint design exists in an open PR; it is not merged or established as deployed. |
| Report statuses OK, UNDETERMINED, CANNOT_PROVIDE | PR #111 design | Proposed / in review | Intended status semantics in an open PR, not a merged endpoint. |
| Durable report retention across pruning/LSU | Tracker #152; PR #111 current design; PR #103 superseded | Not present in current PR design / unresolved | PR #111 reads sequencer counters on demand; it does not retain a durable report archive. Availability depends on counter-history retention and upgrade handling. |
| Operator signature on each report | No report-level signature identified in reviewed PR #111 description or CIP text | Absent from reviewed design | JWT authenticates API caller; it does not sign or attest report contents. |
| Report digest and canonical encoding | No standard field identified | Absent from reviewed design | Proposed interface adds stable content commitment and canonical serialization requirement. |
| Agreement version, effective dates and pricing rule digest | CIP-0132 places discounts/smoothing in off-ledger agreements; no machine-readable version interface identified | Absent from reviewed implementation | Agreement authority and version binding are proposed interface requirements. |
| Deterministic liability calculation | Paymaster automation left to implementer under CIP-0132 | Absent as shared protocol interface | A paymaster can calculate liability, but no common calculation manifest is established. |
| Due-date/smoothing schedule | CIP-0132 permits delayed/smoothed burn by agreement | Proposed off-ledger | Economic permission exists in proposal; a common machine-readable schedule is not established. |
| Burn allocation across multiple synchronizers | CIP-0132 explicitly permits one agreement/volume discount across multiple synchronizers; no allocation manifest identified | Proposed | Portfolio allocation is an essential interface addition, not an existing public field. |
| Global duplicate-allocation prevention | No allocation registry/unique manifest identified | Absent from reviewed implementation | Must be handled by proposed allocation ledger/manifest or another authoritative mechanism. |
| Reconciliation tolerance and exception state | No common public interface identified | Absent from reviewed implementation | Proposed statuses and tolerance rules require agreement/governance definition. |
| Activity weights and paymaster activity calculation | CIP-0132; PR #100/#104 | Partly present in purchase code | Weight parameters and MemberTraffic purchase records are supported in reviewed code. |
| ActivityRecorder hook records | CIP-0132 intent; upstream Splice PR #8449; issue #163 | Proposed / unverified | Hook implementation and full flow are not confirmed complete in this snapshot. |
| Reward issuance linked to report and allocation manifest | No complete report-to-burn-to-reward mapping identified | Unverified | Do not claim end-to-end reward reconciliation. |
| Public proof of allocation arithmetic | No proof-carrying manifest or verifier identified | Absent from reviewed implementation | Cryptographic proof is a research design option only. |
| Auditor-restricted source measurement package | No standard audit export identified | Absent from reviewed implementation | Requires governance and evidence-retention design. |
| Independent source measurement completeness | No independent measurement reference identified | Unverified | Central unresolved assurance dependency. |
| Transaction payload disclosure | Not required by proposed accounting interface | Excluded by design | Audit target is aggregate metering evidence, not private transaction contents. |

## 3. What the evidence says about the current pipeline

### Measurement and reporting

CIP-0132 specifies synchronizer-wide aggregate traffic reports in ten-minute intervals, measured using sequencer record time. PR #103 was closed unmerged and replaced by PR #111, which remains open. PR #111 describes an authenticated, on-demand endpoint reading sequencer counters; it does not retain durable report records. Tracker #152 remains open and includes stronger acceptance criteria for historical availability and four-node consistency. Therefore the report interface is proposed/in review, while durable retention and four-node acceptance remain unverified.

### Purchase and burn

PRs #100 and #104 are merged. They add registered-synchronizer paymaster purchase handling and Scan/SV ingestion. The code checks that the registered paymaster is the payer, the synchronizer matches the registration, and configured activity weights do not exceed maxima. This is purchase authorisation and activity-weight plumbing, not complete accounting reconciliation.

Issue #155 explicitly states that the purchase path does not check the paid amount against the traffic report. A registered paymaster may pay less than usage. This is a documented design gap, not evidence that an actual paymaster has underpaid.

### Reward attribution

CIP-0132 describes ActivityRecorder as part of the intended flow. However, the reviewed upstream PR #8449 remains draft/open and issue #163 remains open. Consequently, the report-to-burn-to-reward chain is not demonstrated as complete by this evidence snapshot. The full end-to-end test issue #159 remains open and depends on report API, ActivityRecorder and related work.

## 4. Architecture implications

1. Do not design around a report endpoint as though it were deployed. The interface should be forward-compatible with proposed statuses and interval semantics, but durable retention and multi-node consistency remain unverified.
2. Do not treat purchase authorisation as payment completeness. PRs #100/#104 constrain who can buy and for which registered synchronizer; they do not bind the amount to a complete liability calculation.
3. Do not treat activity-weight plumbing as reward-chain completion. The hook and full integration test remain unresolved in this snapshot.
4. Keep the off-ledger agreement explicit. CIP-0132 allows cross-synchronizer volume discounts and delayed/smoothed burns. A settlement manifest must represent multiple obligations, pricing segments, due tranches and allocation rules.
5. Treat the report's participant-lifecycle and pruning-boundary semantics as open accounting questions. The PR #111 source test excludes a participant present at interval start but absent at interval end; its source comment also acknowledges a possible pruning/read race at the retention boundary. Neither is proof of production error, but both matter to measurement completeness and report reliability.
5. Prioritise interface and evidence completeness before proof engineering. A proof cannot repair missing interval reports, an unauthorised agreement version or incomplete source metering.

## 5. Source register

- [CIP-0132: Dedicated Synchronizer Paymaster Model](https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md)
- [CIP-0129: Universal Burn and Synchronizer Pricing](https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md)
- [splice-multi-sync PR #100: paymaster traffic purchase](https://github.com/canton-network/splice-multi-sync/pull/100)
- [splice-multi-sync PR #104: Scan/SV handling](https://github.com/canton-network/splice-multi-sync/pull/104)
- [splice-multi-sync PR #103: traffic report API, closed without merge](https://github.com/canton-network/splice-multi-sync/pull/103)
- [Tracker #152: traffic report API](https://github.com/ChainSafe/canton-extending-mainnet/issues/152)
- [Tracker #155: paymaster purchase accounting](https://github.com/ChainSafe/canton-extending-mainnet/issues/155)
- [Tracker #163: ActivityRecorder integration](https://github.com/ChainSafe/canton-extending-mainnet/issues/163)
- [Tracker #159: end-to-end paymaster test](https://github.com/ChainSafe/canton-extending-mainnet/issues/159)
- [Upstream Splice PR #8449: ActivityRecorder](https://github.com/canton-network/splice/pull/8449)

## 6. Next research step

The interface and implementation map define a concrete requirements gap. The next step is to formalise the minimum viable reconciliation algorithm and test its state transitions against actual evidence statuses: complete report set, missing interval, undetermined interval, stale agreement version, not-yet-due smoothing tranche, short payment, duplicate burn allocation and reward-record absence. Keep all data synthetic until a real, authorised end-to-end dataset is available.
