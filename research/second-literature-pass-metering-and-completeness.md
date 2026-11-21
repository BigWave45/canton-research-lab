# Second Literature Pass: Metering, Attestation, and Completeness

**Review date:** 17 November 2026  
**Scope:** Deeper review of verifiable resource accounting, consumer-side accounting, hardware attestation, append-only logs, and privacy-preserving proofs of aggregate liabilities.  
**Status:** Focused scoping review. It narrows the candidate contribution; it does not establish global novelty.

## 1. The important correction: verifiable metering is not a new field

The first literature pass identified ALIBI. The deeper pass found two further directly relevant precedents:

- **VERICOUNT (Tople et al., ACNS 2018)** uses hardware and software isolation to measure CPU time, memory, I/O and network bandwidth for Linux container applications, with refutable billing support. It reports a measured performance overhead and a small trusted computing base.
- **Consumer-centric Resource Accounting in the Cloud (Mihoob, Molina-Jimenez and Shrivastava, 2013)** asks whether consumers can independently collect the data needed to verify provider bills. It distinguishes weak consumer-centric accounting (programmatic access to provider data) from strong consumer-centric accounting (independent measurement by the consumer or a trusted third party). It stresses explicit resource models, state transitions, checkpoint alignment and dispute resolution.

Therefore, the paper must not claim to invent verifiable resource accounting, customer-side billing verification, or trusted metering.

## 2. Remote attestation: useful assurance, not proof of correct accounting

Remote attestation lets a verifier check cryptographic evidence about a hardware-backed environment and the measured software configuration. It can establish that a particular measured program is running in a genuine TEE under an expected configuration, subject to the hardware vendor's trust chain and the verifier's appraisal policy.

It does **not automatically prove**:
- that the program's measurement logic models the correct billable resource;
- that every relevant event was delivered to the program;
- that the input source is complete;
- that the program has no measurement bug;
- that an attested output corresponds to all usage during the billing period;
- that the resulting invoice or token burn covers the measured quantity.

The NIST IR 8320 series and 2026 confidential-computing draft provide useful terminology and trust-chain context. The recent “Mind the Gap” work also cautions that TEE evidence has residual provenance and deployment assumptions.

**Design implication:** A TEE is one possible way to protect a measurement component, not the research contribution by itself. Any TEE-based design must state its threat model, attestation issuer, reference-value governance, rollback protection, upgrade process, availability assumptions and residual trust in the sequencer/counter source.

## 3. Append-only logs: consistency is not completeness

RFC 9162 (Certificate Transparency v2) formalises:
- inclusion proofs: an entry is included in a particular Merkle tree;
- consistency proofs: a later tree is an append-only extension of an earlier tree.

These are powerful tools for detecting equivocation and proving that previously committed entries have not been silently changed or removed from the committed prefix.

But an append-only log cannot prove that the source submitted every event that should have been logged. A log can faithfully preserve an incomplete input stream.

For synchronizer traffic, a chained report sequence or Merkle log could establish:
- the same report history is being shown to different auditors;
- a report interval was committed by a particular time;
- previously committed reports have not been rewritten;
- the report sequence has no gaps, if interval sequence numbers and expected boundaries are independently known.

It cannot, on its own, establish:
- that all participant traffic reached the measurement process;
- that a departing participant's final counter was included;
- that an operator did not omit an interval before committing the sequence;
- that the counter values reflect the correct billable resource.

This yields a critical distinction for the paper:

**Commitment integrity** answers “has this committed record changed?”  
**Sequence completeness** answers “are all expected records in the committed sequence?”  
**Source completeness** answers “did the measurement source capture every event that should count?”

The three properties require different assumptions and evidence.

## 4. Proofs of liabilities: aggregate correctness needs more than a root hash

The literature on summation Merkle trees and privacy-preserving proofs of liabilities shows that aggregate proofs can fail when the relation between leaf values, internal nodes and the root is not fully constrained. Hu, Zhang and Guo (2019) formalise an attack on the Maxwell proof-of-liabilities protocol and propose repairs. “Distributed Auditing Proofs of Liabilities” (IACR ePrint 2020/468) provides further formal treatment of secure summation Merkle structures and distributed verification.

More recent work on privacy-preserving proofs of liabilities, including the 2023 ACM CCS paper using sparse summation Verkle trees, shows that stronger hiding commitments and succinct proofs can prove a user's liability is included in a total without disclosing other users' data.

**Design implication:** A Canton traffic/reward commitment needs to define precisely:
- what each leaf represents;
- how leaves are uniquely identified and ordered;
- how duplicate, missing and stale leaves are handled;
- how numeric values are bound to hashes;
- how parent sums are constrained;
- how the root total is tied to a separately verifiable purchase/burn ceiling;
- how the verifier knows the committed set is complete for the claimed interval.

A valid proof that a leaf is included in a root is not proof that all eligible leaves are present.

## 5. Narrowed research gap

The broad research area is already populated: verifiable metering, customer-side accounting, TEEs, append-only logs, Merkle commitments and privacy-preserving proofs of liabilities all have established literatures.

The more defensible candidate contribution is a **cross-layer accountability model for private, multi-party resource billing** in which:
1. a synchronizer operator controls or reports the metering view;
2. a separate paymaster submits public token purchases/burns;
3. reward rights depend on purchased traffic and activity weights;
4. private transaction payloads and participant-level activity should remain confidential;
5. multiple actors need enough evidence to detect incomplete reporting, underpayment, inconsistent report histories and reward-budget violations.

The novelty candidate is not a new primitive. It is the formal decomposition and evaluation of the assurance obligations across these layers, together with a protocol design that states which actor can verify each property and under which trust assumptions.

This remains provisional pending a wider search for resource billing in permissioned ledgers, multi-operator metering, synchronizer economics, and confidential audit protocols.

## 6. Proposed assurance model

Represent the accounting pipeline as five linked objects:

1. **Source state** (S_t): sequencer/participant cumulative traffic counters and their epoch/version.
2. **Interval report** (M_t): synchronizer ID, interval sequence, record-time bounds, source state references, traffic total, status and software/configuration version.
3. **Commitment** (L_t): authenticated commitment to the ordered report history, with inclusion and consistency proofs.
4. **Payment record** (P_t): on-ledger traffic purchase, payer identity, synchronizer identity, purchased byte quantity and CC burn.
5. **Reward record** (R_t): activity commitment, weight budget, authorised purchase ceiling and reward issuance.

The key relationships are not interchangeable:

- **Source-to-report correctness:** (M_t) accurately derives from (S_t).
- **Report-history consistency:** (L_t) preserves the committed sequence.
- **Report completeness:** all expected intervals and relevant source participants are represented.
- **Payment coverage:** cumulative eligible purchases cover cumulative chargeable reports under the pricing rule.
- **Reward boundedness:** issued rewards do not exceed the authorised activity/purchase budget.

The first four should be evaluated separately. Reward boundedness can be formally enforced even while source completeness remains a trusted assumption.

## 7. Candidate architecture to evaluate, not assume

A plausible baseline is a **sequenced, signed interval-report log**:

- Each report carries a monotonic interval number, synchronizer ID, interval bounds, counter-source epoch and cumulative counter endpoints.
- Each report is hash-linked to the previous report and periodically anchored or attested.
- A verifier can obtain inclusion and consistency proofs for the history.
- A reconciliation contract or independent auditor compares cumulative report totals with cumulative purchases and burn records.
- Reward commitments bind app activity to the authorised purchased-traffic ceiling.

This baseline is intentionally modest. It uses established authenticated-log mechanisms before considering zero-knowledge proofs or hardware attestation.

The critical unresolved question is how to establish source completeness without requiring every participant to disclose private transaction data. Options to compare include:
- sequencer-signed counter snapshots;
- threshold attestations from independently operated infrastructure;
- participant-side receipts or counters;
- TEE-protected metering;
- zero-knowledge proofs over authenticated counter transitions;
- a hybrid in which the operator attests the aggregate while independent participants challenge sampled intervals.

Each option has a different trust, privacy, complexity and operational-cost profile. No option should be selected before modelling the adversary and the data actually available from Canton.

## 8. Falsifiable properties and tests

A prototype should test the following properties:

| Property | Falsifiable test |
|---|---|
| Report integrity | Modify a committed report; verification must fail |
| History consistency | Present divergent report histories to two auditors; consistency checks must detect the fork or equivocation |
| Interval sequencing | Omit, duplicate or reorder an interval; the verifier must detect a sequence gap or duplicate |
| Counter continuity | Reset or roll back a counter without a declared epoch transition; verification must fail |
| Join/leave accounting | Add or remove a participant during an interval and compare the stated billing policy with the resulting aggregate |
| Upgrade handling | Span a logical synchronizer/sequencer upgrade and verify continuity across epochs |
| Payment coverage | Make purchases below cumulative reportable consumption; reconciliation must show the deficit |
| Pricing correctness | Change CC/USD conversion, list price, discount or rounding rule; independently recompute the charge |
| Reward budget | Expand a reward tree beyond the authorised traffic/activity budget; ledger/property check must reject it |
| Source omission | Suppress an event before it enters the report log; determine whether the chosen source-assurance mechanism can detect it |

The last test is the hardest and most important. A plain hash chain, Merkle root or signed report cannot detect an event that never entered the source data.

## 9. Research hypotheses to retain for formalisation

- **H1:** Authenticated append-only report history can detect post-commitment alteration and equivocation, but cannot establish source completeness without an independent source assumption or witness.
- **H2:** A payment reconciliation rule over cumulative report and purchase totals can detect underpayment, but cannot determine whether the report itself is complete.
- **H3:** Reward-budget invariants can bound issuance relative to committed activity and purchased traffic, but do not prove that the committed activity set contains every eligible event.
- **H4:** Increasing independent measurement assurance reduces reliance on a single operator but adds coordination, privacy leakage, verification cost or operational complexity; the trade-off is measurable under explicit threat models.

These are testable statements, not conclusions. H4 especially requires a defined cost model and should not be treated as universally true without qualification.

## 10. Sources added in this pass

1. Chen et al. (2013), “Towards Verifiable Resource Accounting for Outsourced Computation” (ALIBI), VEE 2013. https://www.contrib.andrew.cmu.edu/~vsekar/assets/pdf/vee13_alibi.pdf
2. Tople et al. (2018), “VERICOUNT: Verifiable Resource Accounting Using Hardware and Software Isolation,” ACNS 2018. https://www.microsoft.com/en-us/research/publication/vericount-verifiable-resource-accounting-using-hardware-and-software-isolation-2/
3. Mihoob, Molina-Jimenez and Shrivastava (2013), “Consumer-centric resource accounting in the cloud,” *Journal of Internet Services and Applications*. https://doi.org/10.1186/1869-0238-4-8
4. NIST IR 8320 (2022), “Hardware-Enabled Security: Enabling a Layered Approach to Platform Security.” https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8320.pdf
5. NIST IR 8320E initial public draft (May 2026), “Hardware-Enabled Security: Confidential Computing of Data in Cloud Workloads.” https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8320E.ipd.pdf
6. Rezabek and Passerat-Palmbach (2026), “Mind the Gap: Where TEE Attestations Fall Short and Why We Need Proof of Cloud.” https://www.net.in.tum.de/fileadmin/bibtex/publications/papers/Rezabek-SysTEX-2026.pdf
7. Laurie et al. (2021), RFC 9162, “Certificate Transparency Version 2.0.” https://www.rfc-editor.org/rfc/rfc9162.html
8. Hu, Zhang and Guo (2019), “Breaking the binding: Attacks on the Merkle approach to prove liabilities and its applications,” *Computers & Security* 87, 101585. https://doi.org/10.1016/j.cose.2019.101585
9. “Distributed Auditing Proofs of Liabilities,” IACR ePrint 2020/468. https://eprint.iacr.org/2020/468.pdf
10. “Short Privacy-Preserving Proofs of Liabilities,” ACM CCS 2023. https://doi.org/10.1145/3576915.3616645

## 11. Next research action

Before proposing a specific protocol, inspect the current CIP-0132 and CIP-0104 normative text and map every field and actor in the model to an actual contract, API, sequencer state or governance process. Confirm which evidence is exposed to an operator, paymaster, participant and SV. If the data required for the proposed tests is not available, the paper must remain a formal design and simulation study rather than imply an empirical evaluation.
