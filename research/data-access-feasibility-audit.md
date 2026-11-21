# Canton Public-Data Access Feasibility Audit

**Date:** 17 November 2026  
**Status:** Documentation-level audit only. No authenticated API call or live data extraction has been performed.  
**Purpose:** Establish what can be tested without paid access and prevent the research design from depending on unavailable data.

## 1. Current access findings

### Noves Canton Public Data API

The Noves documentation describes a hosted API for publicly observable Canton data. It supports update history, balances, prices, transfers, rewards, identity, ANS records, contract details, and streams. All endpoints require an API key. Larger list endpoints use cursor-based pagination.

The documentation is explicit that the API is not a complete network ledger view. Canton does not expose one global transaction feed that can be fully indexed by an outside observer. Public APIs cover the public portion of activity; CC transfers are notably public, while many other asset transfers and contract interactions are visible only to entitled parties and witnesses.

Primary references:
- API introduction and privacy/access model: https://docs.noves.fi/reference/welcome-canton-apis
- Public network updates endpoint: https://docs.noves.fi/reference/get_chain-updates
- Party-specific updates endpoint: https://docs.noves.fi/reference/get_chain-updates-party
- Network update statistics: https://docs.noves.fi/reference/get_chain-updates-stats
- API costs: https://docs.noves.fi/reference/api-costs

### Public update endpoint

The documented GET /{chain}/updates endpoint:
- returns paginated public ledger updates across the network;
- orders results newest first;
- allows pageSize from 1 to 100;
- uses nextCursor for subsequent pages;
- describes update metadata including contracts created, exercised and archived, involved parties, payload size, and root-event effects;
- requires an API key.

This may support a public activity sample, but it does not establish the total number or value of private institutional transactions.

### Network analytics endpoints

Noves documents a separate Canton Analytics add-on for supply and price series, issuance versus traffic burn, network transfer volume, update statistics, public/private usage verdict aggregates, cumulative submitting-party aggregates, traffic purchases, burn series, burn by Featured App category, reward totals and ecosystem metrics.

The documentation states that Canton Analytics is available on top of a Canton Platform plan and that an API key without the add-on receives HTTP 403. It instructs users to contact Noves to enable the add-on.

Reference: https://docs.noves.fi/reference/canton-analytics

**Implication:** These network-wide analytics endpoints must be treated as unavailable for the baseline project unless access is explicitly granted or a public dashboard exposes the needed series in an exportable, reproducible form.

### Pricing and free access

Noves' published pricing page lists a free self-hosted Data App tier with 24-hour history, one party and one user; a Pro tier at USD 250/month; a Platform tier at USD 500/month, including Noves Cloud API access; and an Enterprise tier with custom terms.

Reference: https://noves.fi/pricing

The free self-hosted tier is not equivalent to unrestricted network-wide historical public analytics. It is a participant-side product and its coverage depends on the connected participant and the caller's permissions. The pricing page does not establish that the Canton Analytics add-on is included in the Platform tier.

**Implication:** Do not budget for Noves subscriptions or assume paid analytics access. The research must remain viable without them.

## 2. Alternative public sources

Potential public cross-checks:
- Noves public Canton Data dashboard: https://ccdata.noves.fi/
- CCView explorer: https://ccview.io/
- CantonScan: https://www.cantonscan.com/
- Official CIP repository: https://github.com/canton-foundation/cips

These sources can help identify public records, governance events and independently presented metrics. They are not automatically independent in data provenance. Before treating two dashboards as independent corroboration, inspect their indexing source, metric definitions, refresh cadence, and whether they reuse the same underlying provider.

## 3. What can be done without paid analytics

A no-paid-access research path is still possible, but narrower:
1. Build a documented architecture and observer-permission model from primary Canton protocol documentation.
2. Catalogue public metrics visible in public dashboards and explorers, capturing dated screenshots or exports where permitted.
3. Audit definitions and provenance; distinguish first-party protocol data, provider-derived data, and independently computed metrics.
4. Analyse public CIP proposals and governance chronology as documentary evidence.
5. Develop an ex-ante economic model of CIP-0129 using only parameters stated in the approved CIP. Mark all unspecified pricing and discount parameters as variables.
6. Use small, openly available public update samples only if an API key or a permitted public interface is available. Record the sample as a bounded observation, not a census.

## 4. Data feasibility matrix

| Variable / evidence | Publicly documented access | Paid dependency known? | Research use | Current status |
|---|---|---|---|---|
| Public network update feed | Noves /{chain}/updates | API key required; plan access not fully verified | Sample public activity and event metadata | Endpoint documented; live access untested |
| Party-specific public updates | Noves /{chain}/updates/{party} | API key required | Case studies of selected public parties | Endpoint documented; coverage party-specific |
| Network update statistics | Noves /{chain}/updates/stats | Canton Analytics add-on | Network-level activity series | Not assumed accessible |
| Public/private verdict aggregates | Noves Canton Analytics | Canton Analytics add-on | Compare public and private aggregate counts | Not assumed accessible |
| Network CC supply / burn / volume | Noves Canton Analytics and public dashboards | API add-on for API endpoint; dashboard access may differ | Tokenomics and network economics | Dashboard inspect/export capability unverified |
| Party balances / CC transfers / rewards | Noves party endpoints and explorers | API key required | Party-level public accounting | Endpoint documented; actual plan limits untested |
| Private asset transfers and contract activity | Entitled parties/witnesses or participant-side data app | Requires permissioned participant access | Institutional workflow evidence | Not available as general public dataset |
| CIP status and proposal parameters | Official CIPs and governance records | No paid data dependency identified | Mechanism-design and policy chronology | Public documentary source |

## 5. CIP-0129 timing correction

CIP-0129 is approved, but its text describes a staged and estimated rollout:
- Phase 1: universal burn, estimated Q1 2027, with interim discounts voted case by case.
- Phase 2: volume pricing and commitment discounts, estimated Q3 2027, subject to a second CIP.

The document calls these ambitious estimates, not deadlines. Therefore November 2026 research can analyse the approved mechanism ex ante, but cannot claim to measure realised effects of universal burn. A later causal evaluation would require a verified go-live date, a sufficiently long post-implementation period, relevant pre-period data, and controls for concurrent changes.

Primary source: https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md

## 6. Grant programme terms and eligibility: unresolved

The official launch announcement says formal Terms and Conditions were expected on or before 15 November 2026. The announcement says those terms govern eligibility, KYC, sanctions screening, disclosure requirements, and grant payment. It also says no grant will be made before the terms are published.

Searches of the official announcement and indexed official pages in this audit did not locate a separate Terms and Conditions document. This is not proof that no such document exists; it means the terms have not been independently verified here.

Official announcement: https://canton.foundation/introducing-the-canton-community-research-grants/

Before relying on the programme, obtain and read the current official terms or request the document from the Foundation. Specifically verify eligible countries and applicant types; age and legal-capacity requirements; KYC and sanctions screening process; grant agreement and rights/licensing obligations; disclosure requirements; payment mechanics and wallet requirements; tax responsibilities; whether November work remains eligible if submitted/shared after the month ends; and whether a particular submission channel is required.

Do not infer that a Nigerian applicant is eligible or ineligible without the terms.

## 7. Recommended research-design constraint

The research should be designed in two layers:

**Layer 1: fully executable without paid access**
- architecture and observer-capability model;
- public-source metric inventory;
- CIP/governance chronology;
- mechanism-design model using published parameters and explicit variables;
- reproducibility and evidence limitations.

**Layer 2: empirical extension only if access is confirmed**
- public API extraction;
- historical network series;
- public/private aggregate analysis;
- cross-source metric validation.

The paper must remain substantive if Layer 2 is unavailable. No essential claim should depend on purchasing a subscription or receiving privileged institutional data.

## 8. Decision

Do not yet commit to a network-wide quantitative study of Canton activity or private/public usage. The available documentation shows that the most attractive aggregate endpoints are behind a paid add-on. First inspect what can be exported from public dashboards and what public API access can be obtained without cost. If that fails, centre the empirical contribution on public documentary data and a transparent mechanism model, not invented network-wide measurements.