# Verification Audit: CIP-0132 Paymaster Pipeline and Community Research Grant

**Verification date:** 17 November 2026  
**Repository:** private Canton research lab  
**Status:** source-level audit; not a deployment audit

## 1. Scope

This retrospective audit checks two gates for the selected research programme:

1. Whether the proposed CIP-0132 paymaster pipeline is implemented end-to-end in public source as of the verification date.
2. Whether the official Canton Community Research Grant Terms and Conditions and applicant eligibility can be verified from public official sources.

The audit distinguishes proposal text, merged code, open/draft work, issue-tracker acceptance criteria and deployment evidence.

## 2. Protocol trace: intended flow versus observed implementation

### Stage A — Governance registration

CIP-0132 proposes an on-ledger `RegisteredSynchronizer` with synchronizer ID, designated paymaster and maximum app/asset activity weights. SV governance can update or archive the registration.

The paymaster purchase implementation in `canton-network/splice-multi-sync` PR #100 and Scan/SV integration PR #104 are merged (12 November 2026). The PR descriptions say they must be deployed together. The code checks that the payer is the registered paymaster, synchronizer IDs match, the synchronizer is not a required synchronizer, migration ID is zero, member ID is empty, and activity weights stay within configured bounds.

Important limitation: PR #100's description states that the relevant registration/purchase changes had not been deployed to a long-running network at the time of that PR. Merged source is not proof of MainNet deployment.

Sources:
- https://github.com/canton-network/splice-multi-sync/pull/100
- https://github.com/canton-network/splice-multi-sync/pull/104

### Stage B — Traffic measurement and report

CIP-0132 specifies an operator API returning total synchronizer traffic in aligned ten-minute intervals, within the sequencer pruning window.

The implementation PR #111, “serve traffic reports from the sync operator app”, was still open on 17 November 2026. It replaces PR #103, which was closed unmerged. PR #111 reads participant cumulative extra-traffic counters at interval boundaries, uses JWT authentication, and returns `Ok`, `Undetermined` or `CannotProvide` statuses. Its 17 November review thread records that the author dropped the report store, trigger and migration because dedicated-synchronizer sequencers were not being pruned at that time; the handler reads the sequencer on each request. The PR adds tests for a completed interval and an interval spanning an LSU, but this is still an open PR, not merged/deployed evidence.

The corresponding tracker issue #152 remains open. Its acceptance criteria include:
- one total per aligned ten-minute interval matching participant-consumed traffic;
- unfinished intervals not returned as final;
- all four operator apps on a four-node synchronizer returning identical totals;
- persistence sufficient to survive pruning and upgrades.

The PR's visible test additions cover a single operator's report calculation and an LSU-spanning interval using predecessor and successor sequencers. They do not establish that all four operator apps on a four-node synchronizer return identical totals, which remains an acceptance criterion in open tracker issue #152. The PR also documents that a successor sequencer does not carry predecessor counter history; an interval spanning an upgrade can be unavailable if not queried while the required predecessor state is accessible.

This is a material research boundary: the report API was work in progress, not a verified production data feed.

Sources:
- https://github.com/canton-network/splice-multi-sync/pull/111
- https://github.com/ChainSafe/canton-extending-mainnet/issues/152

### Stage C — Payment and CC burn

CIP-0132 makes the link between the off-ledger traffic report and the paymaster's on-ledger CC burn an agreement between the operator and paymaster. Discounts and smoothing/delays may apply. The proposal gives examples of weekly or rolling-window smoothing.

The merged PRs #100 and #104 implement the purchase path and store handling. The implementation tracker issue #155 is closed, but its description explicitly states that nothing checks the amount paid against the traffic report and the paymaster may pay less than the amount used. The proposed response is that SVs can archive a misbehaving registration. This is governance intervention, not automatic period-by-period report-to-payment equality enforcement.

Consequently:
- do not test ten-minute report amount against immediate ten-minute burn as if equality were required;
- define the commercial discount, conversion and smoothing agreement first;
- reconcile over the permitted cumulative settlement window;
- distinguish an on-ledger CC burn from proof that all consumed traffic was measured and paid.

Sources:
- https://github.com/ChainSafe/canton-extending-mainnet/issues/155
- https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md

### Stage D — Reward recording and issuance

CIP-0132 specifies validator rewards corresponding to the burn and app/asset activity records through CIP-0104's `ActivityRecorder_DsoRecordActivity` extension hook.

The implementation is not yet complete in the source snapshot:
- ChainSafe issue #163 remains open and says the purchase does not yet record paymaster app/asset activity through the hook.
- The issue says upstream Splice PR #8449 is a draft and must merge before the fork can integrate the hook.
- Splice PR #8449 remained open and draft on 17 November.
- ChainSafe issue #159, the end-to-end test of registration → participant traffic → report → paymaster burn → activity records, remains open and depends on #152, #155 and #163.
- The validator reward coupon is separate and remains generated by the CC burn path; app activity records are a distinct mechanism.

Therefore, the specification's intended app-reward integration must not be described as an end-to-end implemented and tested flow. The code/issue evidence supports a partially implemented paymaster purchase path, a report API still under review, and a pending app-activity hook plus end-to-end test.

Sources:
- https://github.com/ChainSafe/canton-extending-mainnet/issues/163
- https://github.com/ChainSafe/canton-extending-mainnet/issues/159
- https://github.com/canton-network/splice/pull/8449

## 3. Hypothesis-by-hypothesis verification

| Hypothesis | What public evidence establishes | What remains unavailable | Current research treatment |
|---|---|---|---|
| H1: window-aware reconciliation | CIP-0132 permits discounts and delayed/smoothed burns; issue #155 says report/payment equality is not checked | Actual bilateral discount/smoothing agreements and linked report/burn histories | Model-testable; do not claim empirical underpayment |
| H2: commitments do not prove source completeness | Established cryptographic property; relevant prior art includes Certificate Transparency and Merkle proof-of-liabilities attacks | Actual CIP-0132 commitment scheme: none specified in Phase 1 | Keep as general design result, not a Canton implementation finding |
| H3: aggregate public reconciliation under privacy | CIP-0132 report is an operator API; burn is on-ledger; linkage is off-ledger | Public report publication, signed commitments, accessible paired report/burn data | Reframe: test what an authorised auditor can reconcile, not what any public observer can verify |
| H4: audit incentives | CIP-0132 explicitly relies on operator/paymaster trust; issue #155 points to SV registration archival as governance enforcement | Actual contracts, collateral/penalties, audit probabilities and dispute process | Principal-agent model with parameters labelled hypothetical unless documented |
| H5: assurance/privacy/cost trade-off | Phase 1 trust model and proposed later tightening establish a design comparison | Operational benchmarks and concrete later-phase implementation | Comparative architecture and synthetic cost model |

### Corrections to the prior hypothesis document

1. H3 currently overstates “public” reconciliation. The traffic-report endpoint uses JWT authentication and is an operator API. The public CC burn alone does not expose the off-ledger report-to-burn agreement. Reframe H3 around authorised auditors and separately analyse what the public can verify.
2. H2 should not imply Canton Phase 1 uses a Merkle commitment. CIP-0132 Phase 1 does not specify one. The Merkle reward-reporting work in ChainSafe issue #47 is a separate earlier proof of concept, not the current CIP-0132 paymaster implementation.
3. H4 should distinguish governance remedies (e.g. archival of registration) from automatic economic penalties, collateral slashing or cryptographic detection. Do not assume the latter exist.
4. H1 must use contractually permitted settlement windows, discounts and smoothing. The proposal explicitly allows delayed burn, so an interval mismatch alone is not a shortfall.
5. Separate validator rewards from app/asset activity records. The CC burn produces a validator reward coupon; the app/asset hook is a separate integration and is not yet shown as complete in the reviewed PR/issues.

## 4. CIP status and chronology

- CIP-0129 is Approved (23 October 2026). It states that universal burn rollout is estimated for Q1 2027 and volume/commitment pricing for Q3 2027; the dates are estimates, not deadlines. It says the reference implementation is “None yet” and leaves pricing details to a second CIP.
- CIP-0132 is Proposed (created 9 November, proposed 16 November 2026), not approved in the reviewed source.
- CIP-0104 is Approved. Its current CIP header says Approved 27 October 2026. This corrects earlier notes that gave a different approval date.
- No evidence in this audit establishes that the CIP-0132 system is deployed on Canton MainNet.

Sources:
- https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md
- https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md

## 5. Community Research Grant verification

The official Canton Foundation announcement, dated 4 November 2026, establishes:

- original research and educational content must be publicly published between 1 and 30 November 2026 to be considered for the November cycle;
- work shared on X by 4 December may be reviewed in connection with November; sharing is optional;
- tag `@CantonFdn` and hashtag `#CantonResearchNov26` are the specified sharing convention;
- Foundation membership is not required;
- written research and video are eligible;
- examples explicitly include tokenomics/network economics, technical research, privacy, institutional use cases, settlement, payments and ecosystem analysis;
- the stated considerations are research quality, educational/community value and contribution to public understanding; these are not a scoring rubric;
- the program is discretionary, not a contest or promise of a grant; up to 50,000 CC per month is a programme maximum, not a personal award;
- recipients must pass identity verification/KYC and sanctions screening, satisfy applicable legal, tax and payment requirements, sign a grant agreement and disclose the grant;
- favourable coverage or endorsement is not required.

**Terms and Conditions verification remains unresolved.** The official announcement says they were expected on or before 15 November and that no grant can be made before they are published. Searches of the official Foundation domain and the linked official announcement did not surface a separate Terms and Conditions document as of 17 November. This is not proof that no document exists; it means we have not verified it. Therefore the following remain unknown:
- eligible countries/residency and any restricted jurisdictions;
- individual versus entity applicant rules;
- exact age and legal-capacity requirements;
- identity documents and verification provider;
- sanctions screening scope;
- tax forms/withholding and payment mechanics;
- whether recipients need a Canton wallet or other payout setup;
- intellectual-property licence, warranties and indemnities;
- grant agreement obligations, confidentiality and dispute terms.

The user is based in Nigeria, so country eligibility and payment access are material and must be checked against the actual Terms before treating the programme as a viable funding route. Do not infer Nigeria is eligible or ineligible from the announcement.

Official announcement:
https://canton.foundation/introducing-the-canton-community-research-grants/

## 6. Research design status

The research remains viable as a proposal-level accounting-assurance study, but not yet as an empirical evaluation of live Canton paymaster accuracy. The controlling question remains the one recorded in `research-scope-correction.md`: how privacy-preserving financial infrastructure can make its economic accounting independently verifiable. The narrower operational question and evidence map are in `research/README.md` and `research/research-evidence-map.md`.

The title below is an earlier working-title candidate only. It does not replace the controlling question, and no final title has been selected:

**“Accountability Across a Privacy Boundary: Reconciling Private Synchronizer Traffic with Public Payment and Reward Records.”**

The research package should contain:
1. an implementation-grounded state-transition and trust-boundary map;
2. a reproducible agreement-aware reconciliation simulator;
3. adversarial tests for missing intervals, counter discontinuity, duplicate/altered reports, upgrade/pruning gaps and split views;
4. a principal-agent model of audit/enforcement incentives;
5. a privacy/assurance/cost comparison of staged controls.

Do not claim that current Canton operators misreport, that a vulnerability is exploited, that Phase 1 has deployed, or that public observers can independently match private traffic to burns.

## 7. Immediate next actions

1. Revisit the open PRs/issues after the planned 20 November backend release milestone and check whether #111, #163, #159 and #8449 have changed status.
2. Ask the Foundation directly for the official Community Research Grant Terms and whether a Nigeria-resident individual can receive CC grants, what KYC and payout route are supported, and what IP/disclosure terms apply.
3. Update the hypotheses document to correct H3 and distinguish validator rewards from app rewards.
4. Keep the research repository private until the work is ready for public publication in the programme window.
