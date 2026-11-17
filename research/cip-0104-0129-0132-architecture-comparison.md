# Architecture Comparison: CIP-0104, CIP-0129 and CIP-0132

**Audit date:** 17 November 2026  
**Purpose:** Locate the dedicated-synchronizer reward problem in the sequence of approved and proposed CIPs.  
**Status:** Desk review of public CIP text and the public Splice source snapshot at commit 408f7ed9e742707f0d6fe080ca386aedc742d977.

## 1. Key correction

The initial reward-attribution hypothesis was too broad. It treated CIP-0129's eventual per-party reporting requirement as though it were the mechanism already being implemented in the first phase.

The sequence is more specific:

- **CIP-0104 (approved 27 October 2026)** defines traffic-based application rewards on the Global Synchronizer using sequencer and mediator data. It also defines an extension hook for recording activity not directly visible to those systems, explicitly anticipating dedicated synchronizer integration.
- **CIP-0129 (approved 23 October 2026)** establishes the universal-burn framework. It says dedicated synchronizer operators will publish aggregate traffic reports on the Global Synchronizer, attributed per party as reward rules require. It acknowledges that launch reports rely on operator honesty and may misdirect rewards between participants, while limiting reward claims to traffic paid for.
- **CIP-0132 (proposed 16 November 2026)** specifies a Phase 1 dedicated-synchronizer paymaster model. It does not begin with granular per-party reward distribution. A trusted operator reports total synchronizer traffic; a designated paymaster burns CC on the Global Synchronizer; the paymaster receives the corresponding app and validator rewards. More granular attribution is deferred to later phases.

Therefore the first-phase problem is not an already-live per-party reward misallocation system. It is the design and economics of a trusted measurement-to-burn-to-reward pipeline, and the transition from aggregate paymaster attribution to later granular attribution.

## 2. CIP-0104: existing Global Synchronizer reward measurement

CIP-0104's objective is to base application rewards on actual traffic spent on transactions that change state managed by an app. It uses sequencer and mediator data.

The public Splice implementation inspected contains AppActivityComputation in:

apps/scan/src/main/scala/org/lfdecentralizedtrust/splice/scan/rewards/AppActivityComputation.scala

The code:
- processes accepted verdicts with associated traffic summaries;
- skips SV-submitted transactions because they do not burn traffic;
- reads transaction views and confirming parties;
- uses Featured App rights and operational-party mappings as of the relevant round opening;
- for user-submitted transactions, allocates traffic-weighted app activity among Featured App confirmers using per-envelope traffic cost;
- for Featured-App-submitted transactions, attributes total burn to the submitting app, with additional asset activity rules for featured asset-moving apps;
- uses deterministic integer arithmetic and a 100 MB transaction traffic-cost ceiling to avoid overflow.

This is an implemented Global Synchronizer measurement path, not a public census of private synchronizer activity.

CIP-0104 also introduces the ActivityRecorder_DsoRecordActivity extension hook for activity not directly visible to the mediator and sequencer. It explicitly anticipates dedicated synchronizer integration using this hook.

## 3. CIP-0129: framework and future granular attribution

CIP-0129 states:
- every MainNet production synchronizer should burn CC for traffic;
- dedicated synchronizers should use the Global Synchronizer list price as a baseline, with a future volume curve and commitment discounts;
- apps and validators should earn rewards for traffic on all synchronizers;
- the SVs cannot see traffic on synchronizers they do not operate;
- dedicated synchronizer operators will publish aggregate reports on the Global Synchronizer, attributed per party as reward rules require;
- initial reports rely on operator honesty and may misdirect rewards between participants;
- a future CIP may tighten enforcement.

CIP-0129 is a framework, not a complete implementation specification. Its reference implementation section says none exists at the time of the proposal. It leaves pricing and collateral parameters to a subsequent CIP.

## 4. CIP-0132: proposed Phase 1 paymaster model

CIP-0132 is marked Proposed, created 9 November 2026 and proposed 16 November 2026. It requires CIP-0104 and CIP-0129.

Its Phase 1 model is:

1. The dedicated synchronizer tracks total consumed traffic and exposes an operator-app API reporting bytes per 10-minute interval within the sequencer pruning window.
2. A designated paymaster periodically burns CC on the Global Synchronizer for that reported traffic. The report-to-burn link and any discount agreement are off-ledger. The paymaster is responsible for automation that consumes reports and performs burns.
3. The burn produces validator rewards and invokes CIP-0104's activity-recording extension hook. The resulting app/asset activity records are attributed to the paymaster party, which can receive featured app rewards if it has a Featured App right.

CIP-0132 says the dSync operator and paymaster are trusted to report traffic correctly and burn CC accordingly. It acknowledges that a malicious operator/paymaster could under- or over-report usage. Its stated on-chain protection is that rewards received are commensurate with CC burned. This does not independently prove that the burn matches actual traffic consumed.

CIP-0132 also says the paymaster receives all validator and app rewards for the dSync in this phase because it is the party burning CC. It expects more granular attribution in later states.

## 5. What is and is not enforced

| Property | Evidence in current proposal sequence | Interpretation |
|---|---|---|
| Global Synchronizer app activity is derived from sequencer/mediator traffic data | CIP-0104 and Splice implementation | Implemented measurement path for the Global Synchronizer |
| Dedicated synchronizer reports aggregate traffic in 10-minute buckets | CIP-0132 | Proposed Phase 1 API design; deployment not verified |
| CC burn is recorded on Global Synchronizer | Existing traffic-purchase/burn path; CIP-0132 extends it for registered dSyncs | Existing burn/accounting components exist; CIP-0132 extension remains proposed |
| Reward amount is constrained by CC actually burned | CIP-0104 reward accounting plus CIP-0132 description | Reward entitlement is tied to burn; inspect final implementation before calling it a formal enforcement guarantee |
| Reported traffic equals actual dSync traffic | CIP-0132 trust model | Not independently established by the proposal; operator/paymaster are trusted |
| Burned traffic equals actual dSync traffic after discounts | CIP-0132 trust model | Not independently established; discounting and report-to-burn relation are off-ledger |
| Individual participants receive rewards proportional to their actual dSync traffic | CIP-0132 | Explicitly deferred; Phase 1 rewards go to the paymaster |
| A public observer can verify private dSync transaction content | None | Not established and not assumed possible |

The distinction between reward commensurability and traffic-accounting correctness is central. A system may limit rewards to the amount burned while still relying on a trusted operator/paymaster to determine how much traffic should be burned.

## 6. More precise research problem

A defensible candidate question is:

**What economic and verification properties should a trusted paymaster model satisfy when converting private synchronizer traffic reports into public CC burns and reward entitlements, and how should those properties change as Canton moves toward granular, less-trusted attribution?**

Subquestions:
1. What evidence links a 10-minute aggregate traffic report to underlying sequencer records?
2. Can an independent auditor reconcile reported bytes, discount treatment, CC/USD conversion and actual burn?
3. What exactly is bounded by the on-ledger burn, and what remains dependent on off-ledger reporting?
4. Under what operator/paymaster incentives would under-reporting, over-reporting or delayed burning be rational?
5. Which verification properties can be exposed without revealing transaction payloads, counterparties or individual party activity?
6. What additional evidence or accountability mechanisms are needed before rewards can be attributed to individual parties rather than the paymaster?

## 7. Quantitative research design

A hybrid study could model the pipeline:

- Q: actual traffic consumed, in bytes;
- Q_r: operator-reported traffic;
- d: agreed discount factor, where 0 < d <= 1;
- Q_b: traffic-equivalent amount represented by the CC burn;
- P: list price per MB;
- X: applicable USD/CC conversion price;
- C: CC actually burned.

Under a simple linear illustrative pricing case:

C = (Q_b / 1,000,000) * P / X

The key reconciliation residuals are:

e_Q = Q_r - Q

e_B = Q_b - Q

A simple discounted case may use Q_b = d * Q_r, but actual CIP-0132 arrangements may include other modifiers and smoothing; this expression is illustrative only.

Candidate metrics:
- traffic-report error: (Q_r - Q) / Q;
- burn-equivalent error: (Q_b - Q) / Q;
- effective price per actual MB: (C * X) / Q * 1,000,000;
- report-to-burn lag;
- reward-to-burn ratio;
- proportion of traffic periods independently reconcilable;
- variance between independent operator records, paymaster records and on-ledger burn records.

Use synthetic scenarios until authorised dSync report/burn data are available. Do not present synthetic results as observations of Canton operators.

## 8. Research methods and evidence

A credible hybrid study could include:
- a formal model of the traffic-report / discount / burn / reward pipeline;
- an implementation map of CIP-0104 reward accounting and the proposed CIP-0132 extension;
- sensitivity analysis for under-reporting, over-reporting, discounts, smoothing delays and CC price changes;
- a privacy-verifiability comparison of signed reports, independent audits, commitments, selective disclosure and cryptographic proofs;
- a reproducible reference model and a proposed audit/reconciliation protocol.

Evidence needed before making implementation claims:
- the implementation branch or merged PR for CIP-0132;
- the exact RegisteredSynchronizer contract and governance choices;
- the traffic-report API schema and implementation;
- the traffic-purchase and activity-recorder code path;
- the exact validator and app reward calculation applied to dSync burns;
- any operational report/burn records that can be obtained with permission.

## 9. Limits

- CIP-0132 is proposed, not approved or proven deployed in this snapshot.
- The public Splice code snapshot shows the Global Synchronizer CIP-0104 reward path and existing member traffic purchases, but does not prove CIP-0132's dedicated synchronizer integration is implemented.
- Do not infer that the paymaster model is insecure merely because it is trusted. Assess its intended interim scope and trade-offs.
- Do not claim actual misreporting or losses without evidence.
- Do not claim a zero-knowledge proof or other cryptographic mechanism is necessary before establishing what data are available, what must remain private and what guarantees are required.

## 10. Primary sources

- CIP-0104, Traffic-Based App Rewards (Approved 27 Oct 2026): https://github.com/canton-foundation/cips/blob/main/cip-0104/cip-0104.md
- CIP-0129, Universal Burn and Synchronizer Pricing (Approved 23 Oct 2026): https://github.com/canton-foundation/cips/blob/main/cip-0129/cip-0129.md
- CIP-0132, Dedicated Synchronizer Paymaster Model (Proposed 16 Nov 2026): https://github.com/canton-foundation/cips/blob/main/cip-0132/cip-0132.md
- Splice AppActivityComputation.scala: https://github.com/canton-network/splice/blob/408f7ed9e742707f0d6fe080ca386aedc742d977/apps/scan/src/main/scala/org/lfdecentralizedtrust/splice/scan/rewards/AppActivityComputation.scala
- Splice AmuletConfig.daml: https://github.com/canton-network/splice/blob/408f7ed9e742707f0d6fe080ca386aedc742d977/daml/splice-amulet/daml/Splice/AmuletConfig.daml
