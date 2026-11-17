"""Synthetic reconciliation experiment for a proposed dSync paymaster pipeline.

This is a transparent research simulator, not a Canton protocol implementation.
It tests whether agreement-aware window reconciliation avoids false alarms
caused by discounts and delayed/smoothed burns, while detecting injected
underpayment once the settlement window closes.

Run:
    python analysis/paymaster_reconciliation_experiment.py
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable


D = Decimal


@dataclass(frozen=True)
class Interval:
    index: int
    reported_units: Decimal
    status: str = "ok"


@dataclass(frozen=True)
class Burn:
    interval_index: int
    amount_cc: Decimal


@dataclass(frozen=True)
class Agreement:
    price_per_unit: Decimal
    discount_rate: Decimal = D("0")
    settlement_delay_intervals: int = 0
    rounding_quantum: Decimal = D("0.01")

    def payable(self, units: Decimal) -> Decimal:
        gross = units * self.price_per_unit
        net = gross * (D("1") - self.discount_rate)
        return net.quantize(self.rounding_quantum, rounding=ROUND_HALF_UP)


def expected_total(intervals: Iterable[Interval], agreement: Agreement) -> Decimal:
    usable = [i for i in intervals if i.status == "ok"]
    return sum((agreement.payable(i.reported_units) for i in usable), D("0"))


def interval_equality_flags(
    intervals: list[Interval], burns: list[Burn], agreement: Agreement
) -> list[int]:
    """Naive comparison: each interval's expected payable vs burn tagged to it."""
    burn_by_interval: dict[int, Decimal] = {}
    for burn in burns:
        burn_by_interval[burn.interval_index] = (
            burn_by_interval.get(burn.interval_index, D("0")) + burn.amount_cc
        )
    flags = []
    for interval in intervals:
        if interval.status != "ok":
            continue
        expected = agreement.payable(interval.reported_units)
        actual = burn_by_interval.get(interval.index, D("0"))
        if actual != expected:
            flags.append(interval.index)
    return flags


def window_reconciliation(
    intervals: list[Interval],
    burns: list[Burn],
    agreement: Agreement,
    tolerance: Decimal = D("0.01"),
) -> tuple[Decimal, Decimal, Decimal, bool]:
    """Reconcile all burns over the completed settlement window."""
    expected = expected_total(intervals, agreement)
    actual = sum((b.amount_cc for b in burns), D("0"))
    residual = expected - actual
    return expected, actual, residual, abs(residual) <= tolerance


def make_scenario(
    name: str,
    units: list[str],
    price: str,
    discount: str,
    burn_schedule: list[tuple[int, str]],
    expected_reconciles: bool,
) -> dict:
    agreement = Agreement(D(price), D(discount))
    intervals = [Interval(i, D(v)) for i, v in enumerate(units)]
    burns = [Burn(i, D(v)) for i, v in burn_schedule]
    naive = interval_equality_flags(intervals, burns, agreement)
    expected, actual, residual, reconciled = window_reconciliation(
        intervals, burns, agreement
    )
    assert reconciled is expected_reconciles, (
        name, expected, actual, residual, reconciled
    )
    return {
        "name": name,
        "interval_flags": naive,
        "expected_cc": expected,
        "burned_cc": actual,
        "residual_cc": residual,
        "window_reconciled": reconciled,
    }


def main() -> None:
    # 4 intervals × 10 units × 1 CC/unit × 10% discount = 36 CC.
    # Burns are deliberately smoothed: zero in early intervals, then 36 CC.
    smoothed = make_scenario(
        "permitted aggregate/smoothed settlement",
        ["10", "10", "10", "10"],
        "1",
        "0.10",
        [(3, "36.00")],
        True,
    )

    # Same expected amount, but 4 CC is withheld. Window reconciliation must flag it.
    underpaid = make_scenario(
        "injected 4 CC shortfall",
        ["10", "10", "10", "10"],
        "1",
        "0.10",
        [(3, "32.00")],
        False,
    )

    # Full payment with a discount: an undiscounted model would falsely flag 4 CC.
    discounted = make_scenario(
        "valid contractual discount",
        ["10", "10", "10", "10"],
        "1",
        "0.10",
        [(0, "36.00")],
        True,
    )

    for scenario in (smoothed, underpaid, discounted):
        print(f"\n{scenario['name']}")
        print(f"  naive interval flags: {scenario['interval_flags']}")
        print(f"  expected CC:          {scenario['expected_cc']}")
        print(f"  burned CC:            {scenario['burned_cc']}")
        print(f"  residual CC:          {scenario['residual_cc']}")
        print(f"  window reconciled:    {scenario['window_reconciled']}")

    assert smoothed["window_reconciled"]
    assert underpaid["residual_cc"] == D("4.00")
    assert not underpaid["window_reconciled"]
    assert discounted["window_reconciled"]


if __name__ == "__main__":
    main()
