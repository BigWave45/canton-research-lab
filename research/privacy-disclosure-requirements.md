# Privacy Disclosure Requirements for Verifiable Paymaster Accounting

**Status:** Research requirements model; not a deployed Canton design, cryptographic protocol or formal privacy proof.  
**Model:** `analysis/disclosure_tiers.py`  
**Tests:** `tests/test_disclosure_tiers.py`

## Research question

What is the minimum evidence each participant needs to verify a specific accounting claim, and which information can remain confidential?

The model separates three roles:

1. **Public verifier:** checks public burn evidence and a privacy-preserving proof about the settlement manifest.
2. **Independent auditor:** receives controlled access to detailed reports, agreement terms, obligation allocations and source measurement records.
3. **Operator:** retains operational records needed to generate reports and perform settlement.

The role labels are functional. In a real deployment, the same organisation could occupy more than one role, which would change the independence assumptions.

## Evidence classes

| Evidence | Public verifier | Independent auditor | Operator |
|---|---|---|---|
| Public burn ID, amount, timestamp | Yes | Yes | Yes |
| Commitment to settlement manifest | Yes | Yes | Yes |
| Proof of allocation constraints | Yes | Can inspect / re-check | Can generate |
| Agreement-version reference | Yes | Yes | Yes |
| Exact per-synchronizer liabilities and allocations | No | Yes | Yes |
| Detailed interval measurement report | No | Yes | Yes |
| Source measurement records | No | Yes | Yes |
| Private transaction payloads | No | Not required by this accounting model | Access depends on existing Canton permissions |

The table specifies a candidate minimum-disclosure design. It does not assert that all these records currently exist in the CIP-0132 implementation.

## Claim-to-evidence mapping

| Claim | Minimum evidence needed in this model |
|---|---|
| A burn exists | Public burn record |
| Allocations are unique and do not exceed the burn | Public burn record, manifest commitment and proof of allocation constraints |
| Correct agreement version was used | Authoritative agreement-version reference |
| Each synchronizer's payment reconciles | Agreement reference, exact obligation/allocation data and burn record |
| Measurement matches source records | Interval report and independently inspectable source measurement records |
| Contents of a private transaction | Private transaction payload |

The public verifier can check the burn and a proof of allocation constraints without seeing exact per-synchronizer amounts, assuming the proof system is sound and the committed manifest is correctly bound to the burn.

The public verifier cannot independently recompute each confidential liability from exact agreement terms if those terms and amounts remain hidden. That stronger claim is delegated to the auditor or supported by a suitably specified proof.

## Important boundary: payload privacy versus measurement assurance

The accounting question does not automatically require disclosure of private transaction payloads. It may be possible for an auditor to inspect resource-consumption counters, signed interval reports, retention metadata and agreement terms without seeing transaction contents.

However, that separation is an architectural assumption requiring validation. If source measurement records expose party identities, transaction timing or activity patterns, they may still leak sensitive metadata even when payloads remain encrypted.

A claim that “payloads are private” is therefore weaker than a claim that “the accounting evidence reveals no sensitive information.” The latter requires a leakage analysis.

## Three disclosure layers

### Layer 1: Public verification

Candidate public fields:
- Burn identifier, amount and timestamp.
- Commitment to a canonical settlement manifest.
- Agreement-version reference or opaque version commitment.
- Proof result and public verification parameters.

Potentially public derived outputs:
- Proof that allocation identifiers are unique.
- Proof that total allocated amount does not exceed the burn.
- Proof that the manifest references the relevant burn.

Do not publish exact per-synchronizer amounts by default if public verification can be achieved through a proof.

### Layer 2: Controlled independent audit

Candidate auditor-only fields:
- Exact per-synchronizer obligation and allocation amounts.
- Executed agreement and version history.
- Interval-level traffic/resource reports.
- Source measurement records and retention/completeness evidence.
- Reconciliation and exception history.

Access should be scoped, logged and governed. Auditor independence is an institutional control, not a cryptographic property.

### Layer 3: Operationally confidential data

Private transaction payloads and party-level data should remain governed by Canton’s existing privacy and access model. The accounting design should not request these data unless a specific, justified measurement claim cannot be established without them.

## What this establishes and what it does not

The requirements model shows that the assurance claims are not all-or-nothing. Public verification of allocation arithmetic can be separated from confidential verification of source measurement.

It does not establish:
- That a particular proof system can implement every proposed public claim efficiently.
- That the commitment prevents omission of source activity.
- That the auditor's source records are complete or independent.
- That metadata leakage is negligible.
- That the current Canton paymaster proposal implements these disclosure layers.

A proof over a committed manifest can establish constraints over that manifest. It cannot prove that the manifest contains every chargeable event unless completeness is established by an additional trusted or independently verifiable mechanism.

## Next research task

Integrate the disclosure requirements with the comparative assurance scenarios. For each architecture, assess (a) what must be public, (b) what must be auditor-restricted, (c) what remains operationally private, and (d) which trust assumptions remain. Then add a qualitative operational-cost and latency model without inventing measured performance numbers.
