"""Synthetic paymaster reconciliation model.

This is a research simulator, not a Canton protocol implementation.
It tests accounting logic under incomplete reports, duplicate event ingestion,
agreement changes, rounding, and unavailable counter intervals.

Run:
    python analysis/paymaster_reconciliation_experiment.py
    python -m unittest discover -s tests -v
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

D = Decimal


@dataclass(frozen=True)
class Interval:
    index: int
    reported_units: Decimal | None
    agreement_version: str
    status: str = "ok"  # ok, undetermined, cannot_provide


@dataclass(frozen=True)
class Burn:
    event_id: str
    amount_cc: Decimal
    settlement_window: str


@dataclass(frozen=True)
class Agreement:
    version: str
    price_per_unit: Decimal
    discount_rate: Decimal = D("0")
    rounding_quantum: Decimal = D("0.01")

    def payable(self, units: Decimal) -> Decimal:
        gross = units * self.price_per_unit
        net = gross * (D("1") - self.discount_rate)
        return net.quantize(self.rounding_quantum, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Reconciliation:
    status: str
    expected_cc: Decimal | None
    burned_cc: Decimal
    residual_cc: Decimal | None
    duplicate_events_ignored: int
    reason: str


def deduplicate_burns(burns: Iterable[Burn]) -> tuple[list[Burn], int]:
    """Idempotent ingestion by event ID; conflicting duplicate IDs are invalid."""
    seen: dict[str, Burn] = {}
    duplicates = 0
    for burn in burns:
        previous = seen.get(burn.event_id)
        if previous is None:
            seen[burn.event_id] = burn
        elif previous != burn:
            raise ValueError(f"conflicting duplicate burn event: {burn.event_id}")
        else:
            duplicates += 1
    return list(seen.values()), duplicates


def reconcile_window(
    intervals: list[Interval],
    burns: list[Burn],
    agreements: dict[str, Agreement],
    settlement_window: str,
    tolerance: Decimal = D("0.01"),
) -> Reconciliation:
    """Reconcile the supplied window; never coerce missing reports to zero."""
    incomplete = [i for i in intervals if i.status != "ok" or i.reported_units is None]
    if incomplete:
        statuses = sorted({i.status for i in incomplete})
        return Reconciliation(
            "incomplete", None, D("0"), None, 0,
            "traffic evidence unavailable or undetermined: " + ", ".join(statuses),
        )

    expected = D("0")
    for interval in intervals:
        agreement = agreements.get(interval.agreement_version)
        if agreement is None:
            return Reconciliation(
                "incomplete", None, D("0"), None, 0,
                f"missing agreement version {interval.agreement_version}",
            )
        expected += agreement.payable(interval.reported_units)

    unique_burns, duplicate_count = deduplicate_burns(burns)
    window_burns = [b for b in unique_burns if b.settlement_window == settlement_window]
    actual = sum((b.amount_cc for b in window_burns), D("0"))
    residual = expected - actual
    status = "reconciled" if abs(residual) <= tolerance else "shortfall_or_overpayment"
    return Reconciliation(status, expected, actual, residual, duplicate_count,
                          "complete reports and agreement terms compared with unique burns")


def main() -> None:
    agreements = {
        "v1": Agreement("v1", D("1"), D("0.10")),
        "v2": Agreement("v2", D("1"), D("0.20")),
    }
    intervals = [Interval(i, D("10"), "v1") for i in range(4)]
    cases = [
        ("smoothed full payment", intervals,
         [Burn("tx-1", D("36.00"), "W1")], "reconciled"),
        ("injected 4 CC shortfall", intervals,
         [Burn("tx-2", D("32.00"), "W1")], "shortfall_or_overpayment"),
        ("missing report", intervals[:3] + [Interval(3, None, "v1", "cannot_provide")],
         [Burn("tx-3", D("36.00"), "W1")], "incomplete"),
        ("duplicate event delivery", intervals,
         [Burn("tx-4", D("36.00"), "W1"), Burn("tx-4", D("36.00"), "W1")],
         "reconciled"),
        ("agreement changes mid-window",
         [Interval(0, D("10"), "v1"), Interval(1, D("10"), "v2")],
         [Burn("tx-5", D("17.00"), "W1")], "reconciled"),
    ]
    for name, rows, burns, expected_status in cases:
        result = reconcile_window(rows, burns, agreements, "W1")
        assert result.status == expected_status, (name, result)
        print(f"{name}: {result.status}; expected={result.expected_cc}; "
              f"burned={result.burned_cc}; residual={result.residual_cc}; "
              f"duplicates_ignored={result.duplicate_events_ignored}; {result.reason}")

    try:
        deduplicate_burns([
            Burn("same-id", D("10"), "W1"), Burn("same-id", D("11"), "W1")
        ])
    except ValueError:
        print("conflicting duplicate event: rejected")
    else:
        raise AssertionError("conflicting duplicate event was not rejected")

    fine = Agreement("fine", D("0.005"), D("0"), D("0.01"))
    per_interval = sum((fine.payable(D("1")) for _ in range(3)), D("0"))
    aggregate = (D("3") * D("0.005")).quantize(D("0.01"), rounding=ROUND_HALF_UP)
    assert per_interval == D("0.03") and aggregate == D("0.02")
    print(f"rounding boundary: per_interval={per_interval}; aggregate={aggregate}")


if __name__ == "__main__":
    main()
