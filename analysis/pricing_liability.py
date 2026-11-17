"""Deterministic liability calculation from an OK interval report and tariff.

Amounts use integer CC smallest units. This is a synthetic research model,
not a statement of Canton pricing or a deployed tariff.
"""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class PriceBand:
    upper_units_exclusive: int | None
    price_cc_per_unit: int

@dataclass(frozen=True)
class PricingAgreement:
    agreement_id: str
    version_id: str
    effective_from: str
    effective_until: str | None
    bands: tuple[PriceBand, ...]
    fixed_fee_cc: int = 0
    discount_basis_points: int = 0
    rounding: str = "CEILING"

def _time(value):
    parsed=datetime.fromisoformat(value.replace("Z","+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Timestamp must include UTC offset")
    return parsed

def calculate_liability(report, agreement: PricingAgreement) -> dict:
    if report.status != "OK":
        raise ValueError("Only OK reports can be priced")
    if report.agreement_version != agreement.version_id:
        raise ValueError("Report and pricing agreement versions differ")
    start=_time(report.interval_start)
    end=_time(report.interval_end)
    effective_from=_time(agreement.effective_from)
    effective_until=_time(agreement.effective_until) if agreement.effective_until else None
    if start < effective_from or (effective_until and end > effective_until):
        raise ValueError("Agreement version does not cover the full report interval")
    units=report.consumed_units
    if not isinstance(units,int) or units < 0:
        raise ValueError("consumed_units must be a non-negative integer")
    if agreement.fixed_fee_cc < 0 or not 0 <= agreement.discount_basis_points <= 10000:
        raise ValueError("Invalid fee or discount")
    if agreement.rounding not in {"CEILING","FLOOR","HALF_UP"}:
        raise ValueError("Unsupported rounding policy")
    if not agreement.bands:
        raise ValueError("At least one price band is required")
    previous=0
    remaining=units
    gross=0
    band_results=[]
    for band in agreement.bands:
        if band.price_cc_per_unit < 0:
            raise ValueError("Band price cannot be negative")
        upper=band.upper_units_exclusive
        if upper is not None and upper <= previous:
            raise ValueError("Price band limits must be strictly increasing")
        capacity=remaining if upper is None else min(remaining,max(0,upper-previous))
        charged=capacity*band.price_cc_per_unit
        band_results.append({"units":capacity,"price_cc_per_unit":band.price_cc_per_unit,"gross_cc":charged})
        gross+=charged
        remaining-=capacity
        if upper is None:
            break
        previous=upper
        if remaining==0:
            break
    if remaining:
        raise ValueError("Price bands do not cover all reported units")
    numerator=gross*(10000-agreement.discount_basis_points)
    denominator=10000
    if agreement.rounding=="CEILING":
        discounted=(numerator+denominator-1)//denominator
    elif agreement.rounding=="FLOOR":
        discounted=numerator//denominator
    else:
        discounted=(numerator+denominator//2)//denominator
    total=discounted+agreement.fixed_fee_cc
    return {
        "report_id":report.report_id,
        "agreement_id":agreement.agreement_id,
        "agreement_version":agreement.version_id,
        "consumed_units":units,
        "gross_variable_cc":gross,
        "discount_basis_points":agreement.discount_basis_points,
        "discounted_variable_cc":discounted,
        "fixed_fee_cc":agreement.fixed_fee_cc,
        "liability_cc":total,
        "rounding":agreement.rounding,
        "bands":band_results,
        "assumptions":["Tariff bands and discounts are supplied authoritative inputs.",
                       "The model does not establish source measurement completeness.",
                       "No actual Canton tariff is asserted."]
    }
