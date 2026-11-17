# Quantitative Evaluation Plan for Accounting-Assurance Architectures

**Status:** Research design, not a benchmark or empirical result. This plan defines how to compare the four assurance architectures without inventing Canton operating costs, error probabilities or privacy guarantees.

## 1. Evaluation question

For each architecture, what additional accounting properties can be verified, what evidence must be disclosed to whom, and what incremental economic and operational burden is introduced?

The comparison must preserve three evidence classes:

- **Observed/documented:** facts established by a public CIP, implementation source, issue/PR state or reproducible repository artifact.
- **Synthetic/modelled:** results produced from explicit constructed inputs and assumptions.
- **Unknown/unmeasured:** production costs, failure frequencies, source-meter completeness and performance values not established by available evidence.

Do not combine these classes into a single score.

## 2. Architecture set

Use the four existing architectures without silently changing their definitions:

1. Public burn only.
2. Signed reconciliation.
3. Independent confidential audit.
4. Cryptographic proof.

The second and fourth are capability abstractions in the current model, not implemented report-signing or proof-verification systems. The audit architecture assumes complete and sufficiently reliable source records that have not yet been demonstrated as available. Keep these caveats beside every result.

## 3. Assurance effectiveness

### 3.1 Scenario coverage

Retain the six existing synthetic scenarios:

- accurate accounting;
- under-reporting;
- missing interval;
- agreement-version mismatch;
- smoothing not yet due;
- overdue smoothing shortfall.

For every architecture/scenario pair, report the specific predicate that is and is not established:

- expected interval present;
- report-to-agreement binding consistent;
- liability calculation reproducible;
- amount due at evaluation time covered by burn;
- allocation unique and bounded by burn;
- reward attribution traceable to eligible inputs;
- source measurement completeness independently supported.

Do not turn the number of detected synthetic scenarios into a real-world detection rate. Six constructed cases are not a statistical sample. Report a capability matrix and explain the evidence needed for each predicate.

### 3.2 Additional falsification cases

Only add a case if it tests a distinct accounting property not already covered. Candidate cases, subject to source mapping first:

- duplicate burn allocation across two obligations;
- valid burn assigned to the wrong synchronizer or interval;
- reward attribution uses an ineligible or duplicated allocation;
- correction arrives after an interval was marked settled;
- agreement amendment becomes effective inside a reporting interval.

Before implementing any case, state the invariant, the counterexample, the expected architecture behaviour and the relevant CIP/source rule. Do not add cases merely to increase test count.

## 4. Economic cost model

For architecture (a), define incremental total cost over an evaluation period:

[
C_a = F_a + N_r c_{r,a} + N_i c_{i,a} + H_a w + S_a c_s + D_a + R_a
]

Where:

- (F_a): one-time implementation and integration cost, amortised only if a defensible service life is specified;
- (N_r): number of reports or intervals processed;
- (c_{r,a}): marginal report-processing cost per interval;
- (N_i): number of exceptions or disputes reviewed;
- (c_{i,a}): marginal investigation cost per exception;
- (H_a): recurring human review and governance hours;
- (w): loaded hourly labour cost;
- (S_a): retained evidence volume;
- (c_s): storage and retention cost per unit;
- (D_a): measurable delay cost, where an economic consequence and timing data exist;
- (R_a): expected residual-loss term, included only if event probabilities and loss severities can be supported.

If inputs are unavailable, keep the term symbolic or show a sensitivity surface. Do not insert a guessed probability into (R_a). Report one-time and recurring costs separately. Avoid treating CC burns as assurance-system operating costs: the burn is the settlement being accounted for, not automatically the incremental cost of the assurance architecture.

### 4.1 Parameters that can be measured in a prototype

- Report bytes and manifest bytes per interval.
- CPU time and peak memory for canonicalisation, validation and commitment creation.
- Proof generation and verification time, only if an actual proof implementation exists.
- Storage growth per interval and retention period.
- Auditor minutes per ordinary interval and per exception, measured from a defined review protocol.
- Reconciliation elapsed time, with start/end events defined.
- Dispute-resolution elapsed time, measured separately from routine reconciliation.

Record hardware, software versions, workload size, concurrency, warm/cold state and sample count. Report distributions (at minimum median and 95th percentile) rather than a single best run. If no implementation exists, mark the metric **not benchmarked**, not zero.

### 4.2 Break-even analysis

Where measured inputs exist, compare the incremental cost of architecture (a) with a baseline:

[
Delta C_a = C_a - C_{	ext{public-burn-only}}
]

A break-even analysis may compare (Delta C_a) with a separately evidenced reduction in expected dispute or settlement loss. If the reduction cannot be estimated from data, present the break-even threshold as a conditional statement (for example, the minimum avoided loss per interval required to justify the added cost), not as a claimed realised benefit.

## 5. Privacy and disclosure measurement

Separate contractual billing evidence from optional public analytics.

For each release surface, record:

- fields disclosed;
- audience and access conditions;
- temporal granularity;
- participant/cohort granularity;
- whether releases overlap;
- whether values are exact, rounded, delayed or perturbed;
- retention and query history.

Run the existing synthetic aggregate-differencing examples and extend them to a linear-system analysis of the released aggregates. For a constructed participant vector (x) and release matrix (A), test whether the published values (y=Ax), together with stated auxiliary knowledge, uniquely determine a protected participant value.

Report:
- number of protected values exactly recoverable;
- number recoverable only under specified auxiliary knowledge;
- rank and null-space properties of the constructed release system;
- the minimum additional release that makes a previously hidden value recoverable.

These are properties of the synthetic release design, not measured Canton leakage. Do not label them differential privacy, anonymity or a formal privacy guarantee. Differential privacy would require a defined neighbouring-dataset relation, privacy parameter, mechanism and composition accounting; none is currently implemented.

A disclosure field count can describe exposure surface but is not itself a privacy-risk score. Do not assign arbitrary weights to identity, timing, amount and cohort leakage.

## 6. Operational reliability and latency

Measure or document separately:

- report arrival delay;
- time to identify a missing interval;
- time to reconcile a complete interval;
- time to escalate a discrepancy;
- time to complete an audit or dispute;
- time to publish a public commitment or attestation.

For source-based claims, distinguish protocol-defined intervals from measured wall-clock latency. The ten-minute reporting interval in the proposal is a reporting granularity, not proof of ten-minute settlement finality or audit completion.

## 7. Comparison output

The paper should use four linked exhibits rather than a single weighted ranking:

1. **Assurance matrix:** which accounting predicates each architecture can establish, under which source-truth assumptions.
2. **Cost ledger:** one-time, recurring, per-interval, per-exception, storage and delay costs, with unknowns explicit.
3. **Disclosure matrix and leakage tests:** who sees which fields, plus synthetic composition results and their limits.
4. **Operational profile:** measured or documented processing/review delays, with unbenchmarked values visibly marked.

A final recommendation should be conditional on the trade-offs shown in these exhibits. If the evidence does not support a single dominant architecture, state the Pareto trade-off rather than manufacturing an overall score.

## 8. Data collection and reproducibility protocol

For every measured run, preserve:

- source commit and model version;
- input dataset or generator seed;
- hardware and runtime environment;
- command used;
- raw output;
- sample count and summary statistic;
- exclusions and failed runs;
- assumptions and evidence classification.

For every documentary fact, preserve the source URL, immutable revision or commit where available, access date and exact claim supported.

The current CircleCI suite pass is user-confirmed, but its exact run URL and tested commit SHA have not been recorded in this research checkpoint. This plan does not treat that status as a benchmark or as proof that later changes were tested.

## 9. Decision gate before implementation

Do not build a new benchmark harness yet. First map each proposed metric to an available artifact and decide whether it is:

- directly measurable from existing code;
- measurable only after implementing a prototype component;
- obtainable from public primary sources;
- obtainable only through confidential operator/auditor access;
- currently unavailable.

Only implement a benchmark for the first two categories when the measurement changes the architecture decision. For the remaining categories, state the access dependency and bound the paper's claims accordingly.

## 10. Existing-artifact feasibility audit

A source review of the current analysis modules gives the following starting point. These are capabilities of the research prototypes, not claims about Canton production.

| Proposed measurement | Existing artifact | What can be measured now | Boundary |
|---|---|---|---|
| Expected interval coverage | `analysis/interval_coverage.py` | Missing, overdue, late, corrected, non-OK and invalid interval states against a supplied expected schedule | The function explicitly returns `measurement_completeness = NOT_ESTABLISHED`; a complete report schedule does not prove source counters captured all chargeable activity. |
| Report-to-settlement reconciliation | `analysis/integrated_interval_reconciliation.py`, `analysis/protocol_settlement_interface.py` | Deterministic blocking/reconciliation states, agreement-version linkage and correction adjustments on synthetic cases | The current binding signature authenticates the agreement document, not all report-to-obligation binding fields. Model cardinality and authority assumptions are synthetic. |
| Burn/manifest integrity | `analysis/settlement_manifest_validator.py` | Interval coverage gaps/overlaps, non-OK reports, duplicate burn IDs within a manifest, wrong settlement references, amount mismatch and reuse against a supplied global claimed-ID set | It does not independently query ledger finality, verify a cryptographic report digest, or prove the source report is complete. |
| Shared-paymaster allocation | `analysis/portfolio_allocation_model.py` | Duplicate allocation IDs, wrong burn references, unknown obligations, allocation totals above burn, shortfalls and overpayments | Constructed scenarios only; no production allocation manifest has been established. |
| Aggregate disclosure | `analysis/aggregate_disclosure_experiment.py`, `analysis/aggregate_linear_leakage.py` | Nested-cohort differencing and exact participant identifiability for constructed linear release systems | Synthetic participant vectors and release matrices only; no live Canton disclosure or formal differential-privacy guarantee. |
| Architecture scenario coverage | `analysis/comparative_assurance_model.py`, `analysis/integrated_assurance_comparison.py` | Deterministic outcomes across six accounting scenarios and four capability abstractions | Not a probability model, benchmark, or complete implementation of signing/audit/proof systems. |
| Implementation cost | No cost dataset or benchmark harness identified in this audit | Nothing defensible yet beyond symbolic cost decomposition | Requires a defined implementation, labour protocol, hardware profile and measured resource consumption. |
| Proof overhead | No proof circuit or verifier implementation identified | Not measurable yet | Do not estimate proving cost or latency from generic cryptographic literature as if it were this design's performance. |
| Auditor effort and dispute delay | No time-and-motion or case dataset identified | Not measurable yet | Requires access to a real audit workflow or a clearly labelled tabletop protocol; simulated minutes must not be called observed operations. |
| Production reporting/settlement latency | Public proposal defines ten-minute report intervals; no end-to-end measured dataset identified | Documentary reporting cadence only | A ten-minute interval is not an observed report-arrival, settlement-finality or dispute-resolution latency. |

### Immediate experiment sequence

1. Run and preserve the existing deterministic outputs for interval coverage, manifest validation, portfolio allocation and linear aggregate leakage. Record the exact repository commit, commands and outputs.
2. Add no new scenario until the current outputs have been checked against their corresponding invariants and the six-scenario comparative model.
3. Build a single evidence-to-predicate matrix showing which artifact tests each accounting property and where a property remains untested.
4. Do not build cost, proof-performance or audit-latency benchmarks until there is an implementation or access path that can produce meaningful measurements.
