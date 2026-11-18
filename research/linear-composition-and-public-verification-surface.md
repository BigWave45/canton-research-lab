# Linear composition attacks and the public verification surface

**Status:** synthetic threat-model experiment and design proposal. No live Canton data or private participant data is used.

## 1. Why pairwise differencing is not enough

A disclosure policy must consider the full history of releases, not only whether each new query is safe by itself.

Represent each published cohort total as a row vector over a fixed participant universe. A release for P1, P2 and P3 is the equation x1 + x2 + x3 = total. A participant's value is uniquely determined if the corresponding unit vector can be expressed as a linear combination of the released cohort vectors.

## 2. Reproducible experiment

The dependency-free script analysis/aggregate_linear_leakage.py uses exact rational Gaussian elimination to calculate matrix rank. It identifies a participant variable when its unit vector lies in the row space of the published cohort matrix.

It tests:
- one synchronizer-wide aggregate: no individual is uniquely identifiable;
- two overlapping cohorts of sizes four and three: P1 is identifiable by subtraction;
- a composed set of releases: P1 remains identifiable from the full release history.

This model assumes the recipient knows cohort membership and the participant universe. It does not account for uncertainty in membership, noisy measurements, or external auxiliary information. It is a sufficient-condition audit for exact linear disclosure, not a complete privacy metric.

Run:
- python analysis/aggregate_linear_leakage.py
- python -m unittest discover -s tests -p 'test_aggregate_linear_leakage.py' -v

## 3. Full-rank reconstruction despite k=3

A four-participant construction shows why checking only nested pairs is insufficient. Let the protected traffic vector be:

`x = [A, B, C, D]^T = [40, 30, 20, 10]^T`.

Publish these four cohort totals:

| Release | Cohort | Equation | Total |
|---|---|---|---:|
| R1 | A, B, C | A + B + C | 90 |
| R2 | A, B, D | A + B + D | 80 |
| R3 | A, C, D | A + C + D | 70 |
| R4 | B, C, D | B + C + D | 60 |

Every release contains three participants, so each passes a simple minimum-cohort threshold of k=3. Yet the four equations uniquely determine all four values.

Adding the releases counts each participant three times:

`90 + 80 + 70 + 60 = 3(A+B+C+D) = 300`.

Therefore `A+B+C+D = 100`. Each participant's value is then recovered by subtracting the release that excludes that participant:

- `A = 100 - R4 = 40`
- `B = 100 - R3 = 30`
- `C = 100 - R2 = 20`
- `D = 100 - R1 = 10`

In matrix form, the release matrix is:

`M = [[1,1,1,0], [1,1,0,1], [1,0,1,1], [0,1,1,1]]`.

It has full column rank (rank 4), so all four participant variables are identifiable from the exact releases when cohort membership and the participant universe are known. This is an exact synthetic counterexample, not a Canton data observation.

**Implementation boundary:** `analysis/aggregate_linear_leakage.py` already contains an exact-rational row-space test capable of checking whether an individual unit vector is identifiable from a release matrix. Its current `run()` fixture does not include this four-release full-rank construction. This section is a hand-derived analytical example; do not imply that the new fixture was executed or added to the test suite.

## 4. Disclosure policy implications

A production disclosure controller should maintain a permanent ledger of released aggregates and their cohort/time definitions; evaluate each proposed release against the entire release history; reject releases that make protected variables exactly identifiable or create unacceptable inference risk; include timing windows and participant membership versions; and treat auxiliary public knowledge as part of the threat model.

A linear-rank test catches exact disclosure under a known fixed cohort model. The four-release example demonstrates that full-rank reconstruction can occur even when every individual cohort passes k=3. It does not prevent approximate inference, side-channel correlation, or inference where membership is only partially known. A production system needs a stronger policy and risk assessment.

## 5. Proposed public verification surface

The research should not force a choice between publishing all billing evidence and asking the public to trust an opaque burn. Separate the proof surface from confidential evidence.

**Publicly verifiable layer**
- registered synchronizer and paymaster identities;
- public burn event identifiers, amounts and finality;
- public schema/version for the accounting manifest;
- a commitment to each settlement manifest, anchored to a public record if the architecture supports it;
- a public status such as pending, reconciled, disputed or incomplete, with publication delay where timing itself is sensitive;
- an aggregate proof that allocations do not exceed the committed burn total, if a suitable proof system is justified.

**Authorised auditor layer**
- exact signed operator interval reports;
- effective agreement and pricing-rule version;
- due schedule, discounts and conversion inputs;
- full burn-to-obligation allocation;
- scoped lifecycle evidence where the contract makes participant departure relevant.

**Confidential operational layer**
- participant-level counters and join/leave events;
- internal operator telemetry;
- commercial terms not needed for public verification.

**Excluded from this accounting proof**
- transaction payloads;
- contract contents unrelated to synchronizer billing;
- counterparty identities unrelated to the billing obligation.

This division is a proposal. The current CIP does not establish that such a public commitment or proof surface exists.

## 6. What could a public proof establish?

A commitment alone establishes that a particular manifest has not changed relative to the committed digest, assuming correct cryptographic binding and a trustworthy anchor. It does not establish that the committed report is true or complete.

A public zero-knowledge proof could, in principle, establish that committed signed interval values were used; a committed pricing-rule relation was applied correctly; allocated burns are bounded by the public burn total; and settlement status follows published rules.

But the proof requires a sound statement and defined trust model. It cannot prove that the operator's source meter counted all chargeable traffic unless source completeness is itself part of the proved statement and has trustworthy inputs. A proof over incomplete inputs only proves correct arithmetic over incomplete inputs.

If commercial terms are hidden, the verifier needs a commitment to those terms and a proof that the committed values satisfy the agreed pricing relation. The auditor can inspect exact terms. Public verification can establish consistency with a committed rule without necessarily disclosing the rule, but only if the commitment, circuit and dispute process are specified.

## 7. Candidate assurance tiers

| Tier | Evidence | Public claim | Residual trust |
|---|---|---|---|
| 0: public burn only | On-ledger burn record | A registered paymaster burned this amount | No proof of traffic or liability |
| 1: committed report | Burn plus report digest | A report commitment exists and is tamper-evident after anchoring | Trust in report source and completeness |
| 2: signed report and reconciliation | Operator signature, agreement reference, allocation manifest | An identified operator attested to reports and settlement reconciles under referenced terms | Trust in operator measurement; auditor may need exact terms |
| 3: proof-carrying settlement | Cryptographic proof over committed reports, terms and allocations | Specified arithmetic and allocation invariants hold without publishing underlying values | Trust in input completeness, keys, circuit, setup and governance |
| 4: independently measured source | Tier 3 plus independent source measurement or challenge evidence | Stronger evidence that measured input corresponds to chargeable traffic | Residual dependence on measurement boundary and challenge coverage |

These tiers are conceptual. Tier 3 is not a recommendation to deploy zero-knowledge proofs immediately. First determine whether auditor-verifiable signed manifests are sufficient and what public question actually needs cryptographic proof.

## 8. Research decision

The strongest near-term architecture to evaluate is a two-surface design: exact evidence available to a purpose-limited independent auditor; and public burn and commitment/status evidence, with optional proof of allocation and reconciliation invariants.

The main unresolved research question is source completeness. Cryptography can bind a report and prove calculations over it. It cannot make an untrusted or incomplete meter truthful by itself.

## 9. Limitations

- All participant names, cohort membership and traffic values in the experiment are synthetic.
- The matrix model assumes exact integer aggregate releases and known membership.
- No privacy incident, vulnerability or underpayment on Canton is alleged.
- No production cryptographic circuit, smart contract or API is implemented.
- A commitment, signature or proof should never be described as proving more than its formally stated relation.
