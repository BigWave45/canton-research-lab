"""Portfolio-level settlement allocation and smoothing model."""
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
    allocation_id: str = ""


def validate_portfolio(obligations: Iterable[Obligation], burns: Iterable[Burn],
                       allocations: Iterable[Allocation], as_of: int,
                       prior_allocations: Iterable[Allocation] = ()) -> dict:
    """Validate new allocation claims together with already committed credit."""
    obligations, burns, allocations = tuple(obligations), tuple(burns), tuple(allocations)
    prior_allocations = tuple(prior_allocations)
    errors = set()

    obligation_groups = {}
    for obligation in obligations:
        obligation_groups.setdefault(obligation.obligation_id, []).append(obligation)
    by_obligation = {}
    for obligation_id, entries in obligation_groups.items():
        if not isinstance(obligation_id, str) or not obligation_id.strip():
            errors.add("OBLIGATION_ID_MISSING")
        elif len(entries) != 1:
            errors.add(f"DUPLICATE_OBLIGATION_ID:{obligation_id}")
        else:
            by_obligation[obligation_id] = entries[0]

    burn_groups = {}
    for burn in burns:
        burn_groups.setdefault(burn.event_id, []).append(burn)
    by_burn = {}
    for event_id, entries in burn_groups.items():
        if not isinstance(event_id, str) or not event_id.strip():
            errors.add("BURN_EVENT_ID_MISSING")
        elif len(entries) != 1:
            errors.add(f"DUPLICATE_BURN_EVENT_ID:{event_id}")
        else:
            by_burn[event_id] = entries[0]

    def decimal_amount(value):
        return isinstance(value, Decimal) and value.is_finite()

    for burn in burns:
        if not decimal_amount(burn.amount_cc) or burn.amount_cc < 0:
            errors.add(f"INVALID_BURN_AMOUNT:{burn.event_id}")
        if not isinstance(burn.paymaster_id, str) or not burn.paymaster_id.strip():
            errors.add(f"BURN_PAYMASTER_ID_MISSING:{burn.event_id}")

    for obligation in obligations:
        if not isinstance(obligation.paymaster_id, str) or not obligation.paymaster_id.strip():
            errors.add(f"OBLIGATION_PAYMASTER_ID_MISSING:{obligation.obligation_id}")
        intervals = sorted(obligation.intervals, key=lambda x: (x.start, x.end))
        if not intervals:
            errors.add(f"NO_INTERVALS:{obligation.obligation_id}")
            continue
        cursor = intervals[0].start
        expected = D("0")
        for interval in intervals:
            if interval.start != cursor or interval.end <= interval.start:
                errors.add(f"INTERVAL_GAP_OR_OVERLAP:{obligation.obligation_id}")
            if interval.status != "Ok" or interval.traffic_bytes is None:
                errors.add(f"INCOMPLETE_INTERVAL:{obligation.obligation_id}")
            if not interval.agreement_version or not decimal_amount(interval.expected_cc) or interval.expected_cc < 0:
                errors.add(f"INVALID_PRICING_EVIDENCE:{obligation.obligation_id}")
            else:
                expected += interval.expected_cc
            cursor = interval.end
        scheduled = D("0")
        schedule_valid = True
        for tranche in obligation.due_schedule:
            if not decimal_amount(tranche.amount_cc) or tranche.amount_cc < 0:
                schedule_valid = False
                errors.add(f"INVALID_DUE_SCHEDULE:{obligation.obligation_id}")
            else:
                scheduled += tranche.amount_cc
        if schedule_valid and scheduled != expected:
            errors.add(f"DUE_SCHEDULE_MISMATCH:{obligation.obligation_id}")
        due_dates = [x.due_at for x in obligation.due_schedule]
        if due_dates != sorted(due_dates):
            errors.add(f"DUE_DATES_NOT_ORDERED:{obligation.obligation_id}")

    current_ids = {}
    prior_ids = {}
    for group, records in (("current", allocations), ("prior", prior_allocations)):
        grouped_ids = current_ids if group == "current" else prior_ids
        for allocation in records:
            allocation_id = allocation.allocation_id
            if not isinstance(allocation_id, str) or not allocation_id.strip():
                errors.add("ALLOCATION_ID_MISSING")
            else:
                grouped_ids.setdefault(allocation_id, 0)
                grouped_ids[allocation_id] += 1
    for allocation_id, count in current_ids.items():
        if count > 1:
            errors.add(f"DUPLICATE_ALLOCATION_ID:{allocation_id}")
    for allocation_id, count in prior_ids.items():
        if count > 1:
            errors.add(f"DUPLICATE_PRIOR_ALLOCATION_ID:{allocation_id}")
    for allocation_id in current_ids.keys() & prior_ids.keys():
        errors.add(f"ALLOCATION_ID_REPLAY:{allocation_id}")

    allocated_by_burn, allocated_by_obligation = {}, {}
    all_allocations = sorted(
        prior_allocations + allocations,
        key=lambda item: (
            str(item.event_id), str(item.obligation_id),
            str(item.allocation_id), str(item.amount_cc),
        ),
    )
    for allocation in all_allocations:
        burn = by_burn.get(allocation.event_id)
        obligation = by_obligation.get(allocation.obligation_id)
        if burn is None:
            errors.add(f"UNKNOWN_BURN_REFERENCE:{allocation.event_id}")
        if obligation is None:
            errors.add(f"UNKNOWN_OBLIGATION_REFERENCE:{allocation.obligation_id}")
        if not decimal_amount(allocation.amount_cc):
            errors.add(f"INVALID_ALLOCATION_AMOUNT:{allocation.allocation_id}")
            continue
        if allocation.amount_cc <= 0:
            errors.add(f"NON_POSITIVE_ALLOCATION:{allocation.allocation_id}")
            continue
        if burn is not None:
            allocated_by_burn[allocation.event_id] = (
                allocated_by_burn.get(allocation.event_id, D("0")) + allocation.amount_cc
            )
        if burn is not None and obligation is not None:
            if burn.paymaster_id != obligation.paymaster_id:
                errors.add(f"PAYMASTER_MISMATCH:{allocation.event_id}:{allocation.obligation_id}")
            else:
                allocated_by_obligation[allocation.obligation_id] = (
                    allocated_by_obligation.get(allocation.obligation_id, D("0"))
                    + allocation.amount_cc
                )

    for event_id, amount in allocated_by_burn.items():
        burn = by_burn[event_id]
        if decimal_amount(burn.amount_cc) and amount > burn.amount_cc:
            errors.add(f"BURN_OVERALLOCATED:{event_id}")

    statuses = {}
    for obligation in sorted(obligations, key=lambda item: str(item.obligation_id)):
        expected = sum(
            (x.expected_cc for x in obligation.intervals if decimal_amount(x.expected_cc) and x.expected_cc >= 0),
            D("0"),
        )
        paid = allocated_by_obligation.get(obligation.obligation_id, D("0"))
        due = sum(
            (x.amount_cc for x in obligation.due_schedule
             if decimal_amount(x.amount_cc) and x.amount_cc >= 0 and x.due_at <= as_of),
            D("0"),
        )
        if paid > expected:
            errors.add(f"OBLIGATION_OVERALLOCATED:{obligation.obligation_id}")
            status = "overpaid"
        elif paid >= expected:
            status = "reconciled"
        elif paid < due:
            status = "short_paid"
        else:
            status = "not_yet_due"
        statuses[obligation.obligation_id] = status

    return {
        "status": "invalid" if errors else "valid",
        "obligations": statuses,
        "errors": tuple(sorted(errors)),
    }


def example_portfolio():
    o1 = Obligation("O-A", "PM-1", "dSync-A", (
        PricedInterval(0, 600, "Ok", 1000, "v1", D("5")),
        PricedInterval(600, 1200, "Ok", 1200, "v2", D("4")),
    ), (DueTranche(100, D("3")), DueTranche(200, D("6"))))
    o2 = Obligation("O-B", "PM-1", "dSync-B", (
        PricedInterval(0, 1200, "Ok", 800, "v4", D("6")),
    ), (DueTranche(100, D("6")),))
    burns = (Burn("burn-1", D("9"), "PM-1"), Burn("burn-2", D("6"), "PM-1"))
    allocations = (
        Allocation("burn-1", "O-A", D("3"), "alloc-1"),
        Allocation("burn-1", "O-B", D("6"), "alloc-2"),
        Allocation("burn-2", "O-A", D("6"), "alloc-3"),
    )
    return (o1, o2), burns, allocations


def run():
    obligations, burns, allocations = example_portfolio()
    early = validate_portfolio(obligations, burns, allocations[:2], 150)
    assert early == {"status": "valid", "obligations": {
        "O-A": "not_yet_due", "O-B": "reconciled"}, "errors": ()}
    late = validate_portfolio(obligations, burns, allocations, 250)
    assert late["obligations"] == {"O-A": "reconciled", "O-B": "reconciled"}
    over = (Allocation("burn-1", "O-A", D("4"), "alloc-1"),
            Allocation("burn-1", "O-B", D("6"), "alloc-2"),
            Allocation("burn-2", "O-A", D("6"), "alloc-3"))
    assert validate_portfolio(obligations, burns, over, 250)["status"] == "invalid"
    short = (Allocation("burn-1", "O-A", D("2"), "alloc-1"),
             Allocation("burn-1", "O-B", D("6"), "alloc-2"),
             Allocation("burn-2", "O-A", D("6"), "alloc-3"))
    assert validate_portfolio(obligations, burns, short, 250)["obligations"]["O-A"] == "short_paid"
    print("shared-paymaster smoothing and allocation scenarios passed")


if __name__ == "__main__":
    run()
