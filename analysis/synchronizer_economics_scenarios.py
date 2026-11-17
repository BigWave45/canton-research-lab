#!/usr/bin/env python3
"""Illustrative Canton synchronizer pricing sensitivity model.

All discount, collateral, financing-rate, and throughput values in SCENARIOS
are analyst-selected examples, not approved CIP-0129 parameters or observed
participant data. The USD 60/MB list price is the value stated in CIP-0129
as of its approval snapshot and must be updated if governance changes it.

Run with: python3 analysis/synchronizer_economics_scenarios.py
No third-party dependencies.
"""

from dataclasses import dataclass

LIST_PRICE_USD_PER_MB = 60.0  # CIP-0129 stated current GS list price; time-sensitive


@dataclass(frozen=True)
class Scenario:
    name: str
    traffic_mb: float
    effective_discount: float
    collateral_usd_equivalent: float
    annual_carry_rate: float
    commitment_years: float


SCENARIOS = [
    Scenario("low traffic / no discount", 100, 0.00, 100_000, 0.10, 1),
    Scenario("medium traffic / 10% discount", 1_000, 0.10, 100_000, 0.10, 1),
    Scenario("high traffic / 10% discount", 10_000, 0.10, 100_000, 0.10, 1),
    Scenario("high traffic / 25% discount", 10_000, 0.25, 100_000, 0.10, 1),
    Scenario("high traffic / 10% discount / 20% carry", 10_000, 0.10, 100_000, 0.20, 1),
]


def calculate(s: Scenario) -> dict[str, float | str]:
    if s.traffic_mb < 0:
        raise ValueError("traffic_mb must be non-negative")
    if not 0 <= s.effective_discount < 1:
        raise ValueError("effective_discount must be in [0, 1)")
    if s.collateral_usd_equivalent < 0:
        raise ValueError("collateral must be non-negative")
    if s.annual_carry_rate < 0 or s.commitment_years < 0:
        raise ValueError("carry rate and commitment duration must be non-negative")

    gross_fee = LIST_PRICE_USD_PER_MB * s.traffic_mb
    discounted_fee = gross_fee * (1 - s.effective_discount)
    fee_saving = gross_fee - discounted_fee
    collateral_carry = (
        s.collateral_usd_equivalent * s.annual_carry_rate * s.commitment_years
    )
    net_modelled_benefit = fee_saving - collateral_carry
    required_discount = (
        collateral_carry / gross_fee if gross_fee > 0 else float("inf")
    )
    return {
        "name": s.name,
        "traffic_mb": s.traffic_mb,
        "gross_fee_usd": gross_fee,
        "effective_discount": s.effective_discount,
        "discounted_fee_usd": discounted_fee,
        "fee_saving_usd": fee_saving,
        "collateral_carry_usd": collateral_carry,
        "net_modelled_benefit_usd": net_modelled_benefit,
        "break_even_discount": required_discount,
    }


def main() -> None:
    print("ILLUSTRATIVE ONLY — not actual Canton prices after discounts")
    print(f"List price assumption: USD {LIST_PRICE_USD_PER_MB:,.2f}/MB")
    print()
    headers = (
        "Scenario",
        "Traffic MB",
        "Gross USD",
        "Discount",
        "Fee saving",
        "Collateral carry",
        "Net benefit",
        "Break-even discount",
    )
    print(" | ".join(headers))
    print("-" * 132)
    for scenario in SCENARIOS:
        row = calculate(scenario)
        print(
            f"{row['name']} | "
            f"{row['traffic_mb']:,.0f} | "
            f"{row['gross_fee_usd']:,.2f} | "
            f"{row['effective_discount']:.1%} | "
            f"{row['fee_saving_usd']:,.2f} | "
            f"{row['collateral_carry_usd']:,.2f} | "
            f"{row['net_modelled_benefit_usd']:,.2f} | "
            f"{row['break_even_discount']:.1%}"
        )

    print()
    print("Interpretation:")
    print("- Net benefit = modelled fee saving minus collateral carrying cost.")
    print("- It excludes operating costs, shortfall penalties, CC price risk,")
    print("  rewards, taxes, and any existing synchronizer license or service cost.")
    print("- Discount values and collateral examples are ASSUMED, not protocol terms.")
    print("- A negative net benefit means the assumed discount does not offset")
    print("  the assumed collateral carrying cost in this simplified model.")


if __name__ == "__main__":
    main()
