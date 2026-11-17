# CCView October 2026 Report Audit and CIP-0129 Parameter Register

**Audit date:** 17 November 2026  
**Status:** Desk audit of the published report, its stated methodology, the CCView API landing page, and the approved CIP. No API key, paid subscription, raw endpoint response, or independent ledger export was used.

## 1. CCView October report: what is usable

CCView's October report is publicly accessible without registration and states that its figures derive from public Canton Network data observed by CCView. Its methodology section maps the displayed metrics to named API endpoints. This makes the report a potentially useful public source for a reproducible documentary analysis, but it is not itself a raw-data release.

Report: https://ccview.io/reports/canton-october-stats-2026/

### Metric definitions disclosed by CCView

| Report metric | Endpoint / definition disclosed | What it supports | Main limitation |
|---|---|---|---|
| Transactions | `GET /verdicts/stats`; committed updates observed on Global Synchronizer, deduplicated by update ID, bucketed by record time UTC | A count of observed committed updates in the stated scope | Excludes private updates whose payload is not delivered to CCView; envelope-only observations are counted; not total Canton transactions |
| Active parties | `GET /parties/active/stats`; distinct party IDs appearing as sender or receiver in at least one observed update during period | Observed party-ID activity under CCView's definition | Party IDs are not equivalent to legal entities, customers, institutions or beneficial owners; same-key parties count separately |
| Traffic purchased | `GET /traffic/purchases`; traffic purchase contracts in CC, converted to USD using daily volume-weighted CC/USD reference rate | Publicly observed traffic purchases and their CC/USD representation | USD value moves with exchange-rate reference; not financial settlement value and not necessarily all synchronizer traffic |
| Net CC issuance | `GET /network/supply/pressure`; mint from reward coupon redemption less burn from traffic purchase and fee destruction, aggregated monthly | CC mint/burn accounting under endpoint definition | Must reconcile with report headline and detailed section; not a complete economic-value measure |
| Reward split | `GET /rewards/stats`; coupons redeemed per round, classified by issuing contract | Reward distributions by defined class | Coupon redemption is not equivalent to recipient net profit or economic value created |
| SV locking / compliance | `GET /validators`; locked CC from locking contracts at final round of month; uptime measured from round participation | Contract-based locked CC and protocol-round participation | Round participation is not node telemetry or end-to-end service quality |
| Featured Apps | `GET /featured-apps/leaderboard`; governance grants and proposal-state transitions | Recorded featured-app status and app reward ranking | Classification depends on governance records and endpoint methodology |
| Governance | `GET /governance`; proposals, vote receipts and implementation rounds recorded on governance ledger | Documented proposal/vote/implementation history | Must distinguish proposal, vote, approval and actual implementation |

## 2. Internal consistency issues requiring resolution

The report contains figures that do not reconcile on the face of the published text. These are not necessarily data errors; they may reflect revisions, different aggregation windows, rounding, or extraction/rendering problems. Until the underlying API response or a correction is obtained, they must be treated as unresolved.

| Item | Executive summary | Detailed section / spotlight | Why it matters |
|---|---|---|---|
| October transactions | 35.0M, down 0.7% month-on-month | Spotlight says monthly total dropped 23% and describes October as below one million daily throughout | The direction/magnitude of monthly change is inconsistent unless the measures or comparison windows differ; definitions are not supplied to reconcile this |
| October mint | 645.8M CC | 664.8M CC | 19.0M CC difference |
| October burn | 442.6M CC | 448.5M CC | 5.9M CC difference |
| Net issuance | Summary implies 645.8 - 442.6 = 203.2M CC | Detailed section reports +216.36M CC | Detailed figure matches 664.8 - 448.5 = 216.3M CC, subject to rounding; summary's components imply 203.2M CC |
| Burn ratio | 68.5% (from 71.1%) | 67.5% (down from 68.5% in September) | Both ratios correspond to different component pairs; one cannot be selected without clarification |

**Required action:** request or retrieve the raw October endpoint responses, report data snapshot/version, and any correction notes. Preserve the originally published figures and record subsequent revisions rather than silently replacing values.

## 3. Source independence and conflicts

CCView's report states that PixelPlex operates a Canton validator and submits Featured App applications. It also states that CCView receives no compensation from entities named in the report.

This disclosure does not invalidate the report. It does mean the source has ecosystem participation and potential commercial interests relevant to interpretation. Treat it as a named provider's public-data index and analysis, not as a fully independent audit. Where possible, corroborate governance facts against the official CIP/governance ledger and reconcile token figures against a second provider or directly accessible public contracts.

CCView's API landing page markets broader full-lifetime indexing and shows paid plans beginning at USD 90/month, with higher tiers for aggregate analytics and bulk access. The monthly report is free to read; the API should not be described as free. Pricing and coverage should be rechecked before publication.

API / pricing: https://api.ccview.io/

## 4. CIP-0129 parameter register

Approved CIP: https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md

The distinction below is essential: the approved CIP establishes a framework and some current values. It explicitly defers the detailed volume curve, discount sizes, collateral levels and calculation rules to a second CIP. The accompanying discussion deck's numerical examples are not approved parameters.

| Parameter / rule | Value or status | Evidence class | Treatment in model |
|---|---|---|---|
| CIP status | Approved 23 October 2026 | APPROVED | Framework is approved; implementation status tracked separately |
| Scope of universal burn | Every MainNet synchronizer carrying production workloads, Global and dedicated | APPROVED | Model all eligible production traffic in principle; do not assume rollout has occurred |
| List price | Global Synchronizer list price; currently USD 60/MB, set by SVs under CIP-0084 | APPROVED CURRENT VALUE | Baseline gross price input; time-stamp and sensitivity-test because governance can change it |
| Typical transaction illustration | Approximately USD 1 before rewards at stated list price | APPROVED CIP STATEMENT / ILLUSTRATIVE | Cite as CIP's approximate illustration, not a universal per-transaction fee |
| CC burn conversion | Traffic price paid by burning CC | APPROVED MECHANISM | Need governing conversion-price methodology and timestamp to calculate CC quantity; do not invent X |
| App and validator rewards | Apps and validators earn rewards for traffic on all synchronizers under same reward rules | APPROVED | Model rewards separately from gross burn; exact formulas from governing reward CIPs |
| Reward split | Split between SVs, validators, apps and Development Fund unchanged by CIP-0129; refer to CIP-0082 | APPROVED RULE | Do not assign shares without retrieving current CIP-0082 formula |
| Dedicated synchronizer reporting | Operator publishes aggregate traffic reports on Global Synchronizer with party attribution required by reward rules, because SVs cannot see traffic on synchronizers they do not operate | APPROVED REQUIREMENT | Research transparency and verification implications; inspect implementation once live |
| Commitment | Optional, permissionless, on-chain and binding | APPROVED FRAMEWORK | Include commitment obligation and shortfall exposure in conceptual model |
| Collateral shortfall | Shortfall can be paid from collateral and credited back as traffic; collateral not topped up when required can be forfeited | APPROVED FRAMEWORK | Model expected shortfall loss only when exact rules and probabilities are sourced |
| Volume curve | Deferred to second CIP | UNKNOWN / DEFERRED | Symbolic function only |
| Discount sizes | Deferred to second CIP | UNKNOWN / DEFERRED | No actual discount percentage in baseline model |
| Collateral levels and valuation | Deferred to second CIP | UNKNOWN / DEFERRED | Symbolic variables only |
| Commitment duration / notice / margin call mechanics | Detailed rules deferred to second CIP | UNKNOWN / DEFERRED | Do not assign numerical values |
| Discount combination method | Deferred to second CIP | UNKNOWN / DEFERRED | Multiplicative formula is only an analytical convention; test alternatives |
| Interim discounts | Dedicated synchronizer may request a discount, decided case-by-case by SV vote until full curve goes live | APPROVED FRAMEWORK | Treat actual discounts as case-specific and only include if documentary evidence exists |
| Phase 1 rollout | Estimated Q1 2027 | APPROVED ESTIMATE, NOT DEADLINE | No November 2026 implementation or impact claim |
| Phase 2 rollout | Estimated Q3 2027 after second CIP | APPROVED ESTIMATE, NOT DEADLINE | No actual volume-curve impact claim before verified go-live |

## 5. Discussion-deck numbers: illustrative, not approved

A separately hosted Universal Burn discussion deck gives possible parameter values and worked examples. The approved CIP explicitly says the appendix's illustrative numbers are not part of what the SVs approved. They may be used only as labelled sensitivity scenarios, never as live policy parameters.

Source: https://dach-ny.github.io/universal-burn-cip/

| Illustrative deck parameter | Example value | Status |
|---|---:|---|
| Volume discount | 50% per 10x of sustained throughput | Illustrative only |
| Sustained throughput | Highest of 7-, 30- and 90-day averages and commitment | Illustrative only |
| Minimum collateral | 20% of committed annual spend | Illustrative only |
| Commitment discount | 50% at minimum collateral, then another 25% off per doubling | Illustrative only |
| Maximum collateral | 100% of a year's committed spend | Illustrative only |
| Loyalty discount | 15% per year, capped at 60% after four years | Illustrative only |
| Collateral band | 75%–125% of requirement, marked to market daily | Illustrative only |
| Margin-call top-up period | 7 days | Illustrative only |
| Notice period | 12 months | Illustrative only |

Do not combine these illustrative values into a single assumed policy case without making the scenario label prominent. The second CIP may alter or discard them.

## 6. Baseline arithmetic that can be reproduced now

Only the list price and approximate transaction size stated by the proposal are used here. This is arithmetic, not a forecast or estimate of any participant's actual bill.

Let `q` be traffic in MB and `p = USD 60/MB` be the current stated list price:

`Gross fee (USD) = 60 * q`

If the typical transaction is approximately USD 1 before rewards, that is the CIP's own rough illustration. It must not be used to infer every transaction has identical payload size.

To illustrate scale independently of the CIP's typical-transaction statement, a workload at `n` transactions per second and average payload `s` bytes would have approximate daily traffic:

`Daily MB = n * 86,400 * s / 1,000,000`

`Daily gross fee = 60 * Daily MB`

This formula uses decimal MB (1 MB = 1,000,000 bytes) and assumes every byte counted is billable traffic under the protocol's eventual traffic-accounting rules. That assumption must be checked before any real workload estimate is published. It excludes rewards, discounts, collateral costs, hosting and operational costs.

## 7. Model design changes required

1. Replace the prior generic discount model as a base-case policy formula with a **symbolic deferred-parameter model**. Keep multiplicative/additive alternatives as sensitivity structures only.
2. Split gross CC burn, rewards returned, and net economic cost. Do not call gross burn the participant's net cost.
3. Model Global Synchronizer and dedicated synchronizer cases separately. Dedicated synchronizer volume discounts are proposed for the latter; do not apply them to all traffic.
4. Include the reporting requirement for dedicated synchronizers as a governance/measurement mechanism, and assess whether the aggregate reports are independently verifiable.
5. Add CC price conversion as a time-varying external input, with source, timestamp and price convention. Do not hard-code a spot price.
6. For CCView metrics, keep `observed public committed updates`, `active party IDs`, `traffic purchased`, `CC mint`, `CC burn`, and `rewards redeemed` as separate series. Do not collapse them into a single activity measure.
7. Add a report-quality flag for unreconciled source discrepancies; do not use affected October fields in model calibration until clarified.

## 8. Grant programme terms status

The official announcement says formal Terms and Conditions were expected by 15 November 2026 and that no grant will be made before they are published. The announcement page reviewed for this audit still describes the terms as expected and does not itself link to a current terms document.

Official announcement: https://canton.foundation/introducing-the-canton-community-research-grants/

Eligibility, KYC/sanctions, payment, licensing, disclosure and grant-agreement terms therefore remain unverified. This audit does not establish eligibility for any particular applicant.

## 9. Next steps

1. Obtain CCView's raw October values or API response for each endpoint, and request an explanation of the conflicting transaction and token-economics figures.
2. Retrieve CIP-0082 and CIP-0084 to formalise reward allocation and list-price governance.
3. Watch for the second CIP and replace deferred variables only after approval.
4. Obtain the formal Canton Research Grants Terms and Conditions directly from the Foundation or its official publication channel.
5. After these checks, implement a small spreadsheet or script that calculates gross fee scenarios and collateral opportunity-cost sensitivity without treating illustrative deck parameters as facts.