# Verifiable Accounting for Dedicated Synchronizer Paymasters

**Research paper:** [Verifiable Accounting for Dedicated Synchronizer Paymasters: Guarantees, Trust Boundaries, and Trade-offs](manuscript/verifiable-accounting-dedicated-synchronizer-paymasters.md)

This repository contains the research artefacts supporting the paper: executable accounting models, unit tests, synthetic privacy experiments, implementation evidence reviews, and technical specifications.

## Research question

What verifiable accounting guarantees can be added to the proposed dedicated-synchronizer paymaster model, and what are their economic, privacy and operational costs?

## What the research contributes

- A model of the accounting path from synchronizer activity reports through commercial liability, Canton Coin burns, allocation and reward attribution.
- Executable controls for expected reporting intervals, agreement and signer checks, deterministic liability calculations, settlement reconciliation, burn allocation and correction handling.
- Synthetic experiments on adversarial accounting cases and disclosure through overlapping aggregate releases.
- A comparative assessment of four assurance architectures: public burn-only verification, signed reconciliation, independent confidential audit and cryptographic proof.
- An explicit separation between properties demonstrated by the research prototype and claims that require independent operational evidence.

## Start here

1. Read the [research paper](manuscript/verifiable-accounting-dedicated-synchronizer-paymasters.md).
2. Review the [research map](research/README.md) to locate the evidence and experiments behind each part of the paper.
3. Inspect the [analysis code](analysis/) and [tests](tests/).
4. Follow the [reproducibility instructions](REPRODUCIBILITY.md).
5. Review the [Canton parameter register](data/parameter-register.md) for the status and provenance of protocol and modelling inputs.

## Repository structure

| Path | Contents |
|---|---|
| `manuscript/` | The final research paper |
| `analysis/` | Executable models, validators and synthetic experiments |
| `tests/` | Unit tests for selected model properties |
| `research/` | Technical evidence reviews, experiment specifications and supporting analysis |
| `data/` | Parameter register and data definitions |
| `sources/` | Source provenance and research evidence guidance |

## Evidence boundary

This is a research prototype and public-source study. The models operate on supplied records and explicit assumptions. They are not connected to a production synchronizer, paymaster or reward-distribution service.

The repository does not provide independent ground-truth traffic measurements, a complete production settlement history, or proof that the proposed accounting path is deployed end to end. Passing tests establishes behaviour for the supplied test cases; it does not establish production correctness or measurement completeness. The reward-attribution implementation evidence is narrower than the full validation framework discussed in the paper.

The economic comparison is qualitative. This repository does not provide a reproducible numerical assurance-cost model or measured Canton operating costs.

## Research status

The paper describes a November 2026 public-source snapshot. Protocol proposals, implementation branches and operational interfaces can change. Status statements should be read against the dates and source references in the paper and supporting evidence records.

## Citation

When using this work, cite the paper title and link to this repository. The paper contains the full reference list and explains the evidence classification and limitations.
