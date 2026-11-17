# End-to-End Verification Audit: CIP-0132 and Community Research Grant

**Checked:** 17 November 2026  
**Repository:** `BigWave45/canton-research-lab`  
**Status:** source-level verification; not a production deployment audit

## 1. Executive finding

CIP-0132 is a **Proposed** specification for Phase 1 of the Dedicated Synchronizer Paymaster Model, not an approved CIP and not evidence of a live MainNet deployment. The public implementation work is partial: paymaster purchase and Scan/SV handling PRs are merged in the multi-sync feature fork, but the traffic-report API PR remains open; the ActivityRecorder implementation PR remains draft/open; and the end-to-end test issue remains open.

The strongest verified research problem is therefore not “Canton has a broken paymaster.” It is the design and verification gap between (i) traffic measurement, (ii) an off-ledger operator/paymaster settlement agreement, (iii) public CC burn and (iv) reward issuance, in a proposal whose first phase explicitly relies on trust.

## 2. CIP status and specification

Primary source: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md

The current CIP file states:
- Status: Proposed.
- Created: 9 November 2026.
- Proposed: 16 November 2026.
- Requires CIP-0104 and CIP-0129.
- Phase 1 uses a trusted dedicated synchronizer operator, a traffic-report API split into ten-minute intervals, and a designated paymaster that burns CC post-hoc on the Global Synchronizer.
- The report-to-burn link is off-ledger. Discounts and smoothing/delays may be governed by off-ledger agreements.
- Activity records are made through CIP-0104's ActivityRecorder extension hook.
- The paymaster receives the corresponding validator and app rewards in this phase; more granular attribution is deferred.
- The CIP explicitly says the operator and paymaster are trusted to report and burn correctly. It says malicious parties could under- or over-report, while on-chain enforcement makes rewards commensurate with the burn actually made.

Interpretation: the on-ledger guarantee described here binds reward issuance to burn/activity inputs as specified. It does not by itself prove that actual private synchronizer consumption was completely measured, accurately reported, or fully paid under the off-ledger agreement.

## 3. Implementation status as of 17 November 2026

### 3.1 Merged paymaster purchase path

- `canton-network/splice-multi-sync#100`: merged 12 November 2026. Adds Daml paymaster traffic purchase support.
  https://github.com/canton-network/splice-multi-sync/pull/100
- `canton-network/splice-multi-sync#104`: merged 12 November 2026. Adds Scan and SV app handling for registered synchronizers and paymaster MemberTraffic contracts.
  https://github.com/canton-network/splice-multi-sync/pull/104

The merged changes validate the registered paymaster, synchronizer ID, migration ID and traffic-purchase parameters, and create/merge MemberTraffic contracts. PR #100 explicitly notes that #89 and #100 had not been deployed to a long-running network and that no store had a registration or paymaster purchase to backfill at the time described. Therefore “merged in a feature fork” must not be represented as “deployed on MainNet.”

### 3.2 Traffic-report API remains open

- `splice-multi-sync#111`: open as of the check; created 13 November, updated 17 November.
  https://github.com/canton-network/splice-multi-sync/pull/111
- Tracker issue `ChainSafe/canton-extending-mainnet#152`: open.
  https://github.com/ChainSafe/canton-extending-mainnet/issues/152

The PR describes a JWT-authenticated endpoint returning traffic totals for completed ten-minute intervals with statuses including Ok, Undetermined and CannotProvide. It computes interval totals from sequencer traffic-control state and stores results to survive pruning. It also documents a logical-synchronizer-upgrade boundary: a successor sequencer lacks the prior counter history; intervals spanning an upgrade that were not stored can return CannotProvide.

The tracker acceptance criteria include equality across all four operator apps on a four-node synchronizer. The PR snapshot inspected does not establish that this acceptance criterion has passed. Treat cross-node equality as unverified, not as a proven defect.

### 3.3 ActivityRecorder integration remains incomplete

- Upstream `canton-network/splice#8449`: draft/open as of 17 November.
  https://github.com/canton-network/splice/pull/8449
- Tracker issue `ChainSafe/canton-extending-mainnet#163`: open.
  https://github.com/ChainSafe/canton-extending-mainnet/issues/163

Issue #163 says the purchase can occur, but the paymaster's app and asset activity are not yet recorded through the CIP-0104 hook in that implementation snapshot. It identifies the hook integration as a follow-up dependency. Do not describe the full reward integration as complete.

### 3.4 End-to-end test remains open

- Tracker issue `ChainSafe/canton-extending-mainnet#159`: open.
  https://github.com/ChainSafe/canton-extending-mainnet/issues/159

Its requested test covers registration by SV vote, participant transactions, report retrieval, paymaster payment and resulting activity records. The issue depends on #151, #152, #154, #155 and #163. The open status means the full flow was not demonstrated by that tracker item at the time checked.

### 3.5 Payment completeness gap is explicitly recorded by implementers

- Tracker issue `ChainSafe/canton-extending-mainnet#155`: closed after the purchase-path work.
  https://github.com/ChainSafe/canton-extending-mainnet/issues/155

Its context states: “Nothing checks the paid amount against the report, and the paymaster may pay for less than was used.” It also says SVs can archive a misbehaving paymaster's registration. This is an explicit design/implementation limitation in the tracked work, with governance action as a response; it is not evidence that any real paymaster has underpaid.

## 4. CIP-0104 reward context

Primary source: https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md

CIP-0104 is Approved (27 October 2026). It bases Global Synchronizer app activity on sequencer and mediator data and includes an extension hook for recording activity not directly visible through those data sources. CIP-0132 uses that hook to attribute dedicated-synchronizer purchase-derived activity to the paymaster. The hook's presence in an approved specification does not mean the dedicated-synchronizer integration is fully implemented or deployed; the open/draft PR and tracker states above remain relevant.

## 5. Merkle proof-of-concept status

- Tracker issue `ChainSafe/canton-extending-mainnet#47`: closed, but its own description says the work was Daml/Daml Script tests only, with no Scala automation or end-to-end wiring.
  https://github.com/ChainSafe/canton-extending-mainnet/issues/47
- The issue records assumptions and follow-up items for report totals, purchased-traffic bounds and expansion. Its completion status means the scoped PoC task was closed, not that the system shipped as a production reward mechanism.

The PoC is a useful design precedent for analysing reward bounds and proof expansion. It is not evidence of an operational deployed Merkle reward architecture.

## 6. Grant programme verification

Official announcement:
https://canton.foundation/introducing-the-canton-community-research-grants/

Verified directly from the official announcement:
- Published 4 November 2026.
- November consideration window: original research/education publicly published 1–30 November.
- Sharing on X with @CantonFdn and #CantonResearchNov26 is optional; work shared by 4 December may be reviewed in connection with November.
- Up to 50,000 CC per month is a programme-level maximum, not a guaranteed pool or individual award. The Foundation may award less or nothing.
- Written research and video are eligible. Listed subject areas include tokenomics/network economics, technical research, institutional use cases and ecosystem analysis.
- No Foundation membership is required.
- The Foundation identifies research quality, educational/community value and contribution to public understanding as considerations, not a fixed scoring rubric.
- Positive coverage is not required.
- Before any grant: eligibility requirements, identity verification/KYC and sanctions screening must be met; a grant agreement must be signed; relevant financial interests/sponsorships must be disclosed; recipients must disclose receipt of a grant.
- The announcement says Terms and Conditions were expected on or before 15 November and that no grant will be made before publication.

**Unresolved:** In this verification pass, no separate official Terms and Conditions document or official terms link was located from the announcement or indexed official Foundation pages searched. The announcement still refers to the terms as expected. Therefore eligibility by jurisdiction, payment rails, tax treatment, IP/licensing, confidentiality, liability and detailed KYC requirements remain unverified. Do not assume a Nigeria-based individual is eligible or ineligible. Obtain the actual terms from the Foundation before relying on the grant.

## 7. Hypothesis status after verification

| Hypothesis | Verification status | Required correction |
|---|---|---|
| H1: agreement-aware cumulative reconciliation beats interval equality | Supported as a sound test design because CIP-0132 explicitly permits discounts and smoothing/delays; no empirical result yet | Simulate proposal-permitted settlement patterns; do not claim observed accuracy |
| H2: Merkle commitment does not prove source completeness | Sound cryptographic distinction; PoC status verified as non-production | Test omitted-before-commitment events and split views; avoid implying Canton currently uses the PoC |
| H3: public aggregate burn can independently reconcile private consumption | Not established | CIP-0132 says report-to-burn link is off-ledger; test whether public burn plus signed report commitments is sufficient, and state what remains unknowable |
| H4: audit incentives can make truthful reporting rational | Theoretical only | Build principal-agent model with enforceable sanctions, audit probability, detection and participation constraints |
| H5: accountability has privacy/latency/cost trade-offs | Plausible but unmeasured | Compare architectures under common threat model and benchmark costs before claiming quantified trade-offs |

## 8. Research scope correction

A more defensible candidate research question is:

**What verifiable accounting guarantees can be added to the proposed dedicated-synchronizer paymaster model, and what are their economic, privacy and operational costs?**

The study should compare the current trusted Phase 1 proposal with staged options:
1. signed, sequence-continuous interval reports and durable retention;
2. agreement-aware cumulative report-to-burn reconciliation;
3. independent sampling/challenge and governance enforcement;
4. cryptographic commitments or attestations for stronger report integrity;
5. later granular reward attribution, only if the protocol design advances to that phase.

Do not present any option as an existing Canton feature unless implementation evidence establishes it.

## 9. Immediate next steps

1. Obtain the actual grant Terms and Conditions from the Foundation and check personal eligibility/payment feasibility.
2. Freeze a dated copy of CIP-0132, PR #111, PR #8449 and tracker issues #152, #155, #159 and #163.
3. Build a state-transition diagram separating report creation, off-ledger agreement calculation, CC burn, activity-record creation and reward issuance.
4. Implement Experiment A (agreement-aware reconciliation) with synthetic fixtures and unit tests.
5. Seek clarification from maintainers on the report API's participant-leave semantics, LSU boundary handling and four-node equality status before making implementation-quality claims.
