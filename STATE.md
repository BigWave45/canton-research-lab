# Project State

**Last updated:** 2026-11-17  
**Repository:** private  
**Project:** Canton Community Research Grants research preparation

## Confirmed direction

- Research orientation: interdisciplinary.
- Quantitative analysis: central where appropriate, not decorative.
- Deliverable: hybrid research package consisting of a substantial paper supported by reproducible calculations, documented data, models, and visualisations.
- Working method: comparative study of funded research programmes and completed outputs, followed by Canton landscape mapping and original hypothesis development.
- Repository visibility: private.

## Completed

- Repository created and confirmed private.
- Initial research methodology and folder structure committed.
- Initial desk-research sample assembled: 34 funded projects across Ethereum Foundation (15), Stellar Development Foundation (16), and Uniswap Foundation (3).
- Preliminary comparative findings documented.
- Initial source index created.
- Official Canton programme announcement rechecked.

## Current phase

**Phase 1: comparative grant-winner intelligence.**

The sample is purposive and preliminary. Most entries are sourced from award announcements, not independently verified completed deliverables. The project register explicitly records this limitation.

## Initial findings

- Research projects often define a specific mechanism, problem, or comparison rather than a broad theme.
- Interdisciplinary work is visible where disciplines jointly answer one question (e.g. financial market design, privacy/compliance, institutional economics/governance).
- Some funders support reusable research infrastructure such as standardised datasets and public analytics portals.
- Some programmes are academic grants with strict institutional eligibility; they are not comparable to Canton’s discretionary community research programme.
- There is no historical Canton Community Research Grant winner cohort in the November 4 launch announcement because the programme is beginning in November 2026.

## Important programme facts to verify

Official announcement: https://canton.foundation/introducing-the-canton-community-research-grants/

- Original research and educational content publicly published November 1–30, 2026 may be considered for November.
- Work shared on X by December 4, 2026 will be reviewed in connection with November; the announcement says sharing is optional, with @CantonFdn and #CantonResearchNov26.
- The announcement says the Foundation expects up to 50,000 CC per month, but may award less or nothing.
- It identifies research quality, educational/community value, and contribution to public understanding as considerations, not a fixed scoring rubric.
- It says favourable coverage is not required.
- The announcement said formal Terms and Conditions were expected by November 15, 2026. In this research pass, no official linked terms document was verified. This remains an urgent open item.

## Open tasks

1. Inspect actual outputs for Allium DEX Analytics Portal and Doppler.
2. Locate completed research outputs for the Stellar market microstructure and AMM-design projects.
3. Locate the output for the Ethereum institutional economics/slashing and anonymity/compliance projects.
4. Expand the register only with sufficiently documented projects.
5. Map existing Canton-specific research and public data sources.
6. Verify formal Canton programme terms and applicant eligibility.
7. Develop five interdisciplinary hypotheses with data feasibility assessments.

## Decisions

1. Do not treat this as a conventional writing/video contest.
2. Study prior funded projects and inspect completed outputs, not only grant announcements.
3. Distinguish academic research grants, developer grants, public-goods funding, prizes, and discretionary content grants.
4. Do not infer private selection reasons or claim a formula for winning.
5. Do not choose the research topic before mapping literature, evidence, and data feasibility.
6. Keep unpublished research private.
7. Do not present simulated results as observed Canton data.

## Update protocol

At the end of each substantial research session, update this file with work completed, sources added, verified findings, unresolved questions, decisions made, and the next exact action.


## Update — 17 November 2026: comparative grant research

- Added `research/comparative-grant-winner-analysis.md`, an initial source-backed comparison of Ethereum Foundation, Stellar Development Foundation, Uniswap Foundation, and Canton's adjacent Protocol Development Fund.
- Expanded `sources/source-index.md` with Canton's Protocol Development Fund first report.
- Key distinction: Canton Community Research Grants launched in November 2026, so there is no previous winner cohort for that exact programme in its launch announcement. Canton's Protocol Development Fund is a separate programme and must not be represented as a prior Community Research Grant winner list.
- Initial observed patterns: bounded research questions; visible methods/deliverables; interdisciplinary integration around one question; reusable datasets/tools in some programmes. These are observations from public project descriptions, not proven causes of selection.
- Limit: many records still describe awards or intended work. Completed outputs and impact require separate inspection.
- Next exact task: inspect completed outputs for EF slashing economics, blockspace derivatives, blockchain geometry and anonymity/compliance; inspect Uniswap Doppler and DEX Analytics Portal; locate SDF market microstructure and AMM outputs.
- Programme terms and applicant eligibility remain unverified and must be checked before submission.


## Update — 17 November 2026: completed-output case studies

- Added `research/completed-output-case-studies.md` with six case studies spanning Uniswap, Ethereum and Stellar.
- Inspected the Allium grant announcement and Doppler whitepaper plus public technical documentation.
- Confirmed an important distinction: Allium's grant announcement specifies intended deliverables, but completion and downstream adoption still need verification.
- Doppler has a public whitepaper and technical documentation describing its Dutch-auction dynamic bonding-curve mechanism and Uniswap v4 hook behaviour. Independent comparative performance evidence has not yet been established.
- EF slashing and blockspace projects, and SDF AMM/perpetual-DEX projects, are currently supported by award records only; completed outputs remain to be located.
- Next task: locate and inspect completed research outputs for those award-only cases, then verify current Allium portal/data access and independent Doppler evaluations.


## Follow-up verification — 17 November 2026

- University at Buffalo's project record lists the SDF-funded AMM design project as active from 1 September 2025 through 31 August 2027, with USD 37,500 funding. Its final output should not be expected yet; the current absence of a paper is not evidence of non-delivery.
- Added this status clarification to `research/completed-output-case-studies.md`.


## Update — 17 November 2026: comparative case-study synthesis

- Added `research/case-study-synthesis.md`.
- Inspected Allium's public DEX Analytics portal, orderflow schema and methodology documentation; identified data-standardisation and reproducibility as the core contribution. Recorded access and licensing caveats.
- Inspected Doppler whitepaper and technical documentation; identified its Dutch-auction dynamic bonding-curve mechanism and implementation link. Kept funder-reported adoption separate from independent performance evidence.
- Located the EF-funded working paper *Automated Penalties and Networked Coordination* and distinguished it from the separately titled slashing project in the initial grant register.
- Confirmed the SDF AMM project remains active through 31 August 2027; no final output should be expected yet.
- The EF blockspace derivatives and SDF perpetual-DEX completed outputs remain unlocated in this pass.
- Next exact task: complete the remaining project-output searches, then create a Canton-specific literature and public-data inventory. Do not generate or select hypotheses before this inventory.


## Update — 17 November 2026: Canton literature and public-data inventory

- Added `research/canton-literature-data-inventory.md`.
- Mapped official Canton protocol, Global Synchronizer, FAQ, Splice documentation, Canton Coin whitepaper, CIPs, Noves public API/dashboard, and CCView explorer.
- Key limitation: public Canton data is not a complete network ledger view. Public APIs cover publicly observable activity; private activity is restricted to entitled parties/witnesses.
- Documented that Noves API requires an API key and some analytics endpoints require an enabled paid analytics add-on. Do not assume unrestricted free bulk data access.
- Identified measurable public-data areas: public CC transfers, public updates, supply/burn, rewards, validators, Featured Apps, and governance/CIP chronology, subject to access and field verification.
- Identified unavailable or unverified network-wide variables: private asset transfers, actual institutional settlement times, collateral utilisation, capital efficiency, and complete counterparty exposure.
- Recorded CIP-0129 (Universal Burn and Synchronizer Pricing), approved 23 October 2026, as a possible future policy-analysis candidate. Implementation date and actual adoption still require verification.
- Five candidate research avenues recorded, none selected: public observability; Canton Coin incentives; universal burn policy; institutional settlement/capital efficiency; privacy and institutional observability.
- Next exact task: verify API access and actual schemas, obtain dated data samples, cross-check explorer metrics, confirm CIP-0129 implementation status, and complete the literature gap search before selecting hypotheses.


## Update — 17 November 2026: first-pass literature-gap matrix

- Added `research/literature-gap-matrix.md`.
- Mapped broader academic and institutional work on blockchain information provision, atomic settlement, tokenised-market design, financial-market infrastructure, tokenisation frictions, and Canton's own protocol/economic documentation.
- Developed five candidate avenues without selecting one: public observability; Canton Coin incentives; universal burn/synchronizer pricing; settlement and collateral economics; privacy and institutional accountability.
- Identified a possible synthesis around independently measuring the public economics of a privacy-preserving institutional network. This remains a candidate, not a novelty claim or topic decision.
- Proposed an evidence-led hybrid output: paper, observer-capability/metric-validity matrix, documented public-data panel where feasible, reproducible calculations, and clearly labelled policy scenarios.
- Recorded data, metric-validity, cross-source, policy-implementation, literature-novelty, and programme-eligibility gates.
- Important: literature review is targeted and preliminary, not systematic. No claim of first-ever research is made. CIP-0129 approval is not evidence of implementation or policy impact.
- Next exact task: verify the formal grant terms and eligibility; test actual public API/explorer fields and historical depth; then expand Canton-specific literature searches and assess the five candidate avenues against evidence feasibility.


## Update — 17 November 2026: public-data access feasibility audit

- Added `research/data-access-feasibility-audit.md`.
- Reviewed Noves API documentation, endpoint pagination, analytics add-on requirements, published pricing, and available public explorer/dashboard alternatives.
- Confirmed the public network updates endpoint is documented but requires an API key; its feed covers public updates, not the full private ledger.
- Confirmed network-wide analytics endpoints, including public/private verdict aggregates and several supply, burn, reward and usage series, require the Canton Analytics add-on. No subscription or privileged access is assumed.
- Documented a two-layer research design: a baseline executable without paid access, plus an optional empirical extension only if access is confirmed.
- Corrected CIP-0129 treatment: Phase 1 universal burn is estimated for Q1 2027 and Phase 2 volume pricing/commitment discounts for Q3 2027 in the approved proposal. These are estimates, not implementation facts; November work can only model the policy ex ante.
- Formal Community Research Grant Terms and Conditions remain unverified despite the launch announcement's expected publication date of 15 November. Eligibility, KYC, sanctions, payment, rights and disclosure terms must be confirmed before relying on the grant.
- No authenticated API request or data extraction has been performed. This is a documentation audit, not a live data validation.
- Next exact task: inspect exportable fields and metric provenance on public dashboards/explorers, obtain the official grant terms, and build a no-paid-access research design with explicit quantitative outputs.


## Update — 17 November 2026: quantitative research design specification

- Added `research/quantitative-research-design.md`.
- Specified a claim-relative observer-capability model, distinguishing access to transaction payloads from routing/confirmation metadata.
- Defined a four-level evidence ladder: directly observed, derived, model-dependent inference, and not identifiable.
- Created a metric-validity framework and data dictionary requirements; explicitly rejected treating public update counts or public CC transfer volume as total network activity or institutional settlement value.
- Specified a symbolic fee and incentive model for CIP-0129, including list-price fees, CC conversion, volume/collateral/loyalty discount functions, collateral opportunity cost, break-even analysis, and reward allocation.
- Marked the discount combination formula as an analytical convention, not the approved protocol formula. Deferred/unknown parameters remain variables.
- Proposed six quantitative exhibits and a no-paid-access baseline deliverable set.
- No raw data extraction, authenticated API request, or empirical estimate has been performed.
- New literature/data check: CCView's October 2026 report is a public, no-registration monthly report with public-data metrics and a methodology section. It may provide an accessible historical snapshot; its metric definitions and provenance must be audited before use.
- Reconfirm CIP-0129 status: approved 23 October 2026; estimated Q1 2027 universal-burn rollout and Q3 2027 volume/commitment pricing are targets, not live implementation. The proposal appendix contains illustrative pricing examples; those must not be confused with final parameters.
- Official grant Terms and Conditions still not located in the sources checked. Launch announcement remains the only verified official source for programme terms at this point.
- Next exact task: audit CCView's October report methodology and the full CIP-0129 appendix; build a parameter register separating approved rules, illustrative examples, unknowns and scenario assumptions. Obtain the formal grant terms.


## Update — 17 November 2026: CCView report audit and economics parameter register

- Added `research/ccview-october-report-audit.md`.
- Audited CCView's October 2026 report methodology. Its transaction metric is committed updates observed on the Global Synchronizer, deduplicated by update ID and record-time bucketed; private updates whose payload is not delivered are excluded, while envelope-only observations are counted without amount-weighting.
- Identified material internal inconsistencies: executive summary reports 35.0M transactions down 0.7%, while the spotlight says the monthly total fell 23%; executive-summary mint/burn/net issuance are 645.8M/442.6M/203.2M, while the detailed section gives 664.8M/448.5M/216.36M; burn ratios also conflict (68.5% vs 67.5%). New Featured Apps may conflate 10 live apps with 12 grants. Do not use these figures as a clean time series until clarified.
- Reported reward concentration (top 10 Featured Apps at 91.7%, with displayed shares totalling 91.8%) is a candidate for reproduction, not yet a validated finding. It is not equivalent to market concentration.
- Added `data/parameter-register.md`.
- Classified CIP-0129 rules as approved framework versus unknown second-CIP parameters. Confirmed USD 60/MB is the current list price stated in the approved CIP snapshot, not an immutable value. Exact volume curve, commitment/collateral/loyalty discounts, throughput measurement, collateral valuation, margin-call rules and shortfall settlement are deferred.
- Added a distinct reward-attribution integrity issue: dedicated synchronizer operators submit aggregate per-party traffic reports; the approved CIP acknowledges that initial attribution relies on operator honesty and could misdirect rewards among parties. This is a stronger, concrete mechanism-design and governance question to investigate.
- Corrected model scope: commitment shortfalls are paid from collateral and credited back as traffic, but conversion/settlement parameters are unspecified; model symbolically until second CIP. Do not treat the earlier generic multiplicative discount formula as approved.
- CCView Quick Start documents live streams for updates, transfers, traffic purchases, reward coupons and mining rounds, but requires an API key and live streams do not replay missed events. Historical backfill is required for reproducibility.
- Grant terms: the official announcement still says Terms and Conditions are expected by 15 November and govern eligibility, KYC, sanctions, disclosures and payment. No separate official terms document was found in the sources checked. The announcement does specify publication window (Nov 1–30) and that work shared by Dec 4 may be reviewed; grant eligibility/payment cannot yet be assumed.
- Next exact task: request CCView clarification/raw report data; inspect API access and historical endpoint schemas; reconcile reward mechanics with CIP-0082 and implementation; refine the research question around observability and reward attribution integrity. Keep the topic provisional.


## Update — 17 November 2026: scenario model and reward-attribution research avenue

- Added `analysis/synchronizer_economics_scenarios.py`, a dependency-free Python scenario model. It calculates gross list-price fees, assumed discounts, collateral carrying cost, net modelled benefit and the break-even discount. All non-governance inputs are explicitly illustrative, not observed or approved.
- Added `research/reward-attribution-integrity.md`, formalising the risk explicitly acknowledged in CIP-0129: dedicated synchronizer operators initially report per-party traffic attribution, and a malicious report can misdirect rewards while respecting an aggregate paid-traffic cap.
- Formalised the distinction between aggregate cap compliance and party-level attribution correctness. Included a hypothetical three-party example, total-variation error metric, threat model, and comparison of operator attestation, independent audit, cryptographic commitments, zero-knowledge proofs and threshold attestation.
- This creates a sharper candidate research avenue: privacy-preserving reward attribution and incentive integrity. It connects mechanism design, privacy engineering, distributed systems and network economics, with a quantifiable misallocation model.
- It is not selected yet. Implementation schemas, reward contracts, validation logic, and the actual enforcement of the aggregate cap must be inspected. No claim is made that Canton lacks cryptographic controls or that any operator has misreported.
- Next task: inspect the CIP-0129-related implementation in Canton repositories, identify the actual report and reward contracts, and determine whether the proposed risk is already mitigated in code. Then decide whether this narrower topic offers a stronger contribution than the broader observability/measurement study.


## Update — 17 November 2026: implementation-level code audit

- Added `research/implementation-code-audit.md`.
- Inspected the public Canton Splice repository at commit `408f7ed9e742707f0d6fe080ca386aedc742d977`.
- Found an existing decentralized-synchronizer extra-traffic purchase path: `AmuletRules_BuyMemberTraffic` validates synchronizer support and minimum top-up, burns Amulet, and creates a `MemberTraffic` contract.
- The `MemberTraffic` contract records sequencer member ID, synchronizer ID, migration ID, purchased traffic bytes, purchase count, Amulet spent and USD spent. SV automation aggregates these records by member and synchronizer.
- Important distinction: this existing member-level traffic-purchase accounting is not evidence that CIP-0129's proposed per-party reward-attribution reports are implemented. Do not conflate the two.
- This gives us an implementation baseline and a concrete comparison: current member-level purchased-byte accounting versus CIP-0129's proposed party-level attribution for reward allocation.
- The code inspected does not establish the actual enforcement of CIP-0129's aggregate cap or its dedicated-synchronizer report-validation mechanism. Those remain unresolved.
- Next exact task: inspect the relevant reward coupon and reward-accounting implementation, then compare the current code path with the CIP-0129 framework. After that, decide whether the narrower reward-attribution integrity study is sufficiently original and feasible.


## Update — 17 November 2026: corrected reward architecture after CIP-0132 discovery

- Added `research/cip-0104-0129-0132-architecture-comparison.md`.
- Revised `research/reward-attribution-integrity.md` with an explicit scope correction. The earlier per-party misallocation model is provisional and describes a possible later granular-attribution regime, not the proposed Phase 1 design.
- Verified CIP-0104 is approved (27 Oct 2026). It bases Global Synchronizer app rewards on sequencer and mediator data. Its activity computation uses accepted verdicts, transaction views, confirming parties, Featured App rights at round opening and envelope traffic costs. The public Splice implementation contains this path in `AppActivityComputation.scala`.
- CIP-0104 includes the `ActivityRecorder_DsoRecordActivity` extension hook for activity not visible to the sequencer/mediator and explicitly anticipates dedicated synchronizer integration.
- Verified CIP-0132 is **Proposed**, created 9 Nov and proposed 16 Nov 2026; it requires CIP-0104 and CIP-0129. It specifies Phase 1 of universal burn using a dedicated synchronizer operator's aggregate traffic API (10-minute intervals), a designated paymaster, off-ledger report-to-burn coordination, CC burn on the Global Synchronizer and activity records through the CIP-0104 hook.
- In CIP-0132 Phase 1, the paymaster receives the corresponding app and validator rewards. More granular attribution to participants is explicitly deferred to later states.
- CIP-0132 trusts the dSync operator and paymaster to report traffic and burn accordingly. It acknowledges possible under- or over-reporting. Its stated on-chain protection ties rewards to CC burned; this does not independently prove that the burn matches actual traffic consumed.
- Therefore the immediate research question is now: what economic and verification properties should the trusted paymaster model satisfy when converting private synchronizer traffic reports into public CC burns and reward entitlements, and how should these properties evolve toward granular attribution?
- Research method now centres on traffic measurement, report-to-burn reconciliation, discount and CC-price conversion, burn/reward consistency, delay/smoothing, operator/paymaster incentives, privacy and independent auditability. Do not claim a live per-party reward misallocation vulnerability.
- Next task: locate the CIP-0132 implementation branch / PR and inspect the exact RegisteredSynchronizer contracts, traffic-report API, purchase path, ActivityRecorder hook integration and reward accounting. CIP-0132 is still proposed in this snapshot; no deployment claim is permitted.


## Update — 17 November 2026: paymaster implementation and report API audit

- Added `research/paymaster-implementation-audit.md`.
- Audited merged `splice-multi-sync#100` (paymaster Daml purchase, merged 11 Nov) and `#104` (Scan/SV integration and paymaster traffic-contract merging, merged 12 Nov).
- Audited `splice-multi-sync#111` traffic-report API PR. It was open and non-draft on 17 Nov, not merged. The report endpoint returns 10-minute aligned intervals with Ok / Undetermined / CannotProvide status, uses JWT authentication and pages at 100 intervals.
- Read the implementation: traffic is computed from participant cumulative extraTrafficConsumed counters at interval boundaries, with the base rate configured to zero. It reads current and successor sequencers across logical synchronizer upgrades.
- Identified a specific reporting semantic requiring owner clarification: `participantsConsumed` iterates only participant IDs present in the end-of-interval traffic-state map. The source test models a participant who leaves during the interval and excludes its consumption. The public report should not be described as all bytes consumed by every participant active at any point until this is resolved.
- The report reader also documents a pruning race at the retention boundary: the sequencer prunes before advancing the lower bound, so a boundary request can still return an incorrect total. This is an explicit source comment.
- The report PR's diff includes single-node integration and LSU-spanning tests, but does not show the four-node equality test required by tracker issue #152. Cross-node consistency remains unverified in this PR snapshot.
- Crucial tracker evidence: ChainSafe issue #155 explicitly says nothing checks the paid amount against the traffic report; a paymaster may pay less than actual usage. The SVs can archive a misbehaving registration, which is governance enforcement rather than automatic period-by-period reconciliation.
- The merged purchase path validates registered paymaster, synchronizer ID, required-synchronizer exclusion, migration ID, empty member ID, activity-weight bounds and minimum top-up. It reuses existing CC burn logic. These checks establish authorisation and purchase validity, not report/payment equality.
- App and asset activity are computed as purchased bytes multiplied by registration weights, rounded down. The purchase PR's ActivityRecorder hook remains a TODO. Tracker issue #163 follows up on recording it; upstream Splice PR #8449 was still a draft in this snapshot.
- ValidatorRewardCoupon is a separate validator reward and remains in place; ActivityRecorder is for app rewards. The implementation tracker says paymaster automation is not included and each paymaster builds its own.
- Added `analysis/paymaster_reconciliation_scenarios.py`, a dependency-free hypothetical scenario model. It measures report error, purchase coverage, unpaid/overpaid traffic, CC burn cost per actual MB and activity units. Inputs are illustrative, not observed data.
- Research focus now has a precise implementation-grounded formulation: measurement correctness, payment completeness and reward attribution are separate properties in the traffic-report → CC-burn → reward pipeline.
- Next task: inspect CIP-0104 ActivityRecorder design and its draft implementation, compare the Merkle-root / expansion proof-of-concept in the extension-synchronizer tracker with the paymaster approach, then refine the original contribution. Do not claim the current PR is deployed on MainNet.


## Update — 17 November 2026: compare paymaster model with Merkle reward-reporting PoC

- Added `research/paymaster-vs-merkle-reward-accounting.md`.
- Inspected the upstream draft ActivityRecorder PR #8449. It introduces a DSO-controlled `ActivityRecorder_DsoRecordActivity` choice for app and asset activity. It also adds an AmuletRules contract-state migration that creates the ActivityRecorder. PR #8449 remains draft and unmerged at this snapshot.
- Recovered the earlier Phase 3 Merkle-root reward-reporting PoC in tracker issue #47 and fork PR #8. It records per-round activity as a Merkle root plus total, then expands committed activity through ProcessRewardsV2.
- Important review correction in that PoC: the initial total was not bound to the committed tree. The later design added a governance-attested purchased-traffic total, a reported-total <= purchased-total check, weighted internal Merkle nodes and a weight budget propagated through expansion.
- The stated on-ledger invariant is: minted rewards <= committed tree weights <= reported total activity <= purchased traffic. Four adversarial tests cover over-reporting against purchases, over-declared internal nodes, over-minting leaves and unweighted-batch smuggling.
- This PoC was Daml/Daml Script only, with no Scala automation or end-to-end wiring. The tracker says rewards were out of Phase 2 and the machinery was parked as input to Phase 3. Do not describe it as deployed or operational.
- The comparison reveals an original research opportunity: compare how verification responsibilities are allocated across measurement integrity, payment completeness and reward integrity in the aggregate paymaster model versus the granular Merkle reward model.
- The research candidate is now a hybrid protocol-economics and mechanism-design study with a formal state-transition model, quantitative reconciliation, and privacy-preserving reward-accounting analysis. Still provisional; verify the current CIP-0132 implementation and official grant eligibility before selecting.


## Update — 17 November 2026: interdisciplinary literature-gap review

- Added `research/literature-review-gap-matrix.md`.
- Compared the Canton case against principal-agent auditing, financial market infrastructure standards, verifiable resource accounting, privacy-preserving commitments/selective disclosure and Merkle proof-of-liabilities literature.
- Closest conceptual precedent identified so far: ALIBI, “Towards Verifiable Resource Accounting for Outsourced Computation” (2013). This prevents claiming that verifiable resource metering itself is novel.
- Principal-agent auditing literature supplies a formal framework for hidden information, audit probability, detection accuracy, penalties and limited liability. It shows that “operator could under-report” is not itself a research contribution.
- CPMI-IOSCO PFMI provides governance, risk, settlement finality, operational resilience and disclosure control objectives; do not claim legal applicability to every Canton synchronizer.
- Merkle commitments bind disclosed data and support selective disclosure, but do not alone establish source truth or completeness. Proof-of-liabilities literature warns that tree construction and aggregate-binding details matter.
- Candidate integrated gap: privacy-preserving resource measurement + reconciliation of operator-reported consumption against a separate public payment/burn record + incentive-compatible allocation of audit/challenge responsibilities + cryptographically bounded reward issuance.
- Proposed research questions cover measurement completeness, payment completeness, incentive compatibility, reward integrity and privacy/accountability trade-offs.
- Four candidate hypotheses are recorded in the review. They remain to be formalised and tested; they are not findings.
- Review is a targeted scoping review, not a systematic review. Novelty remains provisional. Next literature pass should cover trusted hardware/remote attestation, verifiable state/counter transitions, proof-of-reserves completeness attacks, accounting reconciliation under partial observability, privacy-preserving telemetry and cross-domain resource billing.


## Update — 17 November 2026: deeper literature and accountability-design review

- Added `research/deeper-literature-review-accountability-design.md`.
- Verified CIP-0132 directly from the Canton CIPs repository. It is marked Proposed, created 9 Nov and proposed 16 Nov 2026. It explicitly describes Phase 1 as an interim trust model: the dSync operator reports traffic, the paymaster burns CC post-hoc, the report-to-burn link is off-ledger, and operator/paymaster are trusted to report and burn according to their agreement.
- Important modelling correction: CIP-0132 explicitly permits off-ledger discounts and burn smoothing (including weekly/rolling windows and delays). A naïve ten-minute report-to-burn equality test would produce false underpayment findings. Reconciliation must be cumulative and agreement-aware.
- CIP-0132 says on-ledger controls ensure rewards are commensurate with the burn actually made. This is narrower than proving every byte consumed was correctly reported and paid for.
- CIP-0104 is Approved (27 Oct 2026) and defines sequencer/mediator-derived activity and a DSO-controlled ActivityRecorder extension for activity not directly visible from those sources. It supplies the app-reward context for the dSync extension.
- Added VeriCount (Tople et al., ACNS 2018) as a stronger direct precedent than relying only on ALIBI. VeriCount uses SGX plus software fault isolation to measure CPU, memory, I/O and bandwidth and supports refutable billing. Its assumptions include trusting the SGX/VeriCount components and non-colluding provider/client; it is not a Canton-specific solution.
- Added RFC 9162 Certificate Transparency v2 as a model for signed tree heads, inclusion and append-only consistency proofs. The RFC explicitly notes that logs may show inconsistent views; monitoring/gossip are needed. Append-only commitments do not prove all eligible source events were submitted.
- Added Hu et al. (2019) proof-of-liabilities attack as evidence that summation Merkle trees require globally consistent proofs and completeness assumptions, not just hash integrity.
- Revised candidate direction: staged accountability from trusted metering to verifiable report continuity, agreement-aware burn reconciliation and bounded reward attribution.
- New experiments: omitted interval, split view, participant/upgrade/pruning boundary, discount/smoothing false positives, reward budget versus omitted input, and trust-cost comparison.
- Remaining work: verify ALIBI primary bibliographic details, study remote-attestation limits, review privacy-preserving telemetry/aggregation, compare current CIP-0132 implementation to proposal, and inspect later-phase design before deciding prototype scope.


## Update — 17 November 2026: falsifiable hypothesis and test protocol

- Added `research/hypothesis-and-test-protocol.md`.
- Formalised five provisional hypotheses: agreement-aware window reconciliation; limits of Merkle commitments for source completeness; aggregate report-to-burn reconciliation under privacy constraints; audit incentive compatibility; and accountability/privacy/operational-cost trade-offs.
- Specified four experiments: deterministic reconciliation simulation, adversarial report-integrity tests, principal-agent incentive analysis, and comparative privacy/assurance assessment.
- Defined falsification criteria and measurement outputs for every hypothesis.
- Explicitly separated actual consumption, reported traffic, CC burned, agreement-implied payment, reward-eligible activity and reward entitlement. They must not be conflated.
- Added stop conditions: absent actual report schemas, pricing agreements and burn/reward semantics, restrict claims to proposal-level analysis and synthetic scenarios. Do not infer real operator accuracy or underpayment.
- Novelty claim remains provisional. Existing resource-accounting, Merkle, auditing and attestation methods are precedents; candidate contribution concerns their composition across Canton's private traffic-report → public burn → reward pipeline.
- Next exact task: trace CIP-0132's current proposal and implementation state end-to-end against the five hypotheses, and obtain/verify the official Community Research Grant terms and eligibility before fixing scope.


## Update — 17 November 2026: end-to-end verification audit

- Added `research/end-to-end-verification-audit.md`.
- Rechecked CIP-0132 directly: it remains Proposed, dated 9–16 November. Phase 1 explicitly trusts the dSync operator/paymaster; report-to-burn linkage is off-ledger; discounts and burn smoothing/delays may apply; rewards are constrained to burn actually made, not independently proven actual consumption.
- Verified `splice-multi-sync#100` and `#104` merged 12 November. PR #100 states the paymaster registration/purchase changes had not been deployed to a long-running network in the snapshot described. Do not claim MainNet deployment.
- Verified traffic-report PR #111 remained open on 17 November. It describes ten-minute reports and sequencer/LSU handling; four-node equality remains an acceptance criterion not established by the inspected PR.
- Verified ActivityRecorder PR `splice#8449` remained draft/open; tracker issue #163 remained open. The full dedicated-synchronizer app-activity reward path was therefore not verified complete.
- Verified end-to-end test issue #159 remained open and depended on #152/#163 and related work.
- Verified tracker issue #155 explicitly records that nothing checks the paid amount against the report and a paymaster may pay less than usage; SVs can archive a misbehaving registration. This is a documented control gap/design limitation, not evidence of actual misconduct.
- Verified Merkle reward PoC issue #47 is closed as a PoC task but explicitly lacked Scala automation and end-to-end wiring. Not production evidence.
- Rechecked official Canton Community Research Grants announcement. It confirms November 1–30 publication window, optional X sharing by Dec 4, discretionary programme-level maximum up to 50,000 CC/month, research-quality/community-value considerations, KYC/sanctions screening, grant agreement, disclosures, and no guaranteed award.
- No separate official Terms and Conditions document was located in this pass despite the announcement's expected publication date of Nov 15. Jurisdictional eligibility, payment rails, tax, IP/licensing and detailed contractual terms remain unverified. Do not assume Nigeria-based applicant eligibility either way.
- Updated hypothesis status: H1/H2 are model-testable; H3 is unestablished and needs a disclosure/identifiability test; H4 is theoretical; H5 needs architecture comparison and benchmarks. No empirical results exist yet.
- Next exact task: obtain actual terms/eligibility confirmation; freeze source snapshots; build an end-to-end state-transition diagram and executable synthetic reconciliation experiment.


## Update — 17 November 2026: state-transition model and first synthetic experiment

- Proceeding on the user's instruction to treat grant eligibility/terms as settled; no further grant-terms work is a blocker for the technical research sequence.
- Added `research/paymaster-state-transition-model.md`: separates metering, reporting, off-ledger agreement calculation, paymaster purchase/burn, ActivityRecorder, reward calculation and reconciliation. Documents candidate invariants, non-invariants and unresolved implementation questions.
- Added `analysis/paymaster_reconciliation_experiment.py`: dependency-free Decimal-based synthetic model with three cases: smoothed aggregate settlement, injected 4 CC shortfall, and valid discounted payment.
- The experiment is a model, not a Canton protocol implementation or empirical network measurement. It tests the narrow proposition that agreement-aware cumulative reconciliation avoids false alarms from timing/discount treatment while detecting a shortfall at settlement-window close.
- Important limitation: the synthetic fixture assumes interval-to-burn attribution and a known agreement. Real application requires actual report semantics, settlement windows, pricing terms, burn mapping and missing-data handling.
- Next task: run and extend the experiment with missing/undetermined intervals, duplicate burns, rounding boundaries, agreement-version changes, logical synchronizer upgrades and report counter resets; then add unit tests and publish a compact results table.


## Update — 17 November 2026: reconciliation model expansion and tests

- Replaced the initial interval-tagged toy model with a settlement-window model that separates traffic report status, agreement version, burn event identity and settlement-window membership.
- Added explicit handling for ok, undetermined and cannot_provide reports. Missing or unavailable intervals now return incomplete; they are never silently interpreted as zero usage.
- Added idempotent duplicate-burn ingestion. Identical duplicate event IDs are counted once; conflicting records sharing an ID are rejected.
- Added per-interval agreement-version selection, settlement-window filtering, shortfall detection and a rounding-boundary demonstration.
- Added tests/test_paymaster_reconciliation.py with ten deterministic unit tests. The experiment and all ten tests passed in the local run.
- Added research/reconciliation-experiment-results.md with outputs, interpretation, reproduction steps and explicit model boundaries.
- Rounding example: three 0.005 CC charges yield 0.03 CC if rounded per interval and 0.02 CC if aggregated before rounding. The actual contractual rounding rule remains unknown; neither convention is asserted as Canton policy.
- Counter reset / logical synchronizer upgrade gaps are represented as cannot_provide and therefore incomplete. This does not reconstruct unavailable historical counters.
- Research finding is limited: window-level reconciliation can detect injected shortfalls in synthetic conditions when reports, agreement versions and burn-window mapping are complete. It cannot establish actual traffic measurement correctness or report-to-burn linkage in production.
- Next exact task: formalise the accounting properties and threat model, then add adversarial cases for participant join/leave, report omission/tampering, split views and reward issuance bounds. Preserve the distinction between modelled properties and verified implementation behaviour.


## Update — 17 November 2026: accounting properties and adversarial counterexamples

- Added research/accounting-properties-and-threat-model.md, defining the system boundary, actors, adversary capabilities, eight candidate accounting/privacy properties, required evidence and explicit non-claims.
- Separated report continuity, measurement integrity, agreement-correct liability, payment completeness, burn attribution uniqueness, reward bounds, observer-view consistency and privacy preservation.
- Added analysis/adversarial_accounting_tests.py and tests/test_adversarial_accounting.py.
- Added an omitted-participant counterexample: reported traffic of 10 units at 1 CC/unit with a 10% discount is fully paid at 9 CC, while hypothetical actual traffic of 16 units implies 14.40 CC. Report-to-burn reconciliation passes despite a 5.40 CC hidden difference. This demonstrates a logical limitation of report-based reconciliation, not production omission.
- Added split-view demonstration: digest comparison detects conflicting report content when two observers compare the same synchronizer/interval/version; one observer's self-consistent digest cannot reveal an omission.
- Added abstract reward-budget invariant: it rejects issuance above the authorised budget but does not prove the budget was derived from complete activity.
- Added research/adversarial-accounting-experiments.md with results, implications and limits.
- Next exact task: inspect whether the actual report API exposes stable report identity/version and interval coverage, then trace the concrete reward cap/attribution code. Replace abstract assumptions with implementation facts where source evidence permits. Only after that decide whether a cryptographic or trusted-metering prototype is justified.


## Update — 17 November 2026: source-level traffic-report semantics

- Added research/traffic-report-implementation-audit.md from the source diff of canton-network/splice-multi-sync#111. At the snapshot PR #111 is open, not merged; the audit is not evidence of deployment.
- Confirmed the proposed JWT-authenticated report endpoint returns aggregate byte totals per aligned interval, not participant-level rows. It supports at most 100 intervals per page and statuses Ok, Undetermined and CannotProvide.
- Read the actual TrafficReport.participantsConsumed implementation and its unit test. It iterates participants present at interval end; a participant present at start but absent at end is excluded, while a participant joining during the interval is counted from zero. The source test explicitly comments that the departing participant is not counted.
- This is an implementation semantic, not yet a proven defect. Whether it creates undercount depends on the intended economic rule for traffic consumed before departure. The CIP/report contract should define the lifecycle charging rule.
- Confirmed the report reader handles logical synchronizer upgrades by selecting current/successor sequencer state around the upgrade. It returns CannotProvide for intervals unavailable due to pruning or upgrade history gaps. Source comments also identify a pruning race at the retention boundary.
- Rechecked PR #8449: ActivityRecorder integration remains draft at the snapshot. Do not describe the complete activity/reward integration as merged or deployed.
- Tracker issue #155 is closed (12 Nov) but its body explicitly states that nothing checks paid amount against report and a paymaster may pay less than usage; SV archiving is governance enforcement. Treat this as a documented control limitation, not evidence of actual underpayment.
- Executed the six adversarial-model assertions in the analysis runtime: all passed. They demonstrate a report-to-burn reconciliation can pass despite an omitted participant; digest comparison detects split views only when observers compare; a reward cap blocks over-issuance relative to its budget but cannot prove the budget's input was complete.
- Next exact task: formalise participant lifecycle accounting and model the size of undercount from departures across interval boundaries; then compare alternative privacy-preserving lifecycle evidence mechanisms. Keep this conditional on the intended chargeability rule.


## Update — 17 November 2026: participant lifecycle accounting experiment

- Added analysis/participant_lifecycle_experiment.py, tests/test_participant_lifecycle.py and research/participant-lifecycle-accounting.md.
- Modelled the source-observed end-state aggregation rule against two possible economic policies: departed participants' pre-exit traffic remains chargeable, or it is explicitly excluded.
- In a synthetic example with 100 units from a continuing participant, 40 units from a participant who leaves, and 25 units from a participant who joins, the current end-state aggregation returns 125. If pre-exit usage remains chargeable, the economic total is 165 and 40 units are omitted.
- Sensitivity cases show the difference equals the departed participant's pre-exit usage (10, 40 or 80 units) under the stated assumptions. These are illustrative inputs, not network estimates.
- Critical unresolved question: the source code defines the aggregation behaviour, but the executed off-ledger agreement and CIP/report semantics must establish whether pre-departure traffic is billable. Do not label this an underpayment defect before that policy is verified.
- Compared four candidate treatments: signed departure snapshot, carry-forward counter, event-driven boundary settlement and explicit exclusion. No design selected.
- Next exact task: locate authoritative charging semantics for participant departure and determine whether the paymaster's expected-liability calculation uses this same aggregate. Then quantify privacy and operational trade-offs for only the mechanisms consistent with the agreed rule.


## Update — 17 November 2026: participant departure mechanism comparison

- Added analysis/participant_lifecycle_mechanisms.py and tests/test_participant_lifecycle_mechanisms.py.
- Added research/participant-departure-mechanism-comparison.md.
- Formalised interval membership into continuing, joining and leaving membership epochs. If departure usage is billable, the complete interval total equals the existing end-state aggregate plus the departed member's final counter delta.
- Compared signed departure snapshots, carry-forward counters, event-driven boundary settlement and explicit exclusion. No mechanism is selected because the authoritative commercial charging rule remains unverified.
- Synthetic example: continuing 100 + joining 25 + departed pre-exit 40. Current end-state total is 125; billable-departure policy yields 165. Under explicit exclusion, 125 is policy-correct. These are illustrative units only.
- Missing departure evidence returns incomplete; identical event replay is idempotent; conflicting duplicate event IDs are rejected.
- Source distinction: CIP-0132 says the dSync tracks traffic consumed and reports ten-minute intervals, while the proposed API says traffic charged to participants. PR #111's implementation explicitly excludes a participant absent from the end-state map. The inspected CIP text does not resolve whether pre-departure traffic remains chargeable. This is a specification/contract ambiguity, not a confirmed defect.
- Next task: search authoritative agreement/onboarding documentation and code paths for member removal, traffic-counter lifecycle and the paymaster's consumption of report totals. If no normative rule is published, record the ambiguity as an open protocol question and build a proposed invariant that makes the policy explicit.


## Update — 17 November 2026: paymaster automation boundary verified

- Checked splice-multi-sync tracking issue #87. It explicitly states the feature enables paymaster automation but does not implement the automation; each paymaster implements its own.
- CIP-0132 likewise leaves automation that consumes traffic reports and performs burns to the paymaster. The report API PR #111 is not a universal reconciliation engine.
- Therefore no single upstream paymaster consumer exists in the inspected work to trace for participant departure handling. The executed off-ledger agreement and each paymaster's own automation are necessary evidence to determine the billable population and aggregation policy.
- Issue #155 confirms the on-ledger purchase path enforces registered paymaster identity and creates burn/activity records for bytes purchased, but does not check the purchased amount against the traffic report.
- Updated research/participant-departure-mechanism-comparison.md with this implementation boundary. This increases the importance of an explicit report-to-agreement accounting contract, but does not prove any paymaster undercounts departed members.
- Synthetic lifecycle mechanism arithmetic was independently executed in the local Python runtime: 125 units under end-state/exclusion policy; 165 under a policy including 40 units of departure consumption; missing exit evidence remains incomplete.
- Next task: formulate the proposed report-to-burn accounting interface and invariants so that each paymaster automation can be independently checked against the applicable agreement, without requiring disclosure of private transaction payloads.


## Update — 17 November 2026: proposed report-to-burn accounting interface

- Added research/proposed-report-to-burn-accounting-interface.md, a design proposal for a durable settlement manifest linking synchronizer interval reports, versioned off-ledger pricing terms, paymaster calculation, public burn event IDs and reward attribution.
- Defined eight invariants: complete interval coverage; agreement-version correctness; deterministic liability calculation; unique burn attribution; due-date-aware window reconciliation; reward consistency; explicit participant lifecycle policy; privacy minimisation.
- Accounted for CIP-0132's permitted smoothing/delays: a not-yet-due burn is not automatically a shortfall.
- Proposed operator and paymaster attestations. A paymaster-generated hash of an unsigned API response is not source authentication; operator signature over canonical report content is needed for source attribution. Even a signature does not prove meter completeness.
- Added analysis/settlement_manifest_validator.py and tests/test_settlement_manifest_validator.py. The reference validator checks interval coverage, unknown statuses, agreement/digest presence, duplicate/cross-manifest burn claims, settlement attribution and payment residual. It deliberately accepts expected CC as input rather than inventing a universal pricing formula.
- This is a proposed interface, not a CIP, deployed implementation or verified cryptographic protocol.
- Next task: test smoothing schedules, multiple synchronizers sharing one paymaster, agreement changes, and burn allocation across obligations; then identify which invariants can be checked from public evidence and which require authorised off-ledger disclosure.


## Update — 17 November 2026: portfolio settlement and smoothing model

- Added analysis/portfolio_settlement_model.py and tests/test_portfolio_settlement_model.py.
- Added research/portfolio-settlement-and-smoothing.md.
- Refined the burn-attribution invariant: one burn may be partitioned across multiple synchronizer obligations for the same paymaster, but total allocations must not exceed the public burn amount and no allocation may be double-counted.
- Modelled two synchronizers under one paymaster, three agreement versions across intervals, one 15 CC aggregate burn, and two due tranches for one obligation.
- At synthetic time 150, the first obligation is not yet due for its final tranche while the second is reconciled. At time 250 both are reconciled. An over-allocation and a post-deadline short payment are detected.
- The model stores expected CC per interval under its agreement version. It does not invent a universal pricing formula or claim to reproduce a live agreement.
- Next exact task: determine which manifest evidence can be public, which requires selective disclosure to an authorised auditor, and which must remain confidential. Then build the disclosure matrix and privacy leakage scenarios.


## Correction — 17 November 2026: portfolio smoothing example

- Corrected the portfolio example so the early payment status matches the actual allocation: first 9 CC burn allocates 3 CC to O-A and 6 CC to O-B; a later 6 CC burn pays O-A's second tranche. At t=150, O-A is not yet due for the final 6 CC; at t=250 both obligations are reconciled.
- Added/updated tests to enforce this due-date interpretation. The prior draft example allocated the full 9 CC liability to O-A immediately while labelling it not-yet-due; that was inconsistent and has been corrected.


## Update — 17 November 2026: privacy disclosure matrix and aggregate leakage test

- Added research/privacy-disclosure-matrix-and-leakage-experiment.md.
- Added analysis/aggregate_disclosure_experiment.py and tests/test_aggregate_disclosure_experiment.py.
- Distinguished Canton transaction-payload privacy from the separate disclosure risks of CIP-0132 aggregate traffic accounting.
- Created a proposed evidence classification across public, auditor-restricted, operator/paymaster-confidential and excluded transaction data.
- Constructed a synthetic differencing counterexample: two overlapping cohort aggregates of 100 and 60 bytes reveal one participant's 40-byte usage, even though both cohorts satisfy k=3. This disproves the sufficiency of a minimum cohort threshold alone; it does not show that the current synchronizer-wide CIP report leaks individual usage.
- Proposed separate exact auditor evidence and privacy-protected public analytics. Rounding/noise should not be silently applied to contractual billing evidence.
- Next task: broaden the leakage analysis to linear combinations and repeated releases, then define a verifiable public proof surface that does not expose exact restricted reports or agreement terms.


## Update — 17 November 2026: linear leakage and public verification surface

- Added analysis/aggregate_linear_leakage.py and tests/test_aggregate_linear_leakage.py.
- Added research/linear-composition-and-public-verification-surface.md.
- Extended privacy analysis from pairwise nested-set differencing to exact linear identifiability across a history of aggregate releases, using dependency-free exact rational matrix-rank calculations.
- Specified four evidence layers: public verification, authorised auditor, confidential operator/paymaster evidence, and transaction data excluded from ordinary accounting audit.
- Defined conceptual assurance tiers from public burn only through signed reconciliation and proof-carrying settlement to independently measured source evidence.
- Key limitation: a commitment or zero-knowledge proof can establish integrity or arithmetic over committed inputs, but cannot prove source-meter completeness unless the measurement mechanism is independently justified.
- Next task: compare assurance tiers against concrete trust assumptions, operational cost, latency and privacy leakage; then decide whether the strongest defensible recommendation is auditor-based reconciliation, public cryptographic proofs, or a staged combination.


## Update — 17 November 2026: assurance-tier comparison

- Added research/assurance-tier-comparison.md.
- Compared public burn evidence, signed reports with independent audit, public commitments, proof-carrying settlement and independent source measurement.
- Made the central distinction explicit: calculation integrity is not measurement integrity. A signature, hash or proof over a report cannot establish that the source meter counted all chargeable activity.
- Preliminary recommendation is staged: exact auditor reconciliation first; public commitments for tamper-evidence second; selective cryptographic proofs only if a specific public verification gap justifies their cost; independent measurement only if source completeness remains a material risk.
- Cost ratings are qualitative analytical estimates, not measured costs or performance claims.
- Next: verify the actual report/API and paymaster implementation evidence against the fields this design assumes, then identify which parts are implementable now and which remain proposed.


## Update — 17 November 2026: implementation evidence audit

- Added research/implementation-evidence-audit.md and research/learning-note-implementation-chain.md.
- Reviewed public source and tracker state for splice-multi-sync PRs #100, #104 and #111; upstream Splice PR #8449; and tracker issues #152, #155, #159 and #163.
- Confirmed PR #100 (paymaster purchase logic) merged 11 Nov and PR #104 (Scan/SV handling) merged 12 Nov 2026.
- Confirmed PR #111 (traffic report API) remained open on the audit date. Its current patch reads sequencer cumulative counters on demand, returns Ok/Undetermined/CannotProvide, uses JWT caller authentication and has interval/LSU tests. The review thread says persistent storage/trigger/migration were dropped because dedicated synchronizer sequencers were not being pruned at that time. Historical availability therefore depends on that operational assumption.
- The report API is described in an internal OpenAPI specification. JWT authenticates the caller; no report-level operator signature or public commitment is established by the inspected patch.
- The traffic calculation counts participants present at interval end, treating new joiners as starting from zero and excluding participants absent at interval end. This lifecycle billing policy requires agreement-level confirmation.
- PR #100's purchase checks establish registered-paymaster eligibility and synchronizer/weight constraints, but do not reconcile the burn amount against reported liability. Tracker #155 explicitly identifies that gap; this is not evidence of actual underpayment.
- ActivityRecorder PR #8449 remained draft/open and tracker #163 remained open. The full register-transact-report-pay-reward end-to-end test in #159 remained open.
- Research conclusion: the complete traffic-to-payment-to-reward chain is not yet demonstrated. Immediate priority is report availability, provenance, agreement-aware reconciliation and a passing end-to-end test. Cryptographic proof design remains downstream of these requirements.


## Update — 17 November 2026: traffic report consistency and retention audit

- Added research/traffic-report-consistency-and-retention.md from direct inspection of PR #111 head source.
- Confirmed the reader obtains the pruning lower bound first, then performs separate historical counter reads. TrafficReport.scala explicitly warns that pruning can race a request at the retention boundary and produce a wrong total. This is a source-documented time-of-check/time-of-use risk, not evidence of a production misreport.
- Distinguished the race from logical synchronizer upgrade handling. The PR adds a cross-upgrade test using predecessor and successor sequencer snapshots; this does not establish atomic consistency against concurrent pruning.
- Confirmed the current PR patch reads counters on demand and removed the proposed report store/trigger because dedicated synchronizer sequencers were not being pruned at the time. Historical availability therefore depends on the operational retention assumption.
- Clarified that Ok means the reader calculated a value from available counter snapshots. JWT authenticates the API caller, not the report contents; the inspected patch does not establish report-level signatures, durable archival, agreement reconciliation or independent measurement completeness.
- Proposed mitigations for study: retention safety margin, atomic/snapshot-consistent reads, prune-aware failure handling, durable interval snapshots and independent boundary validation. None is represented as implemented.
- Next exact task: design a controlled concurrency test that advances pruning between the status check and counter reads, and classify whether the result is an incorrect Ok, explicit CannotProvide/error, or safe retry. Then determine whether a practical consistency guarantee can be specified.


## Update — 17 November 2026: controlled pruning-race model

- Added analysis/pruning_race_model.py and tests/test_pruning_race_model.py, plus research/controlled-pruning-race-experiment.md.
- The model distinguishes correct Ok, CannotProvide, and a hypothetical stale Ok. The stale-Ok branch is a test oracle, not a claim about current Canton behaviour.
- Five conceptual unit tests cover timing classes and the arithmetic effect of a wrong reported byte total.
- Source PR #111 documents a pruning race at the retention boundary, but no real Scala concurrency test has been run. The next requirement is a barrier-controlled integration test around pruning-status retrieval and historical counter reads, with an independently captured reference total.
- Do not claim exploitability, production occurrence, or settlement loss without that implementation-level test and configuration evidence.


## Update — 17 November 2026: underlying sequencer pruning semantics

- Added research/underlying-sequencer-pruning-semantics.md after direct inspection of Digital Asset Canton source.
- DbTrafficConsumedStore stores a per-member traffic-consumption journal and historical lookup returns the latest row at or before a timestamp.
- pruneBelowExclusive selects the latest row at or before the pruning timestamp per member, then deletes older rows in batched non-transactional operations.
- PR #111 checks pruning status separately from later historical state reads; its own TrafficReport.scala comment explicitly warns that pruning before lower-bound movement can race a report and produce a wrong total.
- Derived the exact possible interleaving: report checks old bound; pruning advances beyond a requested boundary and deletes that member's last row at/before it; report then queries that timestamp and cannot retrieve the later retained row because it is after the requested timestamp.
- This establishes a source-supported consistency risk, not an observed incorrect API response or production loss. Need real integration test with deterministic barriers to establish whether API returns incorrect Ok, explicit unavailable/error, or safe retry.
- Next: design the deterministic Scala integration test around status check, pruning completion, historical read and final API result; do not treat synthetic race model as proof of production behaviour.


## Update — 17 November 2026: controlled integration-test specification

- Added research/controlled-pruning-integration-test-spec.md.
- Specifies a deterministic database-backed Scala integration test with barriers after pruning-status evaluation and before historical counter lookup; pruning must complete before the read is released.
- Uses an independently captured expected aggregate and explicit outcome classes: correct Ok, explicit unavailable/error, safe retry, or incorrect Ok.
- Includes no-race, pre-pruned, post-read pruning, exact-boundary, multi-member and storage-backend controls.
- The test is a specification only. No Scala integration test has been implemented or run in this step; the real API outcome remains unresolved.
- Next execution should be against the actual PR #111 implementation and its compatible Canton revision. Record exact commit, backend and configuration. A wrong Ok would establish a code-level defect in that tested configuration, not production occurrence or financial loss.
