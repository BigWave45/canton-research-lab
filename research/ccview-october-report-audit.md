# CCView October 2026 Report: Source and Consistency Audit

**Audit date:** 17 November 2026  
**Source:** CCView Research, *Canton Network October 2026 Report*, published 2 November 2026, data through 31 October 2026.  
**URL:** https://ccview.io/reports/canton-october-stats-2026/  
**Status:** Desk audit of the report text and its disclosed methodology. The underlying API responses and downloadable PDF have not yet been independently retrieved or reproduced.

## 1. Why this source is useful

The report is unusually valuable for a no-paid-access research path because it is public, requires no registration to read, and discloses endpoint names and definitions for its headline measures. It reports monthly activity, active parties, traffic purchases, Canton Coin issuance and burn, reward distribution, validator participation, featured applications and governance.

Its methodology is more useful than the headline figures alone. It states, for example, that its transaction series counts committed updates observed on the Global Synchronizer, deduplicates by update ID and buckets by record time in UTC. It also says private updates whose payload is not delivered to CCView are excluded, while envelope-only observations are counted but not amount-weighted.

That definition is a bounded public observation series. It is not a complete network transaction census, and it does not establish institutional settlement value.

## 2. Internal consistency issues requiring resolution

The report contains several material discrepancies between its executive summary and detailed sections.

| Measure | Executive summary | Detailed section / spotlight | Audit finding |
|---|---|---|---|
| October transactions / monthly change | 35.0M, down 0.7% | Spotlight says monthly total fell 23% | These cannot both describe the same October-versus-September transaction series. Requires correction or clarification of the comparison window / metric. |
| CC mint, burn and net issuance | Mint 645.8M; burn 442.6M; net issuance 203.2M; burn ratio 68.5% | Detailed economics section: mint 664.8M; burn 448.5M; net issuance 216.36M; burn ratio 67.5% | Each set is approximately internally consistent, but the two sets conflict materially. |
| Burn ratio comparison | 68.5%, down from 71.1% | Detailed section says 67.5%, down from 68.5% in September | The reported October burn ratio and September comparator conflict. |
| New Featured Apps | 10 | Featured Apps section says 12 granted status, 10 live on mainnet | Could be a label/definition issue (granted versus live), but executive-summary wording is ambiguous and should be clarified. |

### Arithmetic checks

- Executive-summary issuance: 645.8M - 442.6M = 203.2M CC (arithmetically consistent).
- Executive-summary burn ratio: 442.6 / 645.8 ≈ 68.5% (arithmetically consistent).
- Detailed issuance: 664.8M - 448.5M = 216.3M CC, close to the stated 216.36M after rounding/source precision.
- Detailed burn ratio: 448.5 / 664.8 ≈ 67.5% (arithmetically consistent).

The issue is not simple arithmetic inside either block. It is the disagreement between the blocks and the incompatible month-over-month transaction changes.

## 3. What the methodology does and does not establish

### Transactions

The report defines transactions as committed updates observed on the Global Synchronizer, deduplicated by update ID and bucketed by record time (UTC). It explicitly excludes private updates whose payload is not delivered to CCView and counts envelope-only observations without amount-weighting.

Permitted interpretation: a provider-defined count of committed updates observed under the report's stated Global Synchronizer indexing coverage.

Not permitted without additional evidence:
- total Canton-wide transaction count;
- total private or dedicated-synchronizer activity;
- total institutional settlement count;
- transaction value or financial notional;
- end-to-end settlement latency.

The report's use of the word “transactions” should be quoted with its operational definition whenever used in research.

### Active parties

The report defines active parties as distinct party IDs appearing as sender or receiver in at least one observed update during the period. It says parties sharing a private key are counted separately.

Permitted interpretation: distinct party IDs appearing in the provider's observed update set.

Not permitted: distinct institutions, customers, beneficial owners or independent economic entities. A single institution may operate multiple parties, and party IDs are not necessarily independent users.

### Traffic purchased

The report says CC traffic purchases are converted to USD at the daily volume-weighted CC/USD reference rate. It states CC figures are exact and USD figures move with the reference rate.

This is a traffic-purchase measure, not an all-in institutional operating cost. It does not include all possible infrastructure, licensing, financing, staffing or integration costs.

### Net CC issuance and burn

The report defines net issuance as reward coupon minting minus burn from traffic purchase and fee destruction, per round and aggregated monthly.

This is a source-defined token-flow accounting metric. It is not a direct measure of network utility, demand, institutional adoption or economic value created.

### Rewards

The report counts coupons redeemed per round and classifies them by issuing contract as SV, validator or Featured App rewards.

Reward receipts are not equivalent to revenue, profit, user demand or value added. The report's app-level concentration measure is potentially useful, but should be reproduced from raw reward records before strong conclusions are drawn.

### Validator compliance

The report says uptime is measured from round participation, not node telemetry. Therefore its uptime measure should not be described as conventional infrastructure uptime without qualification.

## 4. Potentially useful research signal: reward concentration

The report states that its ten largest Featured Apps received 91.7% of all app rewards in October. The displayed shares add to 91.8%, a small difference plausibly attributable to rounding, but still worth reproducing.

The top app, Temple, is reported at 43.9% of the app reward pool. This suggests a potentially high concentration of the reported reward distribution. However:
- the report's reward totals and shares need raw-data reproduction;
- the full distribution across all 100 Featured Apps is required for a valid HHI or Gini estimate;
- reward concentration is not the same as market concentration, user concentration or economic value concentration;
- rewards may reflect programme rules and eligibility, not only market demand.

A defensible first statistic is the sum of squared published top-ten shares as a partial HHI contribution, with the remaining 90 apps explicitly unobserved in that calculation. Do not call it the full HHI.

## 5. Provenance and independence

The report states that every figure maps to a public endpoint on api.ccview.io and identifies the endpoint for each metric. This is useful provenance disclosure, but the audit has not yet:
- retrieved the raw API responses;
- inspected endpoint schemas and query parameters;
- verified whether the monthly PDF and website use the same calculation pipeline;
- compared CCView figures with a genuinely independent indexer;
- reproduced any reported total.

The report also discloses that PixelPlex operates a Canton validator and submits Featured App applications. It says CCView receives no compensation from named entities. The disclosed ecosystem involvement does not invalidate the data, but it should be recorded as a potential conflict-of-interest context and the methodology independently tested.

## 6. Questions to send CCView before relying on the report

1. Which October transaction change is correct: -0.7% or -23%? Are the figures based on the same endpoint, date window and definition?
2. Which October mint/burn values are correct: 645.8M/442.6M or 664.8M/448.5M?
3. Which October burn ratio and September comparator are correct?
4. Does “10 new Featured Apps” mean ten live on MainNet while twelve were approved/granted status?
5. Can CCView provide the exact report snapshot, API query parameters, schema version and calculation code for the affected metrics?
6. Can historical endpoint responses be downloaded and independently reproduced?
7. How does CCView classify updates when it sees an envelope but not the payload, and how are those events deduplicated?
8. What is the precise meaning of “private update” in the report's methodology, and what coverage does it have for dedicated synchronizers?

## 7. Research-design consequences

1. Do not use the October report as a clean source of October-versus-September time-series values until the discrepancies are resolved.
2. Do not average conflicting numbers or select whichever value supports a preferred argument.
3. Retain the report as a source-audit case study. Its disclosed metric definitions are valuable, and the inconsistencies themselves demonstrate why metric provenance and reproducibility matter.
4. If CCView supplies raw data and corrections, reproduce the affected metrics and record the correction history.
5. If the discrepancies remain unresolved, either exclude the affected variables from quantitative inference or present them as unresolved provider-reported values.
6. Keep all claims within the report's disclosed Global Synchronizer/public-observation coverage.

## 8. Source

CCView Research, *Canton Network October 2026 Report*, published 2 November 2026, data through 31 October 2026: https://ccview.io/reports/canton-october-stats-2026/

CCView API Quick Start: https://docs.ccview.io/reference/quick-start

Canton privacy and protocol architecture: https://www.canton.network/protocol
