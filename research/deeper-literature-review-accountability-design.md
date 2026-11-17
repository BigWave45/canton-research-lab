# Deeper Literature Review: Metering, Attestation and Verifiable Reporting

**Review date:** 17 November 2026  
**Scope:** Follow-up to the interdisciplinary gap matrix. This pass compares hardware-isolated resource accounting, authenticated transparency logs, Merkle proof-of-liabilities research and Canton CIP-0132's explicit interim trust model. It is a focused scoping review, not a systematic review.

## 1. Important correction to the research framing

CIP-0132 is explicit that Phase 1 is intentionally trust-based:
- the dedicated synchronizer operator reports traffic;
- the paymaster burns CC after consumption;
- the report-to-burn link is off-ledger;
- the operator and paymaster are trusted to report and burn according to their agreement;
- discounts and permitted smoothing are handled off-ledger;
- on-ledger rules ensure rewards are commensurate with the burn actually made;
- later phases are intended to make the trust model and enforcement stricter.

Therefore, the research must not describe Phase 1 as an accidental security flaw or claim that a 1:1 interval match is required. A paymaster may have an agreed discount, and a burn may be delayed/smoothed over an agreed period. The correct question is how the trust boundary can be measured, governed and progressively reduced without sacrificing dSync isolation or privacy.

Source: CIP-0132, proposed 9 November 2026, https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md

## 2. Stronger precedents in verifiable resource accounting

### 2.1 ALIBI

Chen et al., “Towards Verifiable Resource Accounting for Outsourced Computation” (2013), introduces ALIBI, which uses nested virtualisation and TPMs to place an observer at the hypervisor layer. Its objective is to give a customer verifiable resource accounting for outsourced computation.

**Relevance:** This already establishes that verifiable resource accounting and independent observation of a provider's resource usage are mature research topics. It is not defensible to present the broad concept as novel.

**Difference:** ALIBI is built around a cloud provider's compute-resource accounting and a trusted observer. It does not study Canton’s separate operator, paymaster, synchronizer governance and reward-allocation roles, nor the policy problem of reconciling a private usage report with a separate public CC burn under discounts and delayed settlement.

### 2.2 VeriCount

Tople, Park, Kang and Saxena, “VeriCount: Verifiable Resource Accounting Using Hardware and Software Isolation” (ACNS 2018), develops self-accounting for Linux containers using Intel SGX and software fault isolation. It measures CPU time, memory, I/O and network bandwidth, and supports refutable billing. The paper reports 3.62% average overhead in hardware mode and 16.03% in simulation mode for its evaluated workloads.

The threat model explicitly assumes both provider and client may be malicious, but they do not collude. Both must trust VeriCount components and SGX. The paper also constrains execution inputs to make resource accounting well-defined.

**Relevance:** VeriCount demonstrates that measurement can be moved out of the untrusted OS and disputes can be supported by an isolated accounting engine.

**Difference and limitation:** It does not eliminate the trust base; it relocates trust to hardware, enclave code and isolation assumptions. For Canton, introducing a TEE would not automatically prove that the sequencer's source counters are complete or that a report covers all eligible participants. The research must identify the entire measurement trust chain, not equate remote attestation with truth.

Primary sources:
- https://www.microsoft.com/en-us/research/publication/vericount-verifiable-resource-accounting-using-hardware-and-software-isolation-2/
- https://www.microsoft.com/en-us/research/wp-content/uploads/2019/03/vericount.pdf

## 3. Authenticated logs: what append-only proofs solve

RFC 9162 (Certificate Transparency v2) provides a mature design for signed tree heads, inclusion proofs and consistency proofs over an append-only Merkle log.

It allows monitors to verify that:
- a submitted entry appears in a published log;
- a later tree is consistent with an earlier tree;
- a log has not silently rewritten previously committed history, subject to the protocol's trust and monitoring assumptions.

The RFC also explicitly notes that a log can show inconsistent views to different clients; gossip and monitoring are needed to detect such split views. The RFC does not claim that a Merkle tree proves every event that should have been submitted was submitted.

**Implication for Canton:** An append-only report log could make operator reports tamper-evident after submission. It would not prove source completeness. If the operator omits an interval or fabricates its initial measurement, a Merkle root alone faithfully commits to the omission or fabrication.

A Canton-oriented report log would need explicit sequence semantics:
- a unique synchronizer identifier and reporting epoch;
- monotonically increasing interval sequence numbers;
- explicit zero-traffic intervals rather than silence;
- start/end record times and sequencer identity/version;
- counter start and end values or an equivalent signed measurement;
- a status for unavailable/pruned intervals;
- a previous-report hash or append-only log commitment;
- a public or independently witnessed checkpoint;
- an authenticated relationship to later payment and reward records.

The design should also test whether multiple operator nodes or independent participants can compare checkpoints to detect inconsistent views.

Source: RFC 9162, https://www.rfc-editor.org/rfc/rfc9162.html

## 4. Proof-of-liabilities attacks: why sum commitments need completeness

Hu, Zhang and Guo, “Breaking the Binding: Attacks on the Merkle Approach to Prove Liabilities and Its Applications” (Computers & Security, 2019), formalises attacks against the Maxwell proof-of-liabilities protocol and summation Merkle trees. Their attack shows that a party can provide inconsistent proofs to different clients and make a published liabilities total omit most accounts while individual clients believe their balances are included.

**Implication:** A sum-augmented Merkle tree must be analysed for more than hash collision resistance and local inclusion. It needs globally consistent commitments, authenticated tree structure, correct aggregate propagation, and an explicit completeness model.

**Canton distinction:** A reward tree with weighted nodes and a budget can constrain how much can be minted from the committed tree. It does not automatically establish that all eligible synchronizer activity is represented in that tree. This separates:
- integrity: committed data cannot be changed unnoticed;
- inclusion: a particular record is in the commitment;
- consistency: successive commitments preserve prior committed history;
- completeness: all eligible source events are represented;
- correctness: amounts and transformations are computed according to policy.

These are distinct security properties and should be tested separately.

Source: https://doi.org/10.1016/j.cose.2019.101585 and https://eprint.iacr.org/2018/1139.pdf

## 5. Revised comparison of trust-reduction mechanisms

| Mechanism | Property it can support | What it does not prove alone | Cost / trust introduced |
|---|---|---|---|
| Operator-signed interval report | Attribution and non-repudiation of the submitted report | Truth or completeness of source measurements | Operator key and reporting process |
| Hash chain / append-only Merkle log | Tamper evidence and historical consistency after commitment | Omitted events before commitment; source truth | Log availability, monitors and anti-equivocation |
| Independent operator replicas / participant witnesses | Cross-checking of reports and inconsistent views | Correctness if witnesses share the same source failure or collude | Replication and coordination overhead |
| TEE / remote attestation | Evidence that approved measurement code ran in an attested environment | Correctness of external inputs, source-counter completeness, or vendor/platform integrity beyond its assumptions | Hardware trust, attestation service, patching and side-channel assumptions |
| Sequencer-signed counter snapshots (if supported) | Authenticated source measurements and interval boundary evidence | Completeness beyond the sequencer's own accounting semantics | Sequencer signing keys, API support and upgrade semantics |
| Merkle-sum reward tree | Inclusion and bounded aggregate reward expansion under correct construction | Completeness of activity inputs | Tree construction, witness availability and verifier complexity |
| Zero-knowledge proof | Can prove a defined computation over committed inputs without revealing those inputs | Truth/completeness of inputs unless separately anchored | Circuit complexity, proving cost and setup/system assumptions |
| Governance audit / challenge | Institutional accountability and dispute resolution | Continuous prevention or cryptographic correctness by itself | Audit expense, response time and governance capture risk |

No single mechanism is a complete solution. The design space is a composition of source authentication, report continuity, independent observation, payment reconciliation, reward constraints and dispute resolution.

## 6. Canton-specific accounting implications

CIP-0132's payment rule is not a raw interval equality rule. Its example explicitly permits a 50% discount: 100 MB reported can lead to a 50 MB-equivalent burn. It also describes post-hoc burn smoothing over a permitted delay, including weekly stepwise smoothing and a rolling seven-day method.

Therefore, the right reconciliation model is cumulative and agreement-aware:

- (Q_t): actual chargeable traffic;
- (hat Q_t): operator-reported traffic;
- (d_t): agreed discount fraction;
- (P_t): applicable USD list price per MB;
- (X_t): CC/USD conversion price used by the purchase;
- (B_t): traffic-equivalent amount purchased/burned;
- (W): contractual settlement/smoothing window.

For a simple constant discount and price, expected traffic-equivalent payment is (Q_t(1-d_t)). In a real model, discounts, minimum rates, price snapshots and smoothing rules may vary by synchronizer and agreement. A cumulative shortfall should be calculated against the agreed payable schedule, not by comparing every ten-minute report to an immediate burn.

The following should be modelled separately:
1. measurement error: (hat Q_t-Q_t);
2. payment variance: actual cumulative burn-equivalent minus the agreed cumulative payable amount;
3. payment delay: time from the scheduled payable point, not simply from the end of each 10-minute measurement interval;
4. reward attribution: activity records created from purchased traffic and configured weights;
5. privacy leakage: information disclosed by each report/proof to each verifier.

CIP-0132 also says on-ledger enforcement ensures rewards are commensurate with actual burn. That is a narrower guarantee than proving that every byte consumed was correctly reported and paid for.

## 7. More precise candidate research contribution

A defensible research direction is:

**A staged accountability framework for privacy-preserving synchronizer economics: from trusted metering to verifiable report continuity, agreement-aware burn reconciliation and bounded reward attribution.**

This should be a framework and evaluation, not an assumption that one cryptographic primitive solves the entire problem.

### Candidate propositions to test

- **P1 — Commitment/completeness separation:** An append-only commitment can establish report history consistency but cannot prove that the committed reports include every eligible source interval without an independent completeness anchor.
- **P2 — Attestation boundary:** Remote attestation can reduce trust in the report-generation software but does not remove trust in the source counters, hardware root, attestation infrastructure or external input path.
- **P3 — Agreement-aware reconciliation:** Payment completeness must be assessed against a synchronizer-specific discount and smoothing agreement; interval-by-interval equality can incorrectly classify compliant delayed or discounted payment as underpayment.
- **P4 — Reward-budget separation:** A cryptographic reward budget can prevent over-issuance relative to committed purchased activity, while leaving measurement completeness as a separate unresolved property.
- **P5 — Layered controls:** Combining authenticated source snapshots, append-only report continuity, independent checkpoints and cumulative burn reconciliation may reduce reliance on any single trusted operator, with measurable overhead and privacy costs.

These are propositions for formalisation and falsification, not established findings.

## 8. Research experiments to make the work more than a literature essay

1. **Report omission experiment:** Compare a complete sequence of 10-minute reports against a sequence that silently omits one interval. Test which proposed controls detect it: operator signatures, sequence numbers, explicit zero intervals, hash chains, independent checkpoints.
2. **Split-view experiment:** Give two verifiers inconsistent report histories and test whether checkpoint gossip or independent witnesses detect divergence.
3. **Counter-boundary experiment:** Simulate participant joins/leaves, sequencer upgrades and pruning boundaries. Compare totals under different reporting semantics.
4. **Discount and smoothing experiment:** Simulate variable discount agreements, 7-day rolling smoothing and 14-day permitted delay. Measure false-positive underpayment alerts under naive interval matching versus cumulative agreement-aware reconciliation.
5. **Reward-tree experiment:** Test whether weighted Merkle expansion stays within a committed budget, and separately inject omitted eligible activity to show that budget correctness does not imply input completeness.
6. **Trust-cost comparison:** Compare operator-only reporting, signed reports, independent witnesses, TEE-assisted reports and hybrid designs by verification overhead, data exposure, operational dependencies and residual trust.

The experiments can be implemented with synthetic data and a transparent simulator. Any conclusions must be labelled as model-based until real operator data or authorised test-network access is available.

## 9. Revised research questions

- RQ1: What is the minimum evidence needed to authenticate and establish continuity of private synchronizer traffic reports?
- RQ2: Which completeness claims can be independently verified, and which still depend on the sequencer/operator trust boundary?
- RQ3: How should public CC burns be reconciled with private consumption under off-ledger discounts and smoothing agreements?
- RQ4: How can reward allocation be cryptographically bounded without disclosing private transaction payloads?
- RQ5: What is the marginal accountability gained by each trust-reduction mechanism relative to its cost, complexity and privacy leakage?

## 10. References added in this review

1. Tople, S., Park, S., Kang, M. S. and Saxena, P. (2018), “VeriCount: Verifiable Resource Accounting Using Hardware and Software Isolation,” ACNS. https://www.microsoft.com/en-us/research/publication/vericount-verifiable-resource-accounting-using-hardware-and-software-isolation-2/
2. Laurie, B., Messeri, E. and Stradling, R. (2021), RFC 9162, “Certificate Transparency Version 2.0.” https://www.rfc-editor.org/rfc/rfc9162.html
3. Hu, K., Zhang, Z. and Guo, K. (2019), “Breaking the Binding: Attacks on the Merkle Approach to Prove Liabilities and Its Applications,” *Computers & Security*, 87, 101585. https://doi.org/10.1016/j.cose.2019.101585
4. Chen et al. (2013), “Towards Verifiable Resource Accounting for Outsourced Computation” (ALIBI). Bibliographic metadata and exact system assumptions require verification against the primary paper before final citation.
5. Canton Improvement Proposal CIP-0132, “Dedicated Synchronizer Paymaster Model,” proposed 16 November 2026. https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
6. Canton Improvement Proposal CIP-0104, “Traffic-Based App Rewards,” approved 27 October 2026. https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md

## 11. Remaining review work

- Retrieve and verify the primary ALIBI paper metadata and architecture.
- Review TEE remote-attestation trust and revocation limits; do not treat enclave code identity as proof of external input correctness.
- Search privacy-preserving network telemetry and verifiable aggregation, with emphasis on completeness and collusion assumptions.
- Inspect the current CIP-0132 implementation against the proposal, particularly discounts, burn smoothing, report statuses and ActivityRecorder integration.
- Verify whether future Canton phases specify a source-verifiable or self-serve metering model. Do not infer their design from the phrase “fully trustless.”
- Only after these checks decide whether to prototype an authenticated reporting protocol, an economic model, or both.
