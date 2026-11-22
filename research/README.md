# Research evidence and supporting analysis

This directory contains technical records that support the paper. It is organised by the claims and mechanisms examined, rather than by the chronology of the research process.

## Core evidence map

| Research area | Supporting material |
|---|---|
| Protocol and implementation status | [CIP architecture comparison](cip-0104-0129-0132-architecture-comparison.md), [implementation evidence audit](implementation-evidence-audit.md), [Canton implementation evidence map](canton-implementation-evidence-map.md) |
| Accounting invariants and threat model | [Accounting properties and threat model](accounting-properties-and-threat-model.md) |
| Measurement and reporting | [Traffic report implementation audit](traffic-report-implementation-audit.md), [traffic report consistency and retention](traffic-report-consistency-and-retention.md), [participant departure mechanisms](participant-departure-mechanism-comparison.md), [underlying sequencer pruning semantics](underlying-sequencer-pruning-semantics.md) |
| Agreement and liability | [Cryptographic agreement verification](cryptographic-agreement-verification.md), [agreement-aware liability calculation](agreement-aware-liability-calculation.md), [agreement schedule calculator](agreement-schedule-calculator.md) |
| Settlement and correction | [Settlement accounting interface specification](settlement-accounting-interface-specification.md), [paymaster state transition model](paymaster-state-transition-model.md), [correction identity and obligation mapping](correction-identity-and-obligation-mapping.md), [end-to-end verification audit](end-to-end-verification-audit.md) |
| Burn allocation and reconciliation | [Shared paymaster portfolio allocation experiment](shared-paymaster-portfolio-allocation-experiment.md), [reconciliation experiment results](reconciliation-experiment-results.md), [reconciliation model validation results](reconciliation-model-validation-results.md) |
| Reward attribution | [Reward attribution integrity](reward-attribution-integrity.md), [paymaster versus Merkle reward accounting](paymaster-vs-merkle-reward-accounting.md) |
| Privacy | [Privacy disclosure matrix and leakage experiment](privacy-disclosure-matrix-and-leakage-experiment.md), [linear composition and public verification surface](linear-composition-and-public-verification-surface.md), [privacy disclosure requirements](privacy-disclosure-requirements.md) |
| Assurance architecture | [Comparative assurance model specification](comparative-assurance-model-specification.md), [integrated assurance architecture comparison](integrated-assurance-architecture-comparison.md), [comparative findings](comparative-findings.md) |
| Adversarial testing | [Adversarial accounting experiments](adversarial-accounting-experiments.md), [minimum viable reconciliation state machine](minimum-viable-reconciliation-state-machine.md) |

## How to read these records

The research notes are supporting evidence, not independent publications. The final paper is the authoritative synthesis. Where an older technical note differs from the paper's stated November 2026 evidence boundary, use the paper's dated claim and verify the underlying source before relying on the older note.

The executable models are in [`analysis/`](../analysis/), with corresponding tests in [`tests/`](../tests/). Reproduction instructions are in [`REPRODUCIBILITY.md`](../REPRODUCIBILITY.md).
