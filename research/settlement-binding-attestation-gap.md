# Settlement Binding Attestation Gap

**Audit date:** 17 November 2026  
**Source:** `analysis/protocol_settlement_interface.py`, `analysis/agreement_verification.py`, and `tests/test_protocol_settlement_interface.py`  
**Status:** Source-level review of the synthetic research prototype. This is not a finding about a deployed Canton implementation.

## 1. Finding

The prototype verifies the signature on the canonical pricing-agreement document, but it does not cryptographically attest the `SettlementBinding` that connects a protocol interval report to a synchronizer, obligation and agreement version.

In `reconcile_protocol_evidence`, the verifier reconstructs a signed document from the `PricingAgreement` fields (agreement ID, version, effective dates, pricing bands, fixed fee, discount and rounding). It passes that document and `binding.signature_b64` to `verify_signed_agreement`.

The signed document does **not** include:
- `binding_id`;
- `interval_id`;
- `synchronizer_id`;
- `obligation_id`;
- `authority_reference`;
- the protocol report ID or digest being linked.

The `authority_reference` is checked only for non-empty content. It is not resolved against an authoritative registry or included in the signed payload. The trusted-key registry checks whether a key is marked authorised and valid/revoked at the supplied time; it does not establish the signer's legal capacity or mapping-specific authority for a synchronizer/obligation.

## 2. What the prototype currently proves

Given the trusted-key registry supplied to the verifier, a successful signature check establishes that:
1. the canonical pricing-agreement document matches the bytes signed by the key;
2. the signature verifies under that key;
3. the key is marked authorised and valid at the verification time in that supplied registry.

It does **not** establish that the signed agreement was correctly assigned to this interval, synchronizer or obligation. It also does not establish that the signer had authority to make that assignment.

This is an important distinction between **agreement integrity** and **settlement-binding integrity**.

## 3. Why it matters

The settlement adapter joins a protocol report to an off-ledger binding. If the binding metadata can be changed while retaining the same agreement signature, the signature alone does not reveal that the mapping changed.

Some incorrect mappings may be caught later by reconciliation constraints, such as a synchronizer mismatch against the obligation record. That is not a substitute for authenticating the mapping itself. A valid agreement signature can coexist with an unauthenticated interval-to-obligation assignment.

This is not evidence that a production Canton operator has misassigned a report. It is a limitation in the current research prototype and in the assurance claim we can make about it.

## 4. Evidence gap in the current tests

The current `tests/test_protocol_settlement_interface.py` checks valid reconciliation, missing and ambiguous bindings, invalid report payloads, invalid agreement signatures, unknown/revoked signers and missing trusted-key registry.

The test file now includes a controlled case that changes `authority_reference` while retaining the valid agreement signature. The adapter still returns `RECONCILED`. This directly demonstrates that this field is not covered by the signature. Other binding-field mutations have not yet been tested. The test is authored but has not been independently executed in a full-suite run on the latest branch head.

## 5. Next bounded experiment

Before changing the implementation, add a controlled test matrix that:
1. keeps the signed agreement document and signature constant;
2. changes one binding field at a time;
3. observes whether the adapter accepts, blocks or misroutes the report;
4. distinguishes failures caught by downstream obligation matching from failures caught by cryptographic attestation.

The test should include at least:
- altered authority reference;
- altered obligation ID to another valid obligation under the same agreement version;
- altered synchronizer ID where the case contains a matching obligation;
- altered interval ID within the expected interval set;
- report ID/digest substitution if report identity is added to the binding model.

## 6. Candidate design response

A stronger interface would use two distinct attestations:

- **Agreement signature:** signs the canonical commercial terms and effective dates.
- **Settlement-binding attestation:** signs the binding ID, protocol report ID/digest, interval, synchronizer ID, obligation ID, agreement ID/version, authority reference and mapping-effective time.

The binding signer registry would need role and scope constraints (for example, which operator or governance authority may bind which synchronizer and obligation), plus enrolment, rotation, revocation and audit procedures.

This is a candidate design, not an implemented feature. Even a correctly signed binding would establish who authorised the mapping, not whether the underlying traffic measurement was complete.

## 7. Research implication

The assurance architecture must not collapse agreement signature verification and settlement-binding authentication into one claim. The paper should report them as separate properties:

1. agreement content integrity;
2. authority of the agreement signer;
3. integrity and authority of the report-to-obligation mapping;
4. measurement completeness;
5. liability calculation and payment reconciliation.

A cryptographic proof over the final manifest can prove predicates over that manifest only after the manifest's provenance and mapping authority have been established.
