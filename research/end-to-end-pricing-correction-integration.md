# End-to-End Pricing and Correction Integration

**Status:** Synthetic research implementation.  
**Date:** 17 November 2026.

## Purpose

This integration closes the previous gap where a corrected report's revised liability had to be supplied manually. The integration now prices the latest valid interval report against an explicitly supplied agreement schedule, binds it to an obligation, and calculates any adjustment against the prior settled liability.

## End-to-end path

Expected interval -> append-only report versions -> coverage validation -> agreement-version and effective-time validation -> tariff calculation -> obligation binding -> payment reconciliation -> separate correction adjustment.

## Example

A synthetic tariff charges 1 CC per measured unit. The original report records 10 units and the prior settlement records 10 CC. A valid correction records 12 units. The calculator produces a revised liability of 12 CC and an adjustment of +2 CC.

The original settlement remains unchanged. The additional 2 CC is marked REQUIRES_SEPARATE_SETTLEMENT. Since only 10 CC has been allocated against a revised 12 CC liability, current reconciliation reports SHORT_PAID.

## Validation scope

Three new tests cover original report pricing, upward correction and adjustment, and synchronizer-binding mismatch. Tests are authored but not executed.

## Limitations

This is synthetic and implementation-neutral. The tariff is supplied as an authoritative input; no actual Canton pricing schedule is asserted. The model still assumes the report's measured units are complete and truthful. It does not implement credit settlement, legal dispute handling, cryptographic proofs or live Canton integration.
