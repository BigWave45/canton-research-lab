# Assurance-tier comparison: what each layer proves and costs

**Status:** preliminary qualitative comparison. No production implementation, measured operating cost or Canton performance claim is implied.

## 1. The question in plain language

A public CC burn proves that a burn happened. It does not, by itself, prove how much synchronizer traffic occurred or how much the paymaster was contractually required to pay.

An assurance mechanism adds evidence between the traffic report and the burn. The design choice is how much extra evidence is worth its cost.

## 2. Comparison

| Approach | What an independent party can check | What remains trusted | Privacy exposure | Relative implementation burden | Main limitation |
|---|---|---|---|---|---|
| Public burn only | Burn amount, event and finality, if exposed on-ledger | Traffic measurement, report, agreement and payment calculation | Low | Low | Does not connect payment to actual liability |
| Signed report plus independent auditor | Report origin, report completeness against supplied records, agreement calculation, burn allocation and due dates | Source meter accuracy; auditor competence and independence | Low public exposure; high-detail evidence is auditor-restricted | Medium | Public observers still rely on the auditor's attestation |
| Public commitment plus signed report | Report digest was committed and can be compared with the auditor's copy; later alteration can be detected | Source measurement and completeness; truth of original report | Low if only digest and carefully timed status are public | Medium | A hash proves consistency with a committed file, not that the file is correct |
| Proof-carrying settlement | A verifier can check specified arithmetic and allocation rules without seeing confidential values | Input completeness, source measurement, key security, proof-system correctness and governance | Potentially low; proof statement and metadata can still leak | High | Proves only the encoded statement over the supplied inputs |
| Independent source measurement or challenge | Can provide evidence that reported usage matches an independently observed measurement boundary | Independence and integrity of the measurement path; unobserved events and boundary assumptions | Depends on measurement granularity and access | High to very high | No measurement system automatically observes every relevant event |

“Relative burden” is an analytical estimate, not a measured cost. Actual cost depends on the existing operator stack, report API, agreement format, ledger interfaces, audit frequency and proof-system choice.

## 3. The key distinction: checking arithmetic versus checking reality

Suppose the operator reports 100 units of traffic and the pricing agreement says each unit costs 2 CC.

The calculation is:

100 × 2 = 200 CC

A signature can show which operator issued the report. A commitment can make later changes detectable. A proof can show that the stated formula was applied correctly. An auditor can inspect the supporting records.

None of those mechanisms alone proves that the meter counted all 100 units correctly.

This is the central boundary of the research: **calculation integrity is not the same as measurement integrity.**

## 4. Preliminary design recommendation

Evaluate a staged design rather than beginning with a zero-knowledge proof system:

**Stage A: exact auditor reconciliation**
- Canonical interval report with stable IDs and explicit missing-data states.
- Operator signature over the report.
- Versioned agreement and deterministic pricing inputs.
- Paymaster allocation manifest linking burns to obligations.
- Independent auditor checks completeness, pricing, due dates and allocation.
- Dispute and correction procedure.

**Stage B: public tamper-evidence**
- Publish or anchor a commitment to the canonical settlement manifest.
- Publish the relevant burn references and a carefully delayed settlement status.
- Let the auditor and paymaster demonstrate that their copies match the committed manifest.
- Do not publish participant-level counters or confidential agreement terms.

**Stage C: selective public proof, only if justified**
- Identify a specific public claim that cannot be checked adequately through the auditor model.
- Encode only that claim, such as an allocation-sum bound or consistency with a committed pricing rule.
- Compare proof generation, verification, integration and governance costs against the value of removing that specific trust assumption.

**Stage D: independent measurement, only where necessary**
- Test whether source completeness is a material unresolved risk.
- Consider independent counters, cross-checks or sampled challenges at the measurement boundary.
- Do not claim that a proof over operator-supplied counters independently verifies the counters themselves.

## 5. Decision rule for adding cryptography

A more complex cryptographic mechanism is justified only if all four conditions hold:

1. There is a clearly stated verification claim.
2. The current auditor-and-commitment design cannot establish that claim at an acceptable level of trust.
3. A specified proof system can establish it without requiring the confidential inputs to be revealed.
4. The added implementation, operational and governance burden is proportionate to the risk reduced.

If any condition fails, the simpler mechanism is preferable.

## 6. What we still need to establish

Before treating the staged design as a final recommendation, research must verify:
- which report fields and signatures the actual implementation exposes;
- whether report intervals can be independently reconstructed or only retrieved from the operator;
- how the paymaster's agreement and settlement schedule are represented;
- which burn events can be mapped to which obligations;
- what evidence an auditor could access under a realistic mandate;
- whether the public needs to verify arithmetic itself or only verify that an independent audit occurred.

The current CIP proposal and open implementation work do not establish all these details. Where they are absent, the paper must label the mechanism as a proposal and avoid presenting it as an available feature.

## 7. Current research position

The leading candidate is a staged combination: exact auditor reconciliation first, public commitments for tamper-evidence second, and selective cryptographic proofs only for a demonstrated public-verification gap.

This is a provisional research recommendation. It is not a claim that an auditor model has been deployed, that public commitments exist in the current paymaster implementation, or that a ZK proof is necessary.
