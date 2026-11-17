# Literature Review and Research-Gap Matrix

**Review date:** 17 November 2026  
**Purpose:** Position the dedicated-synchronizer traffic-to-burn/reward problem against established work in economics, financial market infrastructure, verifiable resource accounting and privacy-preserving commitments.  
**Review status:** Focused scoping review, not a systematic review. Search terms, sources and unresolved coverage are recorded below. Novelty is provisional.

## 1. Research problem being positioned

Canton's dedicated-synchronizer Phase 1 model separates:
- private resource consumption measured by the synchronizer operator;
- a traffic report supplied by that operator;
- CC burned by a designated paymaster on the Global Synchronizer;
- reward entitlements linked to the burn and activity records.

The Phase 2 implementation work does not automatically reconcile the operator's report with the paymaster's purchase. An earlier Phase 3 reward-accounting proof of concept uses a Merkle commitment and a purchased-traffic budget to constrain reward expansion, but was not wired end-to-end.

The candidate research object is therefore a **multi-stage verification and incentive system**: measurement, payment reconciliation and reward allocation. The problem is not simply “how to use Merkle trees for privacy” or “how to audit a dishonest operator.”

## 2. Literature-gap matrix

| Literature stream | Established contribution | What it does not answer for this case | Research use |
|---|---|---|---|
| Principal-agent theory and auditing | Models hidden information/action, truthful reporting, audit probability, penalties, limited liability and the trade-off between monitoring and incentives | Does not specify the technical evidence chain linking private sequencer counters, interval reports, public token burns and committed reward leaves | Derive operator/paymaster incentives, audit policy and conditions for truthful reporting |
| Financial market infrastructure (FMI) standards | Requires clear governance, operational risk controls, settlement finality, monitoring of liquidity/settlement flows, and transparent rules and fees | Provides principles, not a protocol-level design for private synchronizer traffic metering or cryptographic reward-budget enforcement | Translate the case into control objectives: accuracy, completeness, timeliness, accountability and dispute handling |
| Verifiable resource accounting | ALIBI proposes a trusted reference monitor beneath a service provider to measure resource use and support verifiable customer reconciliation | Focuses on CPU/memory metering for outsourced computation, not multi-party synchronizer governance, CC burn, discounts or reward issuance | Closest conceptual precedent for independent resource metering and bill reconciliation |
| Privacy-preserving commitments and selective disclosure | Merkle commitments can bind data while allowing later inclusion proofs or selective disclosure; blockchain anchoring can establish existence/integrity | A commitment alone does not prove source completeness, truth of the committed inputs, interval coverage or correct payment | Separate cryptographic binding from measurement truth and completeness |
| Proofs of liabilities / Merkle-sum trees | Allow clients to verify inclusion and aggregate liabilities; research has identified attacks on naïve Merkle liability constructions | Different accounting direction and threat model; a Merkle root over activity is not by itself proof that all traffic was included or that the source counter is correct | Import lessons about sum-binding, leaf integrity, inclusion, omissions and independent verification |
| Canton CIPs and implementation | CIP-0104 describes activity-based rewards; CIP-0129 introduces universal burn; CIP-0132 specifies the interim trusted paymaster model; code/tracker work documents the reporting and reward paths | Public proposals and implementation artifacts do not yet provide an independent, end-to-end evaluation of report completeness, burn coverage, incentive compatibility and privacy-preserving dispute evidence | Ground the paper in an actual protocol transition and distinguish proposal, code, tests and deployment |

## 3. Closest prior work and implications

### 3.1 Verifiable resource accounting: ALIBI

Chen et al., “Towards Verifiable Resource Accounting for Outsourced Computation” (2013), introduces ALIBI. Its core observation is directly relevant: customers and providers lack a verifiable basis for reconciling resources charged with resources actually consumed. ALIBI places a minimal trusted reference monitor below the provider's software stack to observe resource allocation and report it to customers. The paper demonstrates verifiable tracking of memory use and CPU cycles.

**Implication:** The broad idea of verifiable resource metering is not new. A Canton contribution must go beyond proposing “a monitor” or “a usage receipt.” It should address the distinct problem of a privacy-preserving multi-party ledger where measurement, payment and rewards are controlled by different actors, and where public settlement records do not reveal the underlying private transactions.

**Difference to test:** ALIBI assumes a trusted measurement component can observe resource allocation. In Canton, the sequencer/operator infrastructure already produces cumulative traffic counters, but the research question is how reports from that source are reconciled with a separate paymaster's public CC purchases and reward records, without exposing private payloads.

### 3.2 Principal-agent auditing and incentive compatibility

Border and Sobel's “The Theory of Auditing” (1987) models an agent who privately observes a relevant state and a principal who chooses transfers, audit probabilities and penalties. Later work studies monitoring versus auditing, auditor reliability, collusion and limited liability.

**Implication:** “The operator could under-report” is not a research contribution by itself. A useful economic model must specify:
- what the operator and paymaster each observe;
- who chooses the reported quantity and purchase quantity;
- the benefit from under-reporting or delayed payment;
- the probability and accuracy of independent detection;
- the cost and consequences of a challenge, audit or governance sanction;
- whether the operator and paymaster are independent or collude.

The model should compare the interim trust-based design with alternatives such as deposits, periodic audits, challenge windows, automatic reconciliation and cryptographic evidence. It must account for audit cost and limited liability rather than assuming arbitrarily large penalties.

### 3.3 Financial market infrastructure standards

The CPMI-IOSCO Principles for Financial Market Infrastructures (2012) are the global standards for systemically important payment systems, securities settlement systems, central counterparties, central securities depositories and trade repositories. Relevant principles include:
- Principle 2: governance;
- Principle 3: comprehensive risk management;
- Principle 8: settlement finality;
- Principle 17: operational risk;
- Principle 21: efficiency and effectiveness;
- Principle 23: disclosure of rules, key procedures and market data.

**Implication:** These standards provide control objectives and institutional context, not a ready-made technical solution. We should not claim Canton or every dedicated synchronizer is legally classified as a systemically important FMI. Use PFMI as a comparative governance/control framework, and state applicability limits.

### 3.4 Merkle commitments, selective disclosure and proof-of-liabilities research

Saito and Watanabe (2021) describe selective disclosure of verifiable documents using salted hashes and Merkle roots. Hu, Zhang and Guo (2019) examine attacks on Merkle approaches to proving liabilities, showing that apparently sound tree constructions can fail under adversarial data construction.

**Implication:** Merkle commitments solve binding and selective disclosure problems only under defined construction and verification rules. They do not establish that the underlying event source is truthful or complete. A root cannot reveal an omitted traffic interval unless the protocol separately binds the expected interval sequence, cumulative counters or a completeness witness.

The Canton Phase 3 proof of concept is interesting because it connects a committed activity tree to a purchased-traffic ceiling. However, this budget invariant is distinct from proving that the operator's activity inputs cover every relevant event.

## 4. Candidate research gap

The focused search did not identify a prior study that combines all of the following in one model:
1. privacy-preserving resource measurement in a permissioned multi-party ledger;
2. reconciliation of operator-reported consumption against a separate public payment/burn record;
3. incentive-compatible allocation of audit, challenge and sanction responsibilities between operator, paymaster and governance actors;
4. cryptographically bounded reward issuance based on committed activity;
5. explicit separation of source completeness, payment completeness and reward correctness.

This is a **candidate gap, not a novelty claim**. The search was targeted, not systematic. The literature on cloud metering, trusted execution, verifiable computation, accounting systems, distributed ledgers, proof of reserves/liabilities and auditing must be searched more deeply before publication.

## 5. A potentially distinctive contribution

A suitable contribution would be a **privacy-preserving traffic-to-burn accountability framework** with three layers:

### Layer A — Measurement assurance
Define the source of truth for traffic, interval boundaries, participants joining/leaving, sequencer upgrades, pruning, counter resets and unavailable history. Specify how completeness is represented. A measurement report should bind the synchronizer identity, interval sequence, counter endpoints, units, version and status.

### Layer B — Payment reconciliation
Match cumulative reportable traffic to traffic-equivalent purchases and CC burns, including pricing, discounts, CC/USD conversion, rounding and timing. Define underpayment, overpayment, arrears, late payment and dispute states. Separate the ledger fact “CC was burned” from the claim “all consumed traffic was paid for.”

### Layer C — Reward correctness
Bind reward allocation to eligible purchased traffic and committed activity. Prove that reward expansion cannot exceed the authorised budget. Separately assess whether the committed activity is complete and whether allocation among apps/parties is economically justified.

The framework should make no public disclosure of transaction payloads or counterparties necessary. It should expose only the minimum aggregate or selectively disclosed evidence required for reconciliation.

## 6. Research questions and testable propositions

**RQ1 — Measurement completeness:** Under what reporting semantics can interval reports be reconciled across participant joins/leaves, logical synchronizer upgrades and sequencer pruning?

**RQ2 — Payment completeness:** What conditions guarantee that cumulative purchases cover reportable consumption under time-varying prices, negotiated discounts and reporting delays?

**RQ3 — Incentive compatibility:** How do audit probability, detection accuracy, penalties, collateral/deposits and governance suspension affect the operator's and paymaster's incentives to under-report or delay payment?

**RQ4 — Reward integrity:** What cryptographic and ledger invariants guarantee that minted rewards are bounded by purchased traffic and committed activity?

**RQ5 — Privacy/accountability trade-off:** What is the minimum information that must be disclosed to let a participant, SV or independent auditor verify a claim without revealing transaction payloads or other participants' activity?

Candidate hypotheses to formalise, not yet accepted:
- H1: A public burn record alone cannot establish payment completeness unless it is bound to a complete, canonical consumption-report sequence.
- H2: A Merkle commitment plus a budget ceiling can bound reward issuance but cannot, by itself, prove that the committed activity tree includes all eligible activity.
- H3: A challenge mechanism can reduce expected under-reporting only when expected sanction cost exceeds the expected gain from misreporting, adjusted for audit accuracy and the probability of successful challenge.
- H4: Stronger privacy constraints increase the cost of independent measurement verification unless the protocol supplies trusted attestations, verifiable counters or selective-disclosure proofs.

## 7. Quantitative and computational plan

The research should use a formal model plus executable scenarios, not claim empirical operator behaviour without data.

### State variables

For synchronizer (s) and interval (t):
- (Q_{s,t}): true chargeable traffic;
- (hat Q_{s,t}): reported traffic;
- (B_{s,t}): traffic-equivalent purchased bytes;
- (C_{s,t}): CC burned;
- (X_t): CC/USD conversion price;
- (P_t): list price per MB;
- (d_{s,t}): negotiated discount factor;
- (R_{s,t}): reward issuance;
- (A_{s,t}): committed eligible activity;
- (a): audit probability;
- (q): probability an audit detects a misstatement;
- (F): enforceable sanction or forfeiture;
- (k): audit cost.

### Core measures

- Measurement error: ((hat Q-Q)/Q)
- Payment coverage: (B/Q)
- Unpaid traffic: (max(0,Q-B))
- Overpayment: (max(0,B-Q))
- Effective CC cost per actual MB: (CX/(Q/10^6))
- Reward budget utilisation: (R/R_{max})
- Report-to-payment lag: payment timestamp minus interval end
- Expected deterrence: (a q F), compared with the gain from misreporting
- Completeness: share of expected intervals with a valid, independently reconcilable report

The simple deterrence expression is only a starting point. The final model must include the operator's and paymaster's separate payoffs, possible collusion, audit cost, limited liability and sanctions that may be governance-based rather than monetary.

### Scenario and property tests

Build reproducible tests for:
- exact reporting and full payment;
- under-reporting and over-reporting;
- accurate reporting but partial payment;
- delayed purchase;
- participant joining or leaving during an interval;
- sequencer upgrade across an interval;
- pruning-boundary missing history;
- CC price movement between usage and purchase;
- discounts and rounding;
- reward tree with excessive leaf weight;
- omitted activity leaves despite a valid root;
- duplicate, stale or reordered reporting intervals.

Where source data is unavailable, scenarios are explicitly synthetic. If authorised operational data becomes available, replace or calibrate the scenarios and preserve provenance.

## 8. Novelty boundaries

Do not claim:
- invention of Merkle trees, selective disclosure or verifiable computation;
- that Canton has a live exploit or demonstrated financial loss;
- that the current paymaster model is defective merely because it is trusted;
- that the Phase 3 Merkle PoC is deployed;
- that a public CC burn proves the full underlying private activity;
- that PFMI legally applies to every Canton synchronizer;
- that the targeted literature search proves global novelty.

The likely contribution is an integrated protocol-economics analysis and verifiable reconciliation framework applied to a real privacy-preserving synchronizer architecture.

## 9. Selected references

1. Border, K. C. and Sobel, J. (1987), “The Theory of Auditing,” *Review of Economic Studies*. https://econweb.ucsd.edu/~jsobel/Papers/auditing.pdf
2. Chen, C., Maniatis, P., Perrig, A., Vasudevan, A. et al. (2013), “Towards Verifiable Resource Accounting for Outsourced Computation,” *ACM SIGPLAN Notices* 48(7). DOI: https://doi.org/10.1145/2451512.2451546
3. CPMI-IOSCO (2012), *Principles for Financial Market Infrastructures*. https://www.bis.org/committees/cpmi/pfmi/overview
4. Hu, K., Zhang, Z. and Guo, K. (2019), “Breaking the binding: Attacks on the Merkle approach to prove liabilities and its applications,” *Computers & Security* 87, 101585. DOI: https://doi.org/10.1016/j.cose.2019.101585
5. Saito, K. and Watanabe, S. (2021), “Lightweight selective disclosure for verifiable documents on blockchain,” *ICT Express* 7(3), 290–294. DOI: https://doi.org/10.1016/j.icte.2021.08.012
6. Strausz, R. (2006), “Timing of verification procedures: Monitoring versus auditing,” *Journal of Economic Behavior & Organization* 59(1), 89–107. DOI: https://doi.org/10.1016/j.jebo.2004.03.013
7. Canton Improvement Proposal CIP-0104, Traffic-Based App Rewards. https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md
8. Canton Improvement Proposal CIP-0129, Universal Burn and Synchronizer Pricing. https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md
9. Canton Improvement Proposal CIP-0132, Dedicated Synchronizer Paymaster Model. https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md

## 10. Search coverage and next review

Searches covered:
- principal-agent auditing, incentive compatibility, monitoring and verification;
- verifiable resource accounting for outsourced computation;
- financial market infrastructure controls, settlement and operational risk;
- Merkle commitments, selective disclosure and proof-of-liabilities attacks;
- Canton CIP-0104, CIP-0129 and CIP-0132.

Next review should cover:
- cloud and edge resource metering, including trusted hardware and remote attestation;
- verifiable computation and proof systems for state/counter transitions;
- blockchain proof-of-reserves and proof-of-liabilities designs, including completeness attacks;
- accounting reconciliation and audit sampling under incomplete observability;
- privacy-preserving telemetry and aggregate proofs;
- research specifically on permissioned multi-ledger synchronizers and cross-domain usage billing.

Only after that review should we finalise a novelty statement and select a specific technical mechanism to prototype.
