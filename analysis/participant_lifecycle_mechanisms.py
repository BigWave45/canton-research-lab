"""Participant lifecycle accounting mechanisms.

Synthetic model for comparing how pre-departure traffic could be accounted for.
Not a Canton implementation or empirical network measurement.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Iterable

D = Decimal


@dataclass(frozen=True)
class MemberInterval:
    member_epoch: str
    start_counter: Decimal | None
    end_counter: Decimal | None
    exit_counter: Decimal | None = None
    departure_event_id: str | None = None


def current_end_state_total(rows: Iterable[MemberInterval]) -> Decimal:
    """Mirrors the inspected API population rule: only end-state members count."""
    total = D("0")
    for row in rows:
        if row.end_counter is not None:
            baseline = row.start_counter if row.start_counter is not None else D("0")
            total += row.end_counter - baseline
    return total


def departure_delta(row: MemberInterval) -> Decimal | None:
    if row.end_counter is not None:
        return D("0")
    if row.exit_counter is None or row.start_counter is None:
        return None
    return row.exit_counter - row.start_counter


def deduplicate_departures(rows: Iterable[MemberInterval]) -> tuple[list[MemberInterval], int]:
    seen: dict[str, MemberInterval] = {}
    unique: list[MemberInterval] = []
    duplicates = 0
    for row in rows:
        event_id = row.departure_event_id
        if event_id is None:
            unique.append(row)
            continue
        previous = seen.get(event_id)
        if previous is None:
            seen[event_id] = row
            unique.append(row)
        elif previous != row:
            raise ValueError(f"conflicting departure event: {event_id}")
        else:
            duplicates += 1
    return unique, duplicates


def lifecycle_total(rows: list[MemberInterval], policy: str) -> dict:
    """Unknown departure evidence is never coerced to zero."""
    if policy not in {"charge_departures", "exclude_departures"}:
        raise ValueError("unknown departure policy")
    base = current_end_state_total(rows)
    if policy == "exclude_departures":
        return {"status": "complete", "total": base, "departure_delta": D("0")}
    departed = [r for r in rows if r.end_counter is None and r.start_counter is not None]
    deltas = [departure_delta(r) for r in departed]
    if any(delta is None for delta in deltas):
        return {"status": "incomplete", "total": None, "departure_delta": None}
    extra = sum(deltas, D("0"))
    return {"status": "complete", "total": base + extra, "departure_delta": extra}


def mechanism_comparison(rows: list[MemberInterval]) -> dict:
    excluded = lifecycle_total(rows, "exclude_departures")
    included = lifecycle_total(rows, "charge_departures")
    return {
        "current_end_state": excluded["total"],
        "signed_departure_snapshot": included["total"],
        "carry_forward_counter": included["total"],
        "event_driven_boundary_settlement": included["total"],
        "explicit_exclusion_policy": excluded["total"],
    }


def example_rows() -> list[MemberInterval]:
    return [
        MemberInterval("continuing#1", D("50"), D("150")),
        MemberInterval("departed#1", D("20"), None, D("60"), "exit-001"),
        MemberInterval("joined#1", None, D("25")),
    ]


def run() -> None:
    rows = example_rows()
    comparison = mechanism_comparison(rows)
    assert comparison == {
        "current_end_state": D("125"),
        "signed_departure_snapshot": D("165"),
        "carry_forward_counter": D("165"),
        "event_driven_boundary_settlement": D("165"),
        "explicit_exclusion_policy": D("125"),
    }
    print("mechanism totals:", comparison)
    missing = [
        MemberInterval("continuing#1", D("50"), D("150")),
        MemberInterval("departed#1", D("20"), None),
        MemberInterval("joined#1", None, D("25")),
    ]
    assert lifecycle_total(missing, "charge_departures")["status"] == "incomplete"
    assert lifecycle_total(missing, "exclude_departures")["total"] == D("125")
    unique, count = deduplicate_departures(rows + [rows[1]])
    assert count == 1
    assert lifecycle_total(unique, "charge_departures")["total"] == D("165")
    conflicting = rows + [
        MemberInterval("departed#1", D("20"), None, D("61"), "exit-001")
    ]
    try:
        deduplicate_departures(conflicting)
    except ValueError:
        pass
    else:
        raise AssertionError("conflicting departure event must be rejected")
    print("missing departure evidence: incomplete, not zero")
    print("duplicate departure event: idempotently ignored")
    print("conflicting duplicate event: rejected")


if __name__ == "__main__":
    run()
