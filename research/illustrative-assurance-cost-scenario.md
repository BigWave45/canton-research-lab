# Illustrative Assurance-Cost Scenario Analysis

**Evidence class:** Synthetic scenario analysis.  
**Status:** Arithmetic illustration only. These values are not Canton prices, operating estimates, measured labour requirements, vendor quotes or forecasts. They must not be presented as empirical findings.

## 1. Purpose and limits

The parameterised cost calculator needs inputs before it can produce a comparison. No defensible Canton-specific cost dataset, proof implementation benchmark or audit time-and-motion dataset is currently available. This note therefore uses deliberately artificial **illustrative cost units (ICU)** to test how the cost structure behaves.

The exercise answers a narrow question: under one explicit set of assumptions, how do one-time implementation and recurring operating burdens change across the four conceptual architectures?

It does **not** establish which architecture is economically optimal. The model does not quantify assurance effectiveness, avoided losses, privacy harm, incident probabilities or source-measurement completeness. A more expensive architecture may provide stronger assurance, but this cost-only scenario does not assign a monetary value to that benefit.

## 2. Common scenario assumptions

The comparison uses the same evaluation scope for all four architectures:

- 100 reporting intervals.
- 5 exceptions requiring investigation.
- One illustrative cost unit for each review hour.
- 0.10 ICU per retained GB over the evaluation period.
- Same currency label (ICU) and same evaluation period (illustrative-100-interval-period).
- Delay cost is set to zero **only because this scenario does not model delay economics**. This is not a claim that delay has no cost.
- Residual expected loss is excluded because there are no supportable event probabilities or loss severities.

The per-architecture inputs are assumptions chosen to make the arithmetic inspectable. They are not inferred from Canton source code or operational data.

## 3. Input assumptions

| Input | Public burn only | Signed reconciliation | Independent confidential audit | Cryptographic proof |
|---|---:|---:|---:|---:|
| One-time implementation cost (ICU) | 10 | 30 | 40 | 100 |
| Report processing per interval (ICU) | 0.10 | 0.15 | 0.20 | 0.25 |
| Exception investigations (count) | 5 | 5 | 5 | 5 |
| Investigation cost per exception (ICU) | 1.00 | 1.50 | 2.00 | 1.50 |
| Human review hours | 2 | 5 | 30 | 5 |
| Loaded cost per review hour (ICU) | 1.00 | 1.00 | 1.00 | 1.00 |
| Retained evidence (GB) | 10 | 20 | 50 | 40 |
| Storage cost per GB (ICU) | 0.10 | 0.10 | 0.10 | 0.10 |
| Delay cost (ICU) | 0 | 0 | 0 | 0 |

The assumptions encode a deliberately simple cost narrative: public burn only has the smallest integration footprint; signed reconciliation adds report and manifest handling; confidential audit adds substantial human review and evidence retention; proof has the largest assumed initial engineering burden but less human review than the audit case. This narrative is a scenario design choice, not an observed property of deployed Canton systems.

## 4. Calculated results

| Cost component (ICU) | Public burn only | Signed reconciliation | Independent confidential audit | Cryptographic proof |
|---|---:|---:|---:|---:|
| One-time implementation | 10.00 | 30.00 | 40.00 | 100.00 |
| Report processing | 10.00 | 15.00 | 20.00 | 25.00 |
| Exception investigation | 5.00 | 7.50 | 10.00 | 7.50 |
| Human review | 2.00 | 5.00 | 30.00 | 5.00 |
| Evidence storage | 1.00 | 2.00 | 5.00 | 4.00 |
| Delay cost modelled | 0.00 | 0.00 | 0.00 | 0.00 |
| **Recurring cost** | **18.00** | **29.50** | **65.00** | **41.50** |
| **Total cost** | **28.00** | **59.50** | **105.00** | **141.50** |
| Increment over public-burn-only | 0.00 | 31.50 | 77.00 | 113.50 |
| Break-even avoided loss per interval | 0.000 | 0.315 | 0.770 | 1.135 |

The break-even row divides incremental cost by the common 100 intervals. It is the average avoided loss per interval that would be needed to offset the incremental cost under these assumptions. It is not a measured avoided loss, expected saving or probability-weighted benefit.

## 5. Sensitivity checks

The scenario is intentionally sensitive to assumptions that are not yet measured.

### 5.1 Independent-audit review effort

Holding the other audit inputs constant:

| Review hours | Total audit cost (ICU) |
|---:|---:|
| 10 | 85.00 |
| 30 | 105.00 |
| 60 | 135.00 |

Each additional review hour adds one ICU under the assumed hourly rate. This shows that audit economics are particularly dependent on the review protocol, automation, evidence quality and exception rate. The hour values themselves are illustrative.

### 5.2 Proof implementation cost

Holding recurring proof costs constant:

| One-time proof implementation cost | Total proof cost (ICU) |
|---:|---:|
| 60 | 101.50 |
| 100 | 141.50 |
| 180 | 221.50 |

The proof architecture's cost ranking is highly sensitive to initial engineering cost. There is no proof circuit or verifier implementation in this research project from which to estimate that cost. These values are therefore scenario inputs only.

## 6. What this exercise does and does not tell us

It tells us:
- How the current cost equation separates implementation from recurring expense.
- Which assumptions drive the illustrative totals.
- How to express an incremental-cost threshold without claiming realised savings.
- Which measurements would materially improve the comparison: implementation effort, review time, report-processing resources, storage growth and exception-handling effort.

It does not tell us:
- Actual Canton operator costs.
- Whether audit will require 10, 30 or 60 hours.
- Whether a proof system would cost 60, 100 or 180 ICU to implement.
- How frequently under-reporting, missing intervals or allocation errors occur.
- How much loss any architecture would prevent.
- Whether a proof or audit system would improve measurement completeness.

## 7. Evidence required to replace assumptions

| Assumption to replace | Required evidence | Current status |
|---|---|---|
| Implementation cost | Engineering time records, scoped build plan, or reproducible prototype effort | Not measured |
| Report-processing cost | CPU, memory and execution-time measurements on defined workloads | Not benchmarked |
| Investigation cost | Defined exception protocol and timed case reviews | Not measured |
| Human review hours | Auditor/operator time-and-motion study with case mix | Not available |
| Storage cost | Actual report/manifest sizes, retention period and applicable storage rates | Not measured |
| Delay cost | Defined economic consequence and observed delay distribution | Not established |
| Avoided loss | Defensible event frequency and loss-severity data | Not available |
| Proof overhead | Implemented circuit, proving/verifying workload and hardware profile | No implementation identified |

## 8. Research implication

The illustrative ranking is not a recommendation. It is a demonstration that architecture costs depend on measurable design choices and that a single total-cost number conceals important trade-offs.

The next empirical step should not be to tune the illustrative values until one architecture wins. It should be to replace the highest-impact assumptions with evidence, beginning with:
1. a scoped engineering-effort estimate for signed reconciliation;
2. a defined audit review protocol and timed synthetic workpapers;
3. report/manifest size and validation-runtime measurements from the existing prototypes;
4. a separate proof-system feasibility study only if the assurance matrix identifies a predicate that cannot be adequately handled more simply.

Until those data exist, the paper should label this comparison as an illustrative sensitivity exercise and avoid using it to claim economic superiority.
