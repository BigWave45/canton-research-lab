# Research scope correction: assurance, not vulnerability hunting

**Date:** 17 November 2026

## Why this correction exists

The research has spent several consecutive steps investigating a possible traffic-report pruning race. That is a useful implementation-audit subtask, but it is not the central research objective. The work must not become a vulnerability hunt.

## Actual research objective

**How can privacy-preserving financial infrastructure make its economic accounting independently verifiable?**

Case study: Canton's proposed Dedicated Synchronizer Paymaster Model.

The research follows the economic accounting chain:

1. Infrastructure activity is measured.
2. Activity is reported.
3. The off-ledger commercial agreement determines the amount payable.
4. The paymaster purchases/burns CC.
5. Activity and payment feed into reward attribution.
6. The parties and, where possible, independent reviewers reconcile the result.

The core concern is whether each transition has sufficient evidence, what trust assumptions remain, and what assurance can be achieved without disclosing private transaction payloads.

## Role of implementation defects and race conditions

A code-level defect is not the research goal. Implementation testing is one method for determining whether the proposed accounting guarantees hold.

The pruning investigation should remain a bounded case study:
- Determine whether the suspected interleaving is reachable in the actual implementation.
- Classify the result as correct, safely unavailable, or incorrect success.
- Record the consequence for measurement assurance and availability.
- Stop. Do not expand into a general Canton security audit.

If the implementation handles the race safely, that is a useful result too. A safe refusal may reduce availability while preserving accounting integrity. It should be analysed as a trade-off, not labelled a failure.

## Main work to resume

The central research should return to comparing accounting assurance designs:

- Public burn records alone.
- Signed interval reports with agreement-aware reconciliation.
- Independent auditor access to confidential evidence.
- Public commitments/proofs over confidential settlement inputs.
- Independent measurement or challenge mechanisms.

Evaluate each on:
- Measurement integrity.
- Payment completeness.
- Reward attribution integrity.
- Privacy leakage.
- Residual trust assumptions.
- Operational complexity, latency and cost.
- Dispute resolution and governance.

The quantitative core should compare the assurance gained against its economic and operational costs. It should not assume cryptographic proofs are necessarily superior.

## Scope boundary

Do not:
- conduct a general vulnerability hunt;
- imply a vulnerability or exploit without a demonstrated result;
- spend the research budget on unrelated security findings;
- build cryptographic machinery before establishing the required assurance properties;
- present synthetic experiments as production measurements.

## Completion target

Produce a defensible, Canton-grounded accounting framework, a quantitative comparison of assurance mechanisms, reproducible experiments, and practical design recommendations. The pruning case study is supporting evidence, not the paper's thesis.
