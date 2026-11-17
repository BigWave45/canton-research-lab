# Hypothesis and Test Protocol

**Status:** provisional research design; no empirical findings  
**Date:** 17 November 2026  
**Scope:** CIP-0132 Phase 1 trusted paymaster accounting and possible staged accountability mechanisms

## 1. Research question

How can a privacy-preserving synchronizer convert operator-reported traffic consumption into CC burns and reward entitlements while making the accounting more independently verifiable, without requiring public disclosure of participant-level transaction activity?

The study evaluates accounting properties and design trade-offs. It does not presume operator misconduct, a protocol exploit, or a deployed defect.

## 2. System boundary and accounting objects

Keep the following quantities distinct:

- (x_{i,t}): actual traffic consumed by participant (i) in interval (t), as defined by the synchronizer's metering system.
- (r_{i,t}): traffic reported for participant (i), where the applicable report is participant-level or aggregate.
- (R_t): total reported traffic for the relevant settlement window.
- (B_w): CC burned by the paymaster over settlement window (w).
- (P_w): CC payment implied by the operator-paymaster agreement, including applicable list prices, discounts, conversion rules and smoothing.
- (A_w): reward-eligible activity recorded through the applicable activity-recorder mechanism.
- (Q_w): reward entitlement generated from eligible burn/activity under the relevant rules.

These are not interchangeable. In particular, (B_w) need not equal a naïve per-interval list-price calculation if discounts, conversion, aggregation or delayed burn are permitted.

The baseline must encode the actual proposal and agreement semantics before any discrepancy is labelled an error.

## 3. Provisional hypotheses

### H1 — Window-aware reconciliation detects payment shortfalls more reliably than interval equality

**Claim:** Given an agreed pricing and settlement rule, cumulative reconciliation over the contractually defined settlement window will classify legitimate smoothing and delayed burns more accurately than comparing each ten-minute traffic report with an immediate burn.

**Test:** Generate or obtain traffic reports with (a) immediate payment, (b) weekly aggregation, (c) rolling-window settlement, (d) delayed burn, and (e) permitted discounts. Compare false-positive and false-negative classifications under interval equality and agreement-aware cumulative reconciliation.

**Measures:** false-positive rate, false-negative rate, detection delay, unexplained residual CC, and proportion of report volume reconciled by window close.

**Falsification:** If interval equality performs as well across all permitted settlement patterns, or window-aware reconciliation cannot reliably identify injected shortfalls, the claimed advantage is unsupported.

**Evidence status:** model-testable now; empirical validation requires real report, agreement and burn records.

### H2 — A valid commitment proves report integrity properties, but not source completeness by itself

**Claim:** A Merkle commitment to a traffic report can make later alteration or selective disclosure detectable under stated cryptographic assumptions, but cannot prove that the source metering process included every eligible event.

**Test:** Construct adversarial cases with (a) a changed committed record, (b) an omitted source event before tree construction, (c) inconsistent tree views, (d) duplicate records, and (e) valid inclusion proofs against an incomplete committed set. Compare a bare Merkle root with signed tree heads, consistency proofs, sequence continuity and an independently anchored source counter.

**Measures:** attacks detected, attacks undetected, proof size, verification cost and additional trust assumptions.

**Falsification:** The hypothesis must be narrowed if the specified source-counter or attestation mechanism independently establishes completeness under a clearly stated threat model. A hash commitment alone is not assumed to do so.

**Evidence status:** protocol-design and executable adversarial simulation; requires careful threat-model specification.

### H3 — Independent reconciliation of report totals and public burns can bound payment discrepancies without exposing participant transaction payloads

**Claim:** If the system publishes sufficiently granular signed aggregate report commitments and burn records, an auditor can bound discrepancies between reported consumption and payment while participant-level transaction payloads remain private.

**Test:** Model aggregate reports, burn events, report hashes, settlement windows and permitted pricing transformations. Evaluate what an auditor can infer from aggregate data alone and what requires selective disclosure or an authorised audit.

**Measures:** maximum undetected discrepancy, disclosure volume, auditor verification cost, and residual ambiguity in participant attribution.

**Falsification:** If the public aggregates cannot distinguish materially different underpayment scenarios, or the required verification necessarily reveals protected participant-level information, the proposed public-audit property is not achievable in that form.

**Evidence status:** model-testable; depends on the final report and burn schemas and the agreed pricing contract.

### H4 — Audit incentives can reduce expected misreporting losses, but only when detection and enforcement are credible

**Claim:** Under a principal-agent model, increasing audit probability or detection accuracy reduces the expected gain from misreporting only when penalties, collateral loss or governance consequences are enforceable and exceed the expected benefit of misreporting.

**Test:** Specify operator benefit from under-reporting, probability of audit, detection sensitivity, false-positive probability, penalty, collateral at risk, and appeal cost. Derive incentive-compatibility conditions and conduct sensitivity analysis.

**Measures:** minimum audit probability, minimum enforceable penalty/collateral, expected loss, operator participation constraint and false-accusation cost.

**Falsification:** If feasible parameter ranges do not satisfy both truthful-reporting incentives and operator participation, the proposed audit regime is not economically viable without another enforcement mechanism.

**Evidence status:** theoretical and scenario-based; parameters must be labelled illustrative until supported by contracts or observed data.

### H5 — Stronger accountability introduces measurable cost and privacy trade-offs

**Claim:** Moving from trusted aggregate reporting to independent attestations, challenge mechanisms or cryptographic proofs increases verification assurance but also introduces operational cost, latency, data availability requirements or additional trust assumptions.

**Test:** Compare four staged designs: (1) trusted operator/paymaster reporting, (2) signed reports with sequence continuity and public burn reconciliation, (3) sampled independent audit/challenge, and (4) cryptographic or hardware-backed attestation. Score each against a common threat model and model verification cost and disclosure.

**Measures:** verification latency, computational cost, proof/report size, audit effort, privacy leakage surface, availability assumptions and number/type of trusted parties.

**Falsification:** If a stronger design dominates the baseline on all measured dimensions under the same threat model, the proposed trade-off is not demonstrated. If assurance cannot be meaningfully compared, report the dimensions separately rather than creating a composite score.

**Evidence status:** comparative architecture analysis and simulation; actual operational costs require implementation benchmarks.

## 4. Experimental plan

### Experiment A — Reconciliation engine

Build a deterministic, dependency-free simulator for traffic reports, settlement windows, discount rules, CC conversion and burn events. Include exact expected outputs and unit tests. Keep protocol parameters separate from scenario assumptions.

### Experiment B — Adversarial report integrity

Generate omitted, duplicated, reordered, altered and split-view records. Compare hash-only commitments, signed append-only logs, continuity counters and sampled audit. Record exactly which attacks each control detects.

### Experiment C — Incentive compatibility

Derive the operator's expected utility under truthful and false reports. Sweep audit probability, detection rate, penalty/collateral, misreporting gain and false-positive costs. Identify feasible parameter regions rather than selecting convenient point estimates.

### Experiment D — Privacy and assurance comparison

For each design, state what is visible to the operator, paymaster, synchronizer governance, public observer and independent auditor. Avoid treating pseudonymisation or aggregation as automatic anonymity.

## 5. Evidence requirements and stop conditions

Before empirical claims, obtain and preserve:

1. The exact CIP-0132 revision and its status at the time of analysis.
2. The relevant implementation commit/PR and test suite, with merged/draft status.
3. The traffic-report schema, interval semantics, error states and pagination/retention behaviour.
4. The paymaster registration, purchase, burn and activity-recorder contract semantics.
5. The applicable pricing agreement, including discount, conversion, smoothing, settlement and dispute terms.
6. A reproducible sample linking report windows to burn records, if access is authorised.

If items 3–5 cannot be established, restrict conclusions to proposal-level design analysis and synthetic scenarios. Do not label model outputs as observed network performance. If no authorised linked dataset is available, do not claim to have measured real operator accuracy or real underpayment.

## 6. Novelty boundary

The project will not claim novelty for Merkle trees, verifiable resource accounting, audit sampling, trusted execution environments, principal-agent auditing or public burn records individually.

The candidate contribution is a Canton-grounded comparison of how these controls compose across a privacy-preserving traffic-report → CC-burn → reward pipeline, with explicit separation of source-measurement completeness, report integrity, payment reconciliation and reward bounds.

This remains a candidate contribution until a broader literature search and implementation review confirm the gap.

## 7. Decision gate

Do not select a final paper title or promise a protocol improvement until:

- the hypotheses are mapped to actual CIP-0132 semantics;
- the report and burn pipeline is traced end-to-end in source;
- the Merkle proof-of-concept's assumptions are independently checked;
- at least one experiment is executable and reproducible;
- the official Community Research Grant terms and eligibility are verified.

## 8. Core sources to preserve

- CIP-0132: https://github.com/canton-foundation/cips
- CIP-0104: https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md
- Splice multi-synchronizer implementation: https://github.com/canton-network/splice-multi-sync
- Extension-synchronizer implementation tracker: https://github.com/ChainSafe/canton-extending-mainnet
- Certificate Transparency, RFC 9162: https://www.rfc-editor.org/rfc/rfc9162
- VeriCount (ACNS 2018): https://link.springer.com/chapter/10.1007/978-3-319-98113-0_11
