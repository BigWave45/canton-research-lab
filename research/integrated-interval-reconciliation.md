# Integrated Interval Coverage and Settlement Adjustments

**Status:** Synthetic integration specification.  
**Date:** 17 November 2026.

## Purpose

This layer connects expected interval coverage to the existing reconciliation model. It blocks final reconciliation when expected reports are missing, non-OK, late under the default policy, or structurally invalid.

## Correction accounting

A corrected report does not overwrite a prior settlement. The integration requires an agreement-aware liability calculation for the corrected report and compares it with the liability used by the prior settlement.

For a prior settled liability L_old and corrected liability L_new:

adjustment = L_new - L_old.

A positive adjustment represents additional liability; a negative adjustment represents a credit or reversal to be handled under the agreement. The model emits an immutable adjustment record with status REQUIRES_SEPARATE_SETTLEMENT. It does not silently rewrite the old settlement or assume that a credit can be netted automatically.

## Late-report policy

Late reports block settlement by default. A caller may explicitly allow them, in which case the result retains COMPLETE_WITH_LATE_REPORTS. This is a policy choice, not a claim about current Canton rules.

## Tests

Eight integration tests cover complete and missing coverage, late-report policy, missing corrected-liability inputs, positive and negative adjustments, and invalid correction lineage. Tests are authored but not executed.

## Limits

The integration is synthetic. It does not prove the expected schedule is authoritative, calculate revised liabilities from traffic quantities, establish source measurement completeness, or implement a legal dispute/credit process. Liability values must come from a separately validated agreement-aware calculation. No production Canton integration is claimed.
