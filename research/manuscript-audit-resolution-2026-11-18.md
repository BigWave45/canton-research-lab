# Manuscript Audit: Resolution of Three Open Issues

**Date:** 18 November 2026  
**Manuscript:** *Verifiable Accounting for Dedicated Synchronizer Paymasters: Guarantees, Trust Boundaries, and Trade-offs*  
**Research repository snapshot:** `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`

This note records the decisions from the source audit. It does not claim that the manuscript file itself was edited: the manuscript text was supplied in conversation and no manuscript source file was present in the repository tree.

## 1. Section 4.3: participant-departure observation

**Resolved source: PR #111, not PR #103.**

The implementation evidence map states that PR #103 introduced an earlier database-backed interval-report trigger/store and that PR #111 explicitly replaces it. The traffic-report implementation audit identifies the participant-departure behaviour in the code and test associated with PR #111: the aggregation iterates participants present in the end-of-interval state and excludes a participant absent at interval end, even if that participant had a start-of-interval counter.

The source is an open pull request at the 17 November 2026 snapshot. It is proposed implementation evidence, not deployed MainNet behaviour.

**Replace the existing Section 4.3 source-attribution paragraph with:**

> The implementation observation discussed here comes from the traffic-report API proposed in Canton Network's `splice-multi-sync` PR #111, reviewed in the 17 November 2026 source snapshot. The implementation calculates interval traffic from sequencer counter snapshots and iterates participants present in the end-of-interval state. Its test excludes a participant who had a start-of-interval counter but was absent at interval end. PR #111 explicitly replaces the earlier PR #103 design. This is an observation about proposed source code, not deployed production behaviour. Whether the exclusion is an accounting defect depends on the intended charging rule for participants that leave during an interval; the protocol specification must define that rule.

**Citation:** [5] and [10] in the main register. PR #103 [8] is historical context only and should not support the current behaviour claim.

## 2. Section 6.1: remove the unsupported I-10 implementation attribution

**Resolved finding: the repository does not support the current claim that the listed reward checks are an implemented I-10 validation model.**

The located formal property register defines P1–P8. P6 is specifically a reward-budget bound, (M_W \leq G_W). It does not cover the full checklist in Section 6.1 (identity binding, references, authorised weights, rule version/epoch, duplicate/superseded records, reward categories, calculation and aggregate limits).

The checked-in `analysis/settlement_manifest_validator.py` and `tests/test_settlement_manifest_validator.py` validate interval coverage, report status, agreement-version presence, digest presence, burn identifiers, burn allocation and payment residual. They do not implement the full reward-attribution validation checklist. `analysis/adversarial_accounting_tests.py` tests a simple reward-budget bound, but not the complete I-10 checklist. The repository's P6 property is the closest formal property, but it is narrower.

**Replace any sentence claiming that “the I-10 validation model validates” the full list with:**

> The research design specifies a reward-attribution validation checklist covering identity and reference binding, authorised activity weights, reward-rule and epoch versions, duplicate or superseded records, reward categories, deterministic calculation and aggregate budget limits. The current prototype evidence is narrower: the checked-in adversarial test demonstrates a reward-budget bound, while the settlement-manifest validator tests interval coverage, agreement references, burn uniqueness and payment reconciliation. The full reward-attribution checklist has not been demonstrated by the checked-in prototype tests and is treated here as a proposed validation requirement.

**Citation:** [9], plus the new repository artefact entries [25] and [26] below. Do not relabel the checklist as P6 or claim it is already implemented. If the manuscript's I-01–I-12 numbering is retained as a paper-defined taxonomy, define it explicitly in Section 3 and cite that section internally; do not imply that the repository's P1–P8 register is the same taxonomy.

## 3. Section 7.2: withdraw the unsupported ICU totals

**Resolved finding: the values 28.0, 59.5, 105.0 and 141.5 ICU are not reproducible from the current repository snapshot.**

A complete tree search found no assurance-cost model, parameter file or output that generates these totals. The checked-in comparative assurance scripts are qualitative or scenario-detection models; they do not calculate those ICU values. The repository's synchronizer-economics script models a different USD/MB pricing and collateral question. It cannot be cited as the source of the Section 7.2 figures.

The arithmetic differences and per-100-interval increments previously checked are internally consistent, but arithmetic consistency does not establish provenance of the inputs.

**Required manuscript action:** remove the four numeric ICU totals, their incremental cost figures, and any break-even calculation that depends on them. Replace Section 7.2 with a qualitative comparison using the dimensions already supported in the research: implementation burden, recurring operator/auditor effort, privacy exposure, latency, residual trust and dispute reproducibility. State explicitly that costs have not been empirically measured or parameterised in a reproducible model.

**Replacement text for the opening of Section 7.2:**

> This comparison does not assign numerical costs to the four architectures. The available repository experiments compare assurance capabilities and qualitative implementation burdens; they do not provide a reproducible cost model for engineering effort, recurring operations, audit fees, proof generation or verification. Accordingly, the cost discussion below is ordinal and conditional. It identifies likely cost drivers and trade-offs rather than estimating monetary expenditure, labour hours or expected losses.

Then retain a qualitative table, with each rating marked as an analytical judgement rather than a measured result. Remove the term “ICU” from the paper unless a unit definition, parameter register, cost function and executable model are added and independently checked.

**Citation:** [15], [19] and [27] below. These support the qualitative comparison only, not numerical cost estimates.

## 4. Additional repository references

### [25] Settlement manifest validator
BigWave45. `canton-research-lab`. `analysis/settlement_manifest_validator.py`, repository snapshot `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`.  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/settlement_manifest_validator.py  
**Supports:** the prototype's interval coverage, status handling, agreement-version/digest presence, duplicate and cross-settlement burn checks, allocation reference checks and payment residual calculation.  
**Does not support:** source measurement completeness, legal authority of agreement signers, or reward-attribution validation.

### [26] Settlement manifest validator tests
BigWave45. `canton-research-lab`. `tests/test_settlement_manifest_validator.py`, repository snapshot `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`.  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/tests/test_settlement_manifest_validator.py  
**Supports:** test cases for complete manifests, missing intervals, gaps, duplicate burns, reused burn IDs, wrong settlement assignment, payment mismatch, uncovered windows, missing agreement versions and missing report digests.  
**Does not support:** the full reward-attribution checklist or production integration.

### [27] Integrated qualitative assurance comparison
BigWave45. `canton-research-lab`. `analysis/integrated_assurance_comparison.py`, repository snapshot `ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c`.  
https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/integrated_assurance_comparison.py  
**Supports:** qualitative architecture ratings for measurement assurance, payment completeness, allocation assurance, reward attribution, disclosure, residual trust, implementation burden, latency and dispute resolution.  
**Qualification:** the file explicitly labels ratings as analytical judgements, not measured performance or probabilities. It does not support numerical ICU costs.

## 5. Revised disposition

| Issue | Decision | Manuscript action |
|---|---|---|
| Section 4.3 PR attribution | Resolved to PR #111 | Replace PR #103 attribution; retain open-PR/non-production caveat |
| Section 6.1 I-10 reward validation | Unsupported as an implemented model | Describe the full checklist as proposed; distinguish the narrower checked-in tests |
| Section 7.2 ICU model | No reproducible source found | Remove numerical cost outputs and break-even claims; use qualitative comparison |

These decisions preserve the paper's central argument while narrowing claims to what the cited evidence actually establishes.
