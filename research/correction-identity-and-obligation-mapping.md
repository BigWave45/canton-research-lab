# Correction Identity and Obligation-Mapping Boundary

**Status:** Synthetic model rule.  
**Date:** 17 November 2026.

## Supported mapping

The current model represents one expected interval as one report-version chain. Each synthetic report record is currently associated with one synchronizer ID, one obligation ID and one agreement version. These are model-side settlement-linkage fields, not fields exposed by the inspected CIP-0132 traffic-report API. The protocol report itself contains interval boundaries, status and an aggregate byte count. Multiple intervals may map to one obligation, and their priced liabilities are summed.

The current model does not represent one interval split across multiple obligations. No evidence has been established that this is required by the proposed paymaster model. It is therefore excluded rather than assumed.

## Correction identity invariant

A correction may revise report content such as measured units, but it must preserve the original interval's accounting identity:

(synchronizer_id, obligation_id, agreement_version).

Any correction revision that changes one of these fields is rejected as INVALID with reason CORRECTION_BINDING_CHANGED. This prevents a corrected quantity from silently being reassigned to a different synchronizer, commercial obligation or tariff version.

## Tests

Five tests cover a valid quantity correction and attempted changes to synchronizer, obligation and agreement version, including a binding change in a later revision.

## Limitations and open evidence question

This rule is a conservative modelling choice, not a verified Canton protocol requirement. The traffic-report endpoint does not itself carry obligation or agreement identifiers; the model currently attaches them as off-ledger mapping metadata. See [protocol report and commercial obligation boundary](protocol-report-to-commercial-obligation-boundary.md). A real agreement amendment or synchronizer migration may require an explicit, separately authorised reassignment process. It should not be represented as an ordinary correction.

The model still assumes that one interval maps to one obligation in its synthetic settlement-binding layer. CIP-0132 does not establish this cardinality. If primary documentation or implementation evidence shows otherwise, the data model must be revised with an explicit allocation object and conservation rule rather than silently allowing many-to-many mapping.
