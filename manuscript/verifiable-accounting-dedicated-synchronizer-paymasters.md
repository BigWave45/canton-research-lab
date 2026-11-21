Verifiable Accounting for Dedicated Synchronizer Paymasters: Guarantees, Trust Boundaries, and Trade-offs

Abstract

The proposed Dedicated Synchronizer Paymaster Model introduces a payment mechanism in which a designated paymaster periodically settles synchronizer traffic costs through Canton Coin burns. The model creates an accounting relationship between reported infrastructure activity, commercial obligations, payment events and reward attribution. However, verifying that a payment corresponds to a reported liability does not establish that the underlying activity was measured completely or correctly.

This research examines the accounting guarantees that can be added to the proposed model and evaluates their economic, privacy and operational trade-offs. It develops and tests a prototype covering interval completeness, signed settlement bindings, deterministic liability calculation, multi-burn allocation, duplicate-payment prevention and correction handling. Reward attribution is examined through a proposed validation framework and a narrower prototype test of reward-budget constraints. Synthetic experiments examine the limits of aggregate privacy controls, while a qualitative comparison evaluates alternative assurance architectures and their implementation and operational cost drivers.


The results distinguish three assurance layers. Settlement integrity can be strengthened through explicit evidence binding, schedule validation, deterministic calculations and allocation controls. Measurement completeness remains dependent on authoritative source records and independent evidence of activity. Reward attribution and privacy can be modelled and constrained, but cannot be considered production-verified without access to the relevant operational evidence and disclosure interfaces.

The central finding is that accounting verification must distinguish the integrity of a settlement from the completeness and authority of the evidence on which that settlement depends. Stronger cryptographic and reconciliation controls can make accounting records more consistent and auditable, but they cannot independently establish that the original measurement was truthful.

1. Introduction

1.1 Background

Canton’s Universal Burn framework seeks to bring traffic on the Global Synchronizer and dedicated synchronizers into a common economic system. Under the previously established arrangement, Global Synchronizer traffic was paid for through Canton Coin (CC) burns, while dedicated synchronizer traffic operated under a separate commercial model. CIP-0129, Universal Burn and Synchronizer Pricing, proposes extending the burn-and-reward framework to production traffic on every synchronizer. The proposal was approved on 23 October 2026 [2].

The economic change is significant. Dedicated synchronizer activity would contribute to the same network-wide burn mechanism, while applications and validators could receive rewards associated with that activity. The framework also anticipates volume-based pricing and commitment discounts, although those pricing mechanisms require further specification and implementation.

CIP-0132, Dedicated Synchronizer Paymaster Model, proposes the first technical phase for bringing dedicated synchronizers into this system [3]. Its proposed model assigns payment responsibility to a designated paymaster. The synchronizer operator reports consumed traffic, and the paymaster periodically settles the reported consumption by burning CC on the Global Synchronizer.

The proposal divides traffic reporting into ten-minute intervals. In this initial phase, traffic is not enforced against a prepaid limit: messages are not rejected because a node has exhausted its traffic allowance. The relationship between the traffic report and the subsequent burn is off-ledger. The proposal explicitly relies on the dedicated synchronizer operator and paymaster being trusted to report and pay the correct amount. The burn invokes an activity-recording mechanism intended to support app and validator reward attribution.

This arrangement is an interim architecture. It provides a path toward including dedicated synchronizers in the Universal Burn economy without requiring the full enforcement and trust model of a later implementation.
 As of 18 November 2026, CIP-0132 remained proposed. The analysis therefore treats it as a proposed protocol model rather than an approved or production-deployed system [3].

1.2 The accounting assurance problem

The paymaster model creates an accounting chain connecting infrastructure activity to economic settlement:

	1.	Traffic is consumed on a dedicated synchronizer.
	2.	The operator measures and reports that activity.
	3.	The applicable commercial agreement determines the payable amount.
	4.	The designated paymaster burns CC to settle the obligation.
	5.	The burn produces activity records used in reward attribution.
	6.	The resulting records may be reconciled by the parties or examined by an authorised reviewer.

Each step makes a different claim. A traffic report claims that a quantity of activity was measured. A commercial agreement determines how that quantity is priced. A burn demonstrates that a payment event occurred. Reward records determine how the resulting activity is recognised by the reward mechanism.

These claims are related, but they are not interchangeable.

In particular, verifying that a burn matches a reported liability does not establish that the report captured all chargeable activity. A report can be correctly signed, internally consistent and correctly priced while still omitting activity at the measurement stage. Likewise, a valid burn does not independently establish that the underlying report was complete or that the resulting reward attribution reflects the intended economic contribution.

This creates a distinction between settlement integrity and measurement assurance. Settlement integrity concerns whether the supplied evidence has been bound together correctly and whether the resulting obligation has been calculated and paid without duplication. Measurement assurance concerns whether the original activity record is complete and accurate. The former can be strengthened through accounting controls; the latter requires evidence about the measurement process itself.

There is also a privacy problem. More detailed reporting can improve auditability, but participant-level traffic, membership changes and repeated aggregate disclosures may reveal commercially sensitive activity. An accounting architecture therefore needs to consider not only what can be verified, but also who can verify it and what information that verification exposes.

1.3 Research question

This research asks:

What verifiable accounting guarantees can be added to the proposed dedicated-synchronizer paymaster model, and what are their economic, privacy and operational costs?

The question is examined across three assurance layers:

	•	Measurement assurance: whether reported activity can be shown to cover the expected reporting period and whether the evidence supports confidence in the underlying measurement.
	•	Settlement assurance: whether reports, agreements, liabilities, burns and corrections can be bound together, checked deterministically and reconciled without double-counting.
	•	Attribution and privacy assurance: whether reward calculations can be tied to appropriate accounting evidence while limiting disclosure of commercially sensitive participant information.

The research does not assume that all three layers can be solved by the same mechanism. Cryptographic signatures, for example, can authenticate a signed statement, but they cannot independently establish that the statement’s original measurement was complete. Similarly, public payment records can support verification of a burn without making the underlying participant-level traffic public.

1.4 Contributions

This work makes five contributions.

First, it develops an accounting assurance model for the proposed paymaster architecture. The model separates measurement, reporting, agreement-based pricing, payment, allocation, correction and reward attribution, identifying the evidence and trust assumptions associated with each stage.

Second, it implements and tests a prototype for selected settlement guarantees. These include expected-interval validation, signed report-to-obligation bindings, deterministic liability calculation, multi-burn and multi-obligation allocation, duplicate and replay prevention, and correction and supersession handling. Reward attribution is addressed through a proposed validation checklist, with prototype evidence limited to a narrower reward-budget constraint.

Third, it examines adversarial and synthetic cases that expose limitations in common assurance mechanisms. These include the inability of signatures to prove measurement completeness, the dependence of interval validation on an independently authorised reporting-window anchor, and the possibility of identifying individual values from overlapping aggregate releases.

Fourth, it compares alternative assurance architectures qualitatively, examining their verification capabilities, implementation burden, privacy exposure, operational requirements, latency and residual trust assumptions. The comparison does not estimate numerical production costs.

Fifth, it provides an evidence-based assessment of what the proposed architecture and the prototype can establish, what remains dependent on trusted external inputs, and what would require independent operational evidence.

1.5 Scope

The subject of this research is the accounting assurance of the proposed dedicated-synchronizer paymaster model. It is not an audit of Canton MainNet, a claim that the proposed model has a live accounting vulnerability, or a demonstration that the complete report-to-burn-to-reward pipeline is operating in production.

The analysis uses four categories of evidence: protocol proposals and public source material; observations of relevant implementation code; prototype tests and synthetic experiments; and analytical deductions about the guarantees and limitations of those mechanisms. These categories are kept distinct throughout the paper.

The prototype evaluates accounting rules over supplied evidence. It does not independently authenticate the completeness of every source record, establish the legal authority of real-world agreements, or prove that a production deployment follows the proposed design. Similarly, the privacy experiments demonstrate mathematical disclosure conditions under stated assumptions; they do not establish that the current protocol exposes the specific overlapping aggregates used in those experiments.

The objective is therefore narrower and more testable than proving the entire paymaster architecture trustworthy. It is to identify which accounting guarantees can be made explicit and reproducible, determine the assumptions on which they depend, and assess the costs and residual risks of adding them.


2. Protocol and Accounting Model

2.1 Dedicated synchronizer paymaster architecture

The accounting model examined in this research emerges from two related proposals [2, 3, 12].

CIP-0129 establishes the economic framework of Universal Burn and Synchronizer Pricing. Its central objective is to bring production traffic on dedicated synchronizers into the same Canton Coin burn-and-reward economy as traffic on the Global Synchronizer. Under this framework, production traffic on every synchronizer is intended to contribute to network-wide burns, while applications and validators receive rewards according to the applicable reward rules.

CIP-0129 also identifies an information asymmetry. Super Validators do not observe traffic on synchronizers they do not operate. The proposal therefore anticipates aggregate traffic reporting by dedicated synchronizer operators, with attribution at the party level where required by reward rules. It establishes the economic direction, but leaves technical implementation details to subsequent proposals.

CIP-0132 specifies an initial technical approach: the Dedicated Synchronizer Paymaster Model. Rather than requiring each participant to pay directly for its traffic, the model designates a paymaster responsible for settling the synchronizer’s reported consumption.

The proposed architecture has four principal roles:

	•	Dedicated synchronizer operator: operates the synchronizer, measures consumed traffic and exposes traffic reports.
	•	Paymaster: purchases traffic through Canton Coin burns on the Global Synchronizer and is the party associated with the initial activity records.
	•	Super Validators: govern synchronizer registration and the parameters associated with its paymaster and activity weights.
	•	Participants and applications: generate the activity whose consumption is measured and whose economic contribution may ultimately be recognised through the reward system.

The architecture separates the infrastructure where traffic is consumed from the ledger where the corresponding payment is recorded. This separation allows the dedicated synchronizer to continue operating without requiring every traffic event to be settled synchronously on the Global Synchronizer.

It also creates the central accounting problem examined in this paper: the evidence connecting consumed traffic to a subsequent burn is not entirely recorded on the same ledger.

2.2 Accounting lifecycle

The proposed Phase 1 lifecycle can be represented as six stages.

Stage 1: Traffic measurement

The dedicated synchronizer tracks traffic consumed on its infrastructure. CIP-0132 specifies reporting in ten-minute intervals, using record times measured against the sequencer clock.

The reporting API is described as returning traffic consumed across the synchronizer within a requested time range, divided into ten-minute intervals. The proposal limits the reportable range to the sequencer pruning window.

This is an infrastructure measurement. It is not itself a Canton Coin payment, nor does the report alone establish a commercial obligation.

Stage 2: Traffic reporting

The operator exposes the measured traffic through the dedicated synchronizer operator application.

The report provides the activity quantity on which the subsequent payment calculation depends. Its completeness, provenance, retention and relationship to the requested reporting window are therefore important accounting properties.

The proposal specifies the reporting interval and measurement clock, but these specifications should not be confused with independent verification of the measurement process. A report can conform to the expected format while still depending on the operator’s measurement system.

Stage 3: Liability determination

The reported consumption is translated into a payment obligation.

The applicable economic terms may include the Global Synchronizer list price and any authorised discount arrangements. CIP-0129 establishes the Universal Burn framework and anticipates volume-based pricing and commitment discounts. CIP-0132 describes an interim arrangement in which discounts are handled through an off-ledger agreement between Super Validators and the dedicated synchronizer operator.

Consequently, the payable amount is not necessarily established by the traffic report alone. It depends on the applicable pricing rules, agreement terms and effective period.

This distinction matters for reproducibility. An independent reviewer needs both the reported activity and the authorised pricing basis to reconstruct the liability.

Stage 4: Canton Coin burn

The designated paymaster periodically settles consumed traffic after the activity has occurred by burning Canton Coin on the Global Synchronizer.

CIP-0132 describes the relationship between the traffic report and the burn as off-ledger during Phase 1. The dedicated synchronizer operator and paymaster are trusted to report and pay the correct amount.

The proposal’s registration mechanism restricts which party may act as paymaster for a registered dedicated synchronizer. Registration is performed through Super Validator governance and records the synchronizer identifier, designated paymaster and maximum app and asset activity weights.

This creates an on-ledger association between a synchronizer and its authorised paymaster. It does not, by itself, create an on-ledger proof that a particular burn corresponds to a complete and accurate traffic report.

Stage 5: Activity recording and reward attribution

CIP-0132 proposes that the paymaster’s traffic purchase exercise the App Activity Recording Extension Hook associated with CIP-0104 [1, 3, 6, 24].

The proposal describes the creation of activity records for the paymaster and a validator reward coupon corresponding to the amount of traffic purchased. App and asset activity records use the registered activity-weight parameters. Subsequent reward issuance occurs through separate transactions.

The initial attribution model therefore associates the recorded activity with the designated paymaster. It should not be interpreted as a complete participant-level reward allocation system for every application and validator operating on the dedicated synchronizer.

The distinction is important because three separate facts are involved:

	1.	A quantity of traffic was reported by the dedicated synchronizer.
	2.	The paymaster burned Canton Coin for a traffic purchase.
	3.	The burn generated activity and reward records under the applicable rules.

The existence of the latter two does not independently prove the completeness of the first.

Stage 6: Reconciliation and review

The final stage is the reconstruction of the accounting relationship between traffic, pricing, payment and reward records.

The parties may need to establish:

	•	Which reporting intervals were included.
	•	Whether the reports cover the entire agreed settlement window.
	•	Which agreement and pricing version applied.
	•	How the reported traffic produced the payable amount.
	•	Which burn events settled the obligation.
	•	Whether each burn was allocated only once.
	•	Whether the resulting activity and reward records followed the authorised rules.

CIP-0132 establishes the initial payment architecture, but it does not make this entire reconciliation chain independently verifiable. That is the gap this research investigates.

2.3 Trust boundaries

The architecture contains several distinct trust boundaries. Treating them as one general trust assumption would obscure where additional accounting controls can help.

Measurement trust. The paymaster model relies on the dedicated synchronizer operator to report consumed traffic correctly. The proposal does not establish an independent measurement source against which the report can be compared.

Commercial authority trust. The payable amount depends on the applicable pricing rules and discount agreement. A technically valid agreement record is useful only if the signing authority is authorised to establish those terms for the relevant parties and synchronizer.

Settlement trust. The operator and paymaster are trusted to connect the traffic report to the correct burn amount. The burn is an on-ledger event, but the report-to-burn relationship is off-ledger in Phase 1.

Reward-rule trust. Activity weights and reward calculations depend on registered parameters and the applicable protocol rules. Verifying the calculation does not independently establish that the source activity was complete.

Evidence-retention trust. Independent review requires access to the relevant reports, agreements, signatures, burn records and correction history. The ability to verify a historical settlement depends on whether the necessary evidence remains available and can be authenticated.

Privacy and access trust. Detailed traffic records may contain commercially sensitive information. The architecture must distinguish information needed for public verification from information that should remain available only to the parties or an authorised auditor.

These boundaries identify different problems. A cryptographic signature may improve report integrity. An agreement registry may improve authority checks. A burn record may prove that payment occurred. None of these mechanisms independently proves that the measurement system captured every chargeable event.

2.4 Scope and assumptions

This research evaluates the proposed Phase 1 accounting model and a prototype designed to test additional assurance mechanisms. It does not assume that every proposed component has been deployed or that the complete accounting lifecycle is already operational.

The protocol sources establish the intended architecture and its stated trust assumptions. Source-code observations provide evidence about particular implementation choices, but do not establish the behaviour of every production deployment. Prototype tests establish the behaviour of the research implementation under supplied inputs. Synthetic experiments demonstrate specific logical or mathematical properties under their stated assumptions.

The analysis therefore uses the following distinctions:

	•	Protocol specification: what the proposals describe or require.
	•	Implementation observation: what a particular source-code revision contains.
	•	Prototype result: what the research implementation demonstrates in tests.
	•	Analytical result: what follows from a stated mathematical or logical model.
	•	Production assurance: what would require independent evidence from an operating network, its authorised operators or its deployed systems.

The research does not assume that a report is complete merely because it is signed, that a burn is correctly allocated merely because it exists, or that a reward is justified merely because its calculation follows the registered rules.

These distinctions define the boundary between what can be strengthened through accounting design and what remains dependent on external evidence.

3. Threat Model and Assurance Requirements
3.1 Failure and adversarial scenarios
The proposed paymaster architecture connects infrastructure measurements, commercial agreements, payment events and reward attribution. Errors or manipulation at any of these stages can propagate through the accounting chain.
This research considers the following scenarios.
T1. Incomplete traffic reporting
A synchronizer operator reports less activity than was actually consumed. The report may be correctly formatted and internally consistent, but the resulting liability is understated.
This scenario tests the distinction between report integrity and measurement completeness. A signature can establish who signed a report, but it cannot establish that the underlying measurement captured every chargeable event.
T2. Missing or malformed reporting intervals
An expected reporting interval is omitted, duplicated, shortened, extended or presented with inconsistent timestamps.
A reconciliation system that processes only the intervals supplied to it may accept an incomplete settlement window unless it has an independent expectation of which intervals should exist.
T3. Report substitution or modification
A report is replaced or modified after it has been used to calculate a liability. Alternatively, a valid report is associated with a different settlement obligation.
This scenario tests whether the evidence is cryptographically bound to the correct reporting interval, synchronizer, agreement and obligation.
T4. Unauthorized commercial terms
A pricing agreement is signed by a key that is not authorised to establish the relevant commercial terms, or a valid agreement is applied outside its effective period.
A valid cryptographic signature is not sufficient evidence of commercial authority. Verification must also consider the signer’s recognised role, authority scope, agreement version and effective dates.
T5. Incorrect or nondeterministic liability calculation
The same report and agreement produce different payable amounts because of inconsistent arithmetic, rounding, pricing-band interpretation or effective-date handling.
This scenario tests whether the liability can be independently reconstructed from explicit inputs and deterministic rules.
T6. Duplicate or excessive burn allocation
A burn is credited more than once, allocated beyond its recorded amount or assigned to an obligation belonging to another paymaster.
The existence of a valid burn does not establish that its accounting credit has been used correctly. Allocation records must preserve uniqueness, amount constraints and identity consistency.
T7. Temporal misclassification
A payment is treated as timely even though it occurred after the applicable deadline, or an unpaid obligation is treated as overdue before its grace period expires.
Historical reconciliation introduces a further problem: a snapshot of total allocated amounts cannot establish what had actually been paid by an earlier point in time unless payment-event timing and finality are recorded.
T8. Invalid corrections and replay
A revised report is used without a valid supersession relationship, an earlier adjustment is applied more than once, or an amendment silently changes an already settled obligation.
Corrections must preserve the original evidence and make the resulting adjustment traceable. Replacing historical records with revised values would weaken auditability.
T9. Incorrect reward attribution
A reward record references activity, payment or synchronizer evidence that does not justify the claimed amount or attribution weight. Duplicate, superseded or incorrectly versioned records may also be included.
This scenario tests the integrity of the attribution calculation, while recognising that the calculation still depends on the authority and completeness of its input evidence.
T10. Aggregate information disclosure
An authorised reviewer or external observer combines multiple aggregate traffic releases to infer participant-level activity.
Even where individual releases satisfy a minimum cohort-size threshold, overlapping membership can make the combined releases more revealing than any single report.
The threat is disclosure through composition, not necessarily unauthorised access to the underlying synchronizer transaction payloads.
3.2 Adversary and failure assumptions
The research does not assume that every participant is malicious or that the protocol is compromised. It evaluates failures under a range of conditions:
	•	An operator may submit incomplete or inconsistent measurements, whether through error or deliberate action.
	•	A paymaster may allocate payments incorrectly or fail to preserve a complete settlement history.
	•	A signing key may be misused, revoked or presented outside its authorised scope.
	•	A reporting system may omit intervals or expose inconsistent revisions.
	•	A reviewer may combine otherwise valid aggregate reports with auxiliary information.
	•	An implementation may behave correctly on supplied records while the supplied records themselves are incomplete.
The prototype treats supplied evidence as input. It can reject inconsistencies within that evidence, but it cannot independently establish the authenticity or completeness of records that it has no means to observe.
This limitation is fundamental. An adversary who controls the only source of a measurement may be able to provide a consistently signed but incomplete record. A verifier cannot distinguish that record from a complete one without an independent measurement source, trusted execution boundary or other evidence that constrains the source’s behaviour.
The research does not attempt to break Canton cryptography, decrypt synchronizer messages, compromise validator infrastructure or infer transaction payloads from traffic volume alone. It also does not establish that any of the scenarios above has occurred in a Canton production deployment.
3.3 Accounting invariants
The threat scenarios are translated into twelve research-defined invariants. An invariant defines a property that an accounting process should preserve; it does not imply that the property is already guaranteed by the protocol. These twelve invariants are distinct from the repository’s P1–P8 prototype property register [9].
Measurement and reporting
I-01 — Interval completeness
Every expected reporting interval within an independently defined settlement window must be represented exactly once, subject to an explicit and valid correction history. Gaps, overlaps, duplicates, malformed timestamps and truncated windows must not be silently accepted.
I-02 — Non-OK report semantics
A report that cannot establish a valid measurement must not be interpreted as a valid zero-traffic report. Missing, undetermined and unavailable evidence must remain distinguishable from a valid report of zero consumption.
I-03 — Report provenance and immutability
A report used in settlement must have identifiable provenance and must remain bound to the evidence version on which the calculation depends. Subsequent modification or substitution must be detectable.
Commercial and settlement integrity
I-04 — Agreement version and authority
Every liability must reference an applicable agreement version whose signer and authority are valid for the relevant parties, synchronizer, obligation and effective period.
I-05 — Report-to-obligation binding
The report set used to calculate a liability must be bound to the specific settlement obligation, reporting interval, synchronizer and agreement. Evidence from one obligation must not be silently substituted into another.
I-06 — Deterministic liability
Given identical valid reports, agreement terms, effective dates and rounding rules, independent calculations must produce the same liability.
Payment and temporal accounting
I-07 — Paid-versus-due integrity
Settlement status must reflect the amount actually allocated to an obligation by the relevant time, including applicable deadlines and grace periods. Historical as-of claims require timestamped payment evidence and an explicit rule for whether payment time means event creation or finality.
I-08 — Unique burn allocation
A burn’s recorded value must not be credited beyond its available amount. Allocation records must be uniquely identifiable and must reference valid burns and obligations.
I-09 — No double counting
A payment credit must not be reused across obligations, amendments, settlement windows or reward calculations. Prior allocations and adjustments must be considered when calculating remaining available credit.
Attribution and privacy
I-10 — Reward attribution integrity
Reward calculations must reference the correct activity and settlement evidence, authorised attribution weights, applicable rule versions and relevant epochs. Duplicate, superseded or unauthorised records must not increase reward attribution.
I-11 — Correction and supersession integrity
A correction must preserve the relationship between original and revised evidence. Supersession chains must be valid, adjustment calculations must be reproducible, and previously applied adjustments must not be replayed.
I-12 — Aggregate disclosure control
The release of aggregate accounting information must consider composition across multiple reports, cohort membership and auxiliary knowledge. A minimum cohort-size threshold alone must not be treated as a general guarantee against individual disclosure.
These invariants cover different assurance properties. I-01 through I-03 concern the quality and provenance of reporting evidence. I-04 through I-06 concern the authority and reproducibility of liability determination. I-07 through I-09 concern payment allocation and temporal accounting. I-10 and I-11 concern attribution and correction. I-12 concerns the privacy implications of making accounting information available for verification.
The distinction also prevents a common category error: passing I-05, for example, establishes that a report is bound to an obligation. It does not establish I-01 or I-03. A correctly bound report may still be incomplete or lack independently verified provenance.

These twelve invariants constitute the research taxonomy developed for this paper. They are distinct from the P1–P8 formal property register in the accompanying repository. In particular, P6 in that register specifies a reward-budget bound; it is not equivalent to the broader reward-attribution requirement expressed by I-10. The distinction between a proposed research invariant and a property demonstrated by the prototype is maintained throughout the evaluation.

3.4 Evidence classification
The strength of a research claim depends on the kind of evidence supporting it. This work uses six evidence levels.
Level	Evidence type	What it can establish
E0	Protocol specification	What a proposal describes or requires
E1	Source-code observation	What a specific inspected source revision implements
E2	Prototype test	Whether the research implementation behaves as expected for supplied cases
E3	Reproducible experiment	Whether a documented synthetic or analytical experiment supports a stated result
E4	Independent network or operator evidence	Independently obtained operational evidence: whether a claim is supported by operational records obtained from a source independent of the party whose accounting assertion is being evaluated. The independence of the source and the method by which the evidence was obtained must be stated.
E5	Production assurance	Whether the property has been validated in the deployed production environment under an appropriate assurance process
These levels are not interchangeable.
A protocol proposal can establish that a reporting mechanism is intended, but not that it has been deployed. A source-code observation can identify an implementation behaviour, but not establish that the behaviour is active in every production environment. A prototype test can demonstrate that a validator rejects a duplicated allocation, but not that the production system supplies a complete list of prior allocations.
Likewise, a synthetic privacy experiment can demonstrate that a set of overlapping aggregates mathematically identifies individual values. It cannot establish that the protocol exposes those aggregates or that an actual participant’s information has been disclosed.
The evidence classification is used throughout the paper to prevent prototype results from being presented as production guarantees.
3.5 Assurance boundary
The twelve invariants do not all admit the same verification strategy.
Some can be checked deterministically once the relevant evidence is supplied. Examples include duplicate allocation identifiers, invalid supersession chains, arithmetic inconsistencies and report-to-obligation digest mismatches.
Other properties depend on external authority or evidence. Agreement validity depends on a trustworthy authority registry. Interval completeness depends on an independently authorised reporting-window anchor. Measurement completeness depends on evidence about the source measurement process. Historical payment status depends on reliable event and finality timestamps.
Privacy assurance introduces another boundary. A system may correctly restrict each individual report while still disclosing sensitive information through combinations of permitted releases.
The research therefore distinguishes three questions for every invariant:
	1.	Can the property be expressed precisely? The requirement must be defined without relying on ambiguous terms such as complete, valid or paid.
	2.	Can the property be checked against supplied evidence? The verifier must have enough information to evaluate the requirement deterministically.
	3.	Can the evidence itself be trusted? The source, authority and completeness assumptions must be established independently where necessary.
A successful answer to the second question does not automatically answer the third. This distinction governs the interpretation of every prototype result in the following sections.
4. Measurement Assurance
4.1 Interval completeness
A traffic accounting system must establish not only that submitted reports are valid, but also that the reports cover the entire period for which a settlement obligation is being calculated.
This is a problem of expected population. A verifier that receives a list of reports cannot determine whether the list is complete unless it has an independent basis for knowing which reports should exist.
For example, suppose a settlement window covers one hour and the reporting cadence is ten minutes. The expected schedule contains six intervals. If the operator supplies five valid reports, each with correct timestamps and signatures, a verifier that examines only the supplied records may find no internal inconsistency. The missing interval becomes detectable only when the verifier independently knows the settlement window and expected cadence.
This distinction motivates I-01.
The prototype implements schedule validation around an explicit expected interval population. It checks for:
	•	Empty or duplicate interval identifiers.
	•	Naive or invalid timestamps.
	•	Non-positive interval durations.
	•	Reporting deadlines earlier than interval completion.
	•	Gaps and overlaps between expected intervals.
	•	Duplicate or temporally inconsistent intervals.
	•	Reports that do not correspond to the expected interval boundaries.
	•	Invalid revision and supersession relationships.
The checks are designed to be independent of input ordering. A valid schedule should not become invalid merely because records are supplied in a different sequence.
However, internal schedule consistency is not sufficient. A caller could provide a contiguous schedule that begins after the true settlement window starts or ends before the true window finishes. The schedule would be internally valid while omitting part of the period under consideration.
The prototype therefore introduces an independent schedule anchor containing the settlement-window start and end, reporting cadence and reporting grace period. The expected intervals are reconstructed from this anchor and compared with the supplied reports.
This makes truncation detectable relative to the anchor. It does not authenticate the anchor itself. The verifier still depends on an authorised source to establish that the settlement window and cadence are the correct ones.
The result is a bounded guarantee: interval completeness can be checked relative to an independently supplied schedule, but cannot be established by the submitted reports alone.
4.2 Report validity versus measurement completeness
A second distinction concerns the meaning of a valid report.
A report may be:
	•	Correctly formatted.
	•	Associated with the expected synchronizer and interval.
	•	Signed by a recognised key.
	•	Bound to a particular settlement obligation.
	•	Used in a deterministic liability calculation.
These properties establish aspects of report integrity and settlement reproducibility. They do not establish that the measurement system observed every chargeable event.
Consider a synthetic example in which actual chargeable activity is 100 units, but the operator reports 90 units. A tariff of 0.1 CC per unit produces a liability of 9 CC. If the paymaster burns 9 CC, the burn correctly matches the liability calculated from the report.
The accounting chain is internally consistent:
Quantity	Value
Synthetic actual activity	100 units
Reported activity	90 units
Tariff	0.1 CC per unit
Calculated liability	9 CC
Burn amount	9 CC
Unreported activity	10 units
The payment is correct relative to the submitted report, but the report is incomplete relative to the synthetic ground truth.
This example does not demonstrate under-reporting on Canton. It demonstrates a logical limitation: reconciliation can verify the relationship between supplied evidence and payment without proving that the evidence represents all chargeable activity.
The same limitation applies to cryptographic mechanisms.
A digital signature can authenticate the signer and detect subsequent modification of the signed content. A digest can bind a settlement to a particular report set. A zero-knowledge proof can establish that specified predicates hold over committed inputs. None of these mechanisms, by itself, proves that the source measurement captured every relevant event.
To establish measurement completeness, the system needs an additional source of assurance. Possible approaches include an independently operated measurement process, independently retained sequencer-level records, trusted instrumentation with an auditable event boundary, or a reconciliation mechanism that compares the operator’s report against a separate authoritative record.
Each approach introduces its own trust and operational assumptions. An independent measurement system may itself be incomplete. Trusted instrumentation requires confidence in its configuration, execution environment and access controls. A comparison against another record is only meaningful if that record covers the same chargeable events and reporting boundaries.
The research prototype does not implement an independent source measurement mechanism. It deliberately treats measurement completeness as an external assurance requirement.
4.3 Participant membership and departure
Interval aggregation introduces a further accounting question: which participants belong to the population whose activity is included in an interval?
The inspected implementation in Canton Network’s proposed traffic-report API, PR #111, aggregates participants present at the end of an interval [5, 10]. A participant who was present at the start but absent at the end is therefore excluded from that end-of-interval participant population.
This is an implementation observation, not proof of incorrect billing.
Whether the behaviour is economically correct depends on the intended charging semantics. If the accounting rule charges only participants present at the interval boundary, the aggregation may be intentional. If activity consumed before departure remains chargeable, an end-of-interval population alone may not capture the complete chargeable population.
A robust accounting specification must therefore distinguish at least three concepts:
	1.	Membership at interval start: participants eligible or present when the interval begins.
	2.	Membership during the interval: participants whose activity occurs at any point within the interval.
	3.	Membership at interval end: participants still present when the interval closes.
These populations are not necessarily identical.
If participant-level activity is relevant to pricing or reward attribution, the reporting specification must define how join and leave events affect the accounting period. It must also define whether activity is attributed to the participant that generated it, the party responsible for the associated costs, or another protocol-defined identity.
The inspected implementation does not, on its own, answer these economic and contractual questions. The research therefore does not classify the observed aggregation behaviour as a billing defect. It identifies a specification question that must be resolved before participant-level completeness can be claimed.
A suitable validation would compare interval aggregation against an independent event history containing participant join and leave times and the corresponding traffic measurements. Such a test would need an authoritative definition of which events are chargeable. No such independent production dataset was available for this research. PR #111 explicitly replaces the earlier PR #103 design [5, 8, 10]. This is an observation about proposed source code, not deployed production behaviour. Whether the exclusion is an accounting defect depends on the intended charging rule for participants that leave during an interval; the protocol specification must define that rule.
4.4 Evidence limitations
The measurement-assurance investigation encountered a boundary between public protocol information and operational evidence.
CIP-0132 describes ten-minute traffic reporting and a proposed operator-facing reporting interface. The associated traffic-report API work was not merged in the source snapshot examined for this research [5, 10, 22]. The proposal and its related implementation work therefore provide architectural and source-level evidence, but not proof of an operational, durable reporting endpoint.
The research also examined the documented Scan API surface. The documented traffic-status endpoint exposes synchronizer traffic information, including actual consumption, limits and purchased targets. This provides a potentially useful operational reference, but it is not equivalent to the proposed private ten-minute traffic report used for paymaster accounting.
Two direct requests to the MainNet and TestNet Global Synchronizer Foundation Scan endpoints returned HTTP 403. The responses did not provide enough diagnostic information to establish the cause. These results are recorded as access failures, not evidence that the API is universally inaccessible or that the underlying traffic records do not exist.
No operator-provided report set, independently retained traffic measurement or production settlement dataset was available to establish the completeness of the proposed accounting measurements [3, 5, 10, 11].
Consequently, the evidence supports the following distinctions:
Property	Research result	Evidence boundary
Expected interval validation	Implemented and locally tested	Prototype behaviour
Gap, overlap and duplicate detection	Implemented and locally tested	Depends on expected schedule
Settlement-window truncation detection	Implemented relative to an anchor	Anchor authority remains external
Report-to-interval correspondence	Implemented and tested	Does not prove source measurement truth
Participant departure semantics	Source behaviour observed	Charging requirement unresolved
Independent measurement completeness	Not established	No independent ground truth
Production reporting availability	Not established	No validated operational report feed
The prototype therefore strengthens the verification of reporting structure without claiming to verify the underlying measurement process.
4.5 Implications for the paymaster model
Measurement assurance is the upstream dependency of the entire accounting lifecycle.
If the source report is incomplete, subsequent controls can preserve and reproduce an incorrect liability with high precision. Agreement signatures can authenticate the pricing terms. Settlement bindings can ensure that the correct report digest is associated with the obligation. Allocation controls can prevent a burn from being counted twice. Reward checks can apply the registered attribution rules correctly.
Those mechanisms remain useful, but they operate downstream of the measurement boundary.
A stronger design should therefore make the measurement assurance level explicit rather than treating every validly reconciled report as equally trustworthy. At minimum, an accounting record should distinguish whether:
	•	The report is structurally valid.
	•	The expected reporting window is covered.
	•	The report’s provenance is authenticated.
	•	The measurement source has independent completeness assurance.
	•	The evidence has been validated against an operational reference.
This classification would prevent a settlement system from presenting a successfully reconciled payment as proof that all chargeable activity was measured.
For the Phase 1 architecture, the most defensible claim is narrower: interval coverage, report binding and downstream settlement integrity can be strengthened through additional controls, but source measurement completeness remains dependent on evidence and trust mechanisms outside the prototype.

5. Settlement Assurance
5.1 Agreement and authority verification
A settlement obligation is meaningful only if the commercial terms used to calculate it are valid for the relevant parties, synchronizer and reporting period.
The prototype models agreements as canonical documents containing the terms required for deterministic verification [9, 25, 26]. Agreement signatures are checked against a key registry, and the verifier evaluates whether the signing key has the required role. Effective dates and agreement versions are also considered when determining whether an agreement applies to a reporting interval.
This addresses a specific weakness in a system that treats the existence of a valid signature as sufficient evidence of authority. A signature establishes that a particular key signed particular content. It does not, by itself, establish that the key was authorised to approve those terms.
The prototype therefore distinguishes agreement signers from settlement-binding signers through explicit roles. It rejects signatures from unknown, revoked or unauthorised keys and prevents an agreement from being accepted solely because its cryptographic signature is valid.
However, role verification is not equivalent to complete commercial authority verification. The current registry model does not establish that a key’s authority is scoped to a particular legal entity, synchronizer, paymaster or commercial obligation. Nor does it establish the legal capacity or enforceability of an actual agreement.
A production implementation would need an authority model that connects key identity and role to the entities and contractual actions the key is permitted to approve. It would also need rules for key rotation, revocation, effective time and disputes over authority.
The prototype demonstrates cryptographic and role-based agreement verification under a supplied registry. It does not establish the authority of real-world commercial agreements.
5.2 Report-to-obligation binding
Agreement verification alone does not establish which report was used to calculate a particular payment.
A report could be validly signed or otherwise accepted, yet be associated with the wrong reporting interval, synchronizer or settlement obligation. This creates a substitution risk: evidence from one accounting context could be reused in another.
The prototype addresses this through a separate settlement-binding attestation.
The binding includes identifiers for the settlement binding, reporting interval, synchronizer, obligation and agreement version, together with a digest of the report set and an authority reference. The canonical binding document is separately signed from the agreement document. During reconciliation, the verifier checks the report-set digest and verifies the binding signature against a registered settlement-binding signer.
This creates two distinct attestations:
	•	The agreement signature authenticates the commercial terms.
	•	The settlement-binding signature authenticates the association between a particular report set and a particular settlement obligation.
The distinction is important. A valid agreement signature should not automatically authenticate later settlement metadata that was never included in the signed agreement.
The prototype’s adversarial test demonstrated this boundary. An authority reference could be changed while retaining a valid agreement signature when the binding fields were not separately authenticated. The binding-attestation mechanism was introduced to prevent that substitution.
Tests cover modified binding fields, report-digest substitution, unknown or revoked signers, unauthorised signer roles and missing binding signer identifiers. Existing call sites were also checked for compatibility.
One limitation remains: the model distinguishes signer roles but does not enforce that the agreement signer and settlement-binding signer must be different principals. A registry could authorise the same key for both roles. The prototype therefore supports separate attestations, but does not impose strict separation of duties.
The result is a stronger evidence-binding mechanism. It does not independently prove that the report was measured completely or that the authority reference corresponds to a legally authorised real-world decision.
5.3 Deterministic liability calculation
Once reports and agreements have been validated and bound to an obligation, the payable amount must be reproducible.
A liability calculation depends on more than a traffic quantity. It may also depend on pricing bands, discounts, effective dates, units, rounding policy and the treatment of invalid reports.
The prototype’s pricing model uses explicit inputs and deterministic arithmetic. It considers the agreement version, effective coverage, report status, pricing terms and rounding policy. Non-OK reports are not silently converted into zero consumption or priced as valid measurements.
The calculation uses integer accounting units and explicit rounding modes, including ceiling, floor and half-up policies. This avoids allowing implicit floating-point behaviour to determine a payment amount.
The intended property is:
Given the same valid reports, agreement terms, effective period and rounding policy, the calculation should produce the same liability.
This is a reproducibility guarantee over supplied inputs. It is not proof that the tariff itself is authorised or that the inputs reflect actual Canton commercial terms.
The prototype uses synthetic pricing data. It does not establish a production Canton tariff schedule, an authoritative CC precision policy or an independently implemented second pricing engine. Consequently, the research demonstrates deterministic calculation under explicit assumptions, rather than independent production validation of the pricing rules.
A stronger production assurance process would publish canonical calculation rules and test vectors, establish authoritative tariff versions and effective periods, and allow independent implementations to reproduce the same liability from the same evidence.
5.4 Burn allocation and double-counting prevention
A burn event establishes that a payment occurred. It does not automatically establish how that payment should be credited across multiple obligations.
This distinction becomes important when a paymaster settles several obligations through one burn, or when one obligation is settled through several burns. A single-burn, single-obligation model cannot represent these cases without additional allocation rules.
The prototype extends the portfolio settlement model to support many-to-many allocation [18, 25, 26]:
	•	One burn may be divided across several obligations.
	•	One obligation may receive allocations from several burns.
	•	Each allocation must have a unique, non-empty identifier.
	•	Every allocation must reference an existing burn and obligation.
	•	The total allocation against a burn must not exceed its recorded amount.
	•	Burn and obligation paymaster identities must match.
	•	Negative and zero allocations are rejected.
	•	Prior allocations are considered to prevent replay or reuse of previously credited payment.
	•	Decimal arithmetic is used to avoid floating-point allocation errors.
The model also distinguishes partial settlement from complete settlement and accounts for whether an obligation is due or still within its permitted grace period.
Adversarial tests cover one-to-many, many-to-one and many-to-many allocation; exact allocation boundaries; fractional over-allocation; duplicate identifiers; duplicate burn evidence; missing references; paymaster mismatches; negative and zero values; partial payment; not-yet-due obligations; replay attempts and input-order invariance.
These checks establish useful accounting properties. Given a complete and authoritative set of burn records and prior allocations, the validator can detect excessive credit, duplicated allocation and inconsistent references.
The qualification is essential. The prototype receives the burn and allocation records as inputs. It does not independently establish that every relevant burn has been supplied, that a burn is authentic and final, or that the historical allocation set is complete.
Without those properties, a validator may correctly enforce its allocation rules over an incomplete record set while failing to detect credit already used elsewhere.
The model also does not invent a Canton Coin quantisation policy. Exact Decimal arithmetic avoids floating-point error, but a production system still needs an authoritative rule defining valid CC units and fractional precision.
5.5 Temporal settlement and corrections
Accounting correctness is time-dependent.
An obligation may be unpaid but not yet overdue. A payment may have been initiated but not reached the required finality condition. A report may be corrected after an earlier settlement has already been made.
The prototype models due dates, grace periods, FIFO allocation and carry-forward treatment. It distinguishes obligations within their grace period from those that are past grace and unpaid. It also models unapplied payment amounts rather than silently assigning excess credit.
However, historical payment status requires more than a current allocation total.
To answer whether an obligation was paid by a particular time, the system needs timestamped payment evidence and an explicit definition of payment time. A burn’s event-creation time and its finality time may differ. If the accounting rule requires finality, a burn created before a deadline but finalised afterward should not automatically be classified as timely.
The current allocation model does not contain the burn event and finality timestamps required to reconstruct every historical as-of settlement state. It can evaluate supplied obligation and allocation snapshots, but cannot independently establish payment-by-time without that temporal evidence.
Corrections create a related problem. A revised traffic report may change a previously calculated liability. The accounting system must preserve the original report, validate the relationship between revisions and calculate the resulting adjustment without silently rewriting settlement history.
The prototype’s correction model addresses several properties:
	•	Supersession chains must be valid.
	•	Cycles and invalid revision branches are rejected.
	•	The latest valid revision is used for recalculation.
	•	Settlement identities and signed authority bindings are preserved.
	•	Adjustment candidates are generated append-only.
	•	Previously processed adjustment identifiers are checked to prevent replay.
	•	Prior allocation and reward claims must be considered explicitly.
	•	Partial settlement, overpayment and potential credit are handled as distinct cases.
The model does not automatically reverse burns, claw back rewards, issue refunds or carry credits forward. It produces adjustment candidates that require an authorised decision and a subsequent settlement action.
Idempotency also depends on the caller supplying a durable set of processed adjustment identifiers. The prototype does not provide a production persistence service or independently authenticate the completeness of the prior allocation history.
Thus, the correction model demonstrates how revised evidence can be reconciled without erasing the original accounting trail. It does not define the governance or operational authority required to execute every possible correction.
5.6 Prototype evaluation
The settlement prototype was developed incrementally around the accounting invariants and evaluated through focused local test suites and the complete local test suite.
The implementation covered:
Area	Implemented property	Principal limitation
Agreement verification	Canonical signatures and signer-role checks	No complete entity-scoped legal authority model
Settlement binding	Signed binding and report-set digest	Depends on trusted binding signer
Liability calculation	Deterministic arithmetic and explicit rounding	Synthetic tariffs; no independent pricing implementation
Burn allocation	Many-to-many allocation and unique identifiers	Depends on complete authoritative burn history
Double-counting prevention	Prior-credit and replay checks	Prior allocation completeness is external
Temporal settlement	Due dates, grace periods and allocation status	No complete historical burn-finality timeline
Corrections	Supersession validation and append-only adjustment candidates	No automatic reversal, refund or durable adjustment service

The prototype was evaluated through focused local tests and successive runs of the local test suite during development. The recorded test counts came from different repository states and are not treated as four independent runs of an unchanged codebase. The available audit record does not establish a reproducible commit-to-count mapping for each reported total. Accordingly, this paper does not use those historical counts as quantitative evidence of test coverage.
The checked-in settlement-manifest validator and its tests provide reproducible evidence for selected properties, including interval coverage, missing reports, duplicate burns, allocation references, agreement-version presence, report digests and payment residuals. These tests establish the behaviour of the research implementation for their supplied cases. They do not establish production integration or source measurement completeness. [25, 26]

5.7 Settlement assurance findings
The settlement experiments support a bounded conclusion.
Several important accounting properties can be made explicit and enforced over supplied evidence. Agreement signatures can be checked against registered roles. Reports can be bound to obligations through separate attestations. Liabilities can be calculated deterministically. Burns can be allocated across obligations without exceeding recorded amounts. Corrections can preserve historical evidence and produce traceable adjustment candidates.
These mechanisms reduce ambiguity and make settlement decisions more reproducible.
However, their guarantees depend on external evidence and authority. The model cannot independently establish the completeness of the traffic measurement, the legal authority of real-world agreements, the completeness and finality of burn records, or the durability of historical allocation and correction records.
Settlement assurance is therefore stronger than measurement assurance in this prototype, but it is conditional rather than absolute. The system can establish that supplied evidence has been processed consistently under specified rules. It cannot establish every fact about the real-world activity and authority represented by that evidence.


6. Reward Attribution and Privacy
6.1 Reward attribution integrity
The Dedicated Synchronizer Paymaster Model connects traffic purchases to the Canton Coin reward mechanism through activity records generated when the paymaster burns CC.
This creates an accounting dependency between the traffic reported by the dedicated synchronizer, the payment made by the paymaster and the activity recognised by the reward system.
The first phase of the proposed model attributes the relevant activity to the designated paymaster through the activity-recording mechanism. The registered activity weights determine how the purchase is represented for application and asset activity. Validator reward attribution is handled through a separate reward mechanism [1, 3, 6, 23, 24].
This should not be confused with complete participant-level attribution. The initial paymaster model does not, by itself, demonstrate that every participant’s individual traffic contribution is independently measured and rewarded through the same accounting path.

The research design specifies a reward-attribution validation checklist covering identity and reference binding, authorised activity weights, reward-rule and epoch versions, duplicate or superseded records, reward categories, deterministic calculation and aggregate budget limits.
The current prototype evidence is narrower: the checked-in adversarial test demonstrates a reward-budget bound, while the settlement-manifest validator tests interval coverage, agreement references, burn uniqueness and payment reconciliation. The full reward-attribution checklist has not been demonstrated by the checked-in prototype tests and is treated here as a proposed validation requirement. [9, 18, 25, 26]

The proposed validation design would use exact Decimal arithmetic and explicit references between activity, settlement and reward records. If implemented, such controls could reject attribution that cannot be reconciled with the supplied accounting evidence. They would address errors such as applying an outdated weight, counting the same activity twice, using a superseded record or associating a reward with the wrong paymaster or synchronizer. The full set of these controls is not demonstrated by the checked-in prototype tests [13, 18, 23, 24].
However, correct calculation is not equivalent to justified attribution.
The prototype assumes that the activity records, burn evidence, registered weights and reward rules supplied to it are authoritative and sufficiently complete. It does not independently establish that the original traffic was measured correctly, that every relevant burn has been included, or that the deployed reward system follows the same rules.
The distinction is particularly important when considering the relationship between payment and reward. A reward calculation can be mathematically correct relative to a supplied burn while still inheriting an incomplete or incorrect upstream traffic report.
The prototype therefore demonstrates attribution integrity over supplied evidence, not end-to-end production verification of the report-to-burn-to-reward process.
6.2 Public verification versus restricted audit
The accounting architecture faces a disclosure problem.
Independent verification requires evidence. Yet exposing every traffic report, participant identifier, membership change and commercial agreement publicly could reveal information that synchronizer operators and participants have legitimate reasons to keep confidential.
The research proposes separating accounting information into three disclosure classes [4, 14].
Publicly verifiable evidence
Public verification should focus on facts that can be checked without exposing the underlying participant-level traffic.
Potentially public information includes:
	•	The registered synchronizer and designated paymaster.
	•	Public burn event identifiers.
	•	Burn amounts and relevant ledger timestamps.
	•	Finality evidence.
	•	Published schema and rule versions.
	•	Publicly disclosed allocation records, where their disclosure is authorised.
These records can support verification that a payment occurred and that published accounting relationships are internally consistent.
However, public burn evidence alone does not establish the traffic report that generated the payment. Nor does publishing an allocation prove that the underlying allocation history is complete.
Auditor-restricted evidence
An authorised auditor may require more detailed records to reconstruct the settlement.
This category may include:
	•	Exact interval traffic reports.
	•	Report signatures and digests.
	•	Settlement-binding attestations.
	•	Effective agreement terms and pricing schedules.
	•	Burn-to-obligation allocation records.
	•	Correction and supersession histories.
	•	Relevant participant membership evidence where the charging rules require it.
Access should be governed by an explicit audit purpose, authorised parties, retention requirements and a process for resolving disputes.
The auditor must be able to verify the accounting relationship without receiving unrelated transaction payloads or information outside the scope of the settlement.
Highly restricted operational evidence
Some information may be more sensitive than the accounting records needed for ordinary settlement verification.
Examples include:
	•	Participant-level traffic counters.
	•	Detailed join and departure times.
	•	Fine-grained utilisation patterns.
	•	Operational metadata that reveals synchronizer usage or business relationships.
This information should be exposed only when necessary for a defined verification or dispute process.
Transaction payloads and unrelated counterparty information are outside the proposed accounting disclosure surface.
This separation is a proposed least-disclosure architecture. It is not a description of the current permissions or access-control implementation of CIP-0132.
6.3 Aggregate disclosure and composition
Aggregating participant traffic can reduce direct exposure of individual activity. However, aggregation does not guarantee that individual values cannot be reconstructed.
The risk becomes particularly important when multiple reports cover overlapping participant groups.
Consider a synthetic example involving five participants:
Participant	Traffic units
P1	40
P2	30
P3	20
P4	10
P5	50
Suppose an accounting interface releases two aggregate values:
	•	Group A: P1, P2, P3 and P4, with a total of 100 units.
	•	Group B: P2, P3 and P4, with a total of 60 units.
Both groups contain at least three participants.
Subtracting the second aggregate from the first gives:
[
100-60=40
]
The result reveals P1’s individual traffic value.
This is a nested-cohort disclosure. The individual value becomes identifiable because the two reports differ by exactly one participant.
The example demonstrates why a minimum cohort-size threshold is not sufficient on its own. A threshold can restrict the size of individual releases while leaving their composition vulnerable to differencing.
A more general problem occurs when several overlapping aggregates are released.
Consider four participants with values:
[
A=40,\quad B=30,\quad C=20,\quad D=10
]
Suppose the system releases four totals:
[
A+B+C=90
]
[
A+B+D=80
]
[
A+C+D=70
]
[
B+C+D=60
]
Every release contains three participants. Nevertheless, summing the four equations gives:
[
3(A+B+C+D)=300
]
Therefore:
[
A+B+C+D=100
]
Subtracting each released total from 100 reveals the excluded participant:
[
A=100-60=40
]
[
B=100-70=30
]
[
C=100-80=20
]
[
D=100-90=10
]
The disclosure does not depend on any one release containing a single participant. It emerges from the mathematical composition of multiple releases.
The repository’s existing linear leakage analysis uses exact rational arithmetic and a row-space test to determine whether individual values are identifiable from a collection of aggregate equations.
The four-participant example above is a hand-derived analytical counterexample. It has not been added as an executable fixture in the research repository. Its purpose is to illustrate the general identifiability problem, not to claim that the proposed Canton interface currently permits these particular overlapping queries.
The threat model assumes that the observer knows the cohort membership associated with each release. Without that information, the inference problem may be different.
The experiment establishes a mathematical limitation of simple cohort-size controls. It does not establish an observed privacy incident or a vulnerability in a deployed Canton service.
6.4 Privacy controls and trade-offs
Several controls can reduce aggregate disclosure risk, but each introduces operational or economic costs.
Fixed cohorts
Restricting reports to predefined participant groups reduces the ability to construct arbitrary overlapping queries. This limits one source of differencing risk.
However, fixed cohorts can reduce reporting flexibility and may become difficult to maintain when participants join, leave or change synchronizers.
Query composition controls
A reporting system can maintain a history of previous releases and evaluate whether a proposed new release, combined with earlier releases, would reveal additional participant-level information.
This approach addresses the composition problem directly. It also introduces state-management requirements, query governance and a need to define which releases belong to the same disclosure context.
Coarser reporting windows
Longer reporting windows can reduce the temporal detail available to an observer. Delaying publication can also make it harder to correlate aggregates with external events or known membership changes.
The cost is reduced operational visibility and slower dispute resolution. Longer windows may also make it harder to identify when an accounting discrepancy occurred.
Rounding
Rounding aggregate values can make exact differencing less reliable.
However, rounding is not a general privacy guarantee. Repeated releases, carefully chosen queries or auxiliary knowledge may still permit useful inferences. Rounding can also introduce discrepancies into contractual accounting if applied to values used to calculate exact liabilities.
Differential privacy
Differential privacy provides a formal framework for limiting how much an aggregate release reveals about an individual’s participation. It can be appropriate for optional public analytics, usage statistics or ecosystem reporting.
Its application to exact contractual billing is more difficult. Adding noise to a liability measurement can create payment disputes and alter the amount owed. A practical design would generally separate exact, access-controlled settlement evidence from privacy-preserving public analytics.
Purpose-limited auditor access
Auditor access can be restricted by contractual purpose, authorisation, retention period and the specific settlement under review. This reduces unnecessary exposure of participant-level information.
However, access restrictions depend on institutional controls and cannot eliminate all disclosure risk. An auditor with access to detailed evidence remains a party that must be trusted and governed.
No single control resolves every privacy problem. A robust design is likely to combine restricted access, release-composition checks, coarse public reporting and exact evidence retained for authorised settlement review.
6.5 The verification-disclosure trade-off
Accounting transparency and commercial confidentiality are not necessarily opposites. They become difficult to reconcile when verification is treated as requiring universal access to the most detailed available records.
The proposed separation between public verification and restricted audit offers a different approach.
Public observers may be able to verify that a registered paymaster made a particular burn and that disclosed accounting records satisfy published consistency rules. An authorised auditor may be able to reconstruct the underlying liability using exact reports and agreement terms. Participant-level operational records can remain more restricted, with access granted only where the charging rules or a dispute require them.
This arrangement does not eliminate trust. It distributes trust across different evidence sources and access boundaries.
The public verifier must trust the authenticity of published ledger evidence. The auditor must trust the authority and completeness of restricted records. The parties must trust the process governing auditor access. The measurement system still requires independent assurance if the objective is to establish that all chargeable traffic was captured.
The distinction is important because cryptographic verification does not automatically solve disclosure. A proof can establish a particular statement about committed inputs without revealing those inputs, but only if the statement is correctly specified, the inputs are appropriately committed and the proof system’s assumptions are satisfied. It also cannot prove that omitted source events were included unless the measurement process is independently constrained.
6.6 Findings and limitations
The reward-attribution analysis identifies integrity requirements that a complete implementation should enforce, including identity consistency, authorised weights, rule versions, duplicate-record exclusion and deterministic reward calculation. The checked-in prototype evidence demonstrates a narrower reward-budget constraint. It does not demonstrate the complete I-10 validation checklist or end-to-end production reward attribution. [9, 13, 18, 25, 26]
The privacy experiments demonstrate that overlapping aggregate releases can reveal individual values even when each release satisfies a minimum cohort-size requirement. The repository's linear leakage analysis extends this examination to general linear identifiability under stated assumptions about cohort membership. [14, 16, 17]
The evidence remains bounded in both cases.
The reward model does not establish that the production reward system receives complete and authoritative traffic and payment evidence. The privacy experiments do not establish that CIP-0132 currently exposes the specific aggregate queries used in the synthetic examples. The proposed disclosure architecture is a design recommendation, not a verified description of deployed access controls.
The resulting design requirement is therefore twofold: reward attribution must remain traceable to authoritative accounting evidence, while independent verification should expose only the information necessary to establish the relevant accounting claim.

7. Economic and Operational Trade-offs
7.1 Assurance architectures
The accounting requirements identified in the preceding sections can be addressed through different assurance architectures. Each architecture provides a different balance between verification strength, information disclosure, operational complexity and reliance on trusted parties.
This research compares four conceptual approaches.
Architecture A: Public burn-only verification
The simplest approach relies primarily on public ledger evidence.
An observer can verify that a designated paymaster executed a burn and inspect the associated public payment records. The accounting relationship between the burn and the underlying traffic report remains dependent on the parties’ off-ledger records and commercial agreement.
This architecture has relatively low verification overhead. It also provides limited assurance about the accuracy of the reported activity, the calculation of the liability and the allocation of the payment across obligations.
Its main limitation is evidentiary: a public burn establishes a payment event, not the completeness of the measurement that generated the payment.

Architecture B: Signed reconciliation

This approach adds report-set digests, agreement verification, separately signed settlement-binding attestations and deterministic liability calculations. Source-report authentication remains a separate requirement.

The objective is to make the relationship between activity evidence, commercial terms and payment reproducible. An independent reviewer can verify that the supplied report set is bound to the correct obligation, that the applicable agreement is recognised and that the calculated liability matches the settlement evidence.
This architecture strengthens integrity and accountability without necessarily making participant-level traffic public.
Its limitation is that signatures and bindings authenticate supplied evidence. They do not independently establish source measurement completeness. The system also requires key management, authority registries, evidence retention and a process for handling corrections and disputes.
Architecture C: Independent confidential audit
This approach introduces an authorised independent reviewer with access to detailed evidence under controlled disclosure conditions.
The auditor can examine traffic reports, participant membership records where relevant, agreement terms, settlement bindings, burn allocations and correction histories. The objective is to provide stronger assurance about the evidence underlying the payment while restricting access to commercially sensitive information.
This architecture can address some of the trust concentration present when the operator and paymaster are responsible for producing and reconciling the same records.
Its effectiveness depends on the auditor’s independence, access to sufficiently complete source records, technical competence and institutional authority. An auditor cannot establish measurement completeness if the only available evidence comes from the same unverified source.
The approach also introduces audit fees, evidence-access procedures, confidentiality obligations, retention requirements and potential delays during disputes.
Architecture D: Cryptographic proof
A cryptographic-proof architecture attempts to establish selected accounting properties without disclosing all underlying records.
Depending on the design, proofs could demonstrate that a liability was calculated according to an authorised rule, that published allocations satisfy amount constraints, or that a set of committed reports meets specified consistency conditions.
This can reduce the need to disclose detailed commercial data to every verifier.
However, proofs establish statements about defined inputs and predicates. They do not automatically establish that the inputs represent all chargeable activity. A proof system also introduces circuit or program specification, trusted input commitments, proving and verification infrastructure, key or parameter management where applicable, and additional engineering and operational complexity.
Cryptographic proof is therefore not a substitute for measurement assurance. It can strengthen verification of a measurement record only to the extent that the source and completeness assumptions of that record are addressed separately.
7.2 Cost drivers and qualitative comparison

This comparison does not assign numerical costs to the four architectures. The available repository experiments compare assurance capabilities and qualitative implementation burdens; they do not provide a reproducible cost model for engineering effort, recurring operations, audit fees, proof generation or verification. Accordingly, the cost discussion is qualitative and conditional. It identifies likely cost drivers and trade-offs rather than estimating monetary expenditure, labour hours or expected losses. [15, 19, 27]
The four architectures introduce different categories of work:
| Architecture | Principal cost drivers | Operational burden | Main residual trust |
|---|---|---|---|
| Public burn-only verification | Public ledger access and basic payment-record interpretation | Low | Operator measurement and off-ledger agreement |
| Signed reconciliation | Report authentication, agreement and authority registries, binding attestations, evidence retention and corrections | Medium | Source measurement and signer authority |
| Independent confidential audit | Auditor fees, secure evidence access, audit procedures, confidentiality controls and dispute handling | Medium to high | Auditor independence, competence and source-record completeness |
| Cryptographic proof | Circuit or program specification, input commitments, proving infrastructure, verification, key or parameter management and maintenance | High initial engineering burden; recurring cost depends on proof design and workload | Input completeness, circuit correctness and governance |
These descriptions are analytical comparisons, not measured cost rankings. Their purpose is to expose the work and institutional arrangements each architecture requires.
Public burn-only verification has the smallest additional assurance surface, but it leaves the report-to-payment relationship dependent on off-ledger evidence. Signed reconciliation introduces more work to authenticate and preserve that relationship. Independent audit adds recurring review and evidence-access obligations. Cryptographic proof requires a carefully specified statement, trustworthy input commitments and maintained proving and verification infrastructure.
The economic case for each architecture depends on the value of the settlements being protected, the consequences of undetected errors, the frequency of disputes, the availability of independent evidence and the cost of operating the required controls.
The current research does not provide empirical values for these variables. It therefore cannot calculate break-even thresholds, expected losses avoided or a real-world return on assurance investment.

7.3 Operational consequences
The cost of an assurance architecture extends beyond its direct computation or audit expense.
Evidence retention. Stronger reconciliation requires historical reports, agreement versions, signatures, bindings, burn evidence and correction histories to remain available. Retention increases storage and governance requirements, but without it historical disputes may become impossible to reconstruct.
Key management. Signed agreements and settlement bindings require recognised signing authorities, secure key storage, rotation, revocation and effective-time rules. A technically valid signature is only useful if the authority behind the key is correctly represented.
Audit access. Independent confidential audit requires a process for granting access to detailed records without exposing unrelated participant or commercial information. This creates access-control, confidentiality and dispute-resolution obligations.
Reporting latency. Ten-minute reporting intervals create a natural accounting cadence, but settlement and verification may occur later. Stronger reconciliation can increase the time between activity consumption and final settlement, particularly when reports are incomplete or disputed.
Correction handling. Append-only corrections preserve historical evidence, but they create additional operational work. Parties must review adjustment candidates, determine whether payment or reward records require changes, and execute authorised settlement actions.
Operational independence. A stronger audit architecture requires a reviewer or evidence source that is meaningfully independent of the operator and paymaster. Independence cannot be obtained merely by assigning an audit role in software.
Privacy governance. More detailed evidence improves the ability to investigate disputes but increases the consequences of unauthorised disclosure. Data classification, purpose limitation, access logging and retention rules become part of the accounting system rather than optional administrative measures.
These consequences suggest that assurance should be designed around the specific accounting claim being verified. Requiring every participant to disclose every operational record for every settlement would impose costs and privacy exposure that may not be justified.
7.4 Limits of the comparison

The four architectures are conceptual assurance models, not four deployed Canton implementations. Their comparison is based on a research specification and a qualitative assessment of their capabilities, implementation requirements and residual trust assumptions. The ratings in the repository are analytical judgements, not measured performance, probabilities or production benchmarks. [15, 19, 27]

The comparison does not measure:
The model’s outputs should therefore be treated as a sensitivity framework rather than a benchmark.
There is also an important comparability limitation. The architectures do not necessarily provide identical assurance. Public burn-only verification provides a weaker evidence relationship than signed reconciliation. Independent audit may provide stronger source examination if complete independent records exist. Cryptographic proof may provide strong verification of specified predicates while leaving source measurement trust unresolved.
A lower modelled cost does not establish better value if the architecture fails to address the relevant risk. Conversely, a more expensive architecture is not automatically justified merely because it uses more sophisticated cryptography.

A defensible quantitative economic comparison would require measured operational costs, observed risk frequencies, the financial consequences of accounting errors and evidence about each control's detection effectiveness. Those inputs were not available for this study. The comparison therefore identifies cost categories and assurance trade-offs without claiming to estimate their monetary value.

7.5 Economic interpretation
The economic question is not whether maximum assurance is desirable in the abstract. It is whether the additional assurance addresses a material risk at a cost proportionate to the value being protected.
For example, signed reconciliation may be a practical improvement where the principal concern is report substitution, agreement mismatch or duplicated settlement credit. It adds evidence binding and deterministic checks without requiring all traffic records to become public.
Independent confidential audit may be justified where the value of the settlement, the concentration of measurement authority or the cost of disputes warrants additional review. Its value depends on whether the auditor can obtain evidence that is genuinely independent of the operator’s own reporting system.
Cryptographic proofs may become attractive where many independent parties need to verify accounting properties while underlying commercial data must remain confidential. Their value depends on whether the statements being proved address the actual trust problem, including the provenance and completeness of source measurements.

The research does not identify a universally optimal architecture. It establishes a qualitative progression of assurance mechanisms and the conditions under which each may be useful. The choice depends on the accounting risk being addressed, the independence and quality of available evidence, the confidentiality requirements and the operational capacity of the parties.
The principal economic constraint remains the measurement boundary. Additional downstream settlement verification can reduce accounting inconsistency, but it cannot compensate for the absence of reliable evidence about the activity being charged. [15, 19, 27]

8. Discussion

8.1 The accounting problem is a chain of dependent claims

The proposed dedicated-synchronizer paymaster model connects infrastructure consumption to payment and reward attribution. Each stage depends on evidence produced by an earlier stage.

The accounting chain can be represented as:

	1.	A synchronizer measures chargeable activity.
	2.	The operator reports the measured activity.
	3.	An authorised commercial agreement determines the liability.
	4.	A designated paymaster burns Canton Coin.
	5.	Activity and payment records contribute to reward attribution.
	6.	The parties reconcile the evidence and resolve discrepancies.

The chain creates several distinct verification questions. Was the activity measured completely? Does the report represent that measurement? Were the correct commercial terms applied? Does the burn settle the resulting liability? Was the payment attributed under the correct reward rules?

These questions cannot be collapsed into a single settlement check.

The research’s central finding is that payment reconciliation is not measurement assurance. A verifier can establish that a burn matches a reported liability without establishing that the report includes all chargeable activity.

This distinction matters because stronger downstream controls can create an appearance of accounting certainty while leaving the earliest and most consequential source assumption unresolved.

8.2 Assurance must be stated at the correct boundary

The prototype demonstrates that several accounting properties can be expressed as executable checks over supplied evidence.

The prototype also demonstrates a narrower reward-budget constraint over supplied evidence. The broader reward-attribution validation checklist remains a proposed requirement.

These are meaningful controls. They improve the ability to detect inconsistencies within an accounting record set.

They do not establish that the record set is complete, that the underlying burn evidence is authentic and final, or that every signer has the necessary legal and institutional authority.

The distinction can be expressed through three assurance layers:

Evidence integrity: Are the records internally consistent, authenticated and correctly bound?

Accounting correctness: Do the supplied records produce the correct liability, allocation and attribution under the stated rules?

Measurement assurance: Do the records represent all relevant chargeable activity?

The prototype provides the strongest evidence for the first two layers. The third remains dependent on source-system controls, independent records and operational verification.

A system should report these assurance states separately. A settlement should not be described as fully verified merely because its arithmetic and signatures pass.

8.3 The proposed model creates an institutional trust problem

The dedicated-synchronizer model places important responsibilities with the operator and designated paymaster.

The operator has access to the infrastructure and produces the activity evidence. The paymaster is responsible for settling the resulting liability. The commercial relationship between the parties determines pricing and may include discounts outside the public protocol.

This arrangement may be operationally efficient, but it concentrates several forms of authority:

	•	Authority over the measurement source.
	•	Authority over the report presented for settlement.
	•	Authority over the commercial terms applied to that report.
	•	Authority over the payment process.

The problem is not that these parties are necessarily dishonest. The problem is that the accounting model needs to distinguish between a party’s assertion and independent evidence supporting that assertion.

Separating agreement approval, report production, settlement binding and independent review can reduce some conflicts of interest. However, assigning separate software roles does not itself establish institutional independence.

A meaningful separation requires independently controlled keys, clearly scoped authority, access to relevant evidence and a defined process for challenging disputed records.

8.4 Privacy and verifiability are coupled design constraints

Public settlement records support transparency, but detailed traffic reports may expose commercially sensitive information.

The research’s aggregate-disclosure experiments demonstrate that a minimum cohort size does not, by itself, guarantee privacy against combinations of overlapping releases. Multiple individually acceptable aggregates can reveal information that no single release exposes.

This is a mathematical limitation of simple threshold-based disclosure policies, not evidence of an existing Canton privacy incident.

The design implication is that disclosure controls must consider the composition of information across releases. A system that checks only whether each individual aggregate meets a minimum cohort size can still permit reconstruction under suitable membership knowledge.

A practical architecture should distinguish public settlement verification from restricted accounting review. Public observers may need to verify burn events and authorised settlement metadata without receiving participant-level traffic records. An authorised reviewer may need more detailed evidence under controlled access.

The challenge is to provide enough information to verify the accounting claim without publishing more information than that claim requires.

Cryptographic techniques may help with selected verification tasks, but they cannot remove the need to define trustworthy inputs, authorised statements and appropriate disclosure policies.

8.5 The reward layer introduces a separate assurance dependency

Canton’s burn and activity-recording mechanisms connect synchronizer payments to the broader reward economy.

This creates a second accounting relationship beyond the operator-paymaster settlement: the relationship between recognised activity, payment evidence and reward attribution.

A correct burn does not automatically establish that the resulting reward attribution is correct. Attribution depends on the applicable rules, weights, identities, epochs and the integrity of the records used in the calculation.

The research design identifies these as validation requirements. The checked-in prototype evidence is narrower: it demonstrates a reward-budget bound, while the settlement-manifest tests cover interval, agreement, burn-uniqueness and payment-reconciliation checks [13, 18, 23, 24, 25, 26].

However, the upstream implementation evidence reviewed for this research does not establish that the complete report-to-burn-to-reward path is deployed and independently verified. The prototype’s reward calculations should therefore be understood as a model of accounting controls, not a production validation of Canton reward distribution.

The research prototype does not establish that the complete reward-attribution checklist is implemented. Its checked-in evidence demonstrates a narrower reward-budget constraint, while identity binding, authorised weights, rule versions, duplicate exclusion and full reward-calculation verification remain requirements for a more complete validation model. The upstream implementation evidence also does not establish that the entire report-to-burn-to-reward path is deployed and independently verified. The prototype's reward analysis should therefore be understood as a proposed accounting-control framework with limited executable evidence, not a production validation of Canton reward distribution. [6, 13, 18, 23, 24]

8.6 What stronger accounting can realistically guarantee

The research supports a bounded set of guarantees.

A system can verify that a supplied schedule is structurally complete relative to an authorised schedule anchor, provided the anchor’s authenticity and authority have been established independently. It can verify that a report set is bound to a specific settlement obligation. It can calculate a liability deterministically under an authorised pricing rule. It can ensure that recorded allocations do not exceed recorded burns or reuse the same evidence in conflicting claims. It can preserve correction history and validate supersession relationships.

Each guarantee depends on explicit assumptions.

The schedule anchor must be authentic and authorised. The report must be trustworthy as an input. The pricing agreement and signer authority must be valid. Burn records must be authentic and final. The allocation history must be complete. Reward rules must be authoritative and correctly versioned.

These assumptions are not weaknesses to hide. They define the boundary of what the accounting system actually proves.

A useful assurance statement should identify the verified property, the evidence used, the authority behind that evidence and the assumptions that remain unresolved.

8.7 Implications for the dedicated-synchronizer design

The analysis suggests several design improvements for the proposed model:

	1.	Make the reporting contract explicit. Define expected intervals, reporting deadlines, missing-report semantics, correction rules and the authoritative settlement window.
	2.	Bind reports to settlement obligations. Preserve report-set digests, agreement versions, interval identities, synchronizer identities and authorised settlement attestations.
	3.	Separate measurement status from settlement status. A reconciled burn should not imply complete measurement unless the measurement claim has separately established support.
	4.	Define authority scope. Signer roles should be scoped to the relevant entity, agreement or synchronizer, with explicit effective-time and revocation rules.
	5.	Preserve payment and correction history. Record burn event and finality timestamps, allocation history, supersession decisions and authorised adjustments.
	6.	Specify reward attribution inputs. Identify the authoritative activity records, reward-rule version, applicable weights and epoch boundaries.
	7.	Adopt composition-aware privacy controls. Evaluate cumulative disclosure across releases rather than relying exclusively on per-query cohort thresholds.
	8.	Define independent review conditions. Specify what records a reviewer can access, how independence is established and how disputed measurements are escalated.

These are design requirements derived from the accounting analysis. They should not be interpreted as claims that the proposed protocol already implements them.

8.8 Proposed Research and Implementation Priorities

The findings support further work in three distinct areas. These priorities are intended to guide subsequent research and implementation; they are not claims that the proposed controls are already part of the Canton protocol.

Protocol-level specification

The reporting and settlement model would benefit from more explicit definitions of chargeable events, reporting intervals, authoritative schedule references, settlement states and correction semantics. These definitions would reduce ambiguity about which activity creates liability and how discrepancies affect subsequent settlement and reward attribution.

Further work should determine which of these requirements need to be specified at the protocol level and which can remain implementation-specific.

Operator-level measurement and evidence controls

The most consequential unresolved issue is measurement completeness. Further research should examine how synchronizer operators could provide independently examinable evidence that reported activity corresponds to the underlying chargeable events.

Candidate mechanisms include independent measurement records, reconciliation between source counters and downstream reports, auditable event-processing procedures, and cryptographic commitments to retained source records. Each mechanism should be evaluated for independence, failure modes, operational cost and the strength of the claims it supports.

The objective is not to assume that an additional signature or commitment establishes completeness, but to identify evidence that meaningfully reduces reliance on an operator’s unverified reporting assertion.

Governance and independent verification

A stronger assurance model also requires explicit authority boundaries. Reporting identities, signing keys, agreement approvals and independent reviewers need defined scopes of authority, effective dates, revocation procedures and accountability.

Further work should examine how these authorities could be established and challenged, how independent reviewers obtain access to relevant evidence, and how corrections and disputes are handled without silently replacing historical accounting records.

Proposed research programme

A subsequent research phase should prioritise four deliverables:

	1.	A formal specification of the reporting, evidence and settlement interfaces, including correction and supersession rules.
	2.	An independently reproducible verification prototype that distinguishes report provenance, measurement completeness, liability calculation and settlement integrity.
	3.	An adversarial evaluation using missing, altered, duplicated and unauthorised records, alongside realistic correction and settlement scenarios.
	4.	An empirical assessment of verification overhead, privacy exposure and operational costs using representative data and clearly stated assumptions.

The results should establish which controls materially improve assurance, which trust assumptions remain unavoidable, and whether the benefits justify their operational and economic costs.

This staged approach provides a basis for moving from analytical findings to an evaluated technical proposal without assuming that every identified gap requires a protocol change.

8.9 Research contribution

The contribution of this work is an assurance framework for analysing the relationship between synchronizer activity, off-ledger commercial obligations, Canton Coin settlement and reward attribution.

It combines protocol-source analysis, implementation observations, executable accounting models, synthetic adversarial examples and a parameterised cost comparison.

The result is not a proof that the proposed paymaster model is unsafe or that a particular operator has misreported activity. Nor is it a claim that the prototype provides production-grade accounting assurance.

The contribution is more specific: it identifies which accounting properties can be checked over supplied evidence, which require independent source evidence, and which introduce economic, privacy or operational costs.

That separation provides a basis for evaluating proposed accounting guarantees without confusing payment correctness with measurement completeness.


9. Limitations and Future Research

9.1 Limitations of protocol and implementation evidence

This study examines a specific public-source snapshot of the Canton protocol and related implementation work from November 2026 [5, 6, 7, 10, 11, 20, 21, 22, 23, 24]. The principal protocol documents describe a proposed dedicated-synchronizer paymaster model, while several implementation components remain under development.

The source review does not constitute an audit of a deployed production system. Public repositories cannot establish the configuration, internal procedures or actual accounting practices of individual synchronizer operators and paymasters.

In particular, the research did not obtain:

	•	Complete production traffic reports from a dedicated synchronizer.
	•	Independent ground-truth measurements of chargeable activity.
	•	Authoritative bilateral pricing agreements.
	•	A complete production history of paymaster burns and their corresponding obligations.
	•	Internal reward-attribution records.
	•	Independent evidence that all stages of the proposed accounting chain operate together in production.

Consequently, the study identifies design requirements and prototype assurance properties. It does not establish that a Canton operator has under-reported activity, that a paymaster has made an incorrect payment or that rewards have been misallocated.

Protocol and implementation status can also change. Findings about open, merged or proposed changes describe the reviewed snapshot and should not be interpreted as permanent statements about the network.

9.2 Limitations of the prototype

The executable models operate on supplied records and explicit assumptions. They are not connected to a production synchronizer, paymaster or reward-distribution service.

Several important trust dependencies remain external:

	•	Authenticity and completeness of source measurements.
	•	Authority and scope of signing keys.
	•	Legal and institutional validity of commercial agreements.
	•	Authenticity and finality of burn evidence.
	•	Completeness of historical allocation records.
	•	Authoritative reward rules and their production enforcement.
	•	Durable storage and governance of processed correction identifiers.

The settlement-binding prototype authenticates a binding through a designated signer role. It does not establish that the signer is institutionally independent from the agreement signer. Nor does its generic role registry establish entity-scoped legal authority.

The correction model produces adjustment candidates and validates supersession relationships. It does not execute burn reversals, refunds, reward clawbacks or other settlement remedies.

The prototype’s deterministic pricing calculations have not been independently reproduced by a second implementation against authoritative production tariffs. Therefore, passing tests demonstrates consistency within the model, not independent confirmation that the model represents the actual commercial rules of a deployed synchronizer.

9.3 Limitations of the privacy experiments

The privacy experiments use synthetic participant values and constructed aggregate releases.

They demonstrate that overlapping aggregates can reveal individual values even when each release satisfies a minimum cohort threshold. The experiments assume that the verifier knows the relevant cohort membership and can combine the published results.

They do not establish that the current or proposed Canton reporting interface permits arbitrary overlapping participant-cohort queries. They also do not measure the practical likelihood of reconstruction under actual Canton access controls.

The results should therefore be interpreted as a design warning: minimum cohort size is not a sufficient general privacy guarantee when releases can be composed.

Future work should evaluate the actual reporting surface, access-control model, query capabilities and information available to different classes of observer.

9.4 Limitations of the economic model

This study does not contain a reproducible numerical assurance-cost model. The repository includes a comparative assurance specification and qualitative architecture assessments, but the inspected source snapshot does not contain the parameters, executable cost function or output-generating process required to reproduce the numerical ICU figures previously considered.
The economic comparison is therefore qualitative. It identifies implementation burden, recurring operator and auditor effort, evidence retention, privacy governance, latency and dispute resolution as relevant cost drivers. It does not estimate monetary expenditure, labour hours, expected losses or return on investment.
A quantitative evaluation would require operational data, including reporting volume, exception frequency, evidence-retention requirements, audit costs, dispute frequency, settlement values and the financial consequences of undetected errors. It would also require sensitivity analysis across different operator sizes, traffic volumes and commercial arrangements.
Until those inputs and a reproducible model are available, numerical cost rankings and break-even claims would be unsupported.

9.5 Measurement completeness remains unresolved

The largest unresolved question concerns the source of traffic evidence.

A verifier can check whether a report is structurally valid, whether expected intervals are present and whether a report is bound to a settlement obligation. But those checks do not establish that the underlying measurement process captured every chargeable event.

Resolving this question requires evidence beyond the report itself.

Potential approaches include:

	•	Independent measurement records produced by a separately controlled component.
	•	Reconciliation between source counters and downstream reporting records.
	•	Auditable event-processing and retention procedures.
	•	Independent operational inspection of measurement and aggregation logic.
	•	Cryptographic commitments to source records combined with verifiable completeness conditions.

Each approach has different costs and limitations. For example, a second measurement component is useful only if its failure modes and control are sufficiently independent. A cryptographic commitment can establish that a record has not changed since commitment, but cannot establish that the original record contained every relevant event.

Future research should compare these mechanisms against a clearly defined chargeable-event model rather than treating independent measurement as a generic solution.

9.6 Priority research questions

The following questions are the most important extensions of this study.

1. What constitutes a chargeable event?

The accounting model needs an explicit definition of which infrastructure events create liability, how participant entry and departure affect chargeability, and how events spanning reporting boundaries are handled.

2. What independent evidence can establish measurement completeness?

The next step is to identify evidence that can be compared against the operator’s report without relying exclusively on the same measurement pipeline.

3. How should signer authority be scoped?

A production design needs a precise relationship between signing keys, synchronizer identities, commercial agreements, authorised entities and effective dates.

4. How should payment finality and corrections interact?

The model should distinguish burn submission, confirmation and finality, and define the accounting consequences of corrections received after settlement.

5. What is the actual privacy exposure of the reporting interface?

This requires analysis of real reporting permissions, available aggregate queries, cohort membership visibility and cumulative disclosure across releases.

6. What are the measured costs of stronger assurance?

An empirical evaluation should collect operational costs and compare them with observed dispute rates, settlement values and the consequences of accounting errors.

7. How does reward attribution behave in the complete implementation?

The relationship between traffic reports, paymaster burns, activity recording and reward distribution requires end-to-end verification against the deployed implementation and authoritative reward rules.

These questions should be answered through source evidence, controlled experiments or operational data before stronger production claims are made.

9.7 Research boundary

The present study deliberately stops short of claiming that a complete production assurance architecture has been implemented.

Its prototype demonstrates how selected accounting invariants can be represented and tested. Its analytical experiments expose limitations in simple privacy thresholds and downstream reconciliation. Its cost model shows how additional assurance requirements can be translated into explicit economic assumptions.

The remaining work is not simply to add more checks. It is to establish the authority, independence and completeness of the evidence on which those checks depend.

That distinction determines the next stage of research.

10. Conclusion

The proposed dedicated-synchronizer paymaster model connects synchronizer activity to Canton Coin settlement and the wider reward economy. That connection creates an accounting requirement: parties must be able to establish how reported infrastructure consumption becomes a commercial liability, how that liability is settled and how the resulting activity is attributed.

This research examined the guarantees that can be added to that process and the economic, privacy and operational costs they introduce.

The prototype demonstrates that several important settlement properties can be expressed as executable controls. Expected reporting intervals can be validated against an explicit schedule. Reports can be bound to settlement obligations through signed attestations. Liabilities can be calculated deterministically under specified commercial terms. Recorded burns can be allocated across obligations without exceeding their recorded amounts or reusing evidence in conflicting claims. Correction and supersession records can also be checked against explicit rules. The reward-attribution analysis identifies a broader set of requirements, but the checked-in executable evidence is limited to a reward-budget constraint.

These controls strengthen the integrity of the accounting relationship. They do not independently establish the completeness of the original traffic measurement.

That is the central result of this study: a payment can be correctly reconciled against an incomplete report. A signature can authenticate a report without proving that the measurement process captured every chargeable event. A cryptographic proof can verify a calculation over committed inputs without proving that those inputs represent all relevant activity.

The distinction establishes a boundary for meaningful accounting guarantees. Settlement integrity, deterministic calculation and allocation correctness can be strengthened through software and verifiable evidence. Measurement completeness requires additional trust mechanisms, independent records or operational assurance.

The research also identifies a corresponding privacy constraint. Public verification does not require unrestricted disclosure of participant-level traffic data, but simple minimum-cohort thresholds do not prevent every form of aggregate reconstruction. Verification and disclosure must therefore be designed together.

The qualitative economic comparison identifies different cost drivers and trust assumptions across signed reconciliation, independent confidential audit and cryptographic proof. It does not establish numerical costs, break-even thresholds or a return on investment. The appropriate architecture depends on the risks being addressed, the evidence available and the value of the settlements being protected. The illustrative cost model provides a framework for evaluating these trade-offs, not a measurement of actual Canton operating costs.

The practical implication is that a dedicated-synchronizer accounting design should state precisely what has been verified, which evidence supports the claim, who is authorised to produce that evidence and which assumptions remain unresolved.

A stronger accounting system is not one that merely produces more signatures, proofs or reconciliation checks. It is one that makes the boundary between verified facts and trusted assumptions explicit.

References

1. Canton Foundation. *CIP-0104: Traffic-Based App Rewards*. Original proposal approved 12 February 2026; amendment aligning the proposal with Featured App Guidance 2.0b approved 27 October 2026. Pinned revision used for the dedicated-synchronizer extension-hook relationship: https://github.com/canton-foundation/cips/blob/92df641487c5e465dad5ea8d03245d3b9b328523/cip-0104/cip-0104.md.

2. Canton Foundation. *CIP-0129: Universal Burn and Synchronizer Pricing*. Approved 23 October 2026. https://github.com/canton-foundation/cips/blob/8e694e509c47ecb59e5731289882b350e3186372/cip-0129/cip-0129.md.

3. Canton Foundation. *CIP-0132: Dedicated Synchronizer Paymaster Model*. Proposed 16 November 2026; status Proposed in the reviewed revision. https://github.com/canton-foundation/cips/blob/538adf41789fa971f3ad397595de4549dd507e79/cip-0132/cip-0132.md.

4. Canton Network. *Privacy Model*. Developer documentation, accessed 17 November 2026. https://github.com/canton-network/cf-docs/blob/main/docs-main/appdev/deep-dives/privacy-model.mdx.

5. Canton Network. splice-multi-sync. Pull request #111, “Traffic report API and interval calculation.” Reviewed 17 November 2026; open at the reviewed snapshot. https://github.com/canton-network/splice-multi-sync/pull/111.

6. Canton Network. splice. Pull request #8449, “ActivityRecorder implementation.” Reviewed 17 November 2026; draft at the reviewed snapshot. https://github.com/canton-network/splice/pull/8449.

7. ChainSafe. canton-extending-mainnet. Issue #155, “Paymaster purchase path and amount checking.” Reviewed 17 November 2026. Issue-tracker evidence, not proof of production underpayment or misconduct. https://github.com/ChainSafe/canton-extending-mainnet/issues/155.

8. Canton Network. splice-multi-sync. Pull request #103, earlier traffic-report implementation. Historical implementation context; superseded by the design in PR #111. https://github.com/canton-network/splice-multi-sync/pull/103.

9. BigWave45. *Accounting Properties and Threat Model*. Canton Research Lab, research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/accounting-properties-and-threat-model.md.

10. BigWave45. *Traffic-Report Implementation Audit*. Canton Research Lab, research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/traffic-report-implementation-audit.md.

11. BigWave45. *Canton Implementation Evidence Map for the Settlement Accounting Interface*. Canton Research Lab, research artefact, 17 November 2026. https://github.com/BigWave45/canton-research-lab/blob/cfddf3a416d0b00284640dd27988d3ee800377f2/research/canton-implementation-evidence-map.md.

12. BigWave45. *Architecture Comparison: CIP-0104, CIP-0129 and CIP-0132*. Canton Research Lab, research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/cip-0104-0129-0132-architecture-comparison.md.

13. BigWave45. *Reward Attribution Integrity*. Canton Research Lab, research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/reward-attribution-integrity.md.

14. BigWave45. *Privacy Disclosure Matrix and Aggregate Leakage Experiment*. Canton Research Lab, research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/privacy-disclosure-matrix-and-leakage-experiment.md.

15. BigWave45. *Comparative Assurance Model Specification*. Canton Research Lab, research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/research/comparative-assurance-model-specification.md.

16. BigWave45. *Aggregate Linear Leakage Analysis*. Canton Research Lab, executable research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/aggregate_linear_leakage.py.

17. BigWave45. *Aggregate Disclosure Experiment*. Canton Research Lab, executable research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/aggregate_disclosure_experiment.py.

18. BigWave45. *Adversarial Accounting Tests*. Canton Research Lab, test artefact, snapshot 18 November 2026. Synthetic and prototype tests, not production integration tests. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/adversarial_accounting_tests.py.

19. BigWave45. *Comparative Assurance Model Code*. Canton Research Lab, executable research artefacts, snapshot 18 November 2026. Includes comparative_assurance_model.py and integrated_assurance_comparison.py; qualitative ratings are analytical judgements, not measured costs or probabilities. https://github.com/BigWave45/canton-research-lab/tree/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis.

20. Canton Network. splice-multi-sync. Pull request #100, “Paymaster traffic purchase support.” Merged source changes; merge status does not establish deployment to MainNet. https://github.com/canton-network/splice-multi-sync/pull/100.

21. Canton Network. splice-multi-sync. Pull request #104, “Scan and SV registered-synchronizer handling.” Merged source changes; merge status does not establish deployment to MainNet. https://github.com/canton-network/splice-multi-sync/pull/104.

22. ChainSafe. canton-extending-mainnet. Issue #152, “Traffic report API acceptance criteria.” Reviewed 17 November 2026. Acceptance criteria are requirements, not proof that they passed. https://github.com/ChainSafe/canton-extending-mainnet/issues/152.

23. ChainSafe. canton-extending-mainnet. Issue #159, “End-to-end paymaster flow test.” Reviewed 17 November 2026; open at the reviewed snapshot. The issue records a requested test sequence, not a passing end-to-end result. https://github.com/ChainSafe/canton-extending-mainnet/issues/159.

24. ChainSafe. canton-extending-mainnet. Issue #163, “ActivityRecorder integration.” Reviewed 17 November 2026. Tracked integration work, not proof of a completed production path. https://github.com/ChainSafe/canton-extending-mainnet/issues/163.

25. BigWave45. *Settlement Manifest Validator*. Canton Research Lab, executable research artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/settlement_manifest_validator.py.

26. BigWave45. *Settlement Manifest Validator Tests*. Canton Research Lab, test artefact, snapshot 18 November 2026. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/tests/test_settlement_manifest_validator.py.

27. BigWave45. *Integrated Qualitative Assurance Comparison*. Canton Research Lab, executable research artefact, snapshot 18 November 2026. Ratings are qualitative analytical judgements, not measured performance, probabilities or monetary costs. https://github.com/BigWave45/canton-research-lab/blob/ecd8e8bdccbe6dc2556d54e8a01fb4d962537d0c/analysis/integrated_assurance_comparison.py.
