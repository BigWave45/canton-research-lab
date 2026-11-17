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
