# Adversarial accounting experiments: results and limitations

**Status:** synthetic demonstrations only. These tests do not interact with Canton nodes, contracts, paymaster services or production traffic.

## Test 1: omitted participant

Assume two participants consume 10 and 6 traffic units. The report includes only 10 units. At a list price of 1 CC/unit and a 10% discount:

- Report-implied liability: 9.00 CC.
- Burn: 9.00 CC.
- Actual-use-implied liability: 14.40 CC.
- Hidden difference: 5.40 CC.

The report-to-burn reconciliation passes while the actual-use liability is understated. This is a counterexample to the claim that a reconciled burn proves correct metering.

This is not a claim that the current Canton report implementation omits a participant in production. It demonstrates the logical limit of relying on the same report as both the liability input and evidence of completeness.

## Test 2: conflicting observer views

Two observers receive reports for the same synchronizer, interval and version, but one says 100 units and the other 92. Comparing deterministic report digests detects the conflict.

If only one observer has a report, its digest is internally consistent and does not reveal omission. Cross-observer comparison detects divergence, not which value is true. A signed digest or Merkle root has the same source-truth limitation.

## Test 3: reward budget

An abstract invariant rejects issuance of 11 units against an authorised budget of 10. However, issuance of 9 against a budget of 9 passes even if that budget was calculated from understated activity. The cap protects the downstream bound; it does not repair upstream measurement error.

## Results matrix

| Attack / failure | Synthetic detection | Additional evidence required |
|---|---|---|
| Omitted participant in aggregate report | Not detectable from report-to-burn reconciliation alone | Independent participant/traffic completeness evidence |
| Conflicting reports to different observers | Detectable if observers compare digests | Authenticated report identity and cross-observer gossip |
| Omission shown to one observer only | Not detectable from its digest alone | Independent source or completeness proof |
| Reward exceeds authorised budget | Detectable by invariant check | Correctly derived and authenticated budget |
| Understated activity and correspondingly low reward budget | Not detected by cap alone | Measurement integrity evidence upstream |

## Implications

The four pipeline questions must remain separate:

1. Did metering count the right traffic?
2. Did the paymaster settle the liability implied by the agreed pricing rules?
3. Was the burn uniquely and correctly attributed?
4. Did the reward system issue no more than the valid activity budget and distribute it under the applicable rules?

A design can satisfy questions 2 and 4 while failing question 1. A privacy-preserving commitment can make a report tamper-evident without proving it complete. Independent metering evidence, or an explicit operator-trust assumption, remains necessary.

## Limitations

- The omitted-participant example assumes a known actual-traffic reference solely to calculate the hidden difference. An external auditor may not possess that reference.
- Digest comparison uses SHA-256 as a deterministic illustration. It does not implement signed reports, a transparency log, Merkle inclusion proofs or gossip.
- The reward-budget check is an abstract upper-bound property, not a reproduction of Canton reward calculation.
- No cryptographic proof, hardware attestation or privacy leakage metric has been implemented.
- No result establishes an actual Canton exploit, real underpayment, production deployment or operator misconduct.
