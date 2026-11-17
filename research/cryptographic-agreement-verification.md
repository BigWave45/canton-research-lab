# Cryptographic Verification of Off-Ledger Agreements

**Status:** Synthetic Ed25519 verification module.  
**Date:** 17 November 2026.

## What is verified

The module canonicalises a structured agreement document as deterministic JSON, hashes it with SHA-256, and verifies an Ed25519 signature over those exact bytes. It checks the signing key against a supplied trusted-key registry, including authorisation, validity dates and revocation.

A valid result establishes:
- the signed document has not changed relative to the signed bytes;
- the signature verifies under the registered public key;
- the key is marked authorised and valid at the supplied verification time.

## What is not verified

A signature alone does not establish the real-world identity of the key holder, their legal capacity, or whether the key registry is correct. The registry must be provisioned, governed, updated and audited through a trusted process. The module does not authenticate legal contracts, resolve disputes, verify traffic measurement, or establish that an agreement is enforceable.

The signer registry is an explicit trust root. If an attacker can alter it, they can substitute authorised keys. Production use would need controlled key enrolment, multi-party approval, rotation, revocation, timestamping and durable audit logs.

## Cryptographic construction

- Canonical payload: UTF-8 JSON with sorted keys, compact separators, no NaN/Infinity.
- Digest: SHA-256, used as a stable document fingerprint.
- Signature: Ed25519 over the canonical document bytes.
- Verification: Ed25519 public-key verification using the trusted registry.

Private keys are generated only inside tests. No production keys or secrets are stored in this repository.

## Test cases

Seven tests cover valid verification, document modification, unknown key, unauthorised key, revoked key, expired key and timezone-naive verification time.

## Research relevance

This layer strengthens agreement authenticity and integrity for the signed-reconciliation architecture. It does not solve measurement completeness. The independent-audit and proof architectures retain distinct assurance properties. The comparative model should not award measurement assurance merely because an agreement signature is valid.
