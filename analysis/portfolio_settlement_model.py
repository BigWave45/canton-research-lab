"""Portfolio-level settlement allocation and smoothing model.

Synthetic reference model. It does not parse Canton ledger events or execute
CIP-0132 paymaster automation.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

D = Decimal


@dataclass(frozen=True)
class PricedInterval:
    start: int
    end: int
    status: str
    traffic_bytes: int | None
    agreement_version: str
    expected_cc: Decimal


@dataclass(frozen=True)
class DueTranche:
    due_at: int
    amount_cc: Decimal


@dataclass(frozen=True)
class Obligation:
    obligation_id: str
    paymaster_id: str
    synchronizer_id: str
    intervals: tuple[PricedInterval, ...]
    due_schedule: tuple[DueTranche, ...]


@dataclass(frozen=True)
class Burn:
    event_id: str
    amount_cc: Decimal
    paymaster_id: str


@dataclass(frozen=True)
class Allocation:
    event_id: str
    obligation_id: str
    amount_cc: Decimal


def validate_portfolio(
    obligations: Iterable[Obligation],
    burns: Iterable[Burn],
    allocations: Iterable[Allocation],
    as_of: int,
) -> dict:
    obligations = tuple(obligations)
    burns = tuple(burns)
    allocations = tuple(allocations)
    errors: list[str] = []
    by_obligation = {o.obligation_id: o for o in obligations}
    by_burn = {b.event_id: b for b in burns}
    if len(by_obligation) != len(obligations):
        errors.append("duplicate obligation ID")
    if len(by_burn) != len(burns):
        errors.append("duplicate burn event ID")

    for obligation in obligations:
        intervals = sorted(obligation.intervals, key=lambda x: x.start)
        if not intervals:
            errors.append(f"{obligation.obligation_id}: no intervals")
            continue
        cursor = intervals[0].start
        for interval in intervals:
            if interval.start != cursor or interval.end <= interval.start:
                errors.append(f"{obligation.obligation_id}: interval gap/overlap")
            if interval.status != "Ok" or interval.traffic_bytes is None:
                errors.append(f"{obligation.obligation_id}: incomplete interval")
            if not interval.agreement_version:
                errors.append(f"{obligation.obligation_id}: missing agreement version")
            if interval.expected_cc < 0:
                errors.append(f"{obligation.obligation_id}: negative priced interval")
            cursor = interval.end

        expected = sum((x.expected_cc for x in intervals), D("0"))
        scheduled = sum((x.amount_cc for x in obligation.due_schedule), D("0"))
        if any(x.amount_cc < 0 for x in obligation.due_schedule):
            errors.append(f"{obligation.obligation_id}: negative due tranche")
        if scheduled != expected:
            errors.append(f"{obligation.obligation_id}: due schedule does not equal liability")
        due_dates = [x.due_at for x in obligation.due_schedule]
        if due_dates != sorted(due_dates):
            errors.append(f"{obligation.obligation_id}: due dates not ordered")

    allocated_by_burn: dict[str, Decimal] = {}
    allocated_by_obligation: dict[str, Decimal] = {}
    for allocation in allocations:
        burn = by_burn.get(allocation.event_id)
        obligation = by_obligation.get(allocation.obligation_id)
        if burn is None:
            errors.append(f"unknown burn event {allocation.event_id}")
            continue
        if obligation is None:
            errors.append(f"unknown obligation {allocation.obligation_id}")
            continue
        if burn.paymaster_id != obligation.paymaster_id:
            errors.append(f"paymaster mismatch for {allocation.event_id}")
        if allocation.amount_cc < 0:
            errors.append(f"negative allocation for {allocation.event_id}")
        allocated_by_burn[allocation.event_id] = (
            allocated_by_burn.get(allocation.event_id, D("0")) + allocation.amount_cc
        )
        allocated_by_obligation[allocation.obligation_id] = (
            allocated_by_obligation.get(allocation.obligation_id, D("0")) + allocation.amount_cc
        )

    for event_id, allocated in allocated_by_burn.items():
        if allocated > by_burn[event_id].amount_cc:
            errors.append(f"burn over-allocated: {event_id}")

    statuses = {}
    for obligation in obligations:
        expected = sum((x.expected_cc for x in obligation.intervals), D("0"))
        paid = allocated_by_obligation.get(obligation.obligation_id, D("0"))
        if paid > expected:
            errors.append(f"{obligation.obligation_id}: allocated above liability")
            statuses[obligation.obligation_id] = "overpaid"
            continue
        due = sum((x.amount_cc for x in obligation.due_schedule if x.due_at <= as_of), D("0"))
        if paid >= expected:
            status = "reconciled"
        elif as_of >= max((x.due_at for x in obligation.due_schedule), default=as_of) and paid < expected:
            status = "short_paid"
        elif paid < due:
            status = "short_paid"
        else:
            status = "not_yet_due"
        statuses[obligation.obligation_id] = status

    if errors:
        return {"status": "invalid", "obligations": statuses, "errors": tuple(errors)}
    return {"status": "valid", "obligations": statuses, "errors": ()}


def example_portfolio():
    o1 = Obligation(
        "O-A", "PM-1", "dSync-A",
        (
            PricedInterval(0, 600, "Ok", 1000, "v1", D("5")),
            PricedInterval(600, 1200, "Ok", 1200, "v2", D("4")),
        ),
        (DueTranche(100, D("3")), DueTranche(200, D("6"))),
    )
    o2 = Obligation(
        "O-B", "PM-1", "dSync-B",
        (PricedInterval(0, 1200, "Ok", 800, "v4", D("6")),),
        (DueTranche(100, D("6")),),
    )
    burn = Burn("burn-portfolio-1", D("15"), "PM-1")
    allocations = (
        Allocation("burn-portfolio-1", "O-A", D("9")),
        Allocation("burn-portfolio-1", "O-B", D("6")),
    )
    return (o1, o2), (burn,), allocations


def run():
    obligations, burns, allocations = example_portfolio()
    early = validate_portfolio(obligations, burns, allocations, as_of=150)
    assert early["status"] == "valid"
    assert early["obligations"] == {"O-A": "not_yet_due", "O-B": "reconciled"}
    late = validate_portfolio(obligations, burns, allocations, as_of=250)
    assert late["obligations"] == {"O-A": "reconciled", "O-B": "reconciled"}

    over_allocated = (
        Allocation("burn-portfolio-1", "O-A", D("10")),
        Allocation("burn-portfolio-1", "O-B", D("6")),
    )
    assert validate_portfolio(obligations, burns, over_allocated, 250)["status"] == "invalid"

    underpaid = (
        Allocation("burn-portfolio-1", "O-A", D("8")),
        Allocation("burn-portfolio-1", "O-B", D("6")),
    )
    assert validate_portfolio(obligations, burns, underpaid, 250)["obligations"]["O-A"] == "short_paid"
    print("shared-paymaster smoothing and allocation scenarios passed")


if __name__ == "__main__":
    run()
