# Correction Identity and Obligation-Mapping Boundary

**Status:** Synthetic model rule.  
**Date:** 17 November 2026.

## Supported mapping

The current model represents one expected interval as one report-version chain. Each report version carries one synchronizer ID, one obligation ID and one agreement version. Multiple intervals may map to one obligation, and their priced liabilities are summed.

The current model does not represent one interval split across multiple obligations. No evidence has been established that this is required by the proposed paymaster model. It is therefore excluded rather than assumed.

## Correction identity invariant

A correction may revise report content such as measured units, but it must preserve the original interval's accounting identity:

(synchronizer_id, obligation_id, agreement_version).

Any correction revision that changes one of these fields is rejected as INVALID with reason CORRECTION_BINDING_CHANGED. This prevents a corrected quantity from silently being reassigned to a different synchronizer, commercial obligation or tariff version.

## Tests

Five tests cover a valid quantity correction and attempted changes to synchronizer, obligation and agreement version, including a binding change in a later revision.

## Limitations and open evidence question

This rule is a conservative modelling choice, not a verified Canton protocol requirement. A real agreement amendment or synchronizer migration may require an explicit, separately authorised reassignment process. It should not be represented as an ordinary correction.

The model still assumes that one interval maps to one obligation. If primary documentation or implementation evidence shows otherwise, the data model must be revised with an explicit allocation object and conservation rule rather than silently allowing many-to-many mapping.
