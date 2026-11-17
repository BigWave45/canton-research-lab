# Research Evidence Map

**Prepared:** 17 November 2026  
**Repository snapshot:** `circleci-project-setup` at `1f7bc8bdec8d65cf70e85ef6615a25ababe734a0`  
**Purpose:** Reconcile the research record, identify what each body of work can support, and separate established findings from hypotheses and unresolved evidence.

## 1. Controlling research question

**What verifiable accounting guarantees can be added to the proposed dedicated-synchronizer paymaster model, and what are their economic, privacy and operational costs?**

The study follows the accounting chain from synchronizer activity measurement, through interval reporting and off-ledger commercial liability, to CC burn, reward attribution and independent reconciliation.

This question is the controlling scope because it is stated in the current project checkpoint and the scope-correction note. Older material in the repository still contains a broader public-network-measurement question. That older question is retained as research history, not as the current thesis.

## 2. Evidence classification

Every claim in the paper must be labelled by its evidence type:

- **Primary-source fact:** directly stated in a CIP, official documentation, source code, issue or pull request. The date and status of the source must be recorded.
- **Implementation observation:** behaviour visible in a specific code revision or test. It does not establish deployment or production behaviour.
- **Observed public data:** a bounded extract from a named public source, with collection date, coverage and provenance.
- **Synthetic/model result:** output generated from explicit assumptions and constructed inputs. It demonstrates model behaviour, not actual Canton incidence.
- **Analytical judgement:** a reasoned interpretation or qualitative comparison, with its assumptions stated.
- **Unknown/unverified:** the available evidence does not settle the claim.

Do not combine these categories or describe one as another.

## 3. Repository inventory at the reviewed branch

The recursive Git tree at the snapshot contains 132 files:
- 23 Python analysis modules, plus `analysis/README.md`;
- 25 test files;
- 62 files under `research/`, including this map once added;
- source, data and output directories, plus root project documentation.

The repository is a research workspace, not a finished paper. File counts are inventory facts, not measures of research quality.

## 4. Evidence-to-claim map

| Research area | Existing artefacts | What the work can support | Evidence class | Main limitation / next validation |
|---|---|---|---|---|
| Grant programme and precedent | `research/comparative-grant-winner-analysis.md`, `research/completed-output-case-studies.md`, `research/grant-winner-register.csv`, `research/comparative-findings.md` | A cautious account of public funding-programme differences and examples of funded research outputs | Documentary / descriptive | The 34-project sample is purposive, not representative. Several entries are award descriptions, not verified completed outputs. It cannot reveal causal selection criteria or a Canton winning formula. |
| Canton literature and research gap | `research/canton-literature-data-inventory.md`, `research/literature-gap-matrix.md`, `research/literature-review-gap-matrix.md`, `research/deeper-literature-review-accountability-design.md`, `research/second-literature-pass-metering-and-completeness.md` | A map of related research, concepts and candidate gaps around privacy, accountability, measurement and institutional infrastructure | Literature synthesis | Verify bibliographic metadata, exact claims and closest prior work before publication. The presence of a gap in our matrix is not proof that no prior work exists. |
| Protocol and proposal description | `research/cip-0104-0129-0132-architecture-comparison.md`, `research/paymaster-implementation-audit.md`, `research/implementation-evidence-audit.md`, `research/implementation-evidence-mapping-2026-11-17.md`, `research/canton-implementation-evidence-map.md` | A dated account of what the reviewed CIPs, public code changes and tracker items describe | Primary-source documentary / implementation review | Recheck upstream status before publication. A merged PR is not proof of deployment. Open or closed-unmerged proposals are not implemented features. This is not a production audit. |
| Measurement and reporting | `analysis/interval_coverage.py`, `research/traffic-report-consistency-and-retention.md`, `research/traffic-report-implementation-audit.md`, `research/traffic-report-test-harness-audit.md`, `research/underlying-sequencer-pruning-semantics.md`, `research/expected-interval-coverage-and-corrections.md` | Modelled consequences of missing, late, undetermined, corrected and unavailable interval reports; source-code observations about proposed reporting semantics | Synthetic model + implementation observation | Synthetic coverage tests do not establish production report completeness. Validate source semantics against the exact upstream revision and distinguish API design from deployed behaviour. |
| Pricing and contractual liability | `analysis/pricing_liability.py`, `analysis/agreement_schedule.py`, `analysis/agreement_verification.py`, `research/agreement-aware-liability-calculation.md`, `research/agreement-schedule-calculator.md`, `research/cryptographic-agreement-verification.md` | Deterministic model behaviour for agreement versions, pricing bands, due tranches, grace periods, tolerances, signatures and key-status checks | Synthetic model / cryptographic prototype | Agreement authority, signer governance, legal enforceability and production key management remain external assumptions. Modelled prices are not Canton tariffs unless sourced as such. |
| Settlement and reconciliation | `analysis/reconciliation_state_machine.py`, `analysis/integrated_interval_reconciliation.py`, `analysis/protocol_settlement_interface.py`, `analysis/settlement_manifest_validator.py`; associated reconciliation and interface notes | Separation of protocol traffic reports from off-ledger settlement bindings; modelled checks for report coverage, identity, agreement version, due amounts, burn allocation and reward-record presence | Synthetic model | A passing reconciliation state cannot prove source-meter truth, completeness, actual burn finality, legal agreement authority or deployed reward execution. |
| Portfolio and allocation | `analysis/portfolio_allocation_model.py`, `analysis/portfolio_settlement_model.py`, `research/shared-paymaster-portfolio-allocation-experiment.md`, `research/portfolio-settlement-and-smoothing.md` | Modelled distinction between valid one-to-many burn allocation and duplicate, excessive or misdirected allocation | Synthetic model | Requires authoritative allocation identifiers and a complete view of relevant obligations/burns. No production allocation manifest has been established by the reviewed evidence. |
| Privacy disclosure and leakage | `analysis/disclosure_tiers.py`, `analysis/aggregate_disclosure_experiment.py`, `analysis/aggregate_linear_leakage.py`, `research/privacy-disclosure-requirements.md`, `research/privacy-disclosure-matrix-and-leakage-experiment.md`, `research/linear-composition-and-public-verification-surface.md` | Constructed examples showing that overlapping aggregates can reveal individual values and that payload confidentiality does not eliminate metadata leakage | Synthetic experiment / analytical model | These are not measured Canton disclosures or a formal privacy proof. State cohort assumptions, attacker knowledge and composition conditions precisely. |
| Reward attribution | `research/reward-attribution-integrity.md`, `research/paymaster-vs-merkle-reward-accounting.md`, `analysis/comparative_assurance_model.py`, `analysis/integrated_assurance_comparison.py` | A framework for asking whether reward attribution is traceable to eligible activity and payment inputs | Documentary + synthetic model + analytical comparison | The reviewed implementation evidence does not establish a complete report-to-burn-to-reward path. Reward correctness must not be claimed from a model alone. |
| Comparative assurance architectures | `analysis/comparative_assurance_matrix.py`, `analysis/comparative_assurance_model.py`, `analysis/integrated_assurance_comparison.py`, `research/initial-comparative-assurance-experiment.md`, `research/integrated-assurance-architecture-comparison.md` | Comparison of public-burn-only, signed reconciliation, independent confidential audit and cryptographic proof under stated assumptions | Synthetic experiment + qualitative analytical judgement | Cost, latency and detection probabilities are not empirically measured. The qualitative ratings must be labelled as judgements, not performance results. |
| Public-data feasibility and network economics | `research/data-access-feasibility-audit.md`, `research/quantitative-research-design.md`, `analysis/synchronizer_economics_scenarios.py`, `research/ccview-cip0129-audit-parameter-register.md`, `research/ccview-october-report-audit.md` | A boundary around public observability, provider access conditions and ex-ante scenario analysis | Documentation audit / scenario model | No authenticated Noves extraction or live data collection is documented in the access audit. Paid analytics are not assumed available. The broad network-measurement question in the quantitative design is not the controlling thesis. |

## 5. Findings currently supportable

### Finding 1: payment reconciliation does not establish measurement completeness

The initial comparative experiment constructs a case where actual activity is 100 units, reported activity is 90, the liability calculated from the report is 9 CC, and the burn is exactly 9 CC. The payment matches the submitted liability, but the report omits 10 units relative to the synthetic reference.

This demonstrates a logical separation between **calculation/payment reconciliation** and **measurement completeness** within the model. It does not show that any Canton operator has under-reported.

Primary artefact: `research/initial-comparative-assurance-experiment.md`.

### Finding 2: signatures and proofs inherit input-truth limitations

A signature can establish provenance and integrity of a report after signing. A proof can establish that a specified calculation or predicate holds over committed inputs. Neither, by itself, proves that the source meter captured every chargeable event.

This is a model/theoretical result under the stated evidence boundary, not an assessment of a deployed Canton proof system.

### Finding 3: missing-report detection requires a known expected population

A verifier cannot infer that an interval is missing unless it knows that the interval was expected. The expected interval schedule is therefore part of the evidence model, not a harmless implementation detail.

### Finding 4: stronger measurement assurance depends on source evidence and governance

An independent audit can challenge a report only if the auditor has access to sufficiently complete and reliable source records, and is institutionally independent of the reporting party. These are substantive trust assumptions, not details solved by adding an auditor role.

### Finding 5: public aggregate disclosure can leak information through composition

The repository's constructed examples show that individually thresholded aggregates may reveal a participant's value when overlapping cohorts are combined. The result depends on the assumed cohort membership and available equations. It should be described as a disclosure-risk demonstration, not as evidence of an observed Canton leak.

### Finding 6: the assurance architecture comparison is currently qualitative

The four-architecture comparison distinguishes what each mechanism can establish and the trust it leaves behind. Its cost, latency and operational-burden entries are qualitative assessments. No measured production benchmarks or empirical detection rates are currently established.

## 6. Important implementation boundary

The implementation evidence map records different maturity states for traffic reporting, paymaster purchase, activity recording and end-to-end testing. The paper must preserve those distinctions.

In particular:
- Paymaster purchase authorisation is not the same as checking whether the amount paid covers the complete traffic liability.
- A traffic-report API proposal is not a merged or deployed endpoint merely because its design and code were inspected.
- A merged purchase or Scan/SV change does not establish a complete report-to-burn-to-reward chain.
- A public burn record does not independently reveal the private activity or contractual liability that should have generated it.

All implementation statements must be rechecked against the upstream repositories and issue tracker immediately before publication.

## 7. What is not yet demonstrated

The current repository does **not** establish:
1. The completeness or truth of production synchronizer traffic measurements.
2. Actual underpayment, fraud, or accounting loss on Canton.
3. The real-world frequency or probability of any failure scenario.
4. Measured cost, latency or operational burden of the four assurance architectures.
5. A formal cryptographic privacy guarantee for the proposed disclosure tiers.
6. A deployed, end-to-end report-to-burn-to-reward reconciliation mechanism.
7. Network-wide Canton activity or settlement totals from a complete public dataset.
8. Causal economic effects of CIP-0129 after implementation.

These are evidence gaps, not negative findings.

## 8. Documentation conflicts found in this audit

The following repository-level conflicts must be resolved:
- Root `README.md` still says Phase 1 grant-winner landscape review and says not to select a topic, while `STATE.md` and `research/research-scope-correction.md` establish the Paymaster accounting question.
- `research/README.md` still says not to begin the paper until the landscape and hypothesis comparison are complete. That instruction is stale as a project-stage instruction; the topic has been selected. Literature review and evidence verification still continue as paper work.
- `research/quantitative-research-design.md` retains a broader public-network-observability research question and describes the Paymaster topic as a working question rather than the selected scope. It should be labelled as an earlier alternative/design note, not silently treated as current scope.
- `STATE.md` contains duplicated historical checkpoint headings and older "next exact task" instructions. Preserve the historical log, but put one current checkpoint at the top and label the remainder as history.
- Test and CI claims must be tied to a specific commit and run. The user reported the latest CircleCI pipeline succeeded, but the GitHub connector did not expose a status for the current head during this audit. Do not imply that every later-added test has been executed solely from that report.

## 9. Prioritised work remaining

1. **Freeze scope and reconcile documentation.** Use the controlling research question above. Retain older research as supporting context, not parallel theses.
2. **Verify source claims.** Recheck current CIP status, PR merge status, tracker issue status and exact upstream code revision. Record access dates and immutable commit references.
3. **Validate the exact repository test suite.** Run the checked-in suite from a reproducible checkout/CI run and record the exact commit and result. Do not rely on a reconstructed subset as full-suite validation.
4. **Turn the comparative experiment into a quantitative design.** Define measurable outputs for disclosure, reconciliation detection, implementation burden and operational delay. Only report numeric costs or probabilities when data or a transparent parameterised model supports them.
5. **Decide whether a bounded public-data case study is feasible.** Do not require paid analytics. If no reproducible public extract is accessible, keep the paper's empirical claims bounded to documentary evidence and synthetic experiments.
6. **Draft the paper from the evidence.** Each result should point to a source, model, test or data extract and carry its evidence classification and limitation.

## 10. Publication rule

The paper should stand on its own. The GitHub repository is its reproducibility and evidence companion, not a substitute for explaining the method and results in the paper. The public version of the repository should be released only after secrets, private data, licensing, source provenance and test reproducibility have been checked.
