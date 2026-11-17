# Multi-Interval and Correction Edge-Case Review

**Status:** Synthetic edge-case specification.  
**Date:** 17 November 2026.

## Defect addressed

The previous pricing integration assigned a liability to an obligation for each interval in sequence. If several intervals belonged to one obligation, a later interval could overwrite an earlier interval's liability. The integration now sums separately priced interval liabilities for each obligation before payment reconciliation.

The pricing path also now requires an explicit synchronizer identity on every interval report and checks it against the bound obligation. Missing identity is rejected rather than treated as a successful binding.

## Added cases

1. Two ten-unit intervals contribute 20 CC to one obligation; 20 CC of burn allocation reconciles.
2. Missing synchronizer identity is rejected.
3. A correction from 10 to 8 units produces a negative 2 CC adjustment, without rewriting the prior settlement.
4. A report claiming the wrong synchronizer is rejected.

## Interpretation

These tests check aggregation and identity-binding logic under synthetic inputs. A negative adjustment is only a credit candidate requiring separate agreement/governance handling; this model does not automatically refund or net it. The model still assumes source measurement completeness and an authoritative schedule/tariff.

## Validation status

Four tests are authored but have not been executed. The previous test inventory also remains unexecuted after the latest integration changes. A full checkout-based run is required before the model can be called validated.
