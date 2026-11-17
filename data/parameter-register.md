# Canton Synchronizer Economics: Parameter Register

**Version:** 0.1  
**As-of date:** 17 November 2026  
**Purpose:** Separate approved governance rules, observed values, external inputs, scenario assumptions and unknown implementation details before quantitative modelling.

## Status labels

- **APPROVED:** stated in an approved governing proposal. This does not necessarily mean implemented.
- **OBSERVED:** measured from a named dataset or source snapshot.
- **EXTERNAL:** sourced from a market or institutional source outside the Canton protocol.
- **ASSUMED:** selected only to explore a scenario.
- **UNKNOWN:** not specified, not verified, or not available.
- **CONFLICTED:** public sources or sections disagree; do not use as a single point estimate.

## 1. CIP-0129 mechanism parameters

| Parameter | Symbol | Value / current state | Status | Source / interpretation |
|---|---|---|---|---|
| CIP status | — | Approved 23 Oct 2026 | APPROVED | CIP-0129 header |
| Universal-burn scope | — | Every MainNet synchronizer running production workloads | APPROVED framework | CIP-0129 §1; implementation not yet verified |
| Current Global Synchronizer list price | p | USD 60 per MB | APPROVED / time-sensitive | CIP-0129 §1.2 says current price; governance can change it |
| Price-setting governance | — | Super Validators via CIP-0084 process | APPROVED | CIP-0129 §1.2 and §5 |
| Dedicated synchronizer permission | — | Permissionless deployment and validator connection | APPROVED framework | CIP-0129 §1.3; operational implementation not verified |
| Reward eligibility | — | Apps and validators earn rewards for dedicated-synchronizer traffic under the same reward rules | APPROVED framework | CIP-0129 §2.1 |
| Reward weight basis | W | CC actually burned after discounts | APPROVED framework | CIP-0129 §2.4 |
| Dedicated synchronizer traffic attribution | — | Operator publishes aggregate traffic reports on Global Synchronizer, attributed per party | APPROVED framework | CIP-0129 §2.2 |
| Initial reporting trust assumption | — | Reports rely on operator honesty at launch; malicious reports can misdirect party rewards but cannot claim rewards on more traffic than paid | APPROVED risk statement | CIP-0129 §2.3 |
| Global Synchronizer volume pricing | — | Single price at every volume | APPROVED framework | CIP-0129 §3.1 |
| Dedicated synchronizer volume curve | d_v(q) | Price per MB decreases with sustained throughput | APPROVED direction only | CIP-0129 §3.2; functional form and thresholds deferred |
| Commitment duration | T | One year or more | APPROVED framework | CIP-0129 §4.1 |
| Commitment collateral | K | CC collateral required; minimum requirement exists | APPROVED direction only | CIP-0129 §4.1 and §4.2; minimum amount unknown |
| Commitment discount | d_commit | Discount for committing with minimum collateral | APPROVED direction only | CIP-0129 §4.2; size unknown |
| Additional collateral discount | d_collateral | Larger discount for more collateral, up to a maximum | APPROVED direction only | CIP-0129 §4.2; curve and cap unknown |
| Loyalty discount | d_loyalty | Further discount for each year commitment and collateral remain | APPROVED direction only | CIP-0129 §4.2; rate and cap unknown |
| Shortfall treatment | S | Commitment shortfalls paid from collateral and credited back as traffic | APPROVED framework | CIP-0129 §4.4; operational formula and timing unknown |
| Collateral top-up / forfeiture | — | Collateral not topped up when required can be forfeited; remainder returned at end | APPROVED framework | CIP-0129 §4.4; triggers and notice rules deferred |
| Governance threshold | — | 2/3 SV vote for parameter changes | APPROVED | CIP-0129 §5 |
| Interim discount mechanism | — | Case-by-case SV vote until later pricing curve is approved | APPROVED framework | CIP-0129 §6 |
| Phase 1 timing | — | Q1 2027 estimate | APPROVED estimate, not deadline | CIP-0129 §8 |
| Phase 2 timing | — | Q3 2027 estimate | APPROVED estimate, not deadline | CIP-0129 §8 |
| Discount formula | f(d_v,d_commit,d_collateral,d_loyalty) | Not specified in approved CIP | UNKNOWN | Second CIP required |
| Throughput measurement window | — | Sustained throughput; exact window and averaging method deferred | UNKNOWN | Second CIP required |
| Collateral valuation / haircut | — | Deferred | UNKNOWN | Second CIP required |
| Margin call / top-up thresholds | — | Deferred | UNKNOWN | Second CIP required |
| Shortfall valuation and settlement timing | — | Deferred | UNKNOWN | Second CIP required |
| Parameter changes applied to existing commitments | — | Deferred | UNKNOWN | Second CIP required |
| Multi-synchronizer commitments | — | Deferred | UNKNOWN | Second CIP required |
| Existing dedicated synchronizer license transition | — | Digital Asset handles transition with each existing customer | APPROVED statement; contract terms private/unknown | CIP-0129 backwards-compatibility section |
| Actual implementation / go-live | — | Not verified in this research snapshot | UNKNOWN | Approval is not deployment evidence |

## 2. Publicly observable inputs and data quality

| Input | Symbol | Value / state | Status | Qualification |
|---|---|---|---|---|
| CC/USD conversion price | X_t | Round-specific / time-varying | OBSERVED in principle | CCView docs say mining-round stream exposes CC price and fee schedule; historical access and provenance need verification |
| Eligible traffic volume | q_t | MB per synchronizer and period | UNKNOWN for full network | Requires traffic purchase records; public report does not expose all synchronizer traffic |
| Public Global Synchronizer updates | U_t | CCView report gives 35.0M for Oct 2026, but monthly change conflicts | CONFLICTED | CCView October report executive summary says -0.7%; spotlight says -23%; do not use until corrected |
| October CC mint | M_t | 645.8M in summary; 664.8M detailed | CONFLICTED | CCView October report internal discrepancy |
| October CC burn | B_t | 442.6M in summary; 448.5M detailed | CONFLICTED | CCView October report internal discrepancy |
| October net issuance | N_t | 203.2M summary; 216.36M detailed | CONFLICTED | Both blocks arithmetically consistent internally but disagree |
| October burn ratio | b_t | 68.5% summary; 67.5% detailed | CONFLICTED | Do not select either without clarification |
| Active party IDs | A_t | 456,173 reported | OBSERVED by provider definition only | Distinct sender/receiver party IDs in observed updates; not institutions or users |
| Traffic purchased | TP_t | USD 48.8M reported | OBSERVED by provider definition only | CC traffic purchases converted using daily VWAP reference rate; not all-in network cost |
| Featured App reward concentration | CR_t | Top ten reported at 91.7%; displayed shares sum to 91.8% | CONFLICTED / rounded | Candidate for raw-data reproduction; not market-share measure |
| CC reward coupons | R_t | Endpoint described by CCView | OBSERVED in principle | Need raw endpoint response and exact scope |
| Historical CC price series | X_t | Endpoint / mining-round stream described | OBSERVED in principle | Need exportability, API key and history limits checked |

## 3. External economic inputs

These are not Canton protocol parameters. They must be sourced separately and timestamped if used.

| Input | Symbol | Role in model | Status |
|---|---|---|---|
| Annual cost of capital / financing rate | r | Opportunity cost of CC collateral | UNKNOWN until a defensible proxy is chosen |
| Alternative collateral yield | y_K | Return foregone or earned while collateral is locked | UNKNOWN |
| USD/CC price volatility | sigma_X | Sensitivity of USD-denominated fee / CC collateral value | UNKNOWN until a source and window are selected |
| Existing dedicated synchronizer license/service cost | L_old | Baseline for comparing pre- and post-change economics | UNKNOWN; may be contract-specific/private |
| Operator integration and operating cost | O | Non-protocol cost in total-cost comparison | UNKNOWN |
| Workload traffic distribution | F(q) | Determines average fee and volume tier exposure | UNKNOWN; requires workload data or clearly hypothetical scenarios |

## 4. Core equations and model boundaries

### List-price fee

For eligible traffic q measured in MB:

Fee_USD = p * q

With p = USD 60/MB in the CIP snapshot, 1 MB has a gross list-price fee of USD 60 before rewards or discounts. The CIP's “about USD 1 per typical transaction” is an illustrative average, not a per-transaction tariff.

### CC burn conversion

If X_t is the USD price per CC used by the relevant round or fee calculation:

Burn_CC = Fee_USD / X_t

Use the actual protocol conversion rule and source field when available. Do not substitute a generic daily spot price if the fee mechanism uses a round-specific price.

### Discounted fee

The approved CIP establishes three additional discount classes on top of volume pricing, but does not specify the formula. Therefore the model should use a generic effective-price function:

p_eff = p * g(q, commitment, collateral, loyalty)

with 0 <= p_eff <= p for a discount-only model.

A multiplicative expression can be used as one sensitivity case, but must be labelled ASSUMED, not an approved formula. An additive or tiered alternative should be tested when the second CIP defines the actual rule.

Fee_USD = q * p_eff

### Commitment shortfall

Let Q_c be the committed throughput quantity over the contractual measurement period and Q_a the actual eligible quantity. The shortfall is:

S = max(0, Q_c - Q_a)

The CIP says shortfalls are paid from collateral and credited back as traffic. The conversion from S to collateral debit, the price used, timing, margin-call threshold and top-up process are deferred. Therefore define:

CollateralDebit = h(S, parameters_not_yet_published)

Do not assign a numeric h() until the second CIP specifies it. Collateral can be forfeited if required top-ups are not made; this tail risk must be modelled separately from routine traffic fees.

### Collateral opportunity cost

For collateral amount K, annual financing/opportunity-cost rate r and duration T:

CollateralCarryCost = K * r * T

This is an external economic cost estimate, not a protocol fee. If collateral earns yield, use net carry cost K * (r - y_K) * T, with both rates and assumptions disclosed.

### Reward attribution and integrity risk

Let total reward-eligible burned CC be B_eligible and party i's reported attributed burned CC be b_i. Reward allocation is weighted by CC actually burned after discounts. The operator's aggregate report is an input to party-level attribution on dedicated synchronizers.

The research should test the accounting invariant:

sum_i b_i <= B_eligible

The CIP states that a malicious report may misdirect rewards between participants but cannot claim rewards on more traffic than the synchronizer or users paid for. The precise on-chain enforcement and report-validation procedure must be inspected before treating this inequality as technically enforced rather than a stated design constraint.

## 5. Parameters explicitly excluded from baseline estimation

Do not estimate these as facts from the public October report:
- total Canton-wide transaction count;
- total institutional settlement volume;
- private asset transfer notional;
- total dedicated synchronizer traffic;
- total network cost to institutions;
- realised savings from universal burn;
- actual volume-discount schedule;
- actual collateral discount schedule;
- actual loyalty discount schedule;
- post-CIP-0129 behavioural response before implementation.

## 6. Immediate modelling plan

1. Use the USD 60/MB list price as a dated CIP parameter, not an immutable constant.
2. Keep CC/USD price as a time-indexed input.
3. Treat all dedicated-synchronizer discount parameters as unknown until the second CIP.
4. Model a family of hypothetical volume and commitment scenarios, clearly marked as assumptions.
5. Include collateral carrying cost and commitment shortfall exposure.
6. Add a separate reward-attribution integrity module, since the approved CIP explicitly relies on operator reports for party-level attribution on dedicated synchronizers.
7. Do not calibrate the model to CCView's conflicting October values.
8. Reconcile reward split mechanics against CIP-0082, its implementation, and the current mining-round schedule before using fixed percentages.

## 7. Primary sources

- CIP-0129, Universal Burn and Synchronizer Pricing: https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md
- CIP-0082, Establish a 5% Development Fund: https://github.com/canton-foundation/cips/blob/main/cip-0082/cip-0082.md
- CCView October 2026 Report: https://ccview.io/reports/canton-october-stats-2026/
- CCView API Quick Start: https://docs.ccview.io/reference/quick-start
- Canton Coin whitepaper: https://www.canton.network/hubfs/Canton%20Network%20Files/whitepapers/The%20Case%20for%20Canton.pdf
