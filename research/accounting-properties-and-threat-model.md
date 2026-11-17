# Accounting properties and threat model

**Scope:** proposed dedicated-synchronizer paymaster accounting pipeline described by CIP-0132, considered alongside CIP-0104. This defines research properties; it does not claim they are implemented or that an exploit has occurred.

## System boundary and actors

1. Synchronizer operator / metering service: observes traffic-control counters and produces interval reports.
2. Paymaster: interprets reports and an off-ledger commercial agreement, then purchases/burns CC.
3. Global Synchronizer / public ledger: exposes the public burn event and associated ledger evidence.
4. Activity/reward mechanism: records eligible activity and computes reward entitlements.
5. Validator-supervisor governance: may register, restrict or archive participants and operators.
6. Auditor / researcher: compares evidence available to authorised parties without assuming access to private transaction payloads.

The pipeline spans private metering state, authenticated report, off-ledger pricing agreement, public burn, activity record and reward result. A link between stages must be demonstrated; temporal proximity is not sufficient attribution.

## Threat model

### Assets
- Correct measurement of chargeable traffic.
- Completeness and continuity of interval reports.
- Correct application of agreement versions, discounts, conversion and rounding.
- Completeness and uniqueness of burn attribution.
- Correct reward eligibility and amount.
- Confidentiality of private transaction payloads and participant relationships.
- Availability of sufficient evidence to resolve disputes.

### Adversary capabilities considered
- Operator omits a participant or interval, understates/overstates a counter, or provides inconsistent reports to different observers.
- Paymaster delays, splits, aggregates or underpays a settlement, or misattributes a burn.
- Report is replayed, duplicated, altered after issuance, or presented under an obsolete agreement version.
- Participant joins/leaves during an interval; sequencer upgrade or counter reset makes a boundary interval unavailable.
- Reward process receives duplicated, incomplete or inflated activity input.
- Multiple actors collude. Collusion is a residual trust assumption, not presumed absent.

### Out of scope
- Forging cryptographic primitives or compromising ledger consensus.
- Access to private payloads not legitimately available to the research.
- Claims about actual operator misconduct or production losses.

## Formal properties

Let A_i be actual chargeable traffic in interval i, potentially unobservable to an external auditor. Let R_i be reported traffic. Let P_i be payable CC under the agreement applicable to interval i. Let B_W be unique public burns attributed to settlement window W. Let E_W be agreement-implied payable for all complete intervals in W. Let Q_W be reward-eligible activity, M_W reward amount issued, and G_W the maximum authorised reward budget derived from applicable rules and paid-activity evidence.

### P1. Evidence completeness
A window is eligible for reconciliation only if every expected interval is represented by a valid report status and all required agreement versions are available. Undetermined and CannotProvide are unknown states, never zero usage.

Testable if the expected interval schedule and report statuses are available. This does not establish that all participants or traffic sources were included inside a report.

### P2. Measurement integrity
For every interval, reported amount equals defined chargeable traffic: R_i = A_i.

Not independently testable from the operator's own report alone. It requires an independent reference, trusted measurement boundary, verifiable counter transition, or explicit trust assumption. A signature or hash proves who committed to a value and whether it changed; it does not prove completeness or truth.

### P3. Agreement-correct liability
For complete evidence, expected liability is computed using the exact agreement version, price, discount, settlement window, conversion and rounding rule applicable to each interval.

Testable only when executed agreement and parameters are known. If agreement-to-report mapping is off-ledger, an auditor needs authorised access or a privacy-preserving proof of correct application.

### P4. Payment completeness
At settlement-window close, absolute difference between E_W and B_W is within contractual tolerance, after applying burn attribution and timing rules.

This is a report-to-payment property, not a measurement-integrity property. It can hold even when reported traffic differs from actual traffic.

### P5. Burn attribution uniqueness
Every counted burn is uniquely identified and assigned to at most one settlement obligation; duplicate ingestion cannot increase credited payment.

Requires stable ledger event identifiers and deterministic attribution. A burn amount alone is insufficient if multiple windows or obligations could claim it.

### P6. Reward bound
Reward issuance must not exceed the applicable authorised budget: M_W <= G_W. The budget itself must be derived from valid reward rules and eligible activity, not merely asserted by the same unverified reporter.

This is a necessary bound, not proof of correct reward distribution or complete source measurement.

### P7. View consistency
Two authorised observers receiving reports for the same synchronizer, interval and version should be able to detect conflicting content. Signed digest comparison or append-only consistency mechanisms can expose divergence if observers exchange evidence.

A commitment without cross-observer comparison may leave split views undetected. A consistent commitment still does not prove source completeness.

### P8. Privacy preservation
Verification evidence should disclose no transaction payloads and minimise participant-level information beyond what is required for billing, dispute resolution and reward allocation.

This requires leakage analysis. Aggregate reporting does not automatically guarantee anonymity; small cohorts, repeated queries and auxiliary information can reveal participant activity.

## Property/evidence matrix

| Property | Evidence needed | What it does not prove |
|---|---|---|
| Report continuity | Expected interval schedule, statuses, signed reports | All source traffic included |
| Measurement integrity | Independent measurement reference or trusted metering proof | Payment was made |
| Agreement correctness | Executed terms and versioned parameters | Reported traffic is true |
| Payment completeness | Complete reports, terms, unique burn mapping | Traffic was measured correctly |
| Burn uniqueness | Ledger event IDs and attribution rules | Correct obligation amount |
| Reward bound | Reward rules, accepted activity and issuance records | Activity source is complete |
| View consistency | Cross-observer digests/proofs | Truth of committed source data |
| Privacy | Leakage model and disclosure analysis | Correct accounting by itself |

## Hypotheses and falsification

- H1: Explicit interval coverage and unknown-state handling prevent missing reports from being silently reconciled as zero. Falsified if incomplete windows are accepted as complete without explicit policy.
- H2: Independent measurement evidence is necessary to distinguish truthful under-reporting from a fully reconciled but understated report. Falsified if the report protocol provides a verifiable completeness guarantee against the stated operator threat model.
- H3: Cross-observer digest comparison can detect inconsistent views but cannot establish source truth. Falsified if the comparison fails to detect unequal committed content, or is shown to establish more than consistency under assumptions not modelled.
- H4: A reward-budget invariant can prevent over-issuance relative to the accepted budget, but cannot repair incomplete source measurement. Falsified if issuance exceeds the budget while the invariant is correctly enforced.
- H5: Aggregate proofs may reduce payload disclosure, but participant-level leakage depends on cohort size, query frequency and auxiliary information. Quantitative leakage analysis remains required.

## Evidence discipline

Every paper claim must be labelled as specification fact, implementation fact, model result, design proposal or unknown. No synthetic test establishes real-world traffic accuracy, actual underpayment, production deployment, or absence of collusion.
