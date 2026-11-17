# Comparative Assurance Model: Formal Specification

**Status:** Research specification; not an empirical result or a Canton protocol proposal.  
**Case study:** Proposed Dedicated Synchronizer Paymaster Model under CIP-0132.  
**Purpose:** Compare assurance architectures for private-activity measurement, contractual payment, public burn evidence and reward attribution.

## 1. Research question

What verifiable accounting guarantees can be added to the proposed dedicated-synchronizer paymaster model, and what are their economic, privacy and operational costs?

The unit of analysis is one synchronizer, one paymaster and one accounting interval, with portfolio extensions where obligations share a paymaster.

## 2. Accounting chain

For synchronizer s and interval t:

1. The synchronizer incurs chargeable activity.
2. A measurement process produces a report.
3. An off-ledger agreement maps reportable activity to a liability.
4. A paymaster burns CC, potentially according to a smoothing schedule.
5. The resulting activity/payment evidence feeds reward attribution.
6. An auditor or public observer checks the evidence available to them.

The model keeps these stages separate. Evidence for a later stage does not automatically validate an earlier stage.

## 3. Variables and notation

| Symbol | Definition | Evidence status |
|---|---|---|
| u(s,t) | Actual chargeable resource consumption | Latent unless independently measured |
| u_hat(s,t) | Reported consumption | Reported value |
| e(s,t) = u_hat - u | Measurement error | Identifiable only with a valid reference measurement |
| A(v) | Version v of the applicable off-ledger agreement | Confidential agreement evidence |
| P(s,t) | Liability calculated under A(v) | Recomputable if report and agreement are available |
| B(s,t,w) | CC burn allocated to the obligation by time window w | Public burn evidence plus allocation manifest |
| R(s,t,w) = P_due - B_allocated | Due-date-adjusted payment residual | Recomputable if liability, due schedule and allocation are available |
| W(i,e) | Reward attributed to participant i in epoch e | Reward evidence and applicable rule |
| W_star(i,e) | Reward that follows from the agreed attribution rule and valid activity evidence | Reference value in a controlled experiment |
| C_priv | Privacy exposure from disclosed evidence | Operationalised by disclosed fields and inference tests |
| C_ops | Operational burden | Measured or explicitly scored implementation effort |
| L | Reconciliation latency | Time from interval close to independently checkable result |

All monetary quantities must use a declared unit and conversion rule. CC amounts must not be silently mixed with USD values. Resource units and agreement pricing are versioned inputs, not assumed protocol constants.

## 4. Core accounting properties

The model evaluates the following properties:

1. **Measurement traceability:** the report identifies its source, interval, status and measurement method.
2. **Completeness:** every required interval and applicable participant population is accounted for, or explicitly marked incomplete/undetermined.
3. **Agreement correctness:** the liability uses the correct agreement version, pricing schedule, rounding and lifecycle policy.
4. **Payment reconciliation:** allocated burns cover liabilities when due, without double allocation or premature shortfall classification.
5. **Reward consistency:** attributed rewards follow the declared reward rule and the accepted activity/payment evidence.
6. **Privacy minimisation:** each verifier receives only the information necessary for its role.
7. **Dispute reproducibility:** an authorised reviewer can reproduce the calculation and identify the source of disagreement.

Missing or undetermined evidence is never converted to zero. A report marked unavailable is not evidence of zero activity.

## 5. Assurance architectures

### A. Public burn records only

Evidence: public CC burn events and whatever public metadata accompanies them.

Can establish: that specified burns occurred, subject to correct event interpretation.

Cannot by itself establish: private activity, report completeness, agreement liability, allocation to a particular interval, or party-level reward correctness.

### B. Signed reports plus agreement-aware reconciliation

Evidence: operator-authenticated interval reports, versioned agreement terms, deterministic liability calculation, paymaster allocation manifest and public burn references.

Can establish: report provenance, reproducibility of the contractual calculation, and whether observed burns reconcile with declared obligations.

Residual limitation: signatures authenticate the signer and document integrity; they do not prove the source meter counted all chargeable activity.

### C. Independent confidential audit

Evidence: controlled auditor access to reports, source records, agreement terms, calculations and burn allocations; public output is a limited audit attestation.

Can establish: stronger source-to-report and agreement-to-payment checks to the extent the auditor can inspect reliable source evidence.

Residual limitation: auditor competence, independence, access completeness and audit procedures remain trust assumptions. Public observers generally cannot reproduce confidential checks.

### D. Cryptographic proofs over private accounting data

Evidence: commitments to canonical records and proofs that specified calculations or rules hold over committed inputs.

Can establish: integrity of committed records and correctness of encoded calculations, subject to circuit/specification correctness and sound input binding.

Cannot by itself establish: that the source measurement captured all real chargeable activity. A proof over incomplete or false inputs can still be a valid proof of the wrong accounting result.

A hybrid of B, C and selected D components is allowed as a candidate design; it must be evaluated as a distinct staged architecture rather than assumed superior.

## 6. Controlled scenario design

All initial experiments use synthetic inputs, clearly labelled as such. The same base case is run through every architecture.

Base case:
- Actual activity: 100 resource units.
- Reported activity: 100 resource units.
- Agreement-derived liability: 10 CC.
- Burn allocated by the due date: 9 CC.
- Reward rule: a declared deterministic function supplied as an experiment parameter.

The values are illustrative only and are not Canton measurements, prices or policy parameters.

Perturbations:
1. **Under-reporting:** reported activity is below actual activity.
2. **Over-reporting:** reported activity is above actual activity.
3. **Missing interval:** one required interval has no usable report.
4. **Agreement-version mismatch:** calculation uses a stale or incorrect agreement version.
5. **Smoothing:** part of the liability is not due until a later contractual date.
6. **Burn misallocation:** one public burn is claimed against multiple obligations or intervals.
7. **Participant lifecycle:** participants join or leave within an interval.
8. **Reward misattribution:** aggregate payment is correct but participant-level allocation is wrong.
9. **Repeated aggregate disclosure:** multiple releases may reveal confidential participant-level values.
10. **False but internally consistent source data:** a signed report or proof is internally valid while its source measurement is incomplete.

Each scenario records which property is violated, which architecture detects it, what evidence is required, and whether the result is public or auditor-restricted.

## 7. Evaluation metrics

| Dimension | Proposed measure |
|---|---|
| Measurement error | Absolute and relative error, only where independent reference activity is available |
| Liability error | Absolute difference between calculated and reference contractual liability |
| Payment residual | Due-date-adjusted CC shortfall or surplus |
| Burn allocation integrity | Duplicate claims and total allocated amount in excess of observed burn |
| Reward attribution error | Total variation distance between reference and reported participant reward distributions |
| Detection coverage | Share of injected scenario failures detected by the architecture |
| False assurance | Share of invalid cases incorrectly classified as reconciled |
| Privacy exposure | Number/type of disclosed fields plus successful inference in defined leakage tests |
| Operational cost | Implementation components, operator/auditor effort and recurring process burden |
| Latency | Time from interval close to checkable reconciliation |
| Dispute reproducibility | Whether an independent authorised reviewer can reproduce the disputed result |

Detection coverage is scenario-suite coverage, not a real-world probability of fraud detection. Synthetic test frequencies must not be interpreted as empirical incident rates.

## 8. Experimental protocol

1. Freeze the scenario inputs, agreement rules and reward function.
2. Define the reference accounting outcome independently of the architecture being tested.
3. Run each scenario through each architecture.
4. Record evidence required, detection result, false-assurance result, privacy disclosure and operational steps.
5. Repeat with sensitivity ranges for audit frequency, measurement error, report availability, settlement delay and proof/audit cost.
6. Publish code, test fixtures, assumptions and machine-readable results.
7. Separate observed implementation facts, synthetic experiment outputs and normative design recommendations in all reporting.

## 9. Hypotheses to test

- **H1:** Public burn records alone cannot identify whether private activity was completely measured or contractually paid.
- **H2:** Signed reports and agreement-aware reconciliation improve calculation and payment traceability but do not independently establish source-measurement completeness.
- **H3:** Independent confidential audit can improve source-to-report assurance, with additional auditor trust, cost and privacy-governance requirements.
- **H4:** Cryptographic proofs can reduce the information disclosed to public verifiers while preserving verifiability of specified calculations, but do not eliminate trust in source measurement.
- **H5:** A staged architecture may offer a better assurance-cost-privacy trade-off than applying cryptographic proofs to every accounting step.

These are falsifiable research hypotheses, not findings.

## 10. Scope boundaries and limitations

- CIP-0132 is treated as a proposal, not a claim of fully deployed production operation.
- The model does not presume access to private Canton transaction payloads.
- No public CC transfer metric is treated as total Canton settlement volume.
- No synthetic input is described as observed network activity.
- No universal pricing formula is assumed; the agreement is an explicit input.
- Cryptographic proofs are not treated as proof of truthful or complete measurement without an independently justified measurement source.
- The model evaluates accounting assurance, not general protocol security.

## 11. Decision rule for the final recommendation

A mechanism is recommended only if its incremental assurance is demonstrated against the scenario suite and its privacy, cost, latency and residual trust assumptions are reported. The strongest cryptographic mechanism is not automatically the preferred mechanism. The final recommendation may be staged or hybrid if the evidence supports that result.
