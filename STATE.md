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
