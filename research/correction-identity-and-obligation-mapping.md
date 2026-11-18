# Correction Identity and Obligation-Mapping Boundary

**Status:** Synthetic model rule.  
**Date:** 17 November 2026.

## Supported mapping

The current model represents one expected interval as one report-version chain. Each synthetic report record is associated with one paymaster ID, synchronizer ID, obligation ID, agreement version and authority reference. The latter are model-side settlement-linkage fields, not fields exposed by the inspected CIP-0132 traffic-report API. The protocol report itself contains interval boundaries, status and an aggregate byte count; the paymaster and commercial metadata come from the separately signed settlement binding. Multiple intervals may map to one obligation, and their priced liabilities are summed.

The current model does not represent one interval split across multiple obligations. No evidence has been established that this is required by the proposed paymaster model. It is therefore excluded rather than assumed.

## Correction identity invariant

A correction may revise report content such as measured units, but it must preserve the original interval's accounting identity:

(paymaster_id, synchronizer_id, obligation_id, agreement_version, authority_reference).

Any correction revision that changes one of these fields is rejected as INVALID with reason CORRECTION_BINDING_CHANGED. This prevents a corrected quantity from silently being reassigned to a different synchronizer, commercial obligation or tariff version.

The current coverage evaluator requires a single predecessor chain with contiguous revisions, rejects forks and cycles, and prices only the terminal valid revision. The protocol adapter requires an updated binding attestation over the report set and compares the authority reference and binding identities with the prior settlement snapshot. This is a conservative prototype control; the relevant CIPs do not specify historical correction authority or a new-versus-prior binding migration process.

## Tests

Tests cover valid quantity corrections, attempted changes to paymaster, synchronizer, obligation and agreement version, report-set rebinding, and authority continuity against the prior settlement.

## Limitations and open evidence question

This rule is a conservative modelling choice, not a verified Canton protocol requirement. The traffic-report endpoint does not itself carry paymaster, obligation, agreement or authority identifiers; the model attaches them as separately signed off-ledger mapping metadata. See [protocol report and commercial obligation boundary](protocol-report-to-commercial-obligation-boundary.md). A real agreement amendment, paymaster change or synchronizer migration may require an explicit, separately authorised reassignment process. It should not be represented as an ordinary correction.

The model still assumes that one interval maps to one obligation in its synthetic settlement-binding layer. CIP-0132 does not establish this cardinality. If primary documentation or implementation evidence shows otherwise, the data model must be revised with an explicit allocation object and conservation rule rather than silently allowing many-to-many mapping.
