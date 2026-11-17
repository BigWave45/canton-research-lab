# Signed agreement verification at the settlement boundary

**Status:** Synthetic research prototype, 17 November 2026.

The protocol-to-settlement reconciliation path now requires a trusted signer registry and a signed agreement binding for every expected interval.

Before pricing, the adapter reconstructs a canonical agreement document from the exact pricing object used by the liability calculator: agreement identity, version, effective dates, price bands, fixed fee, discount and rounding. It verifies the Ed25519 signature over those exact terms and checks signer authorisation, validity and revocation at the expected interval end.

This is stronger than verifying an arbitrary signed document. The signed terms are reconstructed from the pricing object actually used in the calculation, so a valid signature over different terms cannot authorise the tariff being applied.

## Failure behaviour

Missing registry, unknown pricing version, binding mismatch, malformed or invalid signature, unknown signer, unauthorised signer, revoked signer or invalid key validity block reconciliation. Missing traffic reports remain a separate coverage state; a signature does not turn missing evidence into zero consumption.

## Limits

The registry remains an external trust root. This prototype does not establish legal identity or capacity, traffic measurement truth/completeness, actual Canton tariff semantics or production readiness. Revocation is evaluated at the expected interval end. A production design needs an explicit signing-time and trusted-timestamp policy, key rotation, governance and dispute procedures.

This is a research model, not a claim about current Canton protocol implementation.
