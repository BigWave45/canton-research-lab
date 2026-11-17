# Research Workstream

This directory contains the source-backed and model-based work supporting the selected Canton Paymaster accounting study.

## Controlling scope

**What verifiable accounting guarantees can be added to the proposed dedicated-synchronizer paymaster model, and what are their economic, privacy and operational costs?**

The current project stage is evidence consolidation and validation. The topic has been selected; the literature review, source verification and experimental validation continue as parts of the research rather than as prerequisites to selecting a topic.

## Start here

1. [Research evidence map](research-evidence-map.md): maps research claims to existing files, evidence classes, limitations and remaining work.
2. [Research scope correction](research-scope-correction.md): defines the thesis and keeps implementation defects subordinate to the accounting question.
3. [Canton implementation evidence map](canton-implementation-evidence-map.md): distinguishes present, proposed, absent and unverified implementation elements.
4. [Integrated assurance architecture comparison](integrated-assurance-architecture-comparison.md): compares four assurance designs and records the qualitative nature of the ratings.
5. [Initial comparative assurance experiment](initial-comparative-assurance-experiment.md): the six-scenario synthetic experiment and its limitations.
6. [Quantitative assurance evaluation plan](quantitative-assurance-evaluation-plan.md): the evaluation design and existing-artifact feasibility audit.
7. [Assurance cost model](assurance-cost-model.md): the parameterised calculator, inputs, outputs and limits.
8. [Illustrative assurance-cost scenario](illustrative-assurance-cost-scenario.md): a synthetic four-architecture cost comparison and sensitivity checks; not Canton cost evidence.
9. [Prototype measurement protocol](prototype-measurement-protocol.md): the reproducible local microbenchmark method for manifest validation, allocation checks and aggregate-leakage analysis.

## Workstream organisation

- Literature and grant precedent: literature matrices, comparative grant research and completed-output case studies.
- Canton protocol and implementation: CIP analysis, code audits, issue/PR evidence and implementation status.
- Accounting models: measurement, pricing, agreement schedules, settlement, allocation and reward attribution.
- Privacy: disclosure tiers, aggregate composition and leakage experiments.
- Comparative assurance: public burn evidence, signed reconciliation, confidential audit and cryptographic proof.
- Data feasibility: public data access, metric definitions and limits on network-wide inference.

## Publication discipline

Every claim in the paper must be traceable to a primary source, reproducible data extract, model, test or explicitly labelled analytical judgement. Synthetic outputs are not Canton production measurements. Qualitative architecture ratings are not measured cost or latency. See the evidence map before adding new models or expanding scope.
