# Quantitative Research Design: Observability, Metrics, and Synchronizer Economics

**Date:** 17 November 2026  
**Status:** Research design specification; no empirical results claimed.  
**Research programme:** Interdisciplinary, quantitatively grounded, hybrid paper + reproducible analysis.

## 1. Proposed research question

**How can the public economics of a privacy-preserving institutional network be measured, and what do its observable activity and incentive metrics actually tell us? A measurement framework and mechanism analysis of Canton.**

This is a working question, not a final topic commitment. Its value lies in connecting three layers that are often discussed separately:
- protocol architecture determines who can observe which events;
- measurement design determines which public indicators can be constructed and what they represent;
- economic mechanisms determine how fees, burns, rewards and discounts change participant incentives.

The research should not claim to measure total institutional settlement activity. Its central output is a defensible boundary between what can be observed, what can be inferred under assumptions, and what cannot be identified from public evidence.

## 2. Component I: observer-capability matrix

The unit of analysis is an information class, not an assumed universal view of the ledger. Actual visibility depends on the transaction's stakeholders, hosted parties, permissions, divulgence and synchronizer configuration. The table below is an initial protocol-level map; it must be checked against the exact Canton version and deployment before publication.

| Observer | Transaction payload / contract data | Routing or confirmation information | What the observer can independently establish | Key caveat |
|---|---|---|---|---|
| Signatory / stakeholder party | Views for which it is a stakeholder | Its participant receives relevant protocol messages and confirmations | Its own entitled transaction and contract history | Does not imply visibility into unrelated parties' transactions |
| Observer party / entitled witness | Data for views to which it is explicitly entitled | Relevant update/confirmation context | The disclosed contract and lifecycle information within its entitlement | Observer rights are scoped; not a universal auditor role |
| Validator hosting an involved party | Views for parties it hosts | Messages and confirmations needed for those parties | Its hosted parties' entitled ledger state | A validator hosting no involved party receives no transaction view |
| Validator not hosting an involved party | No transaction payload for that transaction | No relevant transaction view merely by being a validator | No direct claim about that transaction's contents | Validator status alone does not confer global visibility |
| Synchronizer operator | Encrypted transaction blobs; not readable transaction contents | Routing metadata and confirmation results | Ordering/routing/confirmation facts within its protocol role | Cannot infer full amounts, terms, contract contents or all party relationships from encrypted payloads |
| Public explorer / API provider | Only data exposed through public interfaces and its own indexing permissions | Depends on public feed and provider index | Its defined public dataset and derived metrics | Coverage and semantics depend on provider, endpoint, filters and update cadence |
| External researcher / public observer | Publicly disclosed data and documentation | Publicly disclosed protocol/governance records | Reproducible measurements of the disclosed dataset | Cannot extrapolate public records into a complete network census without evidence |
| Auditor / regulator / authorised third party | Depends on legal authority, contractual role, observer rights and participant access | Depends on the same permissions and reporting arrangements | Claims supported by its authorised evidence scope | 'Auditor' or 'regulator' is not itself a protocol permission; legal access and technical entitlement are distinct |

### Observer model notation

Let:
- `o` denote an observer;
- `e` denote a ledger event;
- `v(e)` denote the set of views / data items associated with event `e`;
- `A(o,e)` denote the subset of `v(e)` that observer `o` is authorised and technically able to access.

Define an event-level visibility indicator:

`I(o,e) = 1` if `A(o,e)` contains the information required to verify the claim under study, and `0` otherwise.

This is deliberately claim-relative. An observer may verify that a confirmation occurred without being able to verify the transaction's asset amount or commercial terms.

Define the coverage ratio for a specified claim class `C` over a known event population `E_C` as:

`Coverage(o,C) = sum_e I(o,e) / |E_C|`.

This ratio is only computable when the denominator `E_C` is independently known. In a privacy-preserving network, an external researcher may not know the full event population. In that case, report coverage as **not identifiable**, not as zero and not as an estimated percentage.

### Claim-verification ladder

Classify each proposed claim as one of four levels:
1. **Directly observed:** the source explicitly records the quantity being claimed, within a defined scope.
2. **Derived:** computed from observed fields using a documented identity or transformation.
3. **Model-dependent inference:** follows only under stated assumptions that cannot be fully verified from public data.
4. **Not identifiable from available evidence:** the data do not constrain the quantity sufficiently.

Do not merge levels 1–3. Level 4 is a valid research finding, not a data failure to conceal.

## 3. Component II: metric-validity framework

Every metric enters a data dictionary before analysis. Minimum fields:

| Field | Required definition |
|---|---|
| `metric_id` | Stable identifier |
| `name` | Human-readable name |
| `construct` | What concept the metric is intended to represent |
| `operational_definition` | Exact calculation and inclusion/exclusion rules |
| `unit` | CC, USD, MB, event count, party count, ratio, etc. |
| `source` | Primary URL / endpoint / dashboard and provider |
| `source_type` | Protocol, governance, first-party dashboard, third-party indexer, researcher-derived |
| `coverage` | Public-only, party-scoped, synchronizer-scoped, or network aggregate |
| `time_basis` | Event time, ingestion time, daily snapshot, cumulative value |
| `refresh_frequency` | Real-time, daily, irregular, unknown |
| `known_blind_spots` | Private activity, missing parties, provider exclusions, revisions |
| `validation` | Cross-checks and reconciliation performed |
| `claim_level` | Direct, derived, model-dependent, not identifiable |

### Candidate metrics and interpretation limits

| Metric | Valid interpretation | Invalid shortcut |
|---|---|---|
| Public update count | Number of updates returned under the endpoint's documented public coverage and filters | Total Canton transaction count |
| Public CC transfer volume | CC transfer value visible in the defined public dataset | Total institutional settlement value or tokenised-asset notional |
| CC burned for traffic | Observed CC expenditure/burn for the covered traffic category and period | Total network operating cost or all-in institutional cost |
| Rewards by party/type | Rewards recorded for the specified party and reward categories | Profit, net income or economic value created |
| CC supply / issuance series | Supply measure as defined by the source | Spendable float or economic liquidity without further classification |
| Featured App activity / category burn | Activity or burn attributed under the provider's classification | Complete application market share or app-level revenue |
| Submitting-party count | Distinct parties meeting the source's submission definition | Number of institutions, customers or active beneficial owners |
| Synchronizer traffic in MB | Data volume measured under the protocol's traffic accounting | Transaction count or financial value |
| Settlement latency | End-to-end elapsed time only if start/end events and clock definitions are available | Synchronizer confirmation time used as a proxy for full institutional settlement |
| Collateral mobility | Change in collateral availability only with a defined workflow and position data | Inferred from transaction throughput or token transfers alone |

### Metric validation tests

1. **Definition audit:** reconcile source labels with endpoint schema and protocol definitions.
2. **Unit audit:** verify CC versus USD, bytes versus MB, event count versus transaction count, gross versus net.
3. **Temporal audit:** distinguish event timestamp from ingestion timestamp; check timezone, missing days, revisions and outages.
4. **Coverage audit:** document public/private scope, party coverage, synchronizer coverage and excluded event types.
5. **Duplicate audit:** identify repeated event IDs, pagination overlap, reorg/replay semantics and provider deduplication.
6. **Cross-source audit:** compare values only after verifying that two sources measure the same construct and do not share the same upstream data.
7. **Sensitivity audit:** recompute results under plausible alternative definitions, inclusion rules and time windows.
8. **Claim audit:** link every substantive sentence to the metric's claim level and evidence scope.

Do not compute a composite 'network health score' in the first iteration. Combining unlike measures hides their distinct coverage and can manufacture a false sense of precision.

## 4. Component III: synchronizer pricing and incentive model

### 4.1 Mechanism facts taken from CIP-0129

The approved CIP proposes that production traffic on every MainNet synchronizer incur CC burn at the Global Synchronizer list price; apps and validators receive rewards for traffic under the existing reward rules; dedicated synchronizers may receive a volume curve and optional discounts linked to throughput commitments, collateral and loyalty. The proposal says the Global Synchronizer list price is currently USD 60 per MB. It leaves the volume curve, discount sizes, collateral levels, valuation rules and detailed commitment mechanics to a second CIP. The published rollout dates are estimates, not deadlines.

These facts describe the approved framework. They do not establish that implementation has occurred.

### 4.2 Baseline fee equation

Let:
- `q` = eligible production traffic in MB over the period;
- `p` = list price in USD per MB;
- `X` = CC/USD conversion price used for fee conversion;
- `B` = CC burned for traffic.

At the undiscounted list price:

`Fee_USD = p * q`

`B = (p * q) / X`

With the currently stated list price `p = 60`, the gross list-price fee for `q = 1 MB` is USD 60 before rewards or discounts. The CIP's approximate USD 1 per typical transaction is an illustration, not a universal transaction price: actual traffic size varies.

### 4.3 Discount model with unspecified parameters

Let:
- `d_v(q)` = volume discount as a function of eligible throughput;
- `d_c(k)` = collateral-related discount as a function of qualifying collateral `k`;
- `d_l(t)` = loyalty discount as a function of qualifying commitment duration `t`.

A provisional multiplicative representation is:

`EffectivePrice = p * (1 - d_v(q)) * (1 - d_c(k)) * (1 - d_l(t))`

`Fee_USD = q * EffectivePrice`

This is an **analytical convention**, not a claim that the second CIP will combine discounts multiplicatively. If the eventual specification uses additive discounts, tiers, caps, thresholds or a different sequence, the model must be changed to match it.

Each discount is constrained to `[0,1)` and the effective price cannot be negative. Until parameters are published, the functions remain symbolic or are explored over explicitly labelled illustrative ranges. Do not insert illustrative numbers from a presentation appendix as approved parameters.

### 4.4 Commitment and collateral economics

Let:
- `K` = collateral committed;
- `r` = annual opportunity-cost / financing rate for collateral;
- `T` = commitment duration in years;
- `s` = realised throughput shortfall relative to the binding commitment;
- `L(s,K)` = loss or forfeiture associated with a shortfall, as specified by the eventual rules.

A simple collateral carrying-cost approximation is:

`CollateralCost = K * r * T`

An expanded economic cost is:

`TotalEconomicCost = TrafficFee_USD + K*r*T + ExpectedShortfallCost + OperatingCost`

The final two terms require evidence or explicit scenario assumptions. The simple carrying-cost term is not a protocol fee; it is an economic opportunity-cost estimate. It may overstate or understate the true cost depending on collateral liquidity, risk, financing access and whether collateral earns a return.

### 4.5 Adoption / break-even condition

Let `L_old(q)` represent the all-in cost of the pre-change dedicated-synchronizer arrangement, including any license or negotiated fee, where the actual contract is unknown to the researcher. Let `C_new(q,K,r,T)` represent the modelled post-change cost.

A dedicated synchronizer's economic preference under the model changes when:

`C_new(q,K,r,T) <= L_old(q)`

Because `L_old` is generally private and the detailed discount curve is not yet approved, the project cannot estimate a universal adoption threshold from public data alone. It can instead derive a break-even surface over transparent scenarios and identify which unknown parameters drive the result.

### 4.6 Reward allocation

Let total eligible reward pool be `R`, and let shares for apps, validators, super validators and the Development Fund be `w_a`, `w_v`, `w_s`, and `w_d` respectively, with:

`w_a + w_v + w_s + w_d = 1`

Then:

`R_i = w_i * R`

This representation is an accounting abstraction. The exact reward formula, eligibility, weights and distribution timing must be taken from the governing reward CIPs and implementation documentation. Do not assume fixed shares or infer party-level rewards from traffic alone unless the source exposes the applicable calculation.

### 4.7 Comparative statics to investigate

The model should test how the following variables change the economics:
- traffic volume `q`;
- traffic size distribution and peakiness, not just average throughput;
- CC/USD conversion price `X`;
- volume discount curve `d_v(q)`;
- collateral discount `d_c(k)` and collateral requirement `K`;
- loyalty discount `d_l(t)` and commitment duration `T`;
- financing rate `r`;
- commitment shortfall risk;
- reward allocation and timing;
- existing dedicated-synchronizer license or service cost, if it can be sourced.

Expected qualitative propositions to test, not assume as findings:
1. A volume discount can reduce average cost for high-throughput users while increasing the importance of accurate sustained-throughput measurement.
2. Collateral-linked discounts can trade lower traffic fees against capital encumbrance and shortfall risk.
3. Loyalty discounts can lower long-run unit cost while increasing switching costs and commitment exposure.
4. Universal burn can improve consistency of the network-wide fee/reward accounting while changing the cost structure of dedicated-synchronizer workloads.
5. The net effect is heterogeneous: transaction size, traffic regularity, capital cost and workload economics can matter more than gross volume alone.

## 5. Empirical strategy and quantitative outputs

### Baseline empirical package, no paid analytics assumed

1. **Protocol observer map:** sourced table of roles, information classes and permissions.
2. **Metric inventory:** public dashboard/API fields with source, definitions, coverage and provenance.
3. **Governance chronology:** dated record of CIP proposals, status changes, approved parameters and later amendments.
4. **Parameter register:** every model input tagged as approved, observed, externally sourced, assumed or unknown.
5. **Scenario model:** spreadsheet or script calculating gross fees, discount sensitivity, collateral cost and break-even surfaces.
6. **Uncertainty report:** parameter ranges, one-way sensitivity and selected joint scenarios.

### Optional empirical extension if free access is confirmed

- Retrieve a bounded sample from the public updates API or a public explorer interface.
- Preserve raw responses, timestamps, query parameters, pagination cursors and schema version.
- Compute only metrics supported by the retrieved fields.
- Compare public sources only after provenance and definition checks.
- Never describe the sample as a census of all Canton activity.

### Proposed quantitative exhibits

| Exhibit | What it shows | Method |
|---|---|---|
| Figure 1 | Observer visibility by role and information class | Matrix / heatmap with explicit unknown cells |
| Figure 2 | Public metric claim-validity map | Evidence-level classification |
| Figure 3 | Gross fee as a function of traffic volume at list price | Deterministic calculation |
| Figure 4 | Effective fee sensitivity to hypothetical volume discounts | Scenario curves; assumptions clearly marked |
| Figure 5 | Fee savings versus collateral carrying cost | Break-even contour / surface |
| Figure 6 | Sensitivity ranking of unknown parameters | Tornado chart or variance decomposition |
| Table 1 | Public data sources, provenance, coverage and access conditions | Source audit |
| Table 2 | Approved CIP parameters versus deferred parameters | Documentary comparison |

## 6. Reproducibility protocol

Every result must be regenerable from:
- a versioned input data file or exact source snapshot;
- a data dictionary;
- a parameter register;
- formulas and units;
- transformation steps;
- code or spreadsheet formulas;
- a record of missing values and exclusions;
- output tables and figure-generation instructions.

Each model parameter must carry one of these labels:
- `APPROVED`: explicitly approved in an authoritative governing document;
- `OBSERVED`: directly measured from a documented source;
- `EXTERNAL`: sourced from an external market or institutional source;
- `ASSUMED`: selected for scenario analysis, not observed or approved;
- `UNKNOWN`: not currently specified or accessible.

Never silently convert an `ASSUMED` or `UNKNOWN` parameter into an empirical fact.

## 7. Evidence gates and stop rules

| Gate | Pass condition | If it fails |
|---|---|---|
| Protocol correctness | Observer roles and data visibility match current authoritative docs | Narrow claims to the specific documentation/version |
| Metric definitions | Field semantics, units and coverage are documented | Exclude metric from inferential analysis |
| Data access | Free/public access and lawful reproducibility are confirmed | Keep it as a source inventory; do not promise empirical series |
| Model specification | Every equation maps to approved rules or clearly labelled assumptions | Keep model symbolic or scenario-based |
| Discount parameters | Second CIP publishes implementable formula and inputs | Do not estimate actual discounted prices |
| Implementation | Verified deployment/go-live evidence exists | No post-implementation claims |
| Causal inference | Adequate pre/post data and credible comparison strategy exist | Report descriptive patterns only |

## 8. Current limits

- No authenticated API access or raw data extraction has been performed.
- Public data is not a complete view of private institutional activity.
- The approved CIP-0129 framework leaves key discount and collateral parameters to a second CIP.
- Pre-change dedicated-synchronizer license economics may be confidential or heterogeneous.
- A model of potential fee incidence is not evidence of actual participant behaviour.
- A public observer-capability matrix is a protocol/documentation analysis, not a substitute for an audit or regulator's access.
- No causal claim about adoption, settlement efficiency, or network growth is justified by this design alone.

## 9. Sources

### Canton primary documentation
- Canton protocol and privacy architecture: https://www.canton.network/protocol
- Canton privacy model: https://github.com/canton-network/cf-docs/blob/main/docs-main/appdev/deep-dives/privacy-model.mdx
- CIP-0129, Universal Burn and Synchronizer Pricing: https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md
- Canton Improvement Proposals repository: https://github.com/canton-foundation/cips
- Canton Community Research Grants announcement: https://canton.foundation/introducing-the-canton-community-research-grants/

### Public data documentation
- Noves Canton Public Data API introduction: https://docs.noves.fi/reference/welcome-canton-apis
- Noves public network updates endpoint: https://docs.noves.fi/reference/get_chain_updates
- Noves Canton Analytics access and endpoint catalogue: https://docs.noves.fi/reference/canton-analytics
- Noves public Canton dashboard: https://ccdata.noves.fi/
- CCView explorer: https://ccview.io/

## 10. Next research task

Build the parameter register and a small, transparent scenario model from the equations above. In parallel, obtain the current official grant Terms and Conditions and verify eligibility, rights, payment and publication requirements. Do not move to a final topic decision until these checks are complete.