# Manuscript Reference Register

**Manuscript:** *Verifiable Accounting for Dedicated Synchronizer Paymasters: Guarantees, Trust Boundaries, and Trade-offs*  
**Register status:** Working register; not yet the final bibliography.  
**Repository snapshot inspected:** `BigWave45/canton-research-lab`, default branch `main`, tree SHA `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`.  
**Register prepared:** 18 November 2026.

This register separates primary protocol sources, implementation evidence, and the authors' own research artefacts. A source supports only the claims listed against it. A proposed CIP, open pull request, draft pull request, synthetic experiment, or internal prototype must not be cited as proof of production deployment.

## A. Primary protocol and technical sources

### [1] Canton Improvement Proposal 0104 — Traffic-Based App Rewards
Canton Foundation. *CIP-0104: Traffic-Based App Rewards*. Original CIP approved 12 February 2026. The amendment aligning the proposal with Featured App Guidance 2.0b was approved by Super Validator node owners on 27 October 2026; the pinned revision below reflects the amended text.  
Version used for the dedicated-synchronizer extension-hook relationship: https://github.com/canton-foundation/cips/blob/92df641487c5e465dad5ea8d03245d3b9b328523/cip-0104/cip-0104.md  
Current proposal location: https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md  
**Supports:** the Global Synchronizer traffic-based application reward mechanism; the ActivityRecorder_DsoRecordActivity extension hook; the distinction between existing Global Synchronizer measurement and proposed dedicated-synchronizer integration.  
**Use in manuscript:** Sections 1, 2, 6.1, 6.5, 8.5, 9.1 and 9.6.  
**Qualification:** cite the pinned version when describing the hook required by CIP-0132. Do not imply that the dedicated-synchronizer integration was production-deployed merely because the underlying CIP-0104 mechanism is approved.

### [2] Canton Improvement Proposal 0129 — Universal Burn and Synchronizer Pricing
Canton Foundation. *CIP-0129: Universal Burn and Synchronizer Pricing*. Approved 23 October 2026.  
https://github.com/canton-foundation/cips/blob/8e694e509c47ecb59e5731289882b350e3186372/cip-0129/cip-0129.md  
**Supports:** the universal-burn and synchronizer-pricing framework; dedicated-synchronizer traffic reporting and reward attribution context; the trust placed in operator reports in the initial design; the stated limits of aggregate payment-based reward constraints.  
**Use in manuscript:** Sections 1, 2, 3, 6.1, 7.1, 8.1, 8.3, 8.5 and 9.1.  
**Qualification:** this permalink is pinned to the 23 October 2026 approval commit. Approval of CIP-0129 must not be conflated with approval or deployment of CIP-0132.

### [3] Canton Improvement Proposal 0132 — Dedicated Synchronizer Paymaster Model
Canton Foundation. *CIP-0132: Dedicated Synchronizer Paymaster Model*. Created 9 November 2026; proposed 16 November 2026; status Proposed in the reviewed revision.  
Pinned revision: https://github.com/canton-foundation/cips/blob/538adf41789fa971f3ad397595de4549dd507e79/cip-0132/cip-0132.md  
**Supports:** Phase 1 ten-minute aggregate traffic reports; sequencer record-time basis; designated paymaster; off-ledger report-to-burn and discount relationship; operator/paymaster trust assumptions; proposed use of the CIP-0104 activity-recording hook; initial paymaster reward attribution; later-phase expectation of more granular attribution.  
**Use in manuscript:** Sections 1–5, 6.1, 6.2, 6.5, 7.1, 8.1–8.7 and 9.1.  
**Qualification:** status is Proposed in this pinned revision. Do not describe the complete model as approved or production-deployed.

### [4] Canton Network — Privacy Model
Canton Network. *Privacy Model*, developer documentation.  
https://github.com/canton-network/cf-docs/blob/main/docs-main/appdev/deep-dives/privacy-model.mdx  
**Supports:** Canton selective-disclosure model and the separation between transaction payload visibility, participant views, validator visibility and synchronizer routing/metadata.  
**Use in manuscript:** Sections 6.2, 6.5, 8.4 and 9.3.  
**Qualification:** the general Canton privacy model does not establish the actual access controls of the proposed CIP-0132 accounting interface. Pin a commit or record an access date for final publication.

## B. Implementation and governance evidence

### [5] Canton Network. Pull request #111 — Traffic report API and interval calculation
Canton Network, `splice-multi-sync`. Pull request #111.  
https://github.com/canton-network/splice-multi-sync/pull/111  
**Supports:** the reviewed proposed `GET /v0/traffic-report` API; ten-minute interval semantics; aggregate traffic calculation from sequencer counter snapshots; report statuses; participant lifecycle behaviour in the reviewed code; pruning and upgrade-boundary limitations.  
**Use in manuscript:** Sections 2, 4.3, 4.4, 9.1 and 9.5.  
**Qualification:** open at the 17 November 2026 audit snapshot. This is proposed implementation evidence, not proof of deployed MainNet behaviour. The implementation audit states that PR #111 replaces the earlier PR #103 design.

### [6] Canton Network. Pull request #8449 — ActivityRecorder implementation
Canton Network, `splice`. Pull request #8449.  
https://github.com/canton-network/splice/pull/8449  
**Supports:** proposed ActivityRecorder contract and activity-recording implementation details reviewed in the source snapshot.  
**Use in manuscript:** Sections 2, 6.1, 8.5 and 9.1.  
**Qualification:** draft at the 17 November 2026 audit snapshot. Do not cite it as a merged or deployed end-to-end reward path.

### [7] ChainSafe. Issue #155 — Paymaster purchase path and amount checking
ChainSafe, `canton-extending-mainnet`. Issue #155.  
https://github.com/ChainSafe/canton-extending-mainnet/issues/155  
**Supports:** the issue's stated acceptance/design context that the purchase path does not itself compare the amount paid against the traffic report, and the described governance response to misbehaving registration.  
**Use in manuscript:** Sections 2, 5, 8.3, 8.5 and 9.1.  
**Qualification:** issue text is implementation-tracker evidence, not proof of actual underpayment or production misconduct. Cite the exact issue state and access date.

### [8] Canton Network. Pull request #103 — Earlier traffic-report implementation
Canton Network, `splice-multi-sync`. Pull request #103.  
https://github.com/canton-network/splice-multi-sync/pull/103  
**Supports:** historical implementation context only, if the manuscript explicitly discusses the earlier database-backed interval-report trigger/store.  
**Use in manuscript:** only where the historical PR #103 design itself is being discussed.  
**Qualification:** the current implementation audit says PR #111 explicitly replaces PR #103. Do not cite PR #103 as the source for behaviour observed in PR #111. Section 4.3 must be reconciled with this source history before final citation insertion.

## C. Research artefacts and reproducibility sources

All paths below refer to the inspected research-repository snapshot at commit `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`. These are the authors' own analytical artefacts, not independent external validation.

Base repository permalink: https://github.com/BigWave45/canton-research-lab/tree/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c

### [9] Accounting properties and threat model
`research/accounting-properties-and-threat-model.md`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/accounting-properties-and-threat-model.md  
**Supports:** actors, threat model, accounting properties P1–P8, evidence boundaries and explicit limits of each property.  
**Use:** Sections 3, 4, 5, 8 and 9.

### [10] Traffic-report implementation audit
`research/traffic-report-implementation-audit.md`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/traffic-report-implementation-audit.md  
**Supports:** the PR #111 source-code observations, report status semantics, participant departure behaviour, pruning/upgrade boundaries and reward-path evidence status.  
**Use:** Sections 4.3–4.4, 6.1, 8.5 and 9.1.

### [11] Implementation evidence mapping
`research/implementation-evidence-mapping-2026-11-17.md`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/implementation-evidence-mapping-2026-11-17.md  
**Supports:** status classification of proposed/present/partial/unverified interface properties; report API, settlement binding, burn mapping and reward integration evidence gaps.  
**Use:** Sections 2–5, 8 and 9.

### [12] Architecture comparison: CIP-0104, CIP-0129 and CIP-0132
`research/cip-0104-0129-0132-architecture-comparison.md`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/cip-0104-0129-0132-architecture-comparison.md  
**Supports:** chronology and functional distinctions among the three CIPs; Phase 1 paymaster-level reward attribution versus later granular attribution.  
**Use:** Sections 1, 2, 6.1, 8.5 and 9.1.

### [13] Reward attribution integrity
`research/reward-attribution-integrity.md`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/reward-attribution-integrity.md  
**Supports:** analytical distinction between aggregate reward caps and correct participant-level attribution; scope correction for Phase 1; candidate attribution mechanisms.  
**Use:** Sections 6.1, 8.5 and 9.6.  
**Qualification:** this document contains an earlier hypothesis and explicit scope correction. Cite only the corrected aggregate paymaster-to-reward pipeline analysis, not the superseded assumption that Phase 1 performs granular participant-level reward distribution.

### [14] Privacy disclosure matrix and aggregate leakage experiment
`research/privacy-disclosure-matrix-and-leakage-experiment.md`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/privacy-disclosure-matrix-and-leakage-experiment.md  
**Supports:** proposed disclosure tiers, threat-model boundaries, synthetic aggregate leakage analysis and limitations.  
**Use:** Sections 6.2–6.6, 8.4 and 9.3.

### [15] Comparative assurance model specification
`research/comparative-assurance-model-specification.md`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/comparative-assurance-model-specification.md  
**Supports:** four assurance architectures, accounting chain, scenario definitions, evaluation dimensions and model limitations.  
**Use:** Sections 7.1, 7.4–7.5 and 8.

### [16] Aggregate linear leakage analysis
`analysis/aggregate_linear_leakage.py`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/aggregate_linear_leakage.py  
**Supports:** exact-rational row-space method for testing unique identifiability of participant values from linear combinations of aggregate releases.  
**Use:** Section 6.3.  
**Qualification:** cite alongside the synthetic fixture and clearly state the observer's cohort-membership knowledge assumption.

### [17] Aggregate disclosure experiment
`analysis/aggregate_disclosure_experiment.py`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/aggregate_disclosure_experiment.py  
**Supports:** executable nested-cohort differencing example with a minimum cohort threshold.  
**Use:** Section 6.3.

### [18] Adversarial accounting tests
`analysis/adversarial_accounting_tests.py`  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/adversarial_accounting_tests.py  
**Supports:** synthetic omitted-participant counterexample, split-view comparison and reward-bound checks.  
**Use:** Sections 3–5 and 8.  
**Qualification:** these are research tests, not production integration tests.

### [19] Comparative assurance model code
`analysis/comparative_assurance_model.py` and `analysis/integrated_assurance_comparison.py`  
https://github.com/BigWave45/canton-research-lab/tree/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis  
**Supports:** scenario-based comparison of what each assurance architecture can detect or establish, plus qualitative ratings of assurance, disclosure, residual trust, burden and latency.  
**Use:** Sections 7.1 and 7.4.  
**Qualification:** these files do not, in the inspected snapshot, reproduce the ICU totals reported in Section 7.2.

## D. Citation map by manuscript section

| Manuscript section | Main source keys | Citation purpose |
|---|---|---|
| Abstract | [1]–[3], [9], [14]–[19] | Summarise protocol basis, research methods and the bounded nature of results |
| 1. Introduction | [1]–[3] | Protocol chronology, proposal status and motivation |
| 2. Protocol model | [1]–[3], [5]–[7], [12] | Separate CIP design from implementation evidence |
| 3. Threat model and invariants | [3], [9], [18] | Protocol trust assumptions and research-defined threats/invariants |
| 4. Measurement assurance | [3], [5], [10], [11], [18] | Reporting contract, implementation observations and synthetic omission example |
| 5. Settlement assurance | [3], [7], [9], [11], [15], [18], [25], [26] | Off-ledger linkage, settlement properties, prototype checks and evidence limits |
| 6. Reward attribution and privacy | [1]–[4], [6], [13], [14], [16], [17], [18], [25], [26] | Reward hook, Phase 1 attribution, privacy model and explicitly bounded prototype evidence |
| 7. Economic and operational trade-offs | [3], [15], [19], [27] | Qualitative architecture comparison; no reproducible numerical cost model exists in the inspected snapshot |
| 8. Discussion | [1]–[19] as relevant | Synthesis; cite the source for each specific factual or methodological claim rather than attaching a blanket citation |
| 9. Limitations and future research | [1]–[19] as relevant | Snapshot, implementation status, prototype and experiment limitations |
| 10. Conclusion | [1]–[3], [9], [14]–[19] | Restate only results already supported in the body |

### [25] Settlement manifest validator
BigWave45. `canton-research-lab`. `analysis/settlement_manifest_validator.py`, repository snapshot `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`.
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/settlement_manifest_validator.py
**Supports:** interval coverage, report status, agreement-version and digest presence, duplicate and cross-settlement burn checks, allocation references and payment residual calculation.
**Does not support:** source measurement completeness, legal authority of agreement signers or reward-attribution validation.

### [26] Settlement manifest validator tests
BigWave45. `canton-research-lab`. `tests/test_settlement_manifest_validator.py`, repository snapshot `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`.
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/tests/test_settlement_manifest_validator.py
**Supports:** test cases for complete manifests, missing intervals, gaps, duplicate burns, reused burn IDs, wrong settlement assignment, payment mismatch, uncovered windows, missing agreement versions and missing report digests.
**Does not support:** the full reward-attribution checklist or production integration.

### [27] Integrated qualitative assurance comparison
BigWave45. `canton-research-lab`. `analysis/integrated_assurance_comparison.py`, repository snapshot `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`.
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/integrated_assurance_comparison.py
**Supports:** qualitative architecture ratings for measurement assurance, payment completeness, allocation assurance, reward attribution, disclosure, residual trust, implementation burden, latency and dispute resolution.
**Qualification:** ratings are analytical judgements, not measured performance or probabilities. This file does not support numerical ICU costs.

## E. Resolved audit issues and remaining publication checks

The three substantive issues from the initial source audit have been resolved in `research/manuscript-audit-resolution-2026-11-18.md`. Apply the stated replacement text to the manuscript before inserting citations.

1. **Section 4.3:** attribute the participant-departure observation to PR #111, not PR #103. PR #111 replaces the earlier design and was open at the 17 November 2026 snapshot. Cite [5] and [10]. PR #103 [8] is historical context only.
2. **Section 6.1:** do not describe the full reward-attribution checklist as an implemented I-10 model. The located formal property register is P1–P8; P6 is only a reward-budget bound. Describe the full checklist as a proposed validation requirement and distinguish the narrower prototype checks in [18], [25] and [26].
3. **Section 7.2:** remove the unsupported ICU totals and break-even arithmetic. The current repository does not contain the model or parameters that generated them. Use qualitative, explicitly unmeasured cost drivers supported by [15], [19] and [27].
4. **Section 6.3:** retain the qualification that the four-participant example is hand-derived, not an executable fixture. The executable row-space experiment is [16] and [17].
5. **CIP-0129 permalink:** resolved. Reference [2] now points to the 23 October 2026 approval commit `8e694e509c47ecb59e5731289882b350e3186372`.
6. **Implementation status:** cite PR #100 and #104 as merged feature-fork code, PR #111 as open, PR #8449 as draft, and tracker issues #152, #155, #159 and #163 with the 17 November 2026 snapshot qualification. None of this is proof of MainNet deployment.
7. **Prototype test count:** attach a test count only to a precise repository commit and reproducible CI/local run. The isolated 29-test result in [new audit evidence] is not a full repository-suite run and must not be presented as one.
8. **External literature:** do not add generic academic references for appearance. Add a source only when the manuscript makes a substantive claim that depends on it.

## F. Final citation style recommendation

Use numbered citations in square brackets, for example `[1, 3]`, with a numbered References section. Cite the primary CIP for protocol requirements, the exact PR/issue for implementation observations, and the repository artefact for the authors' own experiments. Where a sentence combines multiple evidence classes, cite each class separately.

The final bibliography should keep external sources and the authors' own reproducibility artefacts distinguishable. This register is an editorial working document; it is not itself the paper's final References section.
