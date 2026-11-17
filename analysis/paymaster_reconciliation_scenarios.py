#!/usr/bin/env python3
"""Scenario model for dedicated-synchronizer traffic-to-burn reconciliation.

The inputs are hypothetical. They are not Canton operator observations, approved
pricing parameters, or a prediction of paymaster behaviour.

Run:
    python3 analysis/paymaster_reconciliation_scenarios.py
"""

from dataclasses import dataclass

USD_PER_MB = 60.0  # CIP-0129 snapshot value; time-sensitive, not immutable


@dataclass(frozen=True)
class Scenario:
    name: str
    actual_traffic_mb: float
    reported_multiplier: float
    paid_multiplier_of_report: float
    cc_usd_price: float
    app_activity_weight: float
    asset_activity_weight: float


SCENARIOS = [
    Scenario("exact report / full payment", 100, 1.00, 1.00, 0.80, 1.00, 0.50),
    Scenario("10% under-report / full reported payment", 100, 0.90, 1.00, 0.80, 1.00, 0.50),
    Scenario("10% over-report / full reported payment", 100, 1.10, 1.00, 0.80, 1.00, 0.50),
    Scenario("accurate report / 80% paid", 100, 1.00, 0.80, 0.80, 1.00, 0.50),
    Scenario("10% under-report / 80% paid", 100, 0.90, 0.80, 1.20, 1.00, 0.50),
]


def calculate(s: Scenario) -> dict[str, float | str]:
    if s.actual_traffic_mb <= 0:
        raise ValueError("actual_traffic_mb must be positive")
    if s.reported_multiplier < 0 or s.paid_multiplier_of_report < 0:
        raise ValueError("report and payment multipliers must be non-negative")
    if s.cc_usd_price <= 0:
        raise ValueError("cc_usd_price must be positive")
    if not 0 <= s.app_activity_weight or not 0 <= s.asset_activity_weight:
        raise ValueError("activity weights must be non-negative")

    actual_bytes = s.actual_traffic_mb * 1_000_000
    reported_bytes = actual_bytes * s.reported_multiplier
    purchased_bytes = reported_bytes * s.paid_multiplier_of_report
    gross_fee_usd = reported_bytes / 1_000_000 * USD_PER_MB
    burn_cc = gross_fee_usd / s.cc_usd_price

    coverage = purchased_bytes / actual_bytes
    unpaid_bytes = max(0.0, actual_bytes - purchased_bytes)
    overpaid_bytes = max(0.0, purchased_bytes - actual_bytes)
    report_error = (reported_bytes - actual_bytes) / actual_bytes
    underpayment_rate = unpaid_bytes / actual_bytes

    # CIP-0104 activity units are illustrative here: the paymaster implementation
    # computes purchased bytes multiplied by its registered activity weights,
    # rounded down. This model keeps fractional units to show scenario sensitivity.
    app_activity_units = purchased_bytes * s.app_activity_weight
    asset_activity_units = purchased_bytes * s.asset_activity_weight

    effective_cost_per_actual_mb = burn_cc * s.cc_usd_price / s.actual_traffic_mb

    return {
        "name": s.name,
        "actual_mb": s.actual_traffic_mb,
        "reported_mb": reported_bytes / 1_000_000,
        "purchased_mb": purchased_bytes / 1_000_000,
        "report_error_pct": report_error * 100,
        "payment_coverage_pct": coverage * 100,
        "unpaid_mb": unpaid_bytes / 1_000_000,
        "overpaid_mb": overpaid_bytes / 1_000_000,
        "burn_cc": burn_cc,
        "effective_cost_usd_per_actual_mb": effective_cost_per_actual_mb,
        "app_activity_units": app_activity_units,
        "asset_activity_units": asset_activity_units,
        "underpayment_rate_pct": underpayment_rate * 100,
    }


def main() -> None:
    print("ILLUSTRATIVE SCENARIOS ONLY")
    print(f"List-price input: USD {USD_PER_MB:.2f}/MB (CIP-0129 snapshot)")
    print()
    print(
        "Scenario | Actual MB | Report MB | Purchased MB | "
        "Coverage % | Unpaid MB | Burn CC | Effective USD/actual MB"
    )
    print("-" * 145)
    for scenario in SCENARIOS:
        r = calculate(scenario)
        print(
            f"{r['name']} | {r['actual_mb']:.2f} | {r['reported_mb']:.2f} | "
            f"{r['purchased_mb']:.2f} | {r['payment_coverage_pct']:.1f} | "
            f"{r['unpaid_mb']:.2f} | {r['burn_cc']:.2f} | "
            f"{r['effective_cost_usd_per_actual_mb']:.2f}"
        )
    print()
    print("Activity units are purchased bytes multiplied by the assumed weights.")
    print("The model excludes reward-pool issuance rates, operating costs, discounts,")
    print("taxes, dispute costs, and any participant-level pass-through.")
    print("The model does not assert that any operator has under- or over-reported.")


if __name__ == "__main__":
    main()
