# Agreement-Aware Liability Calculation

**Status:** Synthetic research model, not a Canton tariff implementation.  
**Date:** 17 November 2026.

## Why this component is needed

The interval-correction integration deliberately refused to invent a revised liability. A corrected report must be repriced under the agreement version applicable to that interval. This module supplies that calculation from explicit, versioned tariff inputs.

## Calculation

For a report with measured units q, progressive price bands produce gross variable liability:

G(q) = sum over bands j of q_j * p_j, where q_j is the quantity falling in band j and p_j is that band's integer CC price per unit.

A discount d in basis points is applied as:

V = round_policy(G * (10,000 - d) / 10,000)

Total liability L = V + fixed_fee.

The rounding policy is explicit: CEILING, FLOOR or HALF_UP. Monetary values are integer CC smallest units; floating-point arithmetic is not used.

## Version controls

The report must have status OK, name the same agreement version as the supplied pricing schedule, and fall entirely within that version's effective interval. The tariff bands must cover all reported units.

## Correction use

For a corrected report r_new, calculate L_new using the same authoritative agreement version that governs its interval. Compare L_new with the liability recorded in the prior settlement:

adjustment = L_new - L_old.

A positive result is additional liability; a negative result is a credit candidate. The adjustment is recorded separately. Whether a credit can be netted or refunded is an agreement and governance question, not determined by this arithmetic.

## Tests

Ten unit tests cover flat and progressive tariffs, discounts, rounding, version mismatch, non-OK reports, effective-time boundaries, negative quantities and incomplete tariff bands. They are authored but not executed.

## Limitations

The tariff inputs are synthetic and supplied by the caller. This model does not establish that an agreement was legally authorised, that measured units are truthful or complete, or that any actual Canton dedicated-synchronizer tariff uses these parameters. It prices a report; it does not independently validate the meter.
