# Integrated Assurance Architecture Comparison

**Status:** Research assessment and design recommendation. Qualitative ratings are analytical judgments, not measured cost, latency, detection probability or Canton production performance.

## 1. Purpose

The preceding experiments examined incomplete reports, missing intervals, agreement-version mismatch, payment smoothing, duplicate allocation and over-allocation. The privacy model separated public evidence, auditor-restricted evidence and operationally confidential data.

This report combines those results. The question is which assurance arrangement gives useful economic accountability while limiting disclosure and implementation burden.

## 2. Common assurance requirements

Any candidate must distinguish:

1. **Measurement integrity:** reported activity corresponds to chargeable source activity and the report population is complete.
2. **Calculation integrity:** the correct agreement version, pricing terms, rounding and due schedule are applied.
3. **Payment completeness:** burns cover liabilities due by the evaluation time.
4. **Allocation integrity:** a burn is not credited more than once and total allocations do not exceed the burn.
5. **Reward attribution:** the reward calculation uses the intended eligible activity and payment inputs.
6. **Dispute reproducibility:** parties can reconstruct the evidence and calculation used for a contested interval.

Passing one property does not imply passing the others.

## 3. Integrated architecture comparison

| Dimension | Public burn only | Signed reconciliation | Independent confidential audit | Cryptographic proof |
|---|---|---|---|---|
| Measurement integrity | None | Provenance and consistency only | Stronger if source records are complete and independently inspectable | Does not establish source completeness by itself |
| Calculation integrity | Not established | Checkable against authoritative agreement and due schedule | Independently recalculated | Can prove encoded rules over committed inputs |
| Payment completeness | Not established | Checkable from due schedule and burn manifest | Strong if all relevant obligations and burns are in scope | Can prove encoded payment predicates over committed inputs |
| Allocation integrity | Not established | Checkable from unique allocation manifest | Independently recomputed | Can prove uniqueness and sum constraints |
| Reward attribution | Not established by burn alone | Checkable if reward mapping and rule are included | Auditable if inputs and rule are in scope | Can prove encoded reward formula over committed inputs |
| Public disclosure | Low | Low if detailed manifest is restricted | Low if only an attestation is public | Low to medium; depends on outputs and metadata |
| Auditor disclosure | Not required in this tier | High | Very high | Medium to high for circuit and input validation |
| Residual trust | Operator measurement and off-ledger agreement | Source meter, operator and auditor independence | Auditor competence, independence and source integrity | Input completeness, keys, circuit correctness and governance |
| Implementation burden | Low | Medium | Medium to high | High |
| Incremental latency | Low | Low to medium | Medium or high due to review cycle | Medium to high until benchmarked |
| Dispute resolution | Weak | Moderate with retained signed evidence | Stronger with workpapers and appeal process | Strong for proved predicates; input truth still requires external evidence |

The table compares capabilities under stated assumptions. It does not claim that any arrangement is already implemented end-to-end in Canton.

## 4. Disclosure design

A staged design can separate evidence by audience.

### Public verification surface

Publish or expose:
- Public burn identifier, amount and timestamp.
- A commitment to a canonical settlement manifest.
- A reference to the agreement version or a commitment to it.
- A proof or attestation that allocation identifiers are unique, aggregate allocations do not exceed the burn, and the manifest references the observed burn.
- A clear status for missing, undetermined, disputed and settled intervals.

The public version should not expose exact per-synchronizer liabilities, detailed traffic reports, source records or transaction payloads by default.

A public agreement-version identifier proves only which identifier was referenced. It does not prove that the referenced version was legally authoritative. That requires a governed registry or independently verifiable agreement-authority process.

### Auditor-restricted evidence

Provide the authorised auditor with:
- Exact per-synchronizer liabilities and allocations.
- Executed agreement versions, effective dates and amendments.
- Interval measurement reports and expected-interval schedule.
- Source measurement records, retention evidence and reconciliation history.
- Reward attribution inputs and the applicable reward rule.

Auditor access should be scoped, logged and governed. Auditor independence is institutional, not cryptographic.

### Operationally confidential evidence

Keep private transaction payloads and party-level transaction data within the existing access-control model unless a specific measurement claim demonstrably requires them. Traffic metadata may still reveal timing, identity or activity patterns even without payload disclosure.

## 5. Recommended architecture: staged assurance

The evidence supports a staged design rather than a proof-first design.

**Stage A: authoritative accounting records.** Establish a canonical interval schedule, report status semantics, agreement version, liability, due tranches, burn identifier and allocation manifest. Preserve Undetermined and CannotProvide as distinct from zero activity.

**Stage B: signed reconciliation and independent audit.** Require attributable reports and reproducible reconciliation. An independent auditor checks source measurement evidence, agreement terms, due dates, burn allocations and reward mapping. Publish an attestation and exception status, not confidential source records.

**Stage C: tamper-evident commitments.** Commit to canonical manifests and retain the underlying records. This makes later alteration detectable, but does not prove the original report was complete or true.

**Stage D: selective cryptographic proofs where justified.** Add proofs for well-defined public predicates such as allocation uniqueness, aggregate allocation bounds, correct arithmetic under a committed agreement version, and reward formula execution. Do not use a proof as a substitute for source measurement assurance.

**Stage E: stronger measurement assurance only if needed.** If source completeness remains a material unresolved risk after the implementation and audit design is specified, evaluate independent measurement or independently controlled counter capture. This may increase cost, latency and governance complexity.

This order prioritises reliable records and accountable procedures before adding cryptographic machinery.

## 6. Why audit is not automatically superior

Independent audit has failure modes: incomplete source records, weak auditor independence, limited expertise, conflicts of interest, slow review and poor dispute procedures. Cryptographic proofs can reduce reliance on a verifier for arithmetic and allocation predicates, but cannot establish the truth of omitted source inputs. Signed reports improve provenance and accountability but do not guarantee measurement completeness.

The mechanisms are complementary. A strong design may combine confidential audit for source evidence with public proofs for deterministic settlement constraints.

## 7. Operational evaluation plan

No numeric cost or latency estimates are assigned before implementation evidence or benchmarks exist. Future empirical work should measure:
- Report generation and reconciliation time per interval.
- Auditor review effort and dispute-resolution time.
- Commitment creation and verification overhead.
- Proof generation and verification time, circuit complexity and proving infrastructure requirements.
- Storage and retention requirements for source reports and manifests.
- Operational failure rates for missing, delayed and undetermined reports.
- Public metadata leakage under repeated and overlapping releases.

A benchmark needs a specified workload, hardware profile, data size and proof system before numerical comparisons are credible.

## 8. Recommendation and unresolved dependency

The strongest defensible recommendation at this stage is **auditor-backed signed reconciliation, with canonical commitments and selective proofs for public arithmetic/allocation checks**.

The unresolved critical dependency is measurement completeness: what exact source records demonstrate that all chargeable activity is included, who controls those records, and how can an auditor validate them without seeing private transaction payloads?

The implementation evidence audit also found that the end-to-end report-to-burn-to-reward chain was not demonstrated in the reviewed public implementation snapshot. This recommendation is a target architecture for evaluation, not a claim that the proposed system currently satisfies these requirements.

## 9. Next research step

Translate the staged recommendation into an implementation-neutral interface specification: required fields, report status semantics, signatures, manifest commitments, agreement-version references, burn allocations, reward mapping, audit evidence and public proof predicates. Map each field to current public CIP and implementation evidence, marking it present, proposed, absent or unverified.
