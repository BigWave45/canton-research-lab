# Canton Research Lab

Private research workspace for an interdisciplinary, quantitatively grounded study of economic accounting in privacy-preserving financial infrastructure, using Canton's proposed Dedicated Synchronizer Paymaster Model as the case study.

## Controlling research question

**What verifiable accounting guarantees can be added to the proposed dedicated-synchronizer paymaster model, and what are their economic, privacy and operational costs?**

The project follows activity measurement, interval reporting, off-ledger commercial liability, Canton Coin settlement, reward attribution and independent reconciliation. It is not a general security audit or a claim that Canton has experienced accounting failures.

## Current research status

The repository contains:
- a comparative review of other public research-funding programmes and selected completed outputs;
- Canton literature, protocol and implementation evidence reviews;
- synthetic accounting, pricing, reconciliation, allocation and privacy models;
- a comparative assessment of four assurance architectures;
- a preliminary research evidence map identifying what each artefact can and cannot establish.

The work is now in **evidence consolidation and validation**. The models are not production Canton software. Synthetic scenarios must not be described as observed network behaviour. Public-source implementation reviews do not establish deployment.

Read [the research evidence map](research/research-evidence-map.md) for the current claim-to-evidence inventory and limitations. Read [STATE.md](STATE.md) for the chronological project log and next action.

## Repository map

- `STATE.md`: project checkpoint and historical work log.
- `GRANT_PROGRAMME.md`: programme requirements and verification status.
- `RESEARCH_METHODOLOGY.md`: research and reproducibility standards.
- `research/research-evidence-map.md`: controlling map of claims, artefacts, evidence classes and gaps.
- `research/`: literature, source analysis, implementation reviews, experiments and research notes.
- `sources/`: source index and bibliography.
- `data/`: datasets, metadata and provenance notes.
- `analysis/`: models and calculations.
- `tests/`: tests of the research code.
- `outputs/`: publication-ready research outputs.

## Evidence rules

1. Separate primary-source facts, implementation observations, observed public data, synthetic results, analytical judgements and unknowns.
2. Record source dates, versions, coverage and provenance.
3. A merged pull request is not proof of production deployment.
4. A passing synthetic test is not empirical validation of Canton.
5. A public burn is not proof that all chargeable activity was measured or that the correct private liability was settled.
6. Do not invent data, grant criteria, performance measurements or probabilities of selection.
7. Keep unpublished research and working materials private until the evidence, licensing, privacy and reproducibility checks are complete.

## Publication

The intended primary output is a substantive research paper. The GitHub repository is its reproducibility and evidence companion; it does not replace the paper's explanation of methods, results and limitations. Resonance is the planned public publication venue, subject to the grant programme's current terms.
