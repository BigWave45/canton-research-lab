# Privacy disclosure matrix and aggregate leakage experiment

**Status:** threat-model and synthetic experiment. It does not report a privacy incident or measure a live Canton deployment.

## 1. Scope and distinction

Canton's application privacy model and CIP-0132's paymaster accounting interface are different layers.

The Canton developer privacy documentation describes transaction-tree decomposition into stakeholder views. Validators see only views for parties they host; the synchronizer handles encrypted messages, routing metadata and confirmation results rather than transaction payloads. The public-facing protocol material also describes selective disclosure and observer patterns.

CIP-0132 adds a dedicated-synchronizer traffic report: aggregate traffic for the synchronizer, returned in ten-minute intervals. The report-to-burn relationship and discount terms are off-ledger in Phase 1. The research question is therefore not whether aggregate reporting exposes transaction payloads. It is what information can be inferred from accounting aggregates, their timing, their recipients and any repeated breakdowns.

Primary sources:
- Canton privacy model: https://github.com/canton-network/cf-docs/blob/main/docs-main/appdev/deep-dives/privacy-model.mdx
- CIP-0132: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- CIP-0104: https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md

## 2. Disclosure matrix

| Evidence field | Public ledger / public release | Authorised independent auditor | Operator / paymaster | Routine handling |
|---|---|---|---|---|
| Registered synchronizer ID and registered paymaster | Public where registration is on-ledger | Verify independently | Available | Public |
| Burn event ID, amount, record time and finality | Public ledger evidence | Verify independently | Available | Public |
| Accounting schema and version | Public | Available | Available | Public |
| Settlement status and high-level aggregate amount | Consider delayed publication after policy review | Full access | Full access | Public only if disclosure analysis permits |
| Ten-minute synchronizer traffic totals | Do not assume public; disclose only if operational policy permits | Full access | Full access | Restricted |
| Signed operator report and report digest | Publish digest only if it does not expose sensitive timing or enable correlation | Full report and signature | Full report | Auditor-restricted |
| Agreement version and pricing formula | Publish generic rule or policy version, not commercial terms by default | Exact effective terms | Exact effective terms | Commercially restricted |
| Discounts, minimums, smoothing schedule and settlement deadlines | Not routine public data | Exact terms | Exact terms | Commercially restricted |
| Burn-to-obligation allocation ledger | Public aggregate proof may be possible; raw mapping is not assumed public | Full mapping | Full mapping | Auditor-restricted |
| Participant membership and join/leave times | Not public | Only if required for a scoped audit | Operational access | Highly restricted |
| Participant-level traffic counters | Never routine public disclosure | Scoped access only where necessary | Operational access | Highly restricted |
| Transaction payloads, contract terms and counterparty identities unrelated to billing | Not part of this accounting interface | Not required for ordinary paymaster audit | Not required for ordinary paymaster accounting | Excluded |

This matrix is a proposed least-disclosure policy, not a description of current Canton permissions or an assertion that a paymaster currently has every listed data field.

## 3. Threat model

Adversary: a recipient who can combine published accounting aggregates with auxiliary knowledge, public timing, known membership changes or previously released aggregates.

Protected information:
- a participant's traffic volume;
- participant presence or departure at a time;
- participant activity patterns across intervals;
- commercially sensitive pricing and synchronizer utilisation.

Out of scope:
- decrypting Canton transaction payloads;
- breaking Canton cryptography;
- compromising participant or operator infrastructure;
- inferring a participant's underlying business transaction from traffic bytes alone.

Trust assumptions:
- the operator and paymaster are trusted in the CIP-0132 Phase 1 model to report and pay correctly;
- an auditor is authorised, contractually bound and technically controlled;
- public ledger burn records are independently queryable;
- the synthetic experiment's cohort membership and byte totals are ground truth created by the experiment.

## 4. Synthetic differencing experiment

The experiment uses five synthetic participants with usage:

| Participant | Bytes |
|---|---:|
| P1 | 40 |
| P2 | 30 |
| P3 | 20 |
| P4 | 10 |
| P5 | 50 |

Two aggregate releases are made:
- Cohort A contains P1, P2, P3 and P4: 100 bytes.
- Cohort B contains P2, P3 and P4: 60 bytes.

Both groups satisfy a minimum cohort threshold of k=3. But subtracting the aggregates gives:

100 - 60 = 40 bytes

That exactly reveals P1's usage.

The result is a constructive counterexample to the claim that a minimum cohort size by itself prevents disclosure. It does not show that CIP-0132's synchronizer-wide report exposes participant-level usage. The attack requires overlapping sub-cohort releases or an equivalent source of aggregate equations. The current proposal's default synchronizer-wide aggregate is materially less granular.

The experiment is reproducible with:
- python analysis/aggregate_disclosure_experiment.py
- python -m unittest discover -s tests -p 'test_aggregate_disclosure_experiment.py' -v

## 5. Controls and their limits

**Fixed reporting cohorts and no ad hoc overlapping queries.** Avoid releasing aggregates for arbitrary overlapping participant sets. This directly reduces simple differencing opportunities. It does not stop all inference from external side information.

**Minimum cohort threshold.** Suppress small groups, but do not treat k-anonymity as sufficient. The synthetic counterexample passes k=3.

**Query and release composition audit.** Maintain a ledger of all released cohort definitions and aggregates. Reject a new release if its combination with previous releases isolates a member or creates a high-risk linear equation. Simple subset checks are only a first filter; a production design needs a broader linear-query/privacy review.

**Coarser time windows and delayed publication.** Reduces immediate correlation with known operational events and membership changes. It does not eliminate long-run inference.

**Rounding or differential privacy for public analytics.** These may be suitable for optional ecosystem dashboards, where approximate statistics are acceptable. They must not be applied silently to contractual billing evidence: payment reconciliation requires exact authoritative values. Keep the exact report auditor-restricted and create a separate privacy-protected public analytics release.

**Purpose-limited auditor access.** Give an auditor only the fields and time range needed for the defined check, with access logs, retention limits and confidentiality obligations. An auditor should not receive transaction payloads merely to verify a byte-to-burn calculation.

## 6. What can be independently verified

Publicly verifiable, if the relevant on-ledger records are available:
- that a burn event exists, its amount, its finality and the registered paymaster;
- that a published commitment has not changed since it was anchored, if the commitment is actually anchored and its binding is sound;
- the sum of public allocations if allocation records are published.

Auditor-verifiable with authorised evidence:
- operator report signature and exact interval values;
- completeness of the interval set relative to the settlement window;
- effective agreement version, pricing rule and due schedule;
- paymaster's allocation of burn events to obligations;
- participant departure evidence where contract terms make it relevant.

Not established by these checks alone:
- that source counters captured every chargeable byte;
- that a signed report is truthful merely because it is signed;
- that no undisclosed side channel exists;
- that aggregate publication guarantees anonymity;
- that the paymaster has paid the correct amount unless the agreement and allocation evidence are available.

## 7. Research implications

The design should separate:
1. a public verification surface for registration, burn events, schema and carefully selected aggregate status;
2. a restricted audit surface for signed interval reports, exact agreement terms and allocation records;
3. operationally confidential evidence for participant-level counters and lifecycle events;
4. an excluded layer for transaction payloads and unrelated counterparty data.

The privacy claim should be bounded: this design can reduce routine disclosure while enabling authorised reconciliation. It cannot establish source completeness or universal anonymity without additional mechanisms and evidence.

## 8. Next experiments

- Extend the disclosure test from nested-set subtraction to general linear combinations of released aggregates.
- Compare exact reporting, coarser windows, rounded public analytics and a separately noised public release.
- Model the cost of auditor access, delayed publication and dispute resolution.
- Revisit the matrix if the actual operator API or agreement schema exposes fields not included in this proposal.
