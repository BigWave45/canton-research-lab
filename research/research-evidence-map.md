# Research Evidence Map

**Prepared:** 17 November 2026  
**Initial repository snapshot:** `circleci-project-setup` at `1f7bc8bdec8d65cf70e85ef6615a25ababe734a0`  
**Evidence refresh:** 17 November 2026; upstream PR #111 review and tracker states rechecked  
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

The initial recursive Git tree contained 132 files. After the evidence-map, documentation-alignment, cost-model and benchmark-harness commits, the branch contains at least 139 files at the latest tracked update. The last exact recursive inventory predates the benchmark-harness additions; do not treat this count as a fresh tree audit.
- source, data and output directories, plus root project documentation.

The repository is a research workspace, not a finished paper. File counts are inventory facts, not measures of research quality. The current comparative-assurance test file has ten test methods and the model returns 24 scenario/architecture rows. The user confirmed that the CircleCI research-test pipeline eventually passed after the earlier eight failures. The exact run URL and tested commit SHA were not captured in this record, so the pass is recorded as user-confirmed rather than independently tied to branch head `83c02e68e4f511aa34f3b736653249ac9c51177d`.

## 4. Evidence-to-claim map

| Research area | Existing artefacts | What the work can support | Evidence class | Main limitation / next validation |
|---|---|---|---|---|
| Grant programme and precedent | `research/comparative-grant-winner-analysis.md`, `research/completed-output-case-studies.md`, `research/grant-winner-register.csv`, `research/comparative-findings.md` | A cautious account of public funding-programme differences and examples of funded research outputs | Documentary / descriptive | The 34-project sample is purposive, not representative. Several entries are award descriptions, not verified completed outputs. It cannot reveal causal selection criteria or a Canton winning formula. |
| Canton literature and research gap | `research/canton-literature-data-inventory.md`, `research/literature-gap-matrix.md`, `research/literature-review-gap-matrix.md`, `research/deeper-literature-review-accountability-design.md`, `research/second-literature-pass-metering-and-completeness.md` | A map of related research, concepts and candidate gaps around privacy, accountability, measurement and institutional infrastructure | Literature synthesis | Verify bibliographic metadata, exact claims and closest prior work before publication. The presence of a gap in our matrix is not proof that no prior work exists. |
| Protocol and proposal description | `research/cip-0104-0129-0132-architecture-comparison.md`, `research/paymaster-implementation-audit.md`, `research/implementation-evidence-audit.md`, `research/implementation-evidence-mapping-2026-11-17.md`, `research/canton-implementation-evidence-map.md` | A dated account of what the reviewed CIPs, public code changes and tracker items describe | Primary-source documentary / implementation review | Recheck upstream status before publication. A merged PR is not proof of deployment. Open or closed-unmerged proposals are not implemented features. This is not a production audit. |
| Measurement and reporting | `analysis/interval_coverage.py`, `research/traffic-report-consistency-and-retention.md`, `research/traffic-report-implementation-audit.md`, `research/traffic-report-test-harness-audit.md`, `research/underlying-sequencer-pruning-semantics.md`, `research/expected-interval-coverage-and-corrections.md` | Modelled consequences of missing, late, undetermined, corrected and unavailable interval reports; source-code observations about proposed reporting semantics and participant join/leave handling, plus an untested pruning-boundary concurrency hypothesis narrowed by the harness audit | Synthetic model + implementation observation | Synthetic coverage tests do not establish production report completeness. Validate source semantics against the exact upstream revision and distinguish API design from deployed behaviour. |
| Pricing and contractual liability | `analysis/pricing_liability.py`, `analysis/agreement_schedule.py`, `analysis/agreement_verification.py`, `research/agreement-aware-liability-calculation.md`, `research/agreement-schedule-calculator.md`, `research/cryptographic-agreement-verification.md` | Deterministic model behaviour for agreement versions, pricing bands, due tranches, grace periods, tolerances and signature/key-status checks; a separate review identified that the signature currently authenticates agreement terms, not the settlement binding | Synthetic model / cryptographic prototype | Agreement authority, signer governance, legal enforceability and production key management remain external assumptions. Modelled prices are not Canton tariffs unless sourced as such. |
| Settlement and reconciliation | `analysis/reconciliation_state_machine.py`, `analysis/integrated_interval_reconciliation.py`, `analysis/protocol_settlement_interface.py`, `analysis/settlement_manifest_validator.py`; associated reconciliation and interface notes | Separation of protocol traffic reports from off-ledger settlement bindings; modelled checks for report coverage, identity, agreement version, due amounts, burn allocation and reward-record presence; agreement-document signature verification | Synthetic model | A passing reconciliation state cannot prove source-meter truth, completeness, actual burn finality, legal agreement authority or deployed reward execution. |
| Portfolio and allocation | `analysis/portfolio_allocation_model.py`, `analysis/portfolio_settlement_model.py`, `research/shared-paymaster-portfolio-allocation-experiment.md`, `research/portfolio-settlement-and-smoothing.md` | Modelled distinction between valid one-to-many burn allocation and duplicate, excessive or misdirected allocation | Synthetic model | Requires authoritative allocation identifiers and a complete view of relevant obligations/burns. No production allocation manifest has been established by the reviewed evidence. |
| Privacy disclosure and leakage | `analysis/disclosure_tiers.py`, `analysis/aggregate_disclosure_experiment.py`, `analysis/aggregate_linear_leakage.py`, `research/privacy-disclosure-requirements.md`, `research/privacy-disclosure-matrix-and-leakage-experiment.md`, `research/linear-composition-and-public-verification-surface.md` | Constructed examples showing that overlapping aggregates can reveal individual values and that payload confidentiality does not eliminate metadata leakage | Synthetic experiment / analytical model | These are not measured Canton disclosures or a formal privacy proof. State cohort assumptions, attacker knowledge and composition conditions precisely. |
| Reward attribution | `research/reward-attribution-integrity.md`, `research/paymaster-vs-merkle-reward-accounting.md`, `analysis/comparative_assurance_model.py`, `analysis/integrated_assurance_comparison.py` | A framework for asking whether reward attribution is traceable to eligible activity and payment inputs | Documentary + synthetic model + analytical comparison | The reviewed implementation evidence does not establish a complete report-to-burn-to-reward path. Reward correctness must not be claimed from a model alone. |
| Comparative assurance architectures | `analysis/comparative_assurance_matrix.py`, `analysis/comparative_assurance_model.py`, `analysis/integrated_assurance_comparison.py`, `research/initial-comparative-assurance-experiment.md`, `research/integrated-assurance-architecture-comparison.md` | Comparison of public-burn-only, signed reconciliation, independent confidential audit and cryptographic proof under stated assumptions | Synthetic experiment + qualitative analytical judgement | Cost, latency and detection probabilities are not empirically measured. The qualitative ratings must be labelled as judgements, not performance results. |
| Quantitative assurance evaluation | `research/quantitative-assurance-evaluation-plan.md`, `analysis/assurance_cost_model.py`, `tests/test_assurance_cost_model.py`, `research/assurance-cost-model.md`, `research/illustrative-assurance-cost-scenario.md`, `analysis/research_benchmark.py`, `research/prototype-measurement-protocol.md` | Defines falsifiable assurance predicates, a parameterised cost calculator, a synthetic four-architecture cost scenario and a reproducible local microbenchmark harness for manifest validation, portfolio allocation and aggregate leakage | Research design + executable parameterised model + synthetic scenario + benchmark harness | ICU inputs are artificial. The benchmark harness has been committed but not executed; no runtime, memory or payload measurements are claimed. It measures local synthetic prototypes only, not Canton production performance. New tests remain unexecuted because local/CI execution is unavailable. |
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

The repository's constructed examples show that individually thresholded aggregates may reveal a participant's value when overlapping cohorts are combined. The new benchmark harness measures the exact-rational linear-algebra routine on synthetic two-row cohort matrices; until executed, no timing or scaling result is claimed. The result depends on the assumed cohort membership and available equations. It should be described as a disclosure-risk demonstration, not as evidence of an observed Canton leak.

### Finding 6: the assurance architecture comparison is currently qualitative

The four-architecture comparison distinguishes conceptual capabilities and residual trust assumptions. The signed-reconciliation and cryptographic-proof columns are design abstractions, not implemented report-signing or proof systems. The current code verifies agreement-document signatures only; it does not yet attest report-to-obligation bindings. Cost, latency and operational-burden entries are qualitative assessments, not measured production benchmarks or empirical detection rates.

### Finding 7: traffic-report participant exit semantics may affect the measured liability population

The open PR #111 implementation computes interval traffic by iterating over participants present in the end-of-interval counter snapshot. Its test explicitly includes a participant present at the start but absent at the end and excludes that participant's traffic from the interval total. Participants present only at the end are counted from zero.

This is an implementation observation, not proof of incorrect billing. It creates a precise research question: if a participant leaves during an interval, should its traffic consumed before departure remain chargeable, and if so, how is that amount captured? The CIP's general description of tracking consumed traffic does not, by itself, settle the commercial treatment of mid-interval departures. The paper must distinguish metering semantics from the contract's chargeability rules.

### Finding 8: the report reader's source acknowledges a pruning-boundary race

The PR #111 source comment warns that a request at the retention edge can race pruning. However, the separate test-harness audit found that pruning retains the latest traffic row at or before the pruning timestamp, which may preserve correct lookups at or after the effective boundary. The remaining hypothesis is a stale pruning-status observation combined with pruning advancing before the historical read. Existing mocks do not exercise this database-level concurrency.

No incorrect `Ok` report has been demonstrated. Treat this as an unresolved concurrency hypothesis, not a confirmed implementation defect. A deterministic test must distinguish a correct value, an explicit error/unavailable response, a safe retry and an incorrect `Ok` against an independent reference.

### Finding 9: agreement integrity and settlement-binding integrity require separate attestations

The prototype now verifies the canonical pricing-agreement document and a separate `SettlementBinding` attestation. The binding attestation covers a deterministic digest of the interval report set plus the binding ID, interval, synchronizer, obligation, agreement ID/version and authority reference. It is signed and verified using the explicit `binding_signer_key_id`, with the `settlement_binding` role required by the trusted signer registry. A missing binding signer identity fails closed with `SETTLEMENT_BINDING_SIGNER_ID_MISSING`; the agreement signer identity is not silently substituted.

The targeted `tests/test_protocol_settlement_interface.py` suite was run in Codespaces after commit `85506c9a2d84cd5a7646ee4c9b4773dbcf5f4a0e`: 18 tests passed, including the legacy-binding fail-closed regression. `git diff --check` passed. This is a user-reported local execution result, not a CI result; no CI workflow was invoked. The commit is on `circleci-project-setup`.

This closes the previously demonstrated unsigned report-to-obligation mapping gap in this research prototype. It does not establish source-meter completeness, legal authority of the referenced agreement or mapping, or correctness of the trust registry. The code requires a distinct signer-key field and role, but does not enforce distinct legal principals or prohibit one key from holding both roles. Separation of duties therefore remains a governance/registry policy unless a stricter distinct-key/principal invariant is added and tested.

The paper must distinguish agreement content integrity, signer attribution, mapping integrity, source-measurement completeness and legal authority. This is prototype evidence only, not a Canton production finding.

## 6. Important implementation boundary

The implementation evidence map records different maturity states for traffic reporting, paymaster purchase, activity recording and end-to-end testing. The paper must preserve those distinctions. A second source-level pass corrected the PR history: PR #103 was closed unmerged and superseded by PR #111, which remains open in the 17 November snapshot. PR #111's review thread confirms that its database store, trigger and migration were dropped because dedicated-synchronizer sequencers were not being pruned at that time; the handler reads sequencer counters on demand. Its visible tests cover a single operator report and an interval spanning an LSU, but do not establish the four-node equality criterion still listed in open tracker #152.

In particular:
- Phase 1 has no traffic enforcement: the CIP says messages are not rejected because a node runs out of traffic. Payment is post-hoc, so an accounting shortfall is not automatically prevented by traffic admission control.
- Paymaster purchase authorisation is not the same as checking whether the amount paid covers the complete traffic liability. Tracker #155 explicitly says no purchase check compares paid amount with the report.
- A traffic-report API proposal is not a merged or deployed endpoint merely because its design and code were inspected. PR #111 is open; it is not the closed-unmerged PR #103.
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

The following repository-level documentation issues remain:
- `research/quantitative-research-design.md` retains a broader public-network-observability research question and describes the Paymaster topic as a working question rather than the selected scope. Treat it as an earlier alternative/design note, not as the controlling thesis.
- `STATE.md` retains a long chronological history with older checkpoint headings and next-task instructions. The top checkpoint is authoritative; older entries are historical records and must not be followed as current instructions.
- The CircleCI pass is user-confirmed, but its exact run URL and tested commit SHA are not recorded. The GitHub Actions workflow-runs endpoint returned zero runs for this branch; this is a separate CI system and does not invalidate the CircleCI result.

## 9. Prioritised work remaining

1. **Freeze scope and reconcile documentation.** Use the controlling research question above. Retain older research as supporting context, not parallel theses.
2. **Verify source claims.** Recheck current CIP status, PR merge status, tracker issue status and exact upstream code revision. Record access dates and immutable commit references.
3. **Execute the existing-artifact validation sequence.** Preserve deterministic outputs for interval coverage, manifest validation, portfolio allocation and aggregate leakage at a recorded commit. Then build the evidence-to-predicate matrix. Do not build cost/proof/audit benchmarks until a real measurement path exists.
4. **Decide whether a bounded public-data case study is feasible.** Do not require paid analytics. If no reproducible public extract is accessible, keep empirical claims bounded to documentary evidence and synthetic experiments.
5. **Draft the paper from the evidence.** Each result should point to a source, model, test or data extract and carry its evidence classification and limitation.
6. **Record CI provenance.** Preserve the successful CircleCI run URL and commit SHA if available; rerun only when subsequent code changes or a concrete validation gap justify it.

## 10. Publication rule

The paper should stand on its own. The GitHub repository is its reproducibility and evidence companion, not a substitute for explaining the method and results in the paper. The public version of the repository should be released only after secrets, private data, licensing, source provenance and test reproducibility have been checked.


## 11. Upstream refresh: 17 November 2026

The following primary-source states were checked directly after the initial evidence map was written:

| Source | State observed | Research consequence |
|---|---|---|
| CIP-0132 | Status field says **Proposed**; created 9 November 2026 | The paymaster model remains a proposal in this source snapshot, not an approved or deployed protocol fact. |
| splice-multi-sync PR #103 | Closed 13 November, `merged=false`; explicitly superseded by #111 | Do not treat #103 as the current report implementation. |
| splice-multi-sync PR #111 | Open, not merged; last observed review activity 17 November | Report API remains proposed/in review. It reads sequencer counters on demand. |
| PR #111 review thread | Author states store, trigger and migration were dropped because no dSync sequencer pruning exists today | No durable report archive in the current patch. Historical availability depends on counter-history retention. |
| PR #111 tests | Single-operator interval test and LSU-spanning predecessor/successor read test are present in the patch | Useful implementation-test evidence, but not merged CI or deployment evidence. Four-node equality remains unverified. |
| ChainSafe issue #152 | Open | Its original durable-storage and four-node acceptance requirements remain unresolved in the tracker; the PR's on-demand design narrows the storage approach under a current no-pruning assumption. |
| splice-multi-sync PRs #100 and #104 | Both merged (11 and 12 November respectively) | Registered-paymaster purchase and Scan/SV handling are present in merged source; deployment remains unverified. |
| ChainSafe issue #155 | Closed | Purchase-choice deliverable closed. Its text explicitly says no check compares paid amount with report and paymaster may pay less than usage. Closure does not resolve that accounting gap. |
| Splice PR #8449 | Open and draft | ActivityRecorder integration remains incomplete in public source. |
| ChainSafe issue #163 | Open | Purchase-side ActivityRecorder work remains outstanding. |
| ChainSafe issue #159 | Open | Full registration → traffic → report → payment → activity-record end-to-end test is not demonstrated. |
| Canton Community Research Grants announcement | Official announcement dated 4 November says Terms and Conditions expected by 15 November | This audit has not independently verified the final terms. Do not assume eligibility, payment, KYC or publication conditions. |

The PR #111 patch includes an integration test for a completed interval and a test querying an interval across an LSU. It does **not** prove the four operator apps on a four-node synchronizer return identical values. That remains in issue #152 acceptance criteria. The report API is JWT-protected; JWT authorises a caller but is not a report-level digital signature or public attestation.

Primary links:
- CIP-0132: https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- PR #103: https://github.com/canton-network/splice-multi-sync/pull/103
- PR #111: https://github.com/canton-network/splice-multi-sync/pull/111
- Tracker #152: https://github.com/ChainSafe/canton-extending-mainnet/issues/152
- PR #100: https://github.com/canton-network/splice-multi-sync/pull/100
- PR #104: https://github.com/canton-network/splice-multi-sync/pull/104
- Tracker #155: https://github.com/ChainSafe/canton-extending-mainnet/issues/155
- ActivityRecorder PR #8449: https://github.com/canton-network/splice/pull/8449
- Tracker #163: https://github.com/ChainSafe/canton-extending-mainnet/issues/163
- End-to-end test #159: https://github.com/ChainSafe/canton-extending-mainnet/issues/159
- Grant announcement: https://canton.foundation/introducing-the-canton-community-research-grants/


## 12. Scan API access check: 18 November 2026

A bounded access check was performed from the user's iPhone browser after the official Canton Foundation SV network-status directory opened successfully. The user supplied the directory's 13 TestNet SV names, Scan URLs and advertised versions. Two requests to `GET /api/scan/v0/scans` returned user-observed HTTP 403: one at the Global Synchronizer Foundation MainNet Scan host and one at its TestNet Scan host. No response bodies, headers or request IDs were captured. The cause is therefore unknown; these two failures do not prove that all SV endpoints or all API routes are inaccessible.

The access-check record is [research/scan-api-access-check-2026-11-18.md](scan-api-access-check-2026-11-18.md). Official Scan documentation describes a DSO-party view that includes CC transfers and governance operations but excludes most application transactions not involving the DSO party. The documented traffic-status endpoint reports sequencer traffic-credit state, including consumed and purchased totals; it is not the proposed CIP-0132 private ten-minute traffic report and does not independently establish meter completeness.

**Evidence classification:** user-supplied SV directory transcription; user-observed 403 responses; official documentation for endpoint semantics and visibility boundaries. No live Scan records were retrieved. The earlier statement that authenticated API extraction had not been performed remains correct. Do not claim public empirical data from this attempt.

**Research consequence:** stop repeating the same API request across SV hosts from the same browser context. Continue source-to-invariant validation using public CIPs, Splice code, PRs, issues and local reproducible models. Revisit live Scan extraction only if an SV/operator provides an authorised access path or export.

The current invariant-by-invariant validation plan is [research/accounting-invariant-validation-matrix-2026-11-18.md](accounting-invariant-validation-matrix-2026-11-18.md). It maps twelve accounting/privacy invariants to public Canton evidence, existing prototype artefacts/tests, evidence level and remaining validation. It identifies the settlement-binding attestation gap as the first prototype issue to close.


## 13. Prototype binding-attestation change and local validation: 18 November 2026

Commit `85506c9a2d84cd5a7646ee4c9b4773dbcf5f4a0e` adds an independent binding-signer identity to `SettlementBinding`. The canonical binding document includes that identity; reconciliation rejects a missing identity and verifies the attestation against that key with the `settlement_binding` role. Agreement and binding signatures are represented by separate signer identities in the positive test fixture.

The user reports that the targeted protocol-interface suite passed all 18 tests in Codespaces and `git diff --check` passed. No CI workflow was invoked. The local test result is recorded as user-reported rather than independently rerun here.

The legacy-binding regression verifies fail-closed behavior when the binding signer identity is absent, even when the agreement key is configured with both roles. The implementation does not, however, enforce that agreement and binding keys belong to different principals or prevent a single key from being granted both roles. That is a trust-registry governance requirement, not a code-enforced separation-of-duties guarantee.

The attestation authenticates the mapping and exact report content supplied to the verifier. It does not prove source-meter completeness, truth of the source counters, legal authority of the agreement/mapping, or independence of the signer-governance process. This remains a research prototype result, not a Canton production finding.
