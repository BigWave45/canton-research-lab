# Manuscript Reference Register

**Manuscript:** *Verifiable Accounting for Dedicated Synchronizer Paymasters: Guarantees, Trust Boundaries, and Trade-offs*  
**Register status:** Working register; not yet the final bibliography.  
**Repository snapshot inspected:** `BigWave45/canton-research-lab`, default branch `main`, tree SHA `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`.  
**Register prepared:** 18 November 2026.

This register separates primary protocol sources, implementation evidence, and the authors' own research artefacts. A source supports only the claims listed against it. A proposed CIP, open pull request, draft pull request, synthetic experiment, or internal prototype must not be cited as proof of production deployment.

## A. Primary protocol and technical sources

### [1] Canton Improvement Proposal 0104 — Traffic-Based App Rewards
Canton Foundation. *CIP-0104: Traffic-Based App Rewards*. Approved 12 February 2026; amended text reviewed in the November 2026 source snapshot.  
Version used for the dedicated-synchronizer extension-hook relationship: https://github.com/canton-foundation/cips/blob/92df641487c5e465dad5ea8d03245d3b9b328523/cip-0104/cip-0104.md  
Current proposal location: https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md  
**Supports:** the Global Synchronizer traffic-based application reward mechanism; the ActivityRecorder_DsoRecordActivity extension hook; the distinction between existing Global Synchronizer measurement and proposed dedicated-synchronizer integration.  
**Use in manuscript:** Sections 1, 2, 6.1, 6.5, 8.5, 9.1 and 9.6.  
**Qualification:** cite the pinned version when describing the hook required by CIP-0132. Do not imply that the dedicated-synchronizer integration was production-deployed merely because the underlying CIP-0104 mechanism is approved.

### [2] Canton Improvement Proposal 0129 — Universal Burn and Synchronizer Pricing
Canton Foundation. *CIP-0129: Universal Burn and Synchronizer Pricing*. Approved 23 October 2026.  
https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md  
**Supports:** the universal-burn and synchronizer-pricing framework; dedicated-synchronizer traffic reporting and reward attribution context; the trust placed in operator reports in the initial design; the stated limits of aggregate payment-based reward constraints.  
**Use in manuscript:** Sections 1, 2, 3, 6.1, 7.1, 8.1, 8.3, 8.5 and 9.1.  
**Qualification:** before final publication, replace the mutable `main` URL with the exact commit permalink used for the status and wording claims. Approval of CIP-0129 must not be conflated with approval or deployment of CIP-0132.

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
| 5. Settlement assurance | [3], [7], [9], [11], [15], [18] | Off-ledger linkage, settlement properties, prototype checks and evidence limits |
| 6. Reward attribution and privacy | [1]–[4], [6], [13], [14], [16], [17] | Reward hook, Phase 1 attribution, privacy model and synthetic leakage experiments |
| 7. Economic and operational trade-offs | [3], [15], [19] | Assurance architecture assumptions and scenario comparison; ICU model still needs a reproducible source |
| 8. Discussion | [1]–[19] as relevant | Synthesis; cite the source for each specific factual or methodological claim rather than attaching a blanket citation |
| 9. Limitations and future research | [1]–[19] as relevant | Snapshot, implementation status, prototype and experiment limitations |
| 10. Conclusion | [1]–[3], [9], [14]–[19] | Restate only results already supported in the body |

## E. Outstanding source and manuscript issues

These must be resolved before converting this register into the final numbered References section.

1. **Section 4.3 PR identity:** the current research audit says PR #111 replaces PR #103 and contains the participant-departure implementation observation. The manuscript's earlier correction ties that observation to PR #103. Confirm the exact code revision observed, then cite the correct PR and commit. Do not use PR #103 to support behaviour that exists only in PR #111.
2. **Section 6.1 invariant identifier:** the manuscript says “I-10 validation model”, but the current `research/accounting-properties-and-threat-model.md` defines P1–P8. Locate the authoritative twelve-invariant register and map I-10 to the reward checks listed in the manuscript. If no such register exists, correct the identifier and narrow the claim.
3. **Section 7.2 ICU totals:** the four outputs (28.0, 59.5, 105.0, 141.5 ICU) and per-interval increments were not found in the inspected research-repository tree or the two comparative-assurance model scripts. Locate the exact model, parameter file and execution output, or reproduce the calculations in a committed script. Until then, do not describe the figures as reproducible outputs from the repository.
4. **Section 6.3 four-participant example:** the four-equation example is explicitly hand-derived, not an executable fixture. Keep that qualification unless a matching test is added.
5. **CIP-0129 permalink:** replace the mutable `main` URL with the exact approved revision used in the manuscript.
6. **Current implementation status:** PR #111, PR #8449 and issue #155 must be cited with snapshot dates and status. Do not translate open/draft issue evidence into production behaviour.
7. **Research prototype test count:** the final manuscript should identify the exact repository commit and command behind the final reported test count. Do not cite a test count without a reproducible revision and run record.
8. **External literature:** this manuscript currently relies mainly on protocol specifications, implementation evidence and its own experiments. Do not add generic privacy, ZK or accounting papers merely to make the bibliography look academic. If the text makes general claims about differential privacy, cryptographic proofs or audit independence beyond standard definitions, add authoritative technical sources for those specific claims.

## F. Final citation style recommendation

Use numbered citations in square brackets, for example `[1, 3]`, with a numbered References section. Cite the primary CIP for protocol requirements, the exact PR/issue for implementation observations, and the repository artefact for the authors' own experiments. Where a sentence combines multiple evidence classes, cite each class separately.

The final bibliography should keep external sources and the authors' own reproducibility artefacts distinguishable. This register is an editorial working document; it is not itself the paper's final References section.
