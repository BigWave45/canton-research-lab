> **Scope correction — 17 November 2026:** This document is an early hypothesis generated from CIP-0129 and must now be read alongside [the CIP-0104 / CIP-0129 / CIP-0132 architecture comparison](cip-0104-0129-0132-architecture-comparison.md). CIP-0132 is the proposed Phase 1 design: rewards are initially attributed to the designated paymaster, not granularly distributed to individual dSync participants. The per-party misallocation example below is therefore a model of a possible later granular-attribution regime, not a description of the proposed Phase 1 implementation or a claim of live misreporting. The immediate research focus has shifted to the integrity of the aggregate traffic-report → CC burn → reward pipeline and the transition to granular attribution.

# Reward Attribution Integrity on Dedicated Synchronizers

**Status:** Research avenue under evaluation; not a final topic selection.  
**Date:** 17 November 2026  
**Primary source:** CIP-0129, sections 2 and 4.

## 1. The mechanism problem

CIP-0129 proposes extending traffic-based rewards to apps and validators operating on dedicated synchronizers. The Super Validators do not see traffic on synchronizers they do not operate. The approved proposal therefore requires each dedicated synchronizer operator to publish aggregate traffic reports on the Global Synchronizer, attributed per party as required by the reward rules.

The CIP explicitly says the initial reports rely on the operator being honest. It acknowledges that a maliciously constructed report could misdirect rewards between participants, although it cannot claim rewards on more traffic than the synchronizer or its users paid for. It says a future CIP may tighten enforcement.

This creates a precise mechanism-design question:

**Can a privacy-preserving network distribute traffic-based rewards accurately when the party reporting the underlying activity is not independently observed by the reward administrator?**

This is narrower and more testable than a generic question about Canton transparency.

## 2. Formalising the allocation problem

Let there be n parties using a dedicated synchronizer.

- b_i: true reward-eligible CC burn attributable to party i.
- B: total eligible CC burn for the synchronizer.
- r_i: reported burn attributed to party i.
- R: total reported attribution.

The true total is:

B = sum_i b_i

A basic aggregate cap requires:

R = sum_i r_i <= B

This cap constrains the total amount attributed for rewards. It does not, by itself, prove that each party's share is accurate.

If the report uses the full paid amount, then R = B. A report can still redistribute attribution while preserving the total:

r_i = b_i + delta_i

subject to:

sum_i delta_i = 0 and r_i >= 0

The aggregate total remains unchanged, but party-level rewards can be misallocated.

### Worked illustration (hypothetical)

Suppose actual eligible burn is 1,000 CC:

| Party | True attributable burn | Operator-reported burn |
|---|---:|---:|
| A | 600 CC | 400 CC |
| B | 300 CC | 400 CC |
| C | 100 CC | 200 CC |
| **Total** | **1,000 CC** | **1,000 CC** |

The report respects the total cap, yet shifts 200 CC of reward weight away from A and toward B and C. The example is illustrative, not an allegation about any Canton operator.

## 3. Measuring attribution error

If the true per-party allocation can be established in a controlled experiment or authorised audit, define the normalised attribution error as total variation distance:

TV = 0.5 * sum_i |(r_i / B) - (b_i / B)|

Interpretation:
- TV = 0 means exact attribution.
- TV = 0.10 means 10% of the total reward weight would need to be reassigned to transform one distribution into the other.
- TV = 1 is the maximum possible distance between two distributions.

This metric is not computable by a public observer if the true b_i values are hidden. That limitation is central to the research problem. The project can still use it in a controlled simulation or authorised audit design.

Additional measures:
- Party-level absolute error: AE_i = |r_i - b_i|.
- Largest overstatement: max_i max(0, r_i - b_i).
- Largest understatement: max_i max(0, b_i - r_i).
- Reward-weight concentration: HHI of true and reported party shares, where both distributions are known.
- Total-cap compliance: R / B, which tests aggregate overclaiming but not correct attribution.

## 4. What the aggregate cap can and cannot guarantee

| Property | Aggregate cap alone? | Explanation |
|---|---|---|
| Total reported traffic does not exceed paid traffic | Potentially, if the protocol enforces the cap | Must inspect the actual enforcement path; the CIP states the design constraint |
| Per-party attribution is truthful | No | Many different per-party distributions can sum to the same total |
| Reward recipients are the parties that generated the traffic | No | Requires an independent attribution signal or verifiable evidence |
| Private transaction payloads remain confidential | Potentially | Depends on the reporting/proof design |
| Operator cannot collude with selected participants | No | Requires a threat model and controls beyond a total cap |
| A public observer can verify individual party activity | Not necessarily | Public verification can be limited to aggregate commitments or proofs |

The research must distinguish a rule described in the CIP from a guarantee enforced by code. The relevant contracts, report schema, validation process and implementation status must be inspected before making a security claim.

## 5. Candidate verification designs to compare

These are research candidates, not recommendations that Canton has adopted.

### A. Operator attestation

The operator signs a report asserting per-party traffic attribution.

- Strength: simple, low computational overhead.
- Weakness: shifts trust to the operator; signatures prove origin, not truth.
- Research question: what accountability, audit and dispute process makes the attestation credible?

### B. Independent audit / challenge mechanism

A designated auditor or authorised participant can inspect the underlying traffic records and challenge a report.

- Strength: introduces an independent check.
- Weakness: access, cost, timing, auditor independence and confidentiality become critical.
- Research question: what audit frequency and sampling rate would detect economically material misallocation?

### C. Cryptographic commitment with selective disclosure

The operator commits to a per-party allocation dataset and later reveals or proves selected fields under an authorised challenge.

- Strength: can make a report tamper-evident and support selective verification.
- Weakness: a commitment alone does not prove that the committed data are true; the system still needs a trusted input or proof relation.
- Research question: which properties can be proved without disclosing private transaction contents?

### D. Zero-knowledge proof of accounting constraints

The operator proves that reported party allocations are derived from a committed dataset and that the total does not exceed eligible paid traffic, without disclosing transaction details.

- Strength: can prove a defined computation while hiding underlying values.
- Weakness: correctness depends on circuit design, input authenticity, data completeness, proof-generation cost and how party identities are bound to eligible events.
- Research question: what exactly is being proven, and who can verify that all eligible traffic was included?

### E. Threshold / multi-party attestation

Several independent parties attest to a report or to parts of the underlying accounting.

- Strength: reduces dependence on one operator.
- Weakness: collusion, availability, governance and operational coordination remain.
- Research question: what threshold and independence assumptions are credible for a permissionless ecosystem?

## 6. Threat model

At minimum, analyse these actors and failure modes:

1. **Honest operator:** reports accurate party attribution.
2. **Self-benefiting operator:** shifts reward weight to its own party or affiliated app.
3. **Colluding participants:** coordinate to redirect rewards among a group.
4. **Faulty indexer/reporting pipeline:** introduces omissions, duplicates or party-label errors without malicious intent.
5. **Compromised operator key:** attacker publishes a false but correctly signed report.
6. **Incomplete source records:** the report is internally consistent but excludes eligible traffic.
7. **Governance change:** reward formula or eligibility rules change during a reporting period.

For each case, specify:
- attacker's objective;
- required capabilities;
- information available to the attacker;
- expected economic gain;
- detection probability;
- potential loss to other participants;
- privacy impact;
- remediation and dispute process.

## 7. Quantitative research design

A useful study could combine:

### Model 1: misallocation under an aggregate cap

Simulate n parties with heterogeneous true traffic shares. Generate reports that preserve the total but shift a fraction alpha of reward weight between parties. Measure:
- total variation attribution error;
- largest party gain and loss;
- concentration changes;
- distributional effects by party size;
- sensitivity to number of parties and degree of collusion.

### Model 2: detection under audit sampling

Assume a proportion s of records is independently audited, with a specified error distribution. Estimate detection probability as a function of:
- sampling rate;
- misallocation magnitude;
- number of parties;
- error concentration;
- audit independence.

All error rates and sampling assumptions must be labelled hypothetical unless derived from authorised operational evidence.

### Model 3: privacy-verifiability trade-off

Compare candidate verification approaches across:
- confidentiality leakage;
- correctness guarantees;
- completeness guarantees;
- operator trust;
- verifier trust;
- computation and storage cost;
- latency;
- governance complexity;
- challengeability and recourse.

Do not assign arbitrary numerical scores to these dimensions without a defensible measurement protocol. Begin with a structured qualitative comparison, then quantify only where evidence or a formal model supports it.

## 8. Potential contribution

A credible contribution could be a formal framework for **privacy-preserving reward attribution**, including:
1. a precise threat model;
2. a distinction between aggregate payment caps and party-level attribution correctness;
3. quantitative measures of reward misallocation;
4. a comparison of verification designs;
5. a reproducible simulation showing how aggregate-cap compliance can coexist with significant redistribution;
6. implementation requirements for any future verification proposal.

This contribution would connect mechanism design, distributed systems, privacy engineering and network economics. It would be grounded in an explicit risk acknowledged by CIP-0129 rather than an invented problem.

## 9. Limits and evidence required

Before treating this as the selected research topic, obtain:
- the actual CIP-0129 implementation/report schema, if available;
- the relevant reward calculation and coupon contracts;
- the report validation and aggregate-cap enforcement logic;
- the applicable CIP-0082 and reward-distribution implementation details;
- confirmation of whether Phase 1 universal burn has been implemented (currently only estimated for Q1 2027 in CIP-0129);
- feedback from a synchronizer operator, app provider or protocol engineer if obtainable.

No claim is made that a specific cryptographic technique is necessary, absent from Canton, or technically feasible in its current architecture. That requires implementation-level study.

## 10. Primary source

CIP-0129, *Universal Burn and Synchronizer Pricing*, especially §2 (Rewards), §4 (Commitment discounts), §5 (Governance), and §9 (Left to the second CIP): https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md
