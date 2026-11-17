# Canton Literature and Public-Data Inventory

**Prepared:** 17 November 2026
**Purpose:** Establish what can be researched from public Canton sources, what requires credentials or participant-level access, and which claims cannot be supported with public data alone.

## 1. Executive finding

Canton supports several feasible quantitative research paths using public protocol documentation, governance records, public Canton Coin activity, validator/reward information, and network-level analytics. Public data is not a complete ledger view. Canton intentionally distributes transaction information only to entitled stakeholders. Public APIs expose a subset of activity and selected aggregate statistics. A study must not interpret publicly visible activity as total institutional transaction volume, total asset settlement, or complete network adoption.

A quantitative paper about institutional capital efficiency or settlement performance would require participant-level workflow data or a defensible external dataset. Public network metrics alone cannot establish those outcomes.

## 2. Protocol and institutional literature map

| Domain | Primary source | What it establishes | Research use | Limitation |
|---|---|---|---|---|
| Privacy model | Canton protocol documentation and privacy-model docs | Transaction data is selectively disclosed; validators see views for hosted parties; synchronizers route encrypted payloads and do not see transaction content | Formalise observability boundaries and privacy/control trade-offs | Protocol description is not an empirical measurement of privacy leakage |
| Synchronization and ordering | Global Synchronizer documentation | Decentralised service; 2/3 BFT majority for message ordering/confirmation and governance changes | Study governance, coordination, and operational architecture | Does not by itself provide empirical latency or failure-rate data |
| Cross-domain interoperability | Canton protocol documentation | Sync domains route messages, establish consistent order, and confirm commits; participants may connect to multiple domains | Model cross-domain workflow dependencies | Public documentation does not reveal private workflow volumes |
| Canton Coin economics | Canton Coin whitepaper / The Case for Canton | Utility, fee burn, reward categories and incentive design | Incentive analysis and model construction | Whitepaper assumptions must be separated from observed outcomes |
| Tokenomics governance | Canton Improvement Proposals (CIPs) | Versioned proposals, authorship, status, discussion and approval history | Policy chronology; possible event-study candidates | Approval date is not necessarily implementation date or causal treatment date |
| Institutional workflow | Canton use-case and application documentation | Examples of tokenised assets, collateral, payments and market infrastructure | Define workflow-level research questions | Case descriptions are not independently audited performance data |

## 3. Public data sources and access conditions

### A. Canton Data by Noves
URL: https://ccdata.noves.fi/

Observed public dashboard categories include validator and Super Validator activity, Featured Applications, Canton Coin price and network burn, network activity summaries, reward and rebate views, party directory, and network status/sequenced load. The dashboard is useful for discovery and monitoring. Availability of a chart does not guarantee a downloadable historical dataset or stable public API.

### B. Noves Canton Public Data API
Documentation: https://docs.noves.fi/reference/welcome-canton-apis

Documented data types include public update history, balances and prices, public transfers, rewards, identity and ANS records, contract details, and real-time streams.

Important constraints: API requests require an API key; the public API covers publicly observable activity, not every Canton update; transaction visibility depends on the parties and witnesses entitled to see it; private data from a participant requires authorised access to that participant's environment.

Documented endpoints include:
- GET /{chain}/updates
- GET /{chain}/updates/stats
- GET /{chain}/supply/series
- GET /{chain}/supply/pressure
- GET /{chain}/transfers/volume
- GET /{chain}/network/verdicts/daily
- GET /{chain}/network/submittingParties/cumulative
- GET /{chain}/burn/byCategory
- GET /{chain}/rewards/{party}/totals

The Analytics add-on documentation states that some network-level analytics endpoints require an enabled Canton Analytics add-on on a Canton Platform plan. Endpoint documentation must not be mistaken for free, unrestricted access.

### C. CCView Explorer
URL: https://ccview.io/

Public explorer surfaces include transfers and parties, validators and Super Validators, governance proposals, Featured Applications, network activity and economic metrics, and CIP-56 asset information. Treat explorer metrics as secondary observations until definitions, data coverage, and update frequency are checked. Cross-check key values against primary documentation or a second data source.

### D. Canton Network official documentation
- Protocol: https://www.canton.network/protocol
- Global Synchronizer: https://www.canton.network/global-synchronizer
- FAQ: https://www.canton.network/faq
- Splice / Global Synchronizer docs: https://docs.global.canton.network.sync.global/overview/overview.html

These sources are essential for defining transaction, update, synchronizer, party, validator, and privacy boundary concepts.

### E. Canton Improvement Proposals
Repository: https://github.com/canton-foundation/cips

CIPs are primary sources for proposed and approved changes. Record proposal status, author, created date, approval date, implementation status, and discussion separately.

A potentially relevant example is CIP-0129, Universal Burn and Synchronizer Pricing, marked approved on 23 October 2026. Its abstract describes a proposal to apply Global Synchronizer list-price burn to production traffic on dedicated synchronizers, with application and validator rewards. This may create a future policy-change research opportunity, but implementation timing and actual adoption must be verified before treating it as an empirical intervention.

## 4. Data availability matrix

| Variable / data class | Publicly discoverable? | Quantitative use | Main limitation |
|---|---|---|---|
| Public CC transfers | Yes, via explorers/API | Transfer counts, volume, concentration, temporal patterns | CC transfers are not equivalent to all asset settlement |
| Public ledger updates | Yes, via API/explorers | Public update frequency, payload size, event counts | Private updates omitted |
| Public/private verdict aggregates | Documented analytics endpoint | Compare observable public/private aggregate categories | API add-on/key access; exact definitions need verification |
| Validator / SV roster and status | Yes | Participation, concentration, continuity snapshots | Snapshot and uptime definitions need verification |
| Reward events and totals | Some public surfaces/API | Reward distribution and concentration | Access and coverage; distinguish earned, accrued, minted, locked |
| CC supply, price and burn | Public dashboard and documented endpoints | Time series, issuance/burn relationships | Source definitions, price provenance, access restrictions |
| Featured App activity/rewards | Some public dashboards/API | Ecosystem concentration and reward distribution | Reward is not equivalent to economic value created |
| Governance/CIP history | Yes | Proposal timelines, policy classification, governance network | Votes/approvals do not establish implementation or effects |
| Private asset transfers | No, not generally | Not measurable network-wide from public sources | Entitlement and participant-level access required |
| Institutional settlement time | Not established as public network-wide data | Could support settlement-performance analysis if acquired | Requires workflow timestamps and agreed definitions |
| Collateral utilisation / capital efficiency | Not established as public network-wide data | Could support economic impact analysis with participant data | Requires asset, exposure, financing and workflow data |
| Counterparty exposure | Not publicly observable in complete form | Risk modelling with authorised case data | Requires participant-level records and legal/operational context |
| Synchronizer latency / reliability | Some status/load surfaces; comprehensive history unverified | Operational performance analysis if raw time series obtained | Need definitions, timestamps, incidents, independent validation |

## 5. Candidate quantitative research avenues

These are feasibility assessments, not selected topics.

### Candidate A — Public observability and the measurement of institutional network activity
Question: What can public Canton metrics validly measure, and how large is the gap between observable public activity and the network's private-by-design architecture?
Method: Build a data dictionary; compare public update counts, public/private aggregate verdicts where accessible, CC transfers, and app/reward indicators; measure missingness, source disagreement, and sensitivity to metric definitions; construct an observability taxonomy separating directly observed, aggregated, inferred, and inaccessible variables.
Potential output: reproducible measurement framework and dataset documenting limits of public network analytics.
Feasibility: High, subject to API access and historical data availability.

### Candidate B — Canton Coin incentive distribution and network utility
Question: How do fee burns, reward allocations, and activity-based incentives relate over time across validators, Super Validators and application providers?
Method: Reconstruct reward rules from whitepapers and CIPs; collect time series for burns, supply, app rewards and validator rewards; calculate concentration, reward-to-fee ratios, issuance/burn pressure and category shares; test whether observed reward concentration changes with activity.
Potential output: reproducible incentive-economics report.
Feasibility: Medium to high, dependent on historical endpoint access and consistent metric definitions.
Caution: Correlation between rewards and activity does not prove incentives caused adoption.

### Candidate C — Universal burn and synchronizer pricing as a policy change
Question: What economic incentives change when production traffic on dedicated synchronizers is brought under universal burn and reward treatment?
Method: Analyse CIP-0129 and prior pricing arrangements; formalise before/after incentive equations; map affected participant classes; after implementation data exists, examine traffic, burn and reward changes while accounting for other network changes.
Potential output: policy-economics model plus later empirical evaluation.
Feasibility: Medium for ex-ante modelling; low currently for causal impact evaluation until implementation and sufficient post-change data are confirmed.

### Candidate D — Institutional settlement and capital efficiency
Question: Under what workflow conditions could atomic cross-application settlement reduce settlement exposure, liquidity fragmentation or collateral lock-up?
Method: Define stylised workflows and timing assumptions; model sequential versus atomic settlement; quantify exposure windows and required prefunding under explicit assumptions; conduct sensitivity analysis for settlement delay, failure probability, liquidity buffers and asset volatility.
Potential output: reproducible model and institutional workflow comparison.
Feasibility: Medium for scenario modelling; low for claims about realised Canton outcomes without participant data.

### Candidate E — Privacy architecture and institutional observability
Question: How does Canton's selective-disclosure model change what different participants, synchronizers, and external observers can verify?
Method: Build a role-by-data-access matrix from protocol documentation; model information flows for a multi-party workflow; compare observability, data minimisation and verification requirements; analyse which controls can be performed locally versus globally.
Potential output: formal framework, diagrams and case-based analysis.
Feasibility: High for architecture analysis; empirical validation requires authorised participant environments.

## 6. Research integrity rules
1. Never describe public CC transfers as total Canton settlement volume.
2. Never infer private transaction counts from public update counts.
3. Do not equate tokenised asset notional value with settled value, active value, or economic value added without definitions.
4. Distinguish protocol claims, dashboard estimates, third-party measurements and independently verified facts.
5. Preserve raw snapshots with timestamps, query parameters, API version and source.
6. Record access restrictions, terms of use and data licensing before reuse.
7. Use UTC consistently and document conversions.
8. Record missing observations and API outages rather than silently interpolating.
9. Treat reward amounts, minted amounts, circulating supply, locked supply and market value as separate variables.
10. Do not claim causal effects from descriptive correlations.

## 7. Current research judgement

The public data inventory supports a quantitative study of observable network activity, incentive design, or public-data measurement limitations. It does not currently support a factual claim that Canton has reduced institutional capital requirements, settlement time, or collateral lock-up across the network. Those questions require participant-level evidence or must be presented explicitly as scenario models.

A potentially distinctive direction is to connect Canton's privacy architecture to the economics and measurement of institutional network activity: what can be measured, by whom, at what aggregation level, and what economic conclusions are justified by visible data. This is a direction to test against existing literature, not a final topic selection.

## 8. Next steps
1. Obtain or confirm API access and inspect actual response schemas for public endpoints.
2. Capture a dated sample of available public metrics and record field definitions.
3. Check whether CCView, Noves and official documents agree on core metrics.
4. Build a CIP chronology, including CIP-0129 implementation status.
5. Search academic and industry literature for existing work on Canton privacy, institutional settlement, synchronizer economics and token incentives.
6. Then develop five precise, non-duplicative hypotheses with explicit data and method requirements.